import os
import streamlit as st
from chat import get_answer
working_dir = os.path.dirname(os.path.abspath(__file__))
st.set_page_config(
    page_title="Chat with Doc RAG",
    page_icon="🧠",
    layout="centered",
)
st.title('Document Q&A - Llama3 - Ollama')
upload_file = st.file_uploader(label='Upload your file',type=["pdf"])
user_query = st.text_input('Ask your Question')
if st.button('Answer 🧠'):
    bytes_data = upload_file.read()
    file_name = upload_file.name
    file_path = os.path.join(working_dir,file_name)
    with open(file_path,"wb") as f:
        f.write(bytes_data)
    answer = get_answer(file_name=file_name,query=user_query)
    st.success(answer)

    