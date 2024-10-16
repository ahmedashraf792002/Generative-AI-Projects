import google.generativeai as genai
import os
import json

working_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = f"{working_dir}/config.json"
config_data = json.load(open("config.json"))
GOOGLE_API_KEY = config_data["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)



def Question_mcqs_generator(input_text, num_questions):
    # Construct the prompt for the AI model
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = f"""
    You are an AI assistant helping the user generate multiple-choice questions (MCQs) based on the following text:
    '{input_text}'
    Please generate {num_questions} MCQs from the text. Each question should have:
    - A clear question
    - Four answer options (labeled A, B, C, D)
    - The correct answer clearly indicated
    Format:
    ## MCQ
    Question: [question]
    A) [option A]
    B) [option B]
    C) [option C]
    D) [option D]
    Correct Answer: [correct option]
    """

    # Here you would call your model to generate the response
    response = model.generate_content(prompt).text.strip()
    
    # Optionally, format the response further if needed
    formatted_response = response.replace('\n', '\n\n')  # Ensure line spacing
    return formatted_response



def Question_essay_generator(input_text, num_questions):
    # Construct the prompt for the AI model to generate essay questions and answers
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = f"""
    You are an AI assistant helping the user generate essay questions and answers based on the following text:
    '{input_text}'
    Please generate {num_questions} essay questions from the text, along with a detailed answer for each question.
    Format:
    ## Essay
    Question: [question]
    Answer: [answer]
    """

    # Here you would call your model to generate the response
    response = model.generate_content(prompt).text.strip()
    
    # Optionally, format the response further if needed
    formatted_response = response.replace('\n', '\n\n')  # Ensure line spacing
    return formatted_response



def gemini_pro_vision_response(prompt, image):
    gemini_pro_vision_model = genai.GenerativeModel("gemini-1.5-flash")
    response = gemini_pro_vision_model.generate_content([prompt, image])
    result = response.text
    return result

def chat_with_gemini():
    # Load the model for chat
    model = genai.GenerativeModel("gemini-1.5-pro")
    
    return model
