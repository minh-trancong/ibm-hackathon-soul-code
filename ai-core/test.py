

from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ast import literal_eval

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

model_id = ModelTypes.GRANITE_13B_CHAT_V2
model_sum = Model(
    model_id=model_id,
    params=parameters_sum,
    credentials=credentials,
    project_id=project_id,
)
print("start")
doc = str(input())
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
    """+f"""
    Question: Article:
    ###
    {doc}
    ###
    Answer:"""
    return literal_eval(model_sum.generate_text(input))
print(model_sum.generate_text(input))

