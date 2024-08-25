import uuid

from datetime import datetime

from typing import List, Optional
from pydantic import ConfigDict
from sqlmodel import Field, Relationship, SQLModel

from src.documents_tags.model import DocumentTagModel


class TagModel(SQLModel, table=True):
    __tablename__ = "tags"
    model_config = ConfigDict(extra="ignore")

    id: Optional[str] = Field(
        default_factory=lambda: f"{uuid.uuid4()}", primary_key=True
    )
    name: str = Field(unique=True)

    documents: List["DocumentModel"] = Relationship(
        back_populates="tags", link_model=DocumentTagModel
    )


class TagGet(SQLModel):
    id: str
    name: str
