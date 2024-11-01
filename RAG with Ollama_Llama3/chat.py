import os
from langchain_community.llms import Ollama
from langchain.document_loaders import UnstructuredFileLoader
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA

import nltk
nltk.download('punkt_tab')
print(nltk.find('tokenizers/punkt_tab'))
print(nltk.__version__)
working_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize LLM and Embeddings
llm = Ollama(model="llama3:instruct", temperature=0)
embeddings = HuggingFaceEmbeddings()

def get_answer(file_name, query):
    file_path = f"{working_dir}/{file_name}"
    loaders = UnstructuredFileLoader(file_path)
    documents = loaders.load()
    
    # Split documents into chunks
    text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1000, chunk_overlap=200)
    text_chunk = text_splitter.split_documents(documents)
    
    # Create a knowledge base
    knowledge_base = FAISS.from_documents(text_chunk, embeddings)
    
    # Initialize and query the QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=knowledge_base.as_retriever()
    )
    response = qa_chain.invoke({"query": query})
    return response["result"]
