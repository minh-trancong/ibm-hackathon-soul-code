from fastapi import APIRouter, HTTPException

from src.database import DBAdapter
from src.tags.models import TagGet, TagModel

router = APIRouter()


@router.get("/")
def get_tags():
    try:
        with DBAdapter().get_session() as session:
            tag_models = session.query(TagModel).all()

            return [
                TagGet(id=tag_model.id, name=tag_model.name) for tag_model in tag_models
            ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
