# YouTube Playlist Chatbot

A professional Flask web app for asking study questions against the transcript content of a YouTube playlist.

## Project Structure

```text
youtube_chatbot/
  app.py
  requirements.txt
  templates/
    index.html
  static/
    css/style.css
    js/app.js
```

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Then open http://localhost:5000.

## How It Works

1. Paste a YouTube playlist URL in the sidebar.
2. Click **Analyze Playlist**.
3. The app extracts videos, loads transcripts, chunks content, builds a FAISS vector database, loads a Hugging Face LLM, and generates 5 concise study questions.
4. Ask custom questions or click a suggested question.

Answers are generated from playlist content only. If the answer is not found, the assistant responds:

```text
I could not find that information in the playlist.
```

## Technologies

| Component | Library |
| --- | --- |
| Web framework | Flask |
| Playlist extraction | yt-dlp |
| Transcript loading | YouTube Transcript API + LangChain YoutubeLoader |
| Text splitting | LangChain RecursiveCharacterTextSplitter |
| Embeddings | Hugging Face sentence-transformers |
| Vector store | FAISS |
| LLM | Hugging Face Transformers via LangChain |
| Chat history | Flask session |

## Configuration

The defaults are CPU-friendly:

```text
HF_MODEL_ID=google/flan-t5-base
EMBEDDING_MODEL_ID=sentence-transformers/all-MiniLM-L6-v2
```

Set either environment variable before running the app to use a different Hugging Face model.
