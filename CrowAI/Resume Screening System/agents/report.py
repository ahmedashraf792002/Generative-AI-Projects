"""
agents/report.py — HTML Report Generator.

Builds a polished, self-contained HTML report with:
  - Summary stats bar
  - Ranked candidate cards with score, verdict, accept/reject badge
  - Score breakdown bars
  - Strengths / Gaps / Interview questions
  - Hiring notes
  - "Send Email" button (opens mailto: with the drafted email pre-filled)
  - Filter tabs: All / Accepted / On Hold / Rejected
"""

from pathlib import Path
from datetime import datetime


# ── Colour helpers ────────────────────────────────────────────────────────────

def _score_color(score: int) -> str:
    if score >= 75: return "#16a34a"
    if score >= 60: return "#2563eb"
    if score >= 40: return "#d97706"
    return "#dc2626"

def _verdict_color(verdict: str) -> str:
    return {
        "Strong Fit":  "#16a34a",
        "Good Fit":    "#2563eb",
        "Partial Fit": "#d97706",
        "Poor Fit":    "#dc2626",
    }.get(verdict, "#6b7280")

def _rec_badge(rec: str) -> tuple[str, str, str]:
    return {
        "Advance to Interview":       ("✅ Accepted",  "#dcfce7", "#166534"),
        "Consider with Reservations": ("⏳ On Hold",   "#fef9c3", "#854d0e"),
        "Reject":                     ("❌ Rejected",  "#fee2e2", "#991b1b"),
    }.get(rec, ("❓ Review", "#f3f4f6", "#374151"))


# ── Card builder ──────────────────────────────────────────────────────────────

def _build_card(rank: int, c: dict, email_draft: dict | None, threshold: int) -> str:
    score    = c.get("total_score", 0)
    verdict  = c.get("fit_verdict", "N/A")
    rec      = c.get("recommendation", "")
    email    = c.get("email", "")
    name     = c.get("candidate_name", "Unknown")
    qual     = score >= threshold
    sc       = _score_color(score)
    vc       = _verdict_color(verdict)
    bl, bbg, btxt = _rec_badge(rec)
    bd       = c.get("score_breakdown", {})
    cat      = {
        "Advance to Interview":       "accepted",
        "Consider with Reservations": "hold",
        "Reject":                     "rejected",
    }.get(rec, "rejected")

    # Score breakdown bars
    bars = ""
    for key, label in [
        ("technical_skills",     "Technical Skills"),
        ("experience_level",     "Experience"),
        ("education_credentials","Education"),
        ("projects_portfolio",   "Projects"),
    ]:
        v   = bd.get(key, 0)
        pct = (v / 25) * 100
        bars += f"""
        <div class="bar-row">
          <span class="bar-lbl">{label}</span>
          <div class="bar-track"><div class="bar-fill" style="width:{pct}%;background:{sc}"></div></div>
          <span class="bar-val">{v}/25</span>
        </div>"""

    strengths = "".join(f"<li>{s}</li>" for s in c.get("strengths", []))
    gaps      = "".join(f"<li>{g}</li>" for g in c.get("gaps", []))
    questions = "".join(f"<li>{q}</li>" for q in c.get("suggested_interview_questions", []))

    # Email button
    import urllib.parse
    mailto_btn = ""
    if email_draft and email:
        subj = email_draft.get("subject", "")
        body = email_draft.get("body", "")
        mailto = f"mailto:{email}?subject={urllib.parse.quote(subj)}&body={urllib.parse.quote(body)}"
        mailto_btn = f'<a href="{mailto}" class="email-btn">✉️ Send Email</a>'
    elif email:
        pos = c.get("position_applied", "the position")
        mailto = f"mailto:{email}?subject=Your%20Application%20for%20{urllib.parse.quote(pos)}"
        mailto_btn = f'<a href="{mailto}" class="email-btn">✉️ Send Email</a>'

    qual_tag = f'<span class="qual-tag {"qual-yes" if qual else "qual-no"}">{"✅ Qualified" if qual else "❌ Not Qualified"}</span>'

    return f"""
<div class="card" data-cat="{cat}">
  <div class="card-header">
    <div class="rank">#{rank}</div>
    <div class="cinfo">
      <div class="cname">{name}</div>
      <div class="cpos">📋 {c.get("position_applied","")}</div>
    </div>
    <div class="badges">
      <div class="score-ring" style="border-color:{sc};color:{sc}">
        <span class="snum">{score}</span>
        <span class="sdenom">/100</span>
      </div>
      <span class="vtag" style="color:{vc};border-color:{vc}">{verdict}</span>
      <span class="rec-tag" style="background:{bbg};color:{btxt}">{bl}</span>
      {qual_tag}
    </div>
  </div>

  <div class="breakdown">{bars}</div>

  <div class="detail-grid">
    <div class="dblock">
      <h4>💪 Strengths</h4>
      <ul>{strengths}</ul>
    </div>
    <div class="dblock">
      <h4>⚠️ Gaps</h4>
      <ul>{gaps}</ul>
    </div>
  </div>

  <div class="dblock full">
    <h4>❓ Interview Questions</h4>
    <ol>{questions}</ol>
  </div>

  <div class="notes">
    <h4>📝 Hiring Notes</h4>
    <p>{c.get("hiring_notes","")}</p>
  </div>

  <div class="card-footer">
    <span class="email-lbl">📧 {email if email else "No email on file"}</span>
    {mailto_btn}
  </div>
</div>"""


