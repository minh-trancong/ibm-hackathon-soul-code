import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FilterSelector, MatchValue, FieldCondition
from qdrant_client.models import PointStruct
from qdrant_client.models import VectorParams, Distance

api_key = "yQdGt_qxJJHxkSqJVixA0C818hXv-4_HQ3B1Hoz1KXP_kYjOTGoEpQ"
client_url = "https://e864e345-b71f-4349-b03d-93f1db8b9468.europe-west3-0.gcp.cloud.qdrant.io:6333"


class Qdrant:
    def __init__(self, apikey=api_key, client_url=client_url, collection_name='soulcode'):
        self.embed_size = 384
        self.client = QdrantClient(
            url=client_url,
            api_key=api_key,
        )
        self.collection_name = collection_name
        self.init_collection()

    def init_collection(self):
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.embed_size, distance=Distance.COSINE),
            )
        else:
            print("Collection already exists")

    def add_point(self, point_info):
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=point_info["vec"].tolist(),
                    payload={"user_id": point_info["user_id"], "doc_id": point_info['doc_id'],
                             'summary': point_info['summary']},
                )
            ]
        )

    def add_points(self, point_infos):
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=point_info["vec"].tolist(),
                    payload={"user_id": point_info["user_id"], "doc_id": point_info['doc_id'],
                             'summary': point_info['summary']},
                )
                for idx, point_info in enumerate(point_infos)
            ]
        )

    def search(self, query_vec):
        hits = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vec,
            limit=3
        )
        if abs(float(hits[0].score)) >= 0:
            result = [hits[0]]
            for idx in range(len(hits) - 1):
                if abs(abs(float(hits[idx].score)) - abs(float(hits[idx].score))) >= float(hits[idx].score) * 5 / 100:
                    result.append(hits[idx + 1])
            return result
        return []

    def delete_by_doc_id(self, doc_id):
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=FilterSelector(
                filter=Filter(
                    must=[
                        FieldCondition(
                            key="doc_id",
                            match=MatchValue(value="{}".format(doc_id)),
                        ),
                    ],
                )
            ),
        )
        print("Deleted doc_id: {}".format(doc_id))

    def delete_by_user_id(self, user_id):
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=FilterSelector(
                filter=Filter(
                    must=[
                        FieldCondition(
                            key="user_id",
                            match=MatchValue(value="{}".format(user_id)),
                        ),
                    ],
                )
            ),
        )
        print("Deleted user_id: {}".format(user_id))
