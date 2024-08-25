import os

import requests
from fastapi import FastAPI
from pydantic import BaseModel

import AICore
from db.qdrant import Qdrant
from doc_process.doc_process import extract_text


def download_file(url, save_dir="./assets"):
    # Kiểm tra và tạo thư mục lưu trữ nếu chưa tồn tại
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Tải tệp từ URL
    response = requests.get(url, stream=True)

    # Kiểm tra trạng thái của phản hồi
    if response.status_code == 200:
        # Lấy tên tệp từ URL
        filename = url.split("/")[-1]

        # Đường dẫn lưu tệp
        file_path = os.path.join(save_dir, filename)

        # Ghi nội dung tệp vào thư mục lưu trữ
        with open(file_path, "wb") as file:
            file.write(response.content)

        print(f"File saved to {file_path}")
        return file_path
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
        return None


embed_module = AICore.EmbedModule()
ReviewDocModule = AICore.ReviewDocModule("")

app = FastAPI()


class DocItem(BaseModel):
    doc_id: str
    user_id: str
    doc_url: str


class ChatRequest(BaseModel):
    message: str

DB = Qdrant()


async def doc_summary(file_path):
    return AICore.doc_summary(file_path)


async def get_tags(summary):
    return AICore.get_tags(summary)


@app.post("/documents/")
async def create_document(doc: DocItem):
    file_path = doc.doc_url
    if file_path is not None:
        file_type = file_path.split(".")[-1]
        if file_type in ["png", "jpg", "jpeg"]:
            title, summary = await AICore.get_img_detail(file_path)
            embed_module.post_embed_img(summary)
        else:
            title, summary, text = await doc_summary(file_path)
            embed_module.post_embed_doc(doc.doc_id, doc.user_id, text)
        tags = await get_tags(summary)
        return {"title": title, "summary": summary, "tags": tags}
    return {"title": "", "summary": "", "tags": []}


@app.post("/chat")
async def chat(request: ChatRequest):
    message = request.message
    session = AICore.Session()
    response = session.get_response(message)
    return {"message": response}

@app.post("/chat/start_rv") # khi bắt đầu review 1 doc thì dùng endpoint này đầu tiên
async def start_review(doc: DocItem):
    global ReviewDocModule
    file_path = doc.doc_url
    if file_path is not None:
        file_type = file_path.split(".")[-1]
        if file_type in ["png", "jpg", "jpeg"]:
            title, doc = await AICore.get_img_detail(file_path)
        else:
            doc = extract_text(file_path)
    ReviewDocModule = AICore.ReviewDocModule(doc)
    return {"success": True}

@app.post("/chat/review_doc")
async def chat_review_doc(request: ChatRequest):
    global ReviewDocModule
    message = request.message
    response = ReviewDocModule.get_response(message)
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
