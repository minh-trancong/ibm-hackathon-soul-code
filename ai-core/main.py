import os

import requests
from fastapi import FastAPI
from pydantic import BaseModel
import logging
import AICore
from db.qdrant import Qdrant

DB = Qdrant()
embed_module = AICore.EmbedModule(db=DB)

app = FastAPI()


class DocItem(BaseModel):
    doc_id: str
    user_id: str
    doc_url: str


class ChatRequest(BaseModel):
    message: str


class ChatRVRequest(BaseModel):
    message: str
    doc_id: str


async def doc_summary(file_path):
    return AICore.doc_summary(file_path)


@app.post("/documents/")
async def create_document(doc: DocItem):
    logging.info(f"Received payload: {doc}")
    file_path = doc.doc_url
    if file_path is not None:
        file_type = file_path.split(".")[-1]
        if file_type in ["png", "jpg", "jpeg"]:
            title, summary, tags = await AICore.get_img_detail(file_path)
            await embed_module.post_embed_img(doc.doc_id, doc.user_id, summary)
        else:
            title, summary, tags, doc_text = await doc_summary(file_path)
            await embed_module.post_embed_doc(doc.doc_id, doc.user_id, doc_text)
        return {"title": title, "summary": summary, "tags": tags}
    return {"title": "", "summary": "", "tags": []}


@app.post("/chat")
async def chat(request: ChatRequest):
    message = request.message
    session = AICore.Session()
    response = session.get_response(message)
    return {"message": response}


@app.post("/chat/review_doc")
async def chat_review_doc(request: ChatRVRequest):
    review_module = AICore.ReviewDocModule
    message = request.message
    eb_text = embed_module.get_embedding(message)
    info = DB.search_by_doc_id(eb_text, request.doc_id)
    response = review_module.get_response(message, info)
    return {"message": response}


@app.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    try:
        DB.delete_by_doc_id(document_id)
        return {"success": True}
    except:
        return {"success": False}


@app.delete("/user/documents")
async def delete_user_documents(user_id: str):
    try:
        DB.delete_by_user_id(user_id)
        return {"success": True}
    except:
        return {"success": False}
