import google.generativeai as genai
import PIL.Image


apikey = "AIzaSyCCrkejlNharUNOYrMILPAucgg2Fi558UI"
genai.configure(api_key=apikey)
model = genai.GenerativeModel('gemini-1.5-flash')

async def get_img_detail(file_path):
    img = PIL.Image.open(file_path)
    prompt_title = "You are an expert in visual interpretation and title creation. Your task is to examine the provided image and generate a concise, descriptive title that captures the essence, theme, or most significant aspect of the image."
    prompt_summary = "You are an expert in visual analysis and descriptive writing. Your task is to examine the provided image and compose a detailed description that captures its essential elements, mood, and context. The description should be approximately 50 words long and include information about the setting, subjects, colors, lighting, and any notable features or details that contribute to the overall impression of the image. Give me the short summary, less than 50 words"
    title = model.generate_content([prompt_title, img]).text
    summary = model.generate_content([prompt_summary, img]).text
    if len(summary) >= 100:
        summary = summary[:100]
    return title, summary