# ── Main builder ──────────────────────────────────────────────────────────────

def build_html_report(
    candidates: list[dict],
    email_drafts: list[dict],          # same order as candidates
    position: str,
    company: str,
    threshold: int = 60,
) -> str:
    import urllib.parse

    sorted_c = sorted(candidates, key=lambda x: x.get("total_score", 0), reverse=True)
    draft_map: dict[str, dict] = {}
    for d in email_drafts:
        draft_map[d.get("to", "")] = d

    cards_html = ""
    for rank, c in enumerate(sorted_c, 1):
        draft = draft_map.get(c.get("email", ""))
        cards_html += _build_card(rank, c, draft, threshold)

    # Summary stats
    n        = len(candidates)
    n_qual   = sum(1 for c in candidates if c.get("total_score", 0) >= threshold)
    n_acc    = sum(1 for c in candidates if c.get("recommendation") == "Advance to Interview")
    n_hold   = sum(1 for c in candidates if c.get("recommendation") == "Consider with Reservations")
    n_rej    = sum(1 for c in candidates if c.get("recommendation") == "Reject")
    top_score = sorted_c[0].get("total_score", 0) if sorted_c else 0

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Screening Report — {position}</title>
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: #0f1117;
  color: #e2e8f0;
  min-height: 100vh;
}}

