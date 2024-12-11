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
    GenParams.MAX_NEW_TOKENS: 2000,
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

parameters_vc = {
    GenParams.DECODING_METHOD: "greedy",
    GenParams.MAX_NEW_TOKENS: 3000,
    GenParams.REPETITION_PENALTY: 1,
    GenParams.TEMPERATURE: 0,
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

model_vc = Model(
    model_id=ModelTypes.GRANITE_20B_MULTILINGUAL,
    params=parameters_vc,
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

async def get_vocab(doc):
    if doc == "":
        return {"num":0,"input_language":"","learning_language":["English","German"],"content":[]}
    if len(doc) >= 2000:
        doc = doc[:2000]
    input = """Extract collocations to study in this paragraph. Doing exactly following these steps:
    Step 1: Determine 5 phrases that are Uncommon, Natural, Accurate, Diverse, and Appropriate and store in num with 5.
    Step 2: Determine input_language of original paragraph and thinking about meaning in this language.
    Step 3: Determin learning_language from ["English",   "French","Spanish", "German"], but except input_language
    Step 4: Extract sentence to make an example.
    Step 5: Output in form of JSON with fields.
    
    REMEMBER to only ouput the Step 5. The ouput always below 2000 tokens and ends with character } . Always ends with character } to stop.
    
    
    Question: Article: 
    ###
    The Unexpected Journey
    
    After weeks of meticulous planning, Emily finally embarked on her solo backpacking trip across Southeast Asia. She had always dreamed of immersing herself in the vibrant cultures and breathtaking landscapes of the region. With her backpack securely fastened and a sense of trepidation mixed with excitement, she boarded the plane, ready to embrace the unknown.
    
    Upon arriving in Bangkok, Emily was immediately struck by the bustling energy of the city. The streets were teeming with life, and the air was thick with the aroma of street food. She spent her first few days exploring the city'''s iconic temples and indulging in the local cuisine. One evening, while wandering through a night market, she stumbled upon a hidden gem: a cozy little bar tucked away down a side street. Inside, she met a group of fellow travelers who quickly became her fast friends.
    
    Together, they ventured off the beaten path, exploring remote villages and trekking through lush jungles. They shared stories, laughter, and unforgettable experiences. Along the way, Emily learned to overcome her fears and embrace the unexpected. She discovered hidden talents, forged lifelong friendships, and gained a newfound appreciation for the beauty of the world.
    
    As her journey drew to a close, Emily realized that she had not only explored new places but also discovered new facets of herself. She returned home with a heart full of gratitude and a mind brimming with memories. The trip had been a transformative experience, one that she would cherish forever.
    ###
    Answer: {"num":5,"input_language":"English","learning_language":["French","German"],"content":[{"no":1,"words":"meticulous planning","words-language":{"French":"planification méticuleuse","German":"sorgfältige Planung"},"meaning":"Planning very carefully, paying attention to every small detail.","example":"After weeks of **meticulous planning**, Emily finally embarked on her solo backpacking trip across Southeast Asia."},{"no":2,"words":"embarked on","words-language":{"French":"s'''est lancé dans","German":"sich auf etwas eingelassen"},"meaning":"Started a journey or a new experience.","example":"After weeks of meticulous planning, Emily finally **embarked on** her solo backpacking trip across Southeast Asia."},{"no":3,"words":"vibrant cultures","words-language":{"French":"cultures vibrantes","German":"lebendige Kulturen"},"meaning":"Cultures that are full of life, energy, and excitement.","example":"She had always dreamed of immersing herself in the **vibrant cultures** and breathtaking landscapes of the region."},{"no":4,"words":"breathtaking landscapes","words-language":{"French":"paysages à couper le souffle","German":"atemberaubende Landschaften"},"meaning":"Scenery so beautiful that it takes your breath away.","example":"She had always dreamed of immersing herself in the vibrant cultures and **breathtaking landscapes** of the region."},{"no":5,"words":"a sense of trepidation","words-language":{"French":"un sentiment d'''appréhension","German":"ein Gefühl der Beklommenheit"},"meaning":"A feeling of fear or worry about something that is going to happen.","example":"With her backpack securely fastened and **a sense of trepidation** mixed with excitement, she boarded the plane, ready to embrace the unknown."}]}
    
    Question: Article:
    ###
    "La Tour Eiffel, symbole emblématique de Paris, s'''élève majestueusement au-dessus de la ville. Sa silhouette élancée, illuminée chaque soir, offre un spectacle à couper le souffle. Les visiteurs peuvent gravir ses marches ou prendre l'''ascenseur pour admirer une vue panoramique imprenable sur la capitale française. De nombreux artistes et écrivains ont été inspirés par cette merveille architecturale, et elle continue d'''enchanter les gens du monde entier."
    ###
    Answer: {"num":5,"input_language":"French","learning_language":["English","German"],"content":[{"no":1,"words":"symbole emblématique","words-language":{"English":"iconic symbol","German":"Wahrzeichen"},"meaning":"Un symbole largement reconnu et représentatif d'''un lieu, d'''une idée ou d'''une culture.","example":"La Tour Eiffel, **symbole emblématique** de Paris, s'''élève majestueusement au-dessus de la ville."},{"no":2,"words":"s'''élève majestueusement","words-language":{"English":"rises majestically","German":"erhebt sich majestätisch"},"meaning":"S'''élever avec grandeur et dignité, de manière impressionnante.","example":"La Tour Eiffel, symbole emblématique de Paris, **s'''élève majestueusement** au-dessus de la ville."},{"no":3,"words":"silhouette élancée","words-language":{"English":"slender silhouette","German":"schlanke Silhouette"},"meaning":"Une forme allongée et fine, élégante et gracieuse.","example":"Sa **silhouette élancée**, illuminée chaque soir, offre un spectacle à couper le souffle."},{"no":4,"words":"spectacle à couper le souffle","words-language":{"English":"breathtaking spectacle","German":"atemberaubender Anblick"},"meaning":"Un spectacle si beau ou impressionnant qu'''il vous laisse sans voix.","example":"Sa silhouette élancée, illuminée chaque soir, offre un **spectacle à couper le souffle**."},{"no":5,"words":"vue panoramique imprenable","words-language":{"English":"unobstructed panoramic view","German":"unverbaubarer Panoramablick"},"meaning":"Une vue étendue et dégagée sur un paysage.","example":"Les visiteurs peuvent gravir ses marches ou prendre l'''ascenseur pour admirer une **vue panoramique imprenable** sur la capitale française."}]}
    
    Question: Article:
    ###
    Die Zugspitze, Deutschlands höchster Berg, ist ein atemberaubendes Naturwunder. Mit ihren majestätischen Gipfeln und schneebedeckten Hängen bietet sie eine unvergleichliche Aussicht auf die umliegende Landschaft. Besucher können mit der Seilbahn auf den Gipfel fahren oder sich auf eine anspruchsvolle Wanderung begeben, um die Schönheit der Alpen hautnah zu erleben. Die Zugspitze ist ein beliebtes Ziel für Outdoor-Enthusiasten, die sich für Skifahren, Wandern und Klettern begeistern.
    ###
    Answer: {"num":5,"input_language":"German","learning_language":["English","French"],"content":[{"no":1,"words":"höchster Berg","words-language":{"English":"highest mountain","French":"plus haute montagne"},"meaning":"Der Berg mit der größten Höhe in einem bestimmten Gebiet.","example":"Die Zugspitze, Deutschlands **höchster Berg**, ist ein atemberaubendes Naturwunder."},{"no":2,"words":"atemberaubendes Naturwunder","words-language":{"English":"breathtaking natural wonder","French":"merveille naturelle à couper le souffle"},"meaning":"Ein beeindruckendes Naturschauspiel, das Ehrfurcht und Staunen hervorruft.","example":"Die Zugspitze, Deutschlands höchster Berg, ist ein **atemberaubendes Naturwunder**."},{"no":3,"words":"majestätischen Gipfeln","words-language":{"English":"majestic peaks","French":"sommets majestueux"},"meaning":"Die höchsten Punkte eines Berges, die durch ihre Größe und Schönheit beeindrucken.","example":"Mit ihren **majestätischen Gipfeln** und schneebedeckten Hängen bietet sie eine unvergleichliche Aussicht auf die umliegende Landschaft."},{"no":4,"words":"unvergleichliche Aussicht","words-language":{"English":"incomparable view","French":"vue incomparable"},"meaning":"Eine Aussicht, die so schön oder einzigartig ist, dass sie mit nichts anderem verglichen werden kann.","example":"Mit ihren majestätischen Gipfeln und schneebedeckten Hängen bietet sie eine **unvergleichliche Aussicht** auf die umliegende Landschaft."},{"no":5,"words":"anspruchsvolle Wanderung","words-language":{"English":"challenging hike","French":"randonnée exigeante"},"meaning":"Eine Wanderung, die aufgrund ihrer Länge, Steigung oder des Geländes körperlich anstrengend ist.","example":"Besucher können mit der Seilbahn auf den Gipfel fahren oder sich auf eine **anspruchsvolle Wanderung** begeben, um die Schönheit der Alpen hautnah zu erleben."}]}
    
    Question: Article:
    ###
    La Seine, fleuve emblématique de Paris, serpente gracieusement à travers la ville, offrant des vues pittoresques et romantiques. Ses rives sont bordées de monuments historiques, de musées renommés et de charmants cafés. Les bateaux-mouches glissent paisiblement sur ses eaux, permettant aux visiteurs d'''admirer la beauté de la capitale sous un angle différent.
    ###
    Answer: {"num":5,"input_language":"French","learning_language":["English","German"],"content":[{"no":1,"words":"fleuve emblématique","words-language":{"English":"iconic river","German":"bedeutender Fluss"},"meaning":"Un fleuve largement reconnu et représentatif d'''une ville ou d'''une région.","example":"La Seine, **fleuve emblématique** de Paris, serpente gracieusement à travers la ville."},{"no":2,"words":"serpente gracieusement","words-language":{"English":"winds gracefully","German":"schlängelt sich anmutig"},"meaning":"Coule de manière sinueuse et élégante.","example":"La Seine, fleuve emblématique de Paris, **serpente gracieusement** à travers la ville."},{"no":3,"words":"vues pittoresques","words-language":{"English":"picturesque views","German":"malerische Ausblicke"},"meaning":"Paysages charmants et dignes d'''être peints.","example":"La Seine, fleuve emblématique de Paris, serpente gracieusement à travers la ville, offrant des **vues pittoresques** et romantiques."},{"no":4,"words":"monuments historiques","words-language":{"English":"historical monuments","German":"historische Denkmäler"},"meaning":"Bâtiments ou structures anciens ayant une importance historique.","example":"Ses rives sont bordées de **monuments historiques**, de musées renommés et de charmants cafés."},{"no":5,"words":"glissent paisiblement","words-language":{"English":"glide peacefully","German":"gleiten friedlich"},"meaning":"Se déplacent doucement et calmement sur l'''eau.","example":"Les bateaux-mouches **glissent paisiblement** sur ses eaux, permettant aux visiteurs d'''admirer la beauté de la capitale sous un angle différent."}]}
    
    Question: Article:
    ###
    AdventureLog: Self Hosted Travel Tracker and Planner
    Hi r/selfhosted!
    
    I am super excited to announce the release of AdventureLog. Having done a lot of travel recently I have always wanted to keep track of the places I have visited on a map and plan out new trips. AdventureLog does exactly that. Here are some of the key features:
    
    Features:
    📕 Log past visits and future plans with information like location, date, rating and activities. And place it as a pin on the map.
    
    This can also be done automatically with a Geocoding API.
    
    🔗 Group your ideas and visits into collections. You can then plan a trip by adding things like restaurants, hotels, and flight information. You can also keep notes of important links and make checklists to make sure the trip goes smoothly!
    
    You can also share collections via a link to make group travel planning easier than ever!
    
    🌎 Mark your visits to countries and regions as you explore the globe!
    
    🗺️ View your travels on a map to visualize your travels
    
    🔎 Search your adventures or search adventures published by other users.
    
    If you have any questions feel free to reach out to me or open an issue on the GitHub repo!
    
    Links
    GitHub Repo
    
    Hosted Version
    
    Install Documentation
    
    I would love to hear any feedback or suggestions!
    
    Edit:
    Thanks so much everyone for the positive feedback and support! There is a lot of great discussion here. I would like to layout my plan moving forward and what the priorities are:
    
    Helping people get the app deployed (sorry if the setup is confusing I am trying to figure out how to simplify it)
    
    Working on bug fixes
    
    Adding new features
    
    AdventureLog is my first ever development project and I learned how to code to in order to build AdventureLog, for this reason there are some quirks that I have been working out along the way. I always felt like a self-hostable alterative for something like Wanderlog was missing and this is what I hope AdventureLog fulfills. My time is going to be constrained soon with school but I will make sure to make AdventureLog a stable and strong open-source project. It would be super useful to add any requests/bugs to the GitHub repo issues so I can add them to my project tracker. I'''m sorry if there is frustration trying to deploy it, but I hope to keep making the process easier in the future. As with any project, feel free to contribute, spread the word and, and brainstorm ideas.
    
    This is only the start of AdventureLog, thanks so much!
    ### \n""" + f"""
        \nQuestion: Article:
        ###
        {doc}
        ###
        Answer:"""
    try:
        vocabs = literal_eval(model_vc.generate_text(input))
    except Exception as e:
        print(e)
        vocabs = {"num":0,"input_language":"","learning_language":["English","German"],"content":[]}
    return vocabs
def doc_summary(file_path):
    text = extract_text(file_path)
    doc = text
    if len(text) >= 10000:
        text = text[:10000]
    if text == "":
        return "", ""
    instruction = """Input: You are an expert in summarizing documents and generating concise titles and summaries and tags. Your task is to analyze the provided document and create a clear, brief title and summary that captures the main points of the content and five tags of this documents. Output follow the format:
        {"title": title, "summary": summary, "tags":[]}
My document: 
###
Programs and software are created by coders using different software tools, known as programming software. Some such programs used for software development by coders are as given below-

Compilers – The conversion of codes written by humans into lower-level machine code is performed by compilers. These machine codes can be interpreted directly by computer hardware. While compilers serve a very basic purpose, they are the basis for creating even the most complicated and sophisticated software.
Debuggers – Debuggers play an essential role in ensuring your software or application performs well by testing and debugging the computer code.
Linkers – Linkers are responsible for combining various individual files from a compiler into a single executable file. The file converted, as a result, runs on its own without requiring a programming environment.
Malware – Malware is software developed to attack computers and their software in a harmful way to cause them to misbehave or seize to work. This includes viruses, ransomware, trojans, and worms. Since there are a variety of malware that may be mistakenly downloaded, it is crucial to have antimalware software on your computer to keep it safe from their attacks.
###
Output:  {"title": "Essential Software Tools for Software Development: Compilers, Debuggers, and Linkers", "summary": "Compilers, Debuggers, and Linkers are crucial software tools used in software development. Compilers convert human-readable code into machine code, Debuggers test and debug code, and Linkers combine individual files into a single executable file. Additionally, understanding the importance of antimalware software is essential to protect computers from harmful software attacks.", "tags": ["software development", "programming software", "compilers", "debuggers", "linkers", "malware"]}

Input: You are an expert in summarizing documents and generating concise titles and summaries and tags. Your task is to analyze the provided document and create a clear, brief title and summary that captures the main points of the content and five tags of this documents. Output follow the format:
        {"title": title, "summary": summary, "tags":[]}
My document: 
###
""" + text + "\n###\nOutput:"
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

