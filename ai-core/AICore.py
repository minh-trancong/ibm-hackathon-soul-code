from ast import literal_eval

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Embeddings
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.foundation_models.utils.enums import EmbeddingTypes
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames as EmbedParams
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from langchain.vectorstores import Chroma
from db.qdrant import Qdrant
from doc_process.doc_process import extract_text
from doc_process.image_process import get_img_detail
from langchain.chains import RetrievalQA


apikey = "eNm1192jAWpKDnh7dkL-XB46y2-2otNAiASGGSGLyeYz"
project_id = "0e1ec565-5a03-4411-9046-06a2a89ae93d"
credentials = {
    "url": "https://us-south.ml.cloud.ibm.com",
    "apikey": f"{apikey}",
}
parameters_sum = {
    GenParams.DECODING_METHOD: "greedy",
    GenParams.MAX_NEW_TOKENS: 5000,
    GenParams.STOP_SEQUENCES: ["\n\n"],
    GenParams.TEMPERATURE: 0,
}

parameters_chat = {
    GenParams.DECODING_METHOD: "greedy",
    GenParams.MAX_NEW_TOKENS: 4000,
    GenParams.REPETITION_PENALTY: 1.05,
    GenParams.TEMPERATURE: 1,
}
model_id = ModelTypes.GRANITE_13B_CHAT_V2
model_sum = Model(
    model_id=model_id,
    params=parameters_sum,
    credentials=credentials,
    project_id=project_id,
)

model_chat = Model(
    model_id=model_id,
    params=parameters_chat,
    credentials=credentials,
    project_id=project_id,
)

DB = Qdrant()
class EmbedModule:
    def __init__(self, apikey=apikey, project_id=project_id, db=DB):
        embed_params = {
            EmbedParams.TRUNCATE_INPUT_TOKENS: 3,
            EmbedParams.RETURN_OPTIONS: {"input_text": True},
        }

        self.embedding = Embeddings(
            model_id=EmbeddingTypes.IBM_SLATE_30M_ENG,
            params=embed_params,
            credentials=Credentials(
                api_key=apikey, url="https://us-south.ml.cloud.ibm.com"
            ),
            project_id=project_id,
        )
        self.db = db

    def get_embedding(self, text):
        return self.embedding.embed_query(text)

    async def post_embed_doc(self, doc_id, user_id, text):
        chunk_sums = [
            (self.get_embedding(chunk_sum), chunk_sum)
            for chunk_sum in chunk_summary(text)
        ]
        for chunk_sum in chunk_sums:
            self.db.add_point(
                {
                    "vec": chunk_sum[0],
                    "doc_id": doc_id,
                    "user_id": user_id,
                    "summary": chunk_sum[1],
                }
            )
    async def post_embed_img(self, doc_id, user_id, text):
        img_detail_embed = self.get_embedding(text)
        self.db.add_point(
            {
                "vec": img_detail_embed,
                "doc_id": doc_id,
                "user_id": user_id,
                "summary": text,
            }
        )

    def get_info(self, text):
        embedding = self.get_embedding(text)
        infos = [point.payload["summary"] for point in self.db.search(embedding)]
        return infos


class Session:
    def __init__(self, model_chat=model_chat):
        self.model = model_chat
        self.embedModel = EmbedModule()
        self.instruction = """
        You are Soulcode, an AI language model designed for the Second Brain platform. You are a cautious assistant who meticulously follows instructions. You are helpful, harmless, and adhere strictly to ethical guidelines while promoting positive behavior. You always respond to greetings (e.g., "hi," "hello," "good day," "morning," "afternoon," "evening," "night," "what's up," "nice to meet you," "sup," etc.) with "Hello! I am Soulcode, your virtual assistant on Second Brain. How can I assist you today?" Please do not say anything else and do not initiate conversations
        """

    def get_response(self, question):

        try:
            info = self.embedModel.get_info(question)

        except Exception as e:
            info = []

        prompt = "\n Some infomation found from user documents: " + "\n".join(info)
        ques = self.instruction + prompt
        ques += f"\n Input: {question} \nOutput:"
        return self.model.generate_text(ques)

class ReviewDocModule:
    def __init__(self, doc, model_chat=model_chat, min_doc_size=10000):
        self.model = model_chat
        self.embedding = EmbedModule().get_embedding()
        self.docsearch = None
        self.min_doc_size = min_doc_size
        self.doc_size = len(doc)
        self.doc = doc
        self.set_up_db(doc)

    def set_up_db(self, doc):
        self.docsearch = Chroma.from_documents(doc, self.embedding)

    def get_response(self, question):
        if self.doc_size <= self.min_doc_size:
            instruction = "You will act as an intelligent assistant whose task is to answer questions based on the following the document:\n" + self.doc
            return self.model.generate_text(instruction)
        qa = RetrievalQA.from_chain_type(llm=self.model, chain_type="stuff", retriever=self.docsearch.as_retriever())
        return qa.run(question)


def doc_summary(file_path):
    text, chunks = extract_text(file_path)

    if len(text) >= 10000:
        text = text[:10000]
    if text == "":
        return "", ""
    instruction = (
        """
    You are an expert in summarizing documents and generating concise titles and summaries. Your task is to analyze the provided document and create a clear, brief title and summary that captures the main points of the content. Output follow the format:
    {"title": title, "summary": summary}
    If document can not be summarized, answer in this format: {"title": "empty", "summary": "empty"}
    """
        + f""""
    Input: {text}
    Output:
    """
    )
    result = literal_eval(model_sum.generate_text(instruction))

    summary = result["summary"]

    title, summary = result["title"], result["summary"]
    return title, summary, chunks

def img_summary(file_path):
    return get_img_detail(file_path)
def chunk_summary(chunks):
    def get_prompt(text):
        if len(text) >= 10000:
            text = text[:10000]
        return f"""
        You are an expert in summarizing documents and generating concise titles and summaries. Your task is to analyze the provided document and create a clear, brief title and summary that captures the main points of the content.
    
        Input: {text}
        Output:
        Summary: [Provide a clear and brief summary of the document, highlighting the key information and main ideas]
        """

    chunk_sums = [
        model_sum.generate_text(get_prompt(chunk)).replace("Summary: ", "")
        for chunk in chunks
    ]
    return chunk_sums


def get_tags(summary):
    def get_prompt(text):
        instruction = (
            """
        You are an expert in content categorization, specializing in identifying broad topics and major fields of study. Your task is to analyze the provided document and generate five tags that represent the primary categories or major fields relevant to the document. Please provide the output follow this JSON format:
        ["tag1", "tag2", ...]
        If text can't get tags answer: []
        """ + f"\nInput: {text} \nOutput:"
        )
        return instruction

    result = literal_eval(model_sum.generate_text(get_prompt(summary)))
    return result
