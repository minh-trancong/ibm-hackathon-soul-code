from sqlmodel import Field, Relationship, SQLModel


class DocumentTagModel(SQLModel, table=True):
    __tablename__ = "documents_tags"
    document_id: str | None = Field(
        default=None, foreign_key="documents.id", primary_key=True, ondelete="CASCADE"
    )
    tag_id: str | None = Field(default=None, foreign_key="tags.id", primary_key=True)
