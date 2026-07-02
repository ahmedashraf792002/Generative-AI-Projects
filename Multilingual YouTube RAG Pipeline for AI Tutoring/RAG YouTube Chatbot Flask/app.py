from datetime import datetime
import os
import re
import threading
import uuid
from urllib.parse import parse_qs, urlencode, urlparse

from flask import Flask, jsonify, render_template, request, session


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "youtube-playlist-chatbot-dev-key")

FALLBACK_NOT_FOUND = "I could not find that information in the playlist."

chatbot_state = {
    "vectordb": None,
    "retriever": None,
    "chain": None,
    "embedding_model": None,
    "llm": None,
    "is_ready": False,
    "is_loading": False,
    "current_playlist": None,
    "suggested_questions": [],
    "error": None,
    "progress_message": "Waiting for a playlist.",
    "progress_percent": 0,
    "stats": {},
    "lock": threading.Lock(),
}


def now_stamp():
    return datetime.now().strftime("%I:%M %p")


def set_progress(message, percent):
    with chatbot_state["lock"]:
        chatbot_state["progress_message"] = message
        chatbot_state["progress_percent"] = percent


def normalize_questions(questions):
    clean = []
    seen = set()

    for question in questions or []:
        question = re.sub(r"^\s*[-*\d.)]+\s*", "", str(question)).strip().strip('"')
        question = re.sub(r"\s+", " ", question)
        if not question:
            continue
        if not question.endswith("?"):
            question = question.rstrip(".") + "?"
        key = question.lower()
        if key not in seen:
            clean.append(question)
            seen.add(key)
        if len(clean) == 5:
            break

    fallback = [
        "What are the main ideas covered in this playlist?",
        "Which concepts should I review first?",
        "How do the videos connect to each other?",
        "What examples are used to explain the topic?",
        "What are the most important takeaways?",
    ]
    for question in fallback:
        if len(clean) == 5:
            break
        if question.lower() not in seen:
            clean.append(question)
            seen.add(question.lower())

    return clean[:5]


def normalize_playlist_url(url):
    parsed = urlparse(url)
    playlist_id = parse_qs(parsed.query).get("list", [""])[0].strip()
    if playlist_id:
        return "https://www.youtube.com/playlist?" + urlencode({"list": playlist_id})
    return url


