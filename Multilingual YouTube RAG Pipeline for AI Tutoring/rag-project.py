
# In[1]:
!pip install yt-dlp
!pip install youtube-transcript-api
!pip install -q langchain
!pip install -q langchain-community
!pip install -q langchain-classic
!pip install -q transformers
!pip install -q accelerate
!pip install -q torch
!pip install --upgrade transformers accelerate bitsandbytes
!pip install faiss-cpu
!pip install -U langchain-huggingface
!pip install langchain-text-splitters

# In[2]:
from kaggle_secrets import UserSecretsClient
user_secrets = UserSecretsClient()
#token = user_secrets.get_secret("HF_2")

# In[3]:
from huggingface_hub import login

#login(token)

# In[4]:
from yt_dlp import YoutubeDL

playlist_url = "https://www.youtube.com/playlist?list=PLPTV0NXA_ZSgsLAr8YCgCwhPIJNNtexWu"

def get_playlist_urls(playlist_url):
    with YoutubeDL({
        "extract_flat": True,
        "quiet": True,
        "ignoreerrors": True
    }) as ydl:
        playlist = ydl.extract_info(playlist_url, download=False)

    video_urls = []

    entries = playlist.get("entries", [])
    if not entries:
        print("No entries found in playlist response")
        return []

    for entry in entries:
        if not entry:
            continue

        title = (entry.get("title") or "").lower()

        if any(x in title for x in ["members only", "private video", "deleted video"]):
            continue

        video_id = entry.get("id")
        if video_id:
            video_urls.append(f"https://www.youtube.com/watch?v={video_id}")

    return video_urls

video_urls = get_playlist_urls(playlist_url)

#print(*video_urls, sep="\n")
print(f"\nTotal Videos: {len(video_urls)}")

# In[5]:
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


def get_video_language(video_url):
    try:
        video_id = parse_qs(urlparse(video_url).query)["v"][0]

        transcript_list = YouTubeTranscriptApi().list(video_id)

        first_transcript = next(iter(transcript_list))

        return first_transcript.language_code

    except Exception as e:
        return None
lang = get_video_language(video_urls[0])

print(lang)

# In[6]:
from langchain_community.document_loaders import YoutubeLoader
from yt_dlp import YoutubeDL

def get_title(url):
    try:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "verbose": False,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get("title", "Unknown")
    except Exception:
        return "Unknown"

# In[7]:
def load_youtube_docs(video_urls, lang="en"):
    docs = []

    for i, url in enumerate(video_urls):
        try:
            loader = YoutubeLoader.from_youtube_url(
                url,
                language=[lang],
                add_video_info=False
            )

            video_docs = loader.load()

            title = get_title(url)

            for d in video_docs:
                d.metadata["video_number"] = i + 1
                d.metadata["video_url"] = url
                d.metadata["video_title"] = title   

            docs.extend(video_docs)

        except Exception:
            continue

    return docs
docs = load_youtube_docs(video_urls, lang)
print(f"Total Documents: {len(docs)}")
#docs[1]

# In[8]:
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
    separators=[
        "\n\n",
        "\n",
        ".",
        "؟",
        "?",
        "!",
        "،",
        ",",
        " "
    ]
)

chunks = splitter.split_documents(docs)
print("Chunks:", len(chunks))

# In[9]:
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using:", device)

# In[10]:
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="ibm-granite/granite-embedding-311m-multilingual-r2",
    model_kwargs={"device": device},
    encode_kwargs={"normalize_embeddings": True}
)

# In[11]:
from langchain_community.vectorstores import FAISS

vectordb = FAISS.from_documents(
    chunks,
    embedding_model
)

# In[12]:
retriever = vectordb.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "fetch_k": 30,
        "lambda_mult": 0.7
    }
)

# In[13]:
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="float16",
    bnb_4bit_use_double_quant=True,
)

# In[14]:
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "mistralai/Mistral-7B-Instruct-v0.3"

tokenizer = AutoTokenizer.from_pretrained(model_id)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",
    dtype=torch.float16
)

# In[15]:
from transformers import pipeline

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=200,
    do_sample=True,
    temperature=0.3,
    return_full_text=False
)

# In[16]:
from langchain_huggingface.llms import HuggingFacePipeline

llm = HuggingFacePipeline(pipeline=pipe)

# In[17]:
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("""
You are a helpful AI tutor.

Use the context below from YouTube videos to answer the question.

Context:
{context}

Question:
{question}

Answer in a simple and clear way.
""")

# In[18]:
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)


chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)


# In[19]:
def ask_question(question):
    return chain.invoke(question)
ask_question("what about playlist")

# In[20]:
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser

parser = CommaSeparatedListOutputParser()

prompt_suggestion = PromptTemplate(
    template="""
Based ONLY on the following content, generate 5 relevant study questions.

Content:
{content}

{format_instructions}
""",
    input_variables=["content"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)

suggestion_chain = prompt_suggestion | llm | parser

# In[21]:
def get_suggested_questions():
    docs = vectordb.similarity_search(
        query="course content",
        k=5
    )

    content = "\n\n".join(
        d.page_content for d in docs
    )

    return suggestion_chain.invoke(
        {"content": content}
    )
questions = get_suggested_questions()

for q in questions:
    print(q)

# In[22]:
ask_question("What is the vision for this playlist at the end of the course?")