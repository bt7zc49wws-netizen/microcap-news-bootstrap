from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/health")
def health(request: Request) -> dict:
    return {
        "data": {
            "status": "ok",
        },
        "meta": request.state.meta,
    }
