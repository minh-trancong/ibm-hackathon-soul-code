import uuid

from typing import Optional
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class UserModel(SQLModel, table=True):
    __tablename__ = "users"
    model_config = ConfigDict(extra="ignore")

    id: Optional[str] = Field(
        default_factory=lambda: f"{uuid.uuid4()}", primary_key=True
    )
    name: str | None = None
    username: str = Field(unique=True)
    password: str


class UserCreate(SQLModel):
    name: str
    username: str
    password: str


class UserGet(SQLModel):
    id: str
    name: str
    username: str


class UserUpdate(SQLModel):
    name: str
