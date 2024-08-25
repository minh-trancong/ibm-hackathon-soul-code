import os
from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query
from sqlalchemy import func
from sqlmodel import select

from src.documents.models import DocumentModel, DocumentGet
from src.documents_tags.model import DocumentTagModel
from src.tags.models import TagModel
from src.user.models import UserCreate, UserModel, UserGet
from src.database import DBAdapter

from src.documents import util

router = APIRouter()

FS_PATH = "/var/lib/brain/documents/"


@router.post("/")
async def create_document(
    title: Optional[str] = Form(...), file: UploadFile = File(...)
):
    unique_filename = f"{uuid4()}_{file.filename}"

    # Full file path
    file_path = os.path.join(FS_PATH, unique_filename)

    try:
        # Save the file
        with open(file_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

    editables = ["text/plain"]

    file_type = util.determine_file_type(file_path)

    editable = True if file_type in editables else False

    try:
        with DBAdapter().get_session() as session:
            tag = session.query(TagModel).first()

            document = DocumentModel(
                title=title,
                editable=editable,
                path=file_path,
                thumbnail=None,
                review_date=None,
                summary=None,
                tags=[tag],
            )

            session.add(document)

            session.commit()

            return DocumentGet(
                id=document.id,
                title=document.title,
                path=document.path,
                thumbnail=document.thumbnail,
                review_date=document.review_date,
                editable=document.editable,
                summary=document.summary,
                tags=[tag.name for tag in document.tags],
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")


@router.get("/{id}")
def get_document(id: str):
    return _get_document(id)


@router.delete("/{id}")
def delete_document(id: str) -> bool:
    document = _get_document(id)

    with DBAdapter().get_session() as session:
        document = session.query(DocumentModel).filter_by(id=document.id).first()
        session.delete(document)
        session.commit()

        return True


@router.get("/")
def get_documents(tags: list[str] | None = Query(default=None)) -> list[DocumentGet]:
    if not tags:
        return _get_documents()

    if tags:
        return _get_documents_by_tags(tags)


def _get_document(id: str) -> DocumentGet:
    with DBAdapter().get_session() as session:

        document = session.query(DocumentModel).filter_by(id=id).first()

        if not document:
            raise HTTPException(status_code=404, detail="document not found")

        return DocumentGet(
            id=document.id,
            title=document.title,
            path=document.path,
            thumbnail=document.thumbnail,
            review_date=document.review_date,
            editable=document.editable,
            summary=document.summary,
            tags=[tag.name for tag in document.tags],
        )


def _get_documents():
    with DBAdapter().get_session() as session:
        # Fetch all documents and their associated tags
        documents = session.query(DocumentModel).all()

        return [
            DocumentGet(
                id=document.id,
                title=document.title,
                path=document.path,
                thumbnail=document.thumbnail,
                review_date=document.review_date,
                editable=document.editable,
                summary=document.summary,
                tags=[tag.name for tag in document.tags],
            )
            for document in documents
        ]


def _get_documents_by_tags(tags: list[str]):
    with DBAdapter().get_session() as session:
        documents_with_tags = (
            session.query(DocumentModel, TagModel)
            .join(DocumentTagModel, DocumentTagModel.document_id == DocumentModel.id)
            .join(TagModel, DocumentTagModel.tag_id == TagModel.id)
            .filter(TagModel.name.in_(tags))
            .all()
        )

        document_dict = {}
        for document, tag in documents_with_tags:
            if document.id not in document_dict:
                document_dict[document.id] = {
                    "id": document.id,
                    "title": document.title,
                    "tags": [],
                }
            document_dict[document.id]["tags"].append(tag.name)

        return [
            DocumentGet(
                id=document["id"], title=document["title"], tags=document["tags"]
            )
            for document in document_dict.values()
        ]
