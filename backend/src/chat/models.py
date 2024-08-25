from sqlmodel import SQLModel


class ChatPost(SQLModel):
    message: str
