import os

import requests

from dotenv import load_dotenv

load_dotenv()


class CoreAIClient:

    def __init__(self):
        self.endpoint = os.getenv("CORE_API_ENDPOINT")

    def chat(self, message: str) -> str:

        chat_endpoint = f"{self.endpoint}/chat"

        response = requests.post(chat_endpoint, json={"message": message})

        print(response)

        return response.json()["message"]

    def send_document(self, document_id: str, user_id: str, path: str):
        document_endpoint = f"{self.endpoint}/documents"

        response = requests.post(
            document_endpoint,
            json={"doc_id": document_id, "user_id": user_id, "doc_url": path},
        )

        return response.json()
