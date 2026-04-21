from fastapi import APIRouter, Request

from app.config import settings

router = APIRouter()


@router.get("/meta/version")
def meta_version(request: Request) -> dict:
    return {
        "data": {
            "api_version": "v1",
            "schema_version": settings.SCHEMA_VERSION,
            "build_version": settings.BUILD_VERSION,
        },
        "meta": request.state.meta,
    }
