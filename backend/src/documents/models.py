import uuid

from datetime import datetime

from typing import Optional
from pydantic import ConfigDict
from sqlmodel import Field, Relationship, SQLModel

from src.documents_tags.model import DocumentTagModel
from src.tags.models import TagModel

from fastapi import UploadFile


class DocumentModel(SQLModel, table=True):
    __tablename__ = "documents"
    model_config = ConfigDict(extra="ignore")

    id: Optional[str] = Field(
        default_factory=lambda: f"{uuid.uuid4()}", primary_key=True
    )
    title: str
    path: str | None = None
    thumbnail: str | None = None
    review_date: datetime | None = None
    editable: bool | None = None
    summary: str | None = Field(default=None, max_length=16000)
    file_type: str | None = None

    user_id: str | None = Field(default=None, foreign_key="users.id")

    tags: list[TagModel] = Relationship(
        back_populates="documents",
        link_model=DocumentTagModel,
    )


class DocumentGet(SQLModel):
    id: str
    title: str | None = None
    path: str | None = None
    thumbnail: str | None = None
    review_date: datetime | None = None
    editable: bool | None = None
    summary: str | None = None
    file_type: str | None = None
    tags: list[str] | None = None
