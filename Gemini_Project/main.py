import os
from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
import pdfplumber
import docx
from fpdf import FPDF
from Gemini_helper_fun import Question_mcqs_generator,Question_essay_generator,gemini_pro_vision_response,chat_with_gemini

st.set_page_config(
    page_title="Gemini AI",
    page_icon="🧠",
    layout="centered",
)

with st.sidebar:
    selected = option_menu('Gemini AI',
                           ['Question Generator',
                            'Image Captioning',
                            'ChatBot'],
                           menu_icon='robot', icons=['chat-dots-fill', 'image-alt', 'patch-question-fill'],
                           default_index=0
                           )

def read_document(uploaded_file):
    ext = uploaded_file.name.split('.', 1)[1].lower()  # Access the file name using uploaded_file.name
    if ext == 'pdf':
        with pdfplumber.open(uploaded_file) as pdf:
            text = ''.join([page.extract_text() for page in pdf.pages])
        return text
    elif ext == 'docx':
        doc = docx.Document(uploaded_file)
        text = ' '.join([para.text for para in doc.paragraphs])
        return text
    elif ext == 'txt':
        return uploaded_file.read().decode('utf-8')  # Read text file content directly
    return None

if selected == "Question Generator":
    st.title("📝 Question Generator using Gemini")
    uploaded_file = st.file_uploader("Upload a file (PDF, DOCX, or TXT):", type=["pdf", "docx", "txt"])
    question_type = st.selectbox("Select question type:", ["MCQ", "Essay"])
    num_questions = st.slider("Specify number of questions:", min_value=1, max_value=1000, step=1)

    # Add a button for generating questions
    if st.button("Generate Questions"):
        if uploaded_file is not None and num_questions > 0:
            # Read the document text
            input_text = read_document(uploaded_file)
            
            if question_type == "MCQ":
                try:
                    response = Question_mcqs_generator(input_text=input_text, num_questions=num_questions)
                    st.write(response)  # Display the generated MCQs
                except Exception as e:
                    if "ResourceExhausted" in str(e):
                        st.error("Quota exceeded. Please try again later.")
                    else:
                        st.error(f"An error occurred while generating MCQs: {e}")
            
            elif question_type == "Essay":
                try:
                    response = Question_essay_generator(input_text=input_text, num_questions=num_questions)
                    st.write(response)  # Display the generated essay questions
                except Exception as e:
                    if "ResourceExhausted" in str(e):
                        st.error("Quota exceeded. Please try again later.")
                    else:
                        st.error(f"An error occurred while generating essay questions: {e}")
        
        else:
            st.error("Please upload a file and specify a valid number of questions.")


elif selected == "Image Captioning":
    st.title("🖼️ Image Captioning using Gemini")
    uploaded_image = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"])
    if st.button("Generate Caption"):
        if uploaded_image is not None:
            # Read the image file
            image = Image.open(uploaded_image)            
            # Generate the caption
            col1, col2 = st.columns(2)

            with col1:
                resized_img = image.resize((700, 500))
                st.image(resized_img)
            
            default_prompt = "write a summary caption for this image"  
            caption = gemini_pro_vision_response(default_prompt, image)
            with col2:
                st.info(caption)
        else:
            st.error("Please upload an image to generate a caption.")
            

def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

if selected == "ChatBot":
    # Initialize chat session if it doesn't exist
    model = chat_with_gemini()
    if "chat_session" not in st.session_state: 
        st.session_state.chat_session = model.start_chat(history=[])

    # Display the chatbot's title on the page
    st.title("🤖 ChatBot")

    # Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # Input field for user's message
    user_prompt = st.chat_input("Ask Gemini-Pro...")  # Input field for user

    if user_prompt:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)

        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)  # Send user prompt

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)