/* ── Header ── */
.page-header {{
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border-bottom: 1px solid #334155;
  padding: 2rem 2rem 1.5rem;
  text-align: center;
}}
.page-header h1 {{
  font-size: clamp(1.6rem, 4vw, 2.4rem);
  font-weight: 800;
  letter-spacing: -0.03em;
  color: #f8fafc;
}}
.page-header h1 span {{ color: #60a5fa; }}
.page-header .meta {{
  color: #94a3b8;
  font-size: .85rem;
  margin-top: .5rem;
}}

/* ── Stats ── */
.stats-bar {{
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
  padding: 1.5rem 2rem;
  background: #1e293b;
  border-bottom: 1px solid #334155;
}}
.stat {{
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 12px;
  padding: .9rem 1.4rem;
  text-align: center;
  min-width: 100px;
}}
.stat-num {{ display: block; font-size: 1.9rem; font-weight: 800; color: #60a5fa; }}
.stat-lbl {{ display: block; font-size: .72rem; color: #64748b; text-transform: uppercase; letter-spacing: .07em; margin-top: .15rem; }}

/* ── Filters ── */
.filters {{
  display: flex;
  gap: .6rem;
  flex-wrap: wrap;
  padding: 1.2rem 2rem;
  background: #1a2236;
  border-bottom: 1px solid #334155;
  justify-content: center;
}}
.filter-btn {{
  padding: .45rem 1.1rem;
  border-radius: 999px;
  border: 1.5px solid #334155;
  background: transparent;
  color: #94a3b8;
  font-size: .83rem;
  font-weight: 600;
  cursor: pointer;
  transition: all .18s;
}}
.filter-btn:hover, .filter-btn.active {{
  background: #2563eb;
  border-color: #2563eb;
  color: #fff;
}}

/* ── Cards container ── */
.cards {{ padding: 2rem; max-width: 920px; margin: 0 auto; }}

/* ── Card ── */
.card {{
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 16px;
  margin-bottom: 1.6rem;
  overflow: hidden;
  transition: box-shadow .2s, transform .2s;
}}
.card:hover {{
  box-shadow: 0 8px 32px rgba(0,0,0,.4);
  transform: translateY(-2px);
}}

.card-header {{
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.3rem 1.5rem;
  border-bottom: 1px solid #334155;
  flex-wrap: wrap;
  background: #0f172a;
}}
.rank {{
  background: #334155;
  color: #e2e8f0;
  font-weight: 800;
  font-size: 1rem;
  width: 42px; height: 42px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}}
.cinfo {{ flex: 1; min-width: 140px; }}
.cname {{ font-size: 1.2rem; font-weight: 700; color: #f1f5f9; }}
.cpos  {{ font-size: .78rem; color: #64748b; margin-top: .2rem; }}
.badges {{
  display: flex;
  align-items: center;
  gap: .6rem;
  flex-wrap: wrap;
}}

.score-ring {{
  width: 62px; height: 62px;
  border-radius: 50%;
  border: 3px solid;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  flex-shrink: 0;
}}
.snum   {{ font-size: 1.2rem; font-weight: 800; line-height: 1; }}
.sdenom {{ font-size: .6rem; color: #94a3b8; }}

.vtag {{
  font-size: .78rem; font-weight: 700;
  padding: .28rem .7rem;
  border-radius: 999px;
  border: 1.5px solid;
}}
.rec-tag {{
  font-size: .78rem; font-weight: 700;
  padding: .28rem .7rem;
  border-radius: 999px;
}}
.qual-tag {{
  font-size: .76rem; font-weight: 600;
  padding: .28rem .7rem;
  border-radius: 999px;
}}
.qual-yes {{ background: #14532d22; color: #4ade80; border: 1px solid #166534; }}
.qual-no  {{ background: #7f1d1d22; color: #f87171; border: 1px solid #991b1b; }}

/* ── Breakdown ── */
.breakdown {{
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #334155;
}}
.bar-row {{
  display: flex; align-items: center; gap: .7rem;
  margin-bottom: .5rem;
}}
.bar-lbl   {{ font-size: .77rem; color: #64748b; width: 120px; flex-shrink: 0; }}
.bar-track {{
  flex: 1; height: 7px;
  background: #334155;
  border-radius: 999px;
  overflow: hidden;
}}
.bar-fill  {{ height: 100%; border-radius: 999px; transition: width .5s ease; }}
.bar-val   {{ font-size: .75rem; font-weight: 600; color: #94a3b8; width: 36px; text-align: right; }}

/* ── Details ── */
.detail-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #334155;
}}
@media (max-width: 560px) {{ .detail-grid {{ grid-template-columns: 1fr; }} }}

.dblock h4 {{ font-size: .82rem; font-weight: 700; color: #cbd5e1; margin-bottom: .45rem; }}
.dblock ul, .dblock ol {{ padding-left: 1.15rem; }}
.dblock li {{ font-size: .82rem; color: #94a3b8; line-height: 1.5; margin-bottom: .2rem; }}

.full {{ padding: 1rem 1.5rem; border-bottom: 1px solid #334155; }}

.notes {{
  background: #0f172a;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #334155;
}}
.notes h4 {{ font-size: .82rem; font-weight: 700; color: #cbd5e1; margin-bottom: .4rem; }}
.notes p  {{ font-size: .84rem; color: #94a3b8; line-height: 1.65; }}

/* ── Card footer ── */
.card-footer {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: .9rem 1.5rem;
  flex-wrap: wrap;
  gap: .75rem;
}}
.email-lbl {{ font-size: .82rem; color: #64748b; }}
.email-btn {{
  display: inline-flex;
  align-items: center;
  gap: .4rem;
  background: #2563eb;
  color: #fff;
  border-radius: 8px;
  padding: .5rem 1.1rem;
  font-size: .86rem;
  font-weight: 600;
  text-decoration: none;
  transition: background .18s;
}}
.email-btn:hover {{ background: #1d4ed8; }}

/* ── Footer ── */
.page-footer {{
  text-align: center;
  color: #475569;
  font-size: .76rem;
  padding: 2rem;
  border-top: 1px solid #334155;
  margin-top: 1rem;
}}

/* ── Hidden ── */
.card.hidden {{ display: none; }}
</style>
</head>
<body>

<div class="page-header">
  <h1>🧑‍💼 <span>{company}</span> — Resume Screening</h1>
  <div class="meta">Position: <strong style="color:#e2e8f0">{position}</strong> &nbsp;·&nbsp; {now}</div>
</div>

<div class="stats-bar">
  <div class="stat"><span class="stat-num">{n}</span><span class="stat-lbl">Screened</span></div>
  <div class="stat"><span class="stat-num">{n_qual}</span><span class="stat-lbl">Qualified ≥{threshold}</span></div>
  <div class="stat"><span class="stat-num" style="color:#4ade80">{n_acc}</span><span class="stat-lbl">Accepted</span></div>
  <div class="stat"><span class="stat-num" style="color:#facc15">{n_hold}</span><span class="stat-lbl">On Hold</span></div>
  <div class="stat"><span class="stat-num" style="color:#f87171">{n_rej}</span><span class="stat-lbl">Rejected</span></div>
  <div class="stat"><span class="stat-num" style="color:#a78bfa">{top_score}</span><span class="stat-lbl">Top Score</span></div>
</div>

<div class="filters">
  <button class="filter-btn active" onclick="filter('all')">All Candidates</button>
  <button class="filter-btn" onclick="filter('accepted')">✅ Accepted</button>
  <button class="filter-btn" onclick="filter('hold')">⏳ On Hold</button>
  <button class="filter-btn" onclick="filter('rejected')">❌ Rejected</button>
</div>

<div class="cards">
{cards_html}
</div>

<div class="page-footer">
  Generated by Resume Screening System &nbsp;·&nbsp; Powered by CrewAI &nbsp;·&nbsp; {now}
</div>

<script>
function filter(cat) {{
  document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
  event.target.classList.add("active");
  document.querySelectorAll(".card").forEach(card => {{
    if (cat === "all" || card.dataset.cat === cat) {{
      card.classList.remove("hidden");
    }} else {{
      card.classList.add("hidden");
    }}
  }});
}}
</script>
</body>
</html>"""


# ── Save helper ───────────────────────────────────────────────────────────────

def save_html_report(
    candidates: list[dict],
    email_drafts: list[dict],
    position: str,
    company: str,
    results_dir: Path,
    threshold: int = 60,
) -> Path:
    html     = build_html_report(candidates, email_drafts, position, company, threshold)
    stamp    = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = results_dir / f"screening_report_{stamp}.html"
    out_path.write_text(html, encoding="utf-8")
    return out_path
