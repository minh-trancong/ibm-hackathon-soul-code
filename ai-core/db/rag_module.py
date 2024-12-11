from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Embeddings
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames as EmbedParams
from ibm_watsonx_ai.foundation_models.utils.enums import EmbeddingTypes
from .qdrant import Qdrant

apikey = "eNm1192jAWpKDnh7dkL-XB46y2-2otNAiASGGSGLyeYz"
project_id = "0e1ec565-5a03-4411-9046-06a2a89ae93d"

class EmbedModule:
    def __init__(self, apikey=apikey, project_id=project_id):
        embed_params = {
            EmbedParams.TRUNCATE_INPUT_TOKENS: 3,
            EmbedParams.RETURN_OPTIONS: {
                'input_text': True
            }
        }

        self.embedding = Embeddings(
            model_id=EmbeddingTypes.IBM_SLATE_30M_ENG,
            params=embed_params,
            credentials=Credentials(
                api_key = apikey,
                url = "https://us-south.ml.cloud.ibm.com"),
            project_id=project_id
        )
    def get_embedding(self, text):
        return self.embedding.embed_query(text)

class RAG:
    def __init__(self):
        self.db = Qdrant()


