import uuid
from ast import literal_eval
import asyncio

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Embeddings
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.foundation_models.utils.enums import EmbeddingTypes
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames as EmbedParams
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

from db.qdrant import Qdrant
from doc_process.doc_process import extract_text
from doc_process.image_process import get_img_detail
from doc_process.chunking_doc import chunk_docs

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
    GenParams.MAX_NEW_TOKENS: 1000,
    GenParams.REPETITION_PENALTY: 1.05,
    GenParams.TEMPERATURE: 0.7,
    GenParams.STOP_SEQUENCES: ["\n\n"],
}

parameters_rv = {
    GenParams.DECODING_METHOD: "greedy",
    GenParams.MAX_NEW_TOKENS: 500,
    GenParams.REPETITION_PENALTY: 1,
    GenParams.TEMPERATURE: 0.5,
    GenParams.STOP_SEQUENCES: ["\n\n"],
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

model_rv = Model(
    model_id=ModelTypes.GRANITE_13B_INSTRUCT_V2,
    params=parameters_rv,
    credentials=credentials,
    project_id=project_id,
)
class EmbedModule:
    def __init__(self, db=Qdrant(), apikey=apikey, project_id=project_id):
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

    async def post_embed_doc(self, doc_id, user_id, text, doc_title, doc_summary):
        chunks = chunk_docs(text)
        chunk_points = [(self.get_embedding(chunk), chunk) for chunk in chunks]
        self.db.add_points(
            [{
                "vec": chunk_sum[0],
                "doc_id": doc_id,
                "user_id": user_id,
                "summary": chunk_sum[1],
                "doc_title": doc_title,
                "doc_summary": doc_summary
            } for chunk_sum in chunk_points]
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

    def get_info(self, user_id, text):
        embedding = self.get_embedding(text)
        infos = [point.payload["summary"] for point in self.db.search_by_user_id(user_id, embedding)]
        return infos


class Session:
    def __init__(self, model_chat=model_chat):
        self.model = model_chat
        self.embedModel = EmbedModule()
        self.instruction = """
        You are Soulcode, an AI language model designed for the Second Brain platform. You are a cautious assistant who meticulously follows instructions. You are helpful, harmless, and adhere strictly to ethical guidelines while promoting positive behavior. You always respond to greetings (e.g., "hi," "hello," "good day," "morning," "afternoon," "evening," "night," "what's up," "nice to meet you," "sup," etc.) with "Hello! I am Soulcode, your virtual assistant on Second Brain. How can I assist you today?" Please do not say anything else and do not initiate conversations. Short answer.
        """

    def get_response(self,user_id, question):

        try:
            info = self.embedModel.get_info(user_id, question)

        except Exception as e:
            info = []

        prompt = "\n Some information found from user documents: " + "\n".join(info)
        ques = self.instruction + prompt
        ques += f"\n Input: {question} \nOutput:"
        return self.model.generate_text(ques)


class ReviewDocModule:
    def __init__(self, doc, model_rv=model_rv, min_doc_size=10000):
        self.model = model_rv
        self.min_doc_size = min_doc_size
        self.doc_size = len(doc)
        self.doc = doc

    def get_response(self, question, info):
        doc = "\n".join(["doc title: "+ point.payload["doc_title"] + "\ndoc summary:" + point.payload['doc_summary'] + "\ndoc content:" + point.payload["summary"] for point in info])
        instruction = f"""
        You are Soulcode, an AI language model designed for the Second Brain platform. Answer the following question using only information from the article. If there is no good answer in the article, say I don't know.
        Article: 
        ###
        {doc}
        ###
        Question: {question} 
        Answer:
        """
        return self.model.generate_text(instruction)


def doc_summary(file_path):
    text = extract_text(file_path)
    doc = text
    if len(text) >= 10000:
        text = text[:10000]
    if text == "":
        return "", ""
    instruction = """Input: You are an expert in summarizing documents and generating concise titles and summaries and tags. Your task is to analyze the provided document and create a clear, brief title and summary that captures the main points of the content and five tags of this documents. Output follow the format:
        {"title": title, "summary": summary, "tags":[]}
My document: Programs and software are created by coders using different software tools, known as programming software. Some such programs used for software development by coders are as given below-

Compilers – The conversion of codes written by humans into lower-level machine code is performed by compilers. These machine codes can be interpreted directly by computer hardware. While compilers serve a very basic purpose, they are the basis for creating even the most complicated and sophisticated software.
Debuggers – Debuggers play an essential role in ensuring your software or application performs well by testing and debugging the computer code.
Linkers – Linkers are responsible for combining various individual files from a compiler into a single executable file. The file converted, as a result, runs on its own without requiring a programming environment.
Malware – Malware is software developed to attack computers and their software in a harmful way to cause them to misbehave or seize to work. This includes viruses, ransomware, trojans, and worms. Since there are a variety of malware that may be mistakenly downloaded, it is crucial to have antimalware software on your computer to keep it safe from their attacks.
Output:  {"title": "Essential Software Tools for Software Development: Compilers, Debuggers, and Linkers", "summary": "Compilers, Debuggers, and Linkers are crucial software tools used in software development. Compilers convert human-readable code into machine code, Debuggers test and debug code, and Linkers combine individual files into a single executable file. Additionally, understanding the importance of antimalware software is essential to protect computers from harmful software attacks.", "tags": ["software development", "programming software", "compilers", "debuggers", "linkers", "malware"]}

Input: You are an expert in summarizing documents and generating concise titles and summaries and tags. Your task is to analyze the provided document and create a clear, brief title and summary that captures the main points of the content and five tags of this documents. Output follow the format:
        {"title": title, "summary": summary, "tags":[]}
My document:""" + text + "\nOutput:"
    try:
        result = literal_eval(model_sum.generate_text(instruction))
    except Exception as e:
        print(e)
        result = {"title": "empty", "summary": "empty", "tags": ["empty"]}
    title, summary, tags = result["title"], result["summary"], result['tags']
    return title, summary, tags, doc


def img_summary(file_path):
    return get_img_detail(file_path)


def chunk_summary(chunks):
    def get_prompt(text):
        if len(text) >= 10000:
            text = text[:10000]
        return f"""
        Input: You are an expert in summarizing documents and generating concise titles and summaries. Your task is to analyze the provided document and create a clear, brief summary that captures the main points of the content.
        My document: {text}
        Output:
        """

    chunk_texts = [get_prompt(chunk) for chunk in chunks]
    return model_sum.generate_text([chunk_texts])


# def get_tags(summary):
#     def get_prompt(text):
#         instruction = (
#                 """
#             You are an expert in content categorization, specializing in identifying broad topics and major fields of study. Your task is to analyze the provided document and generate five tags that represent the primary categories or major fields relevant to the document. Please provide the output follow this JSON format:
#             ["tag1", "tag2", ...]
#             If text can't get tags answer: []
#             """ + f"\nInput: {text} \nOutput:"
#         )
#         return instruction
#     try:
#         result = literal_eval(model_sum.generate_text(get_prompt(summary)))
#     except Exception as e:
#         print(e)
#         result = []
#     return result

def get_vocab(doc):
    input = """Extract 10 collocations to study in this paragraph. Doing exactly following these steps:
    Step 1: Think in this articles of phrases that are Uncommon, Natural, Accurate, Diverse, and Appropriate, but identify the 10 most fitting ones that are Uncommon, Natural, Accurate, Diverse, and Appropriate.
    Step 2: For each collocations, thinking about meaning in this context (only in this context), and answer for children understand
    Step 3: Extract sentence to make an example.
    Step 4: Output in form of JSON with fields: no, words, meaning, example.

    REMEMBER to only ouput the Step 4. The ouput always below 1000 tokens and ends with character ] . Always ends with character ] to stop.


    Question: Article: 
    ###
    The Unexpected Journey

    After weeks of meticulous planning, Emily finally embarked on her solo backpacking trip across Southeast Asia. She had always dreamed of immersing herself in the vibrant cultures and breathtaking landscapes of the region. With her backpack securely fastened and a sense of trepidation mixed with excitement, she boarded the plane, ready to embrace the unknown.

    Upon arriving in Bangkok, Emily was immediately struck by the bustling energy of the city. The streets were teeming with life, and the air was thick with the aroma of street food. She spent her first few days exploring the city'''s iconic temples and indulging in the local cuisine. One evening, while wandering through a night market, she stumbled upon a hidden gem: a cozy little bar tucked away down a side street. Inside, she met a group of fellow travelers who quickly became her fast friends.

    Together, they ventured off the beaten path, exploring remote villages and trekking through lush jungles. They shared stories, laughter, and unforgettable experiences. Along the way, Emily learned to overcome her fears and embrace the unexpected. She discovered hidden talents, forged lifelong friendships, and gained a newfound appreciation for the beauty of the world.

    As her journey drew to a close, Emily realized that she had not only explored new places but also discovered new facets of herself. She returned home with a heart full of gratitude and a mind brimming with memories. The trip had been a transformative experience, one that she would cherish forever.
    ###
    Answer: [
    {"no": 1, "words": "meticulous planning", "meaning": "Planning very carefully, paying attention to every small detail.", "example": "After weeks of meticulous planning, Emily finally embarked on her solo backpacking trip across Southeast Asia."},
    {"no": 2, "words": "embarked on", "meaning": "Started a journey or a new experience.", "example": "After weeks of meticulous planning, Emily finally embarked on her solo backpacking trip across Southeast Asia."},
    {"no": 3, "words": "vibrant cultures", "meaning": "Cultures that are full of life, energy, and excitement.", "example": "She had always dreamed of immersing herself in the vibrant cultures and breathtaking landscapes of the region."},
    {"no": 4, "words": "breathtaking landscapes", "meaning": "Scenery so beautiful that it takes your breath away.", "example": "She had always dreamed of immersing herself in the vibrant cultures and breathtaking landscapes of the region."},
    {"no": 5, "words": "securely fastened", "meaning": "Attached or tied very tightly so it won'''t come loose.", "example": "With her backpack securely fastened and a sense of trepidation mixed with excitement, she boarded the plane, ready to embrace the unknown."},
    {"no": 6, "words": "a sense of trepidation", "meaning": "A feeling of fear or worry about something that is going to happen.", "example": "With her backpack securely fastened and a sense of trepidation mixed with excitement, she boarded the plane, ready to embrace the unknown."},
    {"no": 7, "words": "embrace the unknown", "meaning": "To accept and welcome new and unfamiliar experiences.", "example": "With her backpack securely fastened and a sense of trepidation mixed with excitement, she boarded the plane, ready to embrace the unknown."},
    {"no": 8, "words": "bustling energy", "meaning": "Full of activity and excitement.", "example": "Upon arriving in Bangkok, Emily was immediately struck by the bustling energy of the city."},
    {"no": 9, "words": "teeming with life", "meaning": "Full of people and activity.", "example": "The streets were teeming with life, and the air was thick with the aroma of street food."},
    {"no": 10, "words": "iconic temples", "meaning": "Temples that are very famous and represent the city or culture.", "example": "She spent her first few days exploring the city'''s iconic temples and indulging in the local cuisine."}
    ]

    Question: Article:
    ###
    The City That Never Sleeps

    New York City, a bustling metropolis teeming with life, is a place where dreams are made and ambitions soar. The city'''s iconic skyline, dominated by towering skyscrapers, is a testament to human ingenuity and perseverance. From the bright lights of Times Square to the tranquil oasis of Central Park, the city offers a myriad of experiences that cater to every taste and interest.

    Visitors can immerse themselves in the vibrant cultural scene, exploring world-class museums, attending Broadway shows, or simply people-watching in one of the city'''s many cafes. Foodies can indulge in a culinary adventure, sampling everything from authentic ethnic cuisine to Michelin-starred restaurants. And for those seeking a bit of retail therapy, the city'''s endless shopping options are sure to satisfy even the most discerning shopper.

    New York is a city that never sleeps, with a vibrant nightlife scene that keeps the energy flowing well into the early hours. Whether you'''re looking to dance the night away in a trendy club, catch a live music performance in a cozy bar, or simply enjoy a quiet drink with friends, the city has something for everyone.

    Beyond its attractions, New York is a city of resilience and spirit. It has weathered its share of challenges, from economic downturns to natural disasters, but it always emerges stronger and more vibrant than ever. The city'''s diverse population, hailing from all corners of the globe, contributes to its unique character and unwavering energy.

    New York City is a place that captures the imagination and leaves a lasting impression. It is a city of dreams, a city of possibilities, and a city that will forever hold a special place in the hearts of those who have experienced its magic.
    ###
    Answer: [
    {"no": 1, "words": "bustling metropolis", "meaning": "a very large and busy city", "example": "New York City, a bustling metropolis teeming with life, is a place where dreams are made and ambitions soar."},
    {"no": 2, "words": "teeming with life", "meaning": "full of people and activity", "example": "New York City, a bustling metropolis teeming with life, is a place where dreams are made and ambitions soar."},
    {"no": 3, "words": "dreams are made", "meaning": "people can achieve their goals and wishes", "example": "New York City, a bustling metropolis teeming with life, is a place where dreams are made and ambitions soar."},
    {"no": 4, "words": "ambitions soar", "meaning": "people have big hopes and dreams", "example": "New York City, a bustling metropolis teeming with life, is a place where dreams are made and ambitions soar."},
    {"no": 5, "words": "iconic skyline", "meaning": "the easily recognizable outline of buildings against the sky", "example": "The city'''s iconic skyline, dominated by towering skyscrapers, is a testament to human ingenuity and perseverance."},
    {"no": 6, "words": "towering skyscrapers", "meaning": "very tall buildings", "example": "The city'''s iconic skyline, dominated by towering skyscrapers, is a testament to human ingenuity and perseverance."},
    {"no": 7, "words": "human ingenuity", "meaning": "the ability of people to invent and create clever things", "example": "The city'''s iconic skyline, dominated by towering skyscrapers, is a testament to human ingenuity and perseverance."},
    {"no": 8, "words": "bright lights", "meaning": "the colorful and dazzling lights of the city", "example": "From the bright lights of Times Square to the tranquil oasis of Central Park, the city offers a myriad of experiences that cater to every taste and interest."},
    {"no": 9, "words": "tranquil oasis", "meaning": "a calm and peaceful place in the middle of a busy area", "example": "From the bright lights of Times Square to the tranquil oasis of Central Park, the city offers a myriad of experiences that cater to every taste and interest."},
    {"no": 10, "words": "a myriad of experiences", "meaning": "a large variety of different things to see and do", "example": "From the bright lights of Times Square to the tranquil oasis of Central Park, the city offers a myriad of experiences that cater to every taste and interest."}
    ]
    """ + f"""
    Question: Article:
    ###
    {doc}
    ###
    Answer:"""
    try:
        vocab = literal_eval(model_sum.generate_text(input))
    except:
        vocab = {"no": 0, "words": "", "meaning": "", "example": ""},

    return vocab