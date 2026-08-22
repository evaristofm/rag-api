from fastapi import APIRouter

from app.api.v1.routes import ask, document

router = APIRouter()
router.include_router(document.router, tags=["documents"])
router.include_router(ask.router, tags=["ask"])
