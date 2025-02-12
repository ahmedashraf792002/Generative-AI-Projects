import g4f
import google.generativeai as genai
import os
import json
from langchain_community.llms import Ollama

# Load configuration
working_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = f"{working_dir}/config.json"
config_data = json.load(open(config_file_path))
GOOGLE_API_KEY = config_data["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

def chat_response(model, temperature, query):
    response_text = ""
    if model == 'gemini-1.5-pro':
        response = genai.GenerativeModel(model_name=model)
        gemini_response = response.generate_content(query)
        response_text = gemini_response.text
    elif model in ["gemma:2b","llama3:instruct"]:
        llm = Ollama(model=model, temperature=temperature)
        response_text = llm.invoke(query)
    else:
        response = g4f.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": query}],
            temperature=temperature
        )
        for message in response:
            response_text += message
    
    return response_text
