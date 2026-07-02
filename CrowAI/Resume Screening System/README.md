# 🧑‍💼 Resume Screening System

Batch AI-powered resume screening using CrewAI — processes **all resumes in one pipeline pass** for speed and scoring consistency.

---

## 📁 Project Structure

```
resume_screener/
│
├── agents/
│   ├── __init__.py          ← exports everything
│   ├── models.py            ← Pydantic output schemas for all agents
│   ├── parser.py            ← Resume Parser agent (batch)
│   ├── matcher.py           ← Job Matcher agent (batch)
│   ├── advisor.py           ← Hiring Advisor agent (batch)
│   ├── email_agent.py       ← Email Drafter + SMTP sender
│   ├── report.py            ← HTML report builder
│   └── crew.py              ← BatchScreeningCrew orchestrator
│
├── main.py                  ← CLI entry point
├── app.py                   ← Desktop GUI (tkinter)
├── llm_loader.py            ← LLM factory (Ollama / OpenAI)
├── resume_loader.py         ← Load PDF/DOCX/TXT resumes
├── .env                     ← All configuration
├── requirements.txt
├── job_description.txt      ← Put your job description here
├── resumes/                 ← Put candidate CVs here
└── results/                 ← Reports saved here
    └── outputs/             ← Per-agent JSON outputs saved here
```

---

## ⚙️ Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure your LLM in .env
#    For Ollama (local):
#      LLM_PROVIDER=ollama
#      OLLAMA_MODEL=llama3:instruct
#    For OpenAI:
#      LLM_PROVIDER=openai
#      OPENAI_API_KEY=sk-...
#      OPENAI_MODEL=gpt-4o-mini

# 3. Put job_description.txt in the folder
# 4. Put resumes in resumes/ folder (PDF, DOCX, or TXT)
```

---

## 🚀 Run

### Desktop GUI (recommended)
```bash
python app.py
```
- Browse for job description file or paste it directly
- Add a folder of resumes or individual files
- Click **▶ Start Screening**
- HTML report opens automatically when done

### CLI
```bash
python main.py

# Or with explicit paths:
python main.py --job path/to/job.txt --resumes path/to/resumes/

# Multiple resume files:
python main.py --job job.txt --resumes cv1.pdf,cv2.pdf,cv3.docx
```

---

## 🤖 Agent Pipeline (Chunked Batching)

Candidates are processed in **small batches**, not one giant prompt and not one-by-one:

```
📥 All Resumes + Job Description
         │
   split into chunks (default: 4 candidates/batch)
         │
   ┌─────▼─────┐
   │  Batch 1  │──▶ Parser → Matcher → Advisor  (3 LLM calls)
   ├───────────┤
   │  Batch 2  │──▶ Parser → Matcher → Advisor  (3 LLM calls)
   ├───────────┤
   │   ...     │
   └─────┬─────┘
         │  merge all batch results
   ┌─────▼─────────┐
   │ Email Drafter │  also chunked
   └─────┬─────────┘
         │
   ┌─────▼──────┐
   │ HTML Report │
   └────────────┘
```

### Why chunking instead of one giant batch or one-by-one?

| Approach | Problem |
|---|---|
| **One giant batch** (all 15 resumes in one prompt) | Risks exceeding the model's context window → truncated/broken JSON output, or the LLM mixing up details between candidates (hallucination/cross-talk) |
| **One-by-one** (1 resume per call) | Accurate, but slow (N × 3 LLM calls), and no consistent scoring rubric across candidates |
| **Chunked batching** (this system, default 4/batch) | Stays inside context limits reliably, lets the model compare a small group consistently, and keeps total LLM calls low — `ceil(N / chunk_size) × 3` |

**Tune it** via `.env` → `CHUNK_SIZE`, the GUI's "Batch size" field, or `--chunk-size` on the CLI:
- Local models (Ollama, smaller context) → 3–4
- GPT-4o-class models → 5–8

**Built-in safety check**: after each batch, the system verifies the LLM returned the *same number* of results as candidates sent — if not, it logs a warning and realigns by index rather than silently shipping mismatched data.



---

## 📊 Output Files

| File | Description |
|---|---|
| `results/screening_report_TIMESTAMP.html` | Main interactive report |
| `results/results_TIMESTAMP.json` | Full results JSON |
| `results/outputs/parse_output.json` | Parser agent output |
| `results/outputs/match_output.json` | Matcher agent output |
| `results/outputs/advisor_output.json` | Advisor agent output |
| `results/outputs/email_output.json` | Email draft output |

---

## 📧 Email Setup

### Option A — mailto: links (default, no config needed)
The HTML report's **Send Email** button opens your default mail client with the subject and body pre-filled from the AI-drafted email.

### Option B — Direct SMTP sending
Fill in SMTP settings in `.env`:
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@email.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_NAME=Hiring Team
```
Then call `send_email(draft, smtp_config)` from `agents.email_agent`.

---

## 📝 Pydantic Models

Every agent has a typed output model in `agents/models.py`:

| Agent | Model |
|---|---|
| Parser | `ParseResult` |
| Matcher | `MatchResult` |
| Advisor | `AdvisorResult` |
| Email | `EmailDraft` |
