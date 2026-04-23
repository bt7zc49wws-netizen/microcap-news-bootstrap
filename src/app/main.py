import uuid
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes.event_candidates import router as event_candidates_router
from app.api.routes.health import router as health_router
from app.api.routes.meta import router as meta_router
from app.api.routes.ready import router as ready_router
from app.api.routes.signals import router as signals_router
from app.api.routes.status import router as status_router
from app.config import settings
from app.db import init_db


app = FastAPI(title=settings.APP_NAME)


@app.middleware("http")
async def add_meta(request: Request, call_next):
    request.state.meta = {
        "request_id": str(uuid.uuid4()),
        "api_version": "v1",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    response = await call_next(request)
    return response


@app.exception_handler(RuntimeError)
async def runtime_error_handler(request: Request, exc: RuntimeError):
    return JSONResponse(
        status_code=503,
        content={
            "error": {
                "error_code": "service_unready",
                "message": str(exc),
            },
            "meta": getattr(
                request.state,
                "meta",
                {
                    "request_id": str(uuid.uuid4()),
                    "api_version": "v1",
                    "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                },
            ),
        },
    )


@app.on_event("startup")
def on_startup() -> None:
    init_db()


app.include_router(health_router, prefix="/api/v1")
app.include_router(ready_router, prefix="/api/v1")
app.include_router(status_router, prefix="/api/v1")
app.include_router(meta_router, prefix="/api/v1")
app.include_router(event_candidates_router, prefix="/api/v1")
app.include_router(signals_router, prefix="/api/v1")
