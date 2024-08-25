import os
from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query

from fastapi.responses import FileResponse

from sqlalchemy import func
from sqlmodel import select

from src.documents.models import DocumentModel, DocumentGet
from src.documents_tags.model import DocumentTagModel
from src.tags.models import TagModel
from src.user.models import UserCreate, UserModel, UserGet
from src.database import DBAdapter

from src.documents import util
from src.core_ai.client import CoreAIClient

router = APIRouter()

FS_PATH = "/var/lib/brain/documents/"

core_ai_client = CoreAIClient()


@router.get("/content/{id}")
def get_document_content(id: str):
    try:
        with DBAdapter().get_session() as session:
            document = session.query(DocumentModel).filter_by(id=id).first()

            return FileResponse(path=document.path)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Can not get document")


@router.post("/")
async def create_document(
    user_id: Optional[str] = Form(default=None),
    title: Optional[str] = Form(default=None),
    file: UploadFile = File(...),
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
                file_type=file_type,
                user_id=None,
                thumbnail=None,
                review_date=None,
                summary=None,
                tags=[tag],
            )

            session.add(document)

            session.commit()

            ai_info = core_ai_client.send_document(
                document_id=document.id, user_id=user_id, path=file_path
            )

            # Create tag if tag does not exist

            tag_models = session.query(TagModel).all()

            tags = [tag_model.name for tag_model in tag_models]

            ai_tags = ai_info["tags"]

            new_tags = list(set(ai_tags) - set(tags))

            new_tags_model = [TagModel(name=new_tag) for new_tag in new_tags]

            session.add_all(new_tags_model)
            session.commit()

            # Get all tag model from AI tags

            tag_models = session.query(TagModel).all()

            ai_tag_models = []

            for tag_model in tag_models:
                if tag_model.name in ai_tags:
                    ai_tag_models.append(tag_model)

            document = session.query(DocumentModel).filter_by(id=document.id).first()

            document.title = ai_info["title"]
            document.summary = ai_info["summary"]
            document.tags = ai_tag_models

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
