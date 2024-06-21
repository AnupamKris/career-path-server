from flask import jsonify
import google.generativeai as genai
import os
# from dotenv import load_dotenv
# load_dotenv()

API_KEY = os.environ['API_KEY']


genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
summarize_prompt = """
Summarize the following content from the resume and return 5 suitable jobs with explanations in the following JSON format
format:
{
    "jobs": [
        {
            "title" : "...", 
            "description" : "<what is the job and what are the responsibilities>",
            "why" : "<why is this job suitable for the candidate>"
        }, ...]
}

content:
"""




def generate_content_as_json(text):
    while True:
        try:
            response = model.generate_content(text)
            out = eval(response.text.lstrip('```json').rstrip('```'))
            break
        except:
            pass
    return out

def summarize_resume(text):
    out = generate_content_as_json(summarize_prompt + text)
    print(out)
    return out



def getChatHistory(chat):
    his = []
    for i in chat.history:
        d = {}
        d['role'] = i.role
        d['text'] = ''
        for j in i.parts:
            d['text'] += j.text
        his.append(d)
    return jsonify(his)