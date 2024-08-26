import google.generativeai as genai
import PIL.Image
from ast import literal_eval


apikey = "AIzaSyCCrkejlNharUNOYrMILPAucgg2Fi558UI"
genai.configure(api_key=apikey)
model = genai.GenerativeModel('gemini-1.5-flash')

async def get_img_detail(file_path):
    img = PIL.Image.open(file_path)
    prompt_title = "You are an expert in visual interpretation and title creation. Your task is to examine the provided image and generate a concise, descriptive title that captures the essence, theme, or most significant aspect of the image."
    prompt_summary = "You are an expert in visual analysis and descriptive writing. Your task is to examine the provided image and compose a detailed description that captures its essential elements, mood, and context. The description should be approximately 200 words long and include information about the setting, subjects, colors, lighting, and any notable features or details that contribute to the overall impression of the image. Give me the short summary, less than 200 words"
    prompt_tags = """You are an expert in content categorization, specializing in identifying broad topics and major fields of study. Your task is to analyze the provided document and generate five tags that represent the primary categories or major fields relevant to the document. Please provide the output follow this JSON format: ["tag1", "tag2", ...]"""
    title = model.generate_content([prompt_title, img]).text
    summary = model.generate_content([prompt_summary, img]).text
    try:
        prompt_tags += f"\nMy document: {summary}"
        tags = literal_eval(model.generate_content([prompt_tags]).text)
    except:
        tags = ["IMAGE"]
    return title, summary, tags
