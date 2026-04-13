from fastapi import APIRouter

from .analyze import router as analyze_router
from .compare import router as compare_router
from .insights import router as insights_router
from .upload import router as upload_router


def api_router() -> APIRouter:
    root = APIRouter()
    root.include_router(upload_router, tags=["upload"])
    root.include_router(analyze_router, tags=["analyze"])
    root.include_router(compare_router, tags=["compare"])
    root.include_router(insights_router, tags=["insights"])
    return root