def build_pipeline(playlist_url):
    import torch
    from langchain_community.document_loaders import YoutubeLoader
    from langchain_community.vectorstores import FAISS
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import PromptTemplate
    from langchain_core.runnables import RunnablePassthrough
    from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline as hf_pipeline
    from youtube_transcript_api import YouTubeTranscriptApi
    from yt_dlp import YoutubeDL

    playlist_url = playlist_url #normalize_playlist_url(playlist_url)

    def get_playlist_urls(url):
        options = {"extract_flat": True, "quiet": True, "ignoreerrors": True, "no_warnings": True}
        with YoutubeDL(options) as ydl:
            playlist = ydl.extract_info(url, download=False)

        entries = (playlist or {}).get("entries") or []
        if not entries:
            webpage_url = (playlist or {}).get("webpage_url") or ""
            extractor = (playlist or {}).get("extractor_key") or ""
            if extractor.lower() == "youtube" or "watch?v=" in webpage_url:
                raise ValueError("This looks like a single YouTube video, not a playlist URL.")
            raise ValueError(
                "No videos were returned by YouTube. The playlist may be private, empty, unavailable, "
                "region-restricted, or the URL may not be a valid playlist link."
            )

        urls = []
        skipped = 0
        for entry in entries:
            if not entry:
                skipped += 1
                continue
            title = (entry.get("title") or "").lower()
            if any(marker in title for marker in ("members only", "private video", "deleted video")):
                skipped += 1
                continue
            video_id = entry.get("id") or entry.get("url")
            if video_id:
                if str(video_id).startswith("http"):
                    urls.append(str(video_id))
                else:
                    urls.append(f"https://www.youtube.com/watch?v={video_id}")
            else:
                skipped += 1

        if not urls and skipped:
            raise ValueError(
                "The playlist was found, but all videos appear to be private, deleted, members-only, "
                "or inaccessible from this machine."
            )
        return urls

    def get_title(url):
        try:
            with YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return info.get("title", "Untitled video")
        except Exception:
            return "Untitled video"

    def detect_language(video_url):
        try:
            video_id = video_url.split("v=", 1)[1].split("&", 1)[0]
            transcripts = YouTubeTranscriptApi().list(video_id)
            for transcript in transcripts:
                return transcript.language_code
        except Exception:
            return "en"
        return "en"

    set_progress("Extracting playlist videos...", 10)
    video_urls = get_playlist_urls(playlist_url)

    set_progress("Loading YouTube transcripts...", 25)
    language = detect_language(video_urls[0])
    docs = []
    for index, url in enumerate(video_urls):
        try:
            loader = YoutubeLoader.from_youtube_url(url, language=[language, "en"], add_video_info=False)
            video_docs = loader.load()
            title = get_title(url)
            for doc in video_docs:
                doc.metadata.update(
                    {
                        "video_number": index + 1,
                        "video_url": url,
                        "video_title": title,
                    }
                )
            docs.extend(video_docs)
            loaded_percent = 25 + int((index + 1) / len(video_urls) * 25)
            set_progress(f"Loaded transcripts for {index + 1} of {len(video_urls)} videos...", loaded_percent)
        except Exception:
            continue

    if not docs:
        raise ValueError("Could not load transcripts for any video in this playlist.")

    set_progress("Splitting transcripts into study-sized chunks...", 55)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=160,
        separators=["\n\n", "\n", ".", "?", "!", ",", " "],
    )
    chunks = splitter.split_documents(docs)

    set_progress("Creating embeddings and rebuilding FAISS index...", 70)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    embedding_model = HuggingFaceEmbeddings(
        model_name=os.environ.get("EMBEDDING_MODEL_ID", "sentence-transformers/all-MiniLM-L6-v2"),
        model_kwargs={"device": device},
        encode_kwargs={"normalize_embeddings": True},
    )
    vectordb = FAISS.from_documents(chunks, embedding_model)
    retriever = vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 5, "fetch_k": 24})

    set_progress("Loading Hugging Face language model...", 84)
    model_id = os.environ.get("HF_MODEL_ID", "google/flan-t5-base")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
    pipe = hf_pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=240,
        do_sample=False,
    )
    llm = HuggingFacePipeline(pipeline=pipe)

    rag_prompt = PromptTemplate.from_template(
        """You are a helpful AI tutor. Answer using only the playlist context below.
If the context does not contain the answer, respond exactly with:
I could not find that information in the playlist.

Playlist context:
{context}

Question: {question}

Answer:"""
    )

    def format_docs(retrieved_docs):
        return "\n\n".join(doc.page_content for doc in retrieved_docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    set_progress("Generating suggested study questions...", 93)
    suggestion_docs = vectordb.similarity_search("core concepts summary examples study", k=min(8, len(chunks)))
    suggestion_context = "\n\n".join(doc.page_content[:900] for doc in suggestion_docs)
    suggestion_prompt = PromptTemplate.from_template(
        """Based only on the playlist content below, write exactly 5 concise study questions.
Return one question per line. Do not add numbering.

Playlist content:
{content}

Questions:"""
    )
    suggestion_text = (suggestion_prompt | llm | StrOutputParser()).invoke({"content": suggestion_context})
    suggested_questions = normalize_questions(suggestion_text.splitlines())

    set_progress("Playlist analyzed successfully.", 100)
    return {
        "vectordb": vectordb,
        "retriever": retriever,
        "chain": chain,
        "embedding_model": embedding_model,
        "llm": llm,
        "suggested_questions": suggested_questions,
        "stats": {
            "video_count": len(video_urls),
            "transcript_count": len(docs),
            "chunk_count": len(chunks),
            "model_id": model_id,
        },
    }


@app.route("/")
def index():
    session.setdefault("session_id", str(uuid.uuid4()))
    session.setdefault("chat_history", [])
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    playlist_url = data.get("playlist_url", "").strip()
    reset_chat = bool(data.get("reset_chat", True))

    if not playlist_url:
        return jsonify({"success": False, "error": "Please enter a playlist URL."}), 400

    with chatbot_state["lock"]:
        if chatbot_state["is_loading"]:
            return jsonify({"success": False, "error": "Analysis already in progress."}), 409
        chatbot_state.update(
            {
                "is_loading": True,
                "is_ready": False,
                "current_playlist": playlist_url,
                "suggested_questions": [],
                "error": None,
                "progress_message": "🔄 Analyzing playlist...",
                "progress_percent": 3,
                "stats": {},
            }
        )

    if reset_chat:
        session["chat_history"] = []
        session.modified = True

    def run_pipeline():
        try:
            result = build_pipeline(playlist_url)
            with chatbot_state["lock"]:
                chatbot_state.update(
                    {
                        "vectordb": result["vectordb"],
                        "retriever": result["retriever"],
                        "chain": result["chain"],
                        "embedding_model": result["embedding_model"],
                        "llm": result["llm"],
                        "suggested_questions": result["suggested_questions"],
                        "stats": result["stats"],
                        "is_ready": True,
                        "is_loading": False,
                        "error": None,
                        "progress_message": "Playlist analyzed successfully.",
                        "progress_percent": 100,
                    }
                )
        except Exception as exc:
            with chatbot_state["lock"]:
                chatbot_state.update(
                    {
                        "is_loading": False,
                        "is_ready": False,
                        "error": str(exc),
                        "progress_message": "Analysis failed.",
                        "progress_percent": 0,
                    }
                )

    threading.Thread(target=run_pipeline, daemon=True).start()
    return jsonify({"success": True, "message": "Analysis started."})


@app.route("/status", methods=["GET"])
def status():
    with chatbot_state["lock"]:
        return jsonify(
            {
                "is_ready": chatbot_state["is_ready"],
                "is_loading": chatbot_state["is_loading"],
                "suggested_questions": chatbot_state["suggested_questions"],
                "error": chatbot_state["error"],
                "current_playlist": chatbot_state["current_playlist"],
                "progress_message": chatbot_state["progress_message"],
                "progress_percent": chatbot_state["progress_percent"],
                "stats": chatbot_state["stats"],
            }
        )


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"success": False, "error": "Please enter a question."}), 400

    with chatbot_state["lock"]:
        if chatbot_state["is_loading"]:
            return jsonify({"success": False, "error": "Playlist analysis is still running."}), 409
        if not chatbot_state["is_ready"] or chatbot_state["chain"] is None:
            return jsonify({"success": False, "error": "Please analyze a playlist first."}), 400
        chain = chatbot_state["chain"]

    try:
        answer = chain.invoke(question).strip()
        if not answer:
            answer = FALLBACK_NOT_FOUND
    except Exception as exc:
        return jsonify({"success": False, "error": f"Could not answer the question: {exc}"}), 500

    timestamp = now_stamp()
    session.setdefault("chat_history", [])
    session["chat_history"].append({"role": "user", "content": question, "timestamp": timestamp})
    session["chat_history"].append({"role": "assistant", "content": answer, "timestamp": timestamp})
    session.modified = True

    return jsonify({"success": True, "answer": answer, "timestamp": timestamp})


@app.route("/clear_chat", methods=["POST"])
def clear_chat():
    session["chat_history"] = []
    session.modified = True
    return jsonify({"success": True})


@app.route("/history", methods=["GET"])
def history():
    return jsonify({"history": session.get("chat_history", [])})


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False, port=5000, threaded=True)
