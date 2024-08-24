from fastapi import FastAPI
from pydantic import BaseModel
import AICore
import os
import requests
from db.qdrant import Qdrant

def download_file(url, save_dir="./assets"):
    # Kiểm tra và tạo thư mục lưu trữ nếu chưa tồn tại
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Tải tệp từ URL
    response = requests.get(url, stream=True)

    # Kiểm tra trạng thái của phản hồi
    if response.status_code == 200:
        # Lấy tên tệp từ URL
        filename = url.split('/')[-1]

        # Đường dẫn lưu tệp
        file_path = os.path.join(save_dir, filename)

        # Ghi nội dung tệp vào thư mục lưu trữ
        with open(file_path, 'wb') as file:
            file.write(response.content)

        print(f"File saved to {file_path}")
        return file_path
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
        return None
embed_module = AICore.EmbedModule()

app = FastAPI()


class DocItem(BaseModel):
    doc_id: str
    user_id: str
    doc_url: str

DB = Qdrant()
async def doc_summary(file_path):
    return AICore.doc_summary(file_path)

async def get_tags(summary):
    return AICore.get_tags(summary)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/documents/")
async def create_document(doc: DocItem):
    url = doc.doc_url
    file_path = download_file(url)
    if file_path is not None:
        title, summary, text = await doc_summary(file_path)
        tags = await get_tags(summary)
        embed_module.post_embed_doc(doc.doc_id, doc.user_id, text)
        return {'title': title, 'summary': summary, 'tags': tags}
    return {"title": "", 'summary': "", 'tags': []}

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