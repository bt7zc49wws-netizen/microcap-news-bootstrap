from fastapi import APIRouter, Request

from app.db import ping_db

router = APIRouter()


@router.get("/ready")
def ready(request: Request) -> dict:
    db_ok = ping_db()
    if not db_ok:
        raise RuntimeError("database not ready")

    return {
        "data": {
            "status": "ready",
            "dependencies": {
                "read_model": "ok",
            },
        },
        "meta": request.state.meta,
    }
