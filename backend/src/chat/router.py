from fastapi import APIRouter, HTTPException

from src.chat.models import ChatPost
from src.database import DBAdapter
from src.tags.models import TagGet, TagModel


from src.core_ai.client import CoreAIClient

router = APIRouter()

core_ai_client = CoreAIClient()


@router.post("/")
async def chat(chat_post: ChatPost) -> str:
    return core_ai_client.chat(chat_post.message)
