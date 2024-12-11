from fastapi import APIRouter

from src.user.router import router as user_router
from src.auth.router import router as auth_router
from src.documents.router import router as document_router
from src.tags.router import router as tag_router
from src.chat.router import router as chat_router

router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(document_router, prefix="/documents", tags=["documents"])
router.include_router(tag_router, prefix="/tags", tags=["tags"])
router.include_router(chat_router, prefix="/chat", tags=["chat"])
