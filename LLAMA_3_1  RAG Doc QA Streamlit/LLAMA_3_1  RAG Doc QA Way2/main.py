import os
import json
import streamlit as st
from langchain.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

# Load API key
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
GROQ_API_KEY = config_data["api_key"]
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Set up constants
persist_directory = "doc_db"

# Initialize the LLM
llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0
)

# Define functions
def load_document(file_path):
    loader = UnstructuredPDFLoader(file_path)  # Load PDF
    documents = loader.load()
    return documents

def setup_vectorstore(documents):
    embeddings = HuggingFaceEmbeddings()  # Initialize embeddings
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    doc_chunks = text_splitter.split_documents(documents)
    return doc_chunks

def ChromaDB(texts):
    embeddings = HuggingFaceEmbeddings()  # Use embeddings again for vector store
    vectordb = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    return vectordb

def model(file_path):
    documents = load_document(file_path)
    doc_chunks = setup_vectorstore(documents)
    vectordb = ChromaDB(doc_chunks)
    retriever = vectordb.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain

# Streamlit interface
st.set_page_config(
    page_title="Chat with Doc",
    page_icon="📄",
    layout="centered"
)

st.title("🦙 Chat with Doc - LLAMA 3.1")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Upload PDF file
uploaded_file = st.file_uploader(label="Upload your pdf file", type=["pdf"])

if uploaded_file:
    # Only if a file is uploaded, load and set up the QA chain
    file_path = f"{working_dir}/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Set up the model with the uploaded file
    qa_chain = model(file_path)

# Display the chat history (messages from both user and assistant)
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Ask Llama...")

if user_input:
    # Add user input to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        # Process the user input using the QA chain
        response = qa_chain({"query": user_input})  # Corrected method
        assistant_response = response["result"]
        st.markdown(assistant_response)
        
        # Add assistant's response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
