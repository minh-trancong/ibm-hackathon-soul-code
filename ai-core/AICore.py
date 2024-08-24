from ast import literal_eval

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Embeddings
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.foundation_models.utils.enums import EmbeddingTypes
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames as EmbedParams
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

from doc_process.doc_process import extract_text, chunk_text
from db.qdrant import Qdrant

apikey = "eNm1192jAWpKDnh7dkL-XB46y2-2otNAiASGGSGLyeYz"
project_id = "0e1ec565-5a03-4411-9046-06a2a89ae93d"
credentials = {
    "url": "https://us-south.ml.cloud.ibm.com",
    "apikey": f"{apikey}",
}
parameters = {
    GenParams.DECODING_METHOD: "greedy",
    GenParams.MAX_NEW_TOKENS: 5000,
    GenParams.STOP_SEQUENCES: ["\n\n"],
    GenParams.TEMPERATURE: 0
}
model_id = ModelTypes.GRANITE_13B_INSTRUCT_V2
model = Model(
    model_id=model_id,
    params=parameters,
    credentials=credentials,
    project_id=project_id
)

class EmbedModule:
    def __init__(self, apikey=apikey, project_id=project_id, db=Qdrant()):
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
        self.db = db
    def get_embedding(self, text):
        return self.embedding.embed_query(text)

    def post_embed_doc(self, doc_id, user_id, text):
        chunk_sums = [(self.get_embedding(chunk_sum), chunk_sum) for chunk_sum in chunk_summary(text)]
        for chunk_sum in chunk_sums:
            self.db.add_point({'vec': chunk_sum[0], 'doc_id': doc_id, 'user_id': user_id, 'summary': chunk_sum[1]})
    def get_info(self, text):
        embedding = self.get_embedding(text)
        infos = [point.payload['summary'] for point in self.db.search(embedding)]
        return infos

class Session:
    def __init__(self, model):
        history = []
        self.model = model
        self.embedModel = EmbedModule()
        self.instruction = """
            You are Soulcode, an AI assistant developed for the Second Brain platform. You are a diligent and attentive assistant. You meticulously follow instructions and adhere to ethical guidelines, ensuring that all interactions are helpful and respectful. You are designed to assist users with their queries and tasks effectively. 
            When users greet you (for example, "hi", "hello", "good day", "morning", "afternoon", "evening", "night", "what's up", "nice to meet you", "sup", etc.), you should respond with: "Hello! I am Soulcode, your assistant on the Second Brain platform. How can I assist you today?" Please ensure you do not provide any other information or initiate additional conversation beyond this greeting.
            
        """

    def get_response(self, question):
        prompt = """
        Here is some information from the user database, if you find it useful for your answer then you can use it:
        
        """
        info = self.embedModel.get_info(question)
        if len(info) != 0:
            info = "\n".join(info)
            prompt += info
            self.instruction += prompt
        self.instruction += f"""
            Input: {question}
            Output:
        """
        return self.model.get_response(question)

def doc_summary(file_path):
    def extract(text):
        print(text)
        title, summary = text.split("Summary: ")
        title = title.replace('Title: ', "")
        return title, summary
    text, chunks = extract_text(file_path)

    if len(text) >= 10000:
        text = text[:10000]
    if text == "":
        return "", ""
    instruction = """
    You are an expert in summarizing documents and generating concise titles and summaries. Your task is to analyze the provided document and create a clear, brief title and summary that captures the main points of the content. Output follow the format:
    {"title": title, "summary": summary}
    """+f""""
    Input: {text}
    Output:
    """
    result = model.generate_text(instruction)
    title, summary = extract(result)
    return title, summary, chunks


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
    chunk_sums = [model.generate_text(get_prompt(chunk)).replace("Summary: ", "") for chunk in chunks]
    return chunk_sums


def get_tags(summary):
    def get_prompt(text):
        instruction = """
        You are an expert in content categorization, specializing in identifying broad topics and major fields of study. Your task is to analyze the provided document and generate tags that represent the primary categories or major fields relevant to the document. Please provide the output in JSON format with the following structure:
        {"tag1": tag1, "tag2": tag2, "tag3": tag3}
        """ + f"""
        
        Input: {text}
        Output: [Generate a list of broad topic tags that describe the major fields of the document, using the format shown above and less than 5 tags]
        """
        return instruction
    result = model.generate_text(get_prompt(summary))
    return result