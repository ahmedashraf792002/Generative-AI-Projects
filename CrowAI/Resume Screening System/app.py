"""
app.py — Modern Desktop GUI for the Resume Screening System.

Built with CustomTkinter for a clean, colorful, professional look
(rounded widgets, themed colors, light/dark aware, icon-rich).

Install:
    pip install customtkinter

Features:
  • Upload job description (file picker loads text into the editor, or paste directly)
  • Upload resume folder or individual files
  • LLM provider selection (Ollama / OpenAI) with live config
  • Start screening with a live progress log
  • Auto-opens HTML report when done
  • Email / SMTP credentials configuration
"""

import os
import sys
import threading
import webbrowser
from pathlib import Path

# ── Guard customtkinter ─────────────────────────────────────────────────────────
try:
    import customtkinter as ctk
    from tkinter import filedialog, messagebox
except ImportError:
    print("Error: customtkinter is not installed. Run:  pip install customtkinter")
    sys.exit(1)

from dotenv import load_dotenv, set_key

load_dotenv()

ENV_FILE = Path(__file__).parent / ".env"


# ══════════════════════════════════════════════════════════════════════════════
# Theme — colorful & professional
# ══════════════════════════════════════════════════════════════════════════════
ctk.set_appearance_mode("System")          # follows OS light/dark
ctk.set_default_color_theme("blue")

COL = {
    "primary":     "#4f46e5",   # indigo
    "primary_h":   "#4338ca",
    "accent":      "#0ea5e9",   # sky
    "accent_h":    "#0284c7",
    "success":     "#10b981",   # emerald
    "success_h":   "#059669",
    "danger":      "#ef4444",   # red
    "danger_h":    "#dc2626",
    "header":      "#6366f1",
    "muted":       "#6b7280",
    "faint":       "#9ca3af",
    "log_bg":      "#0f172a",
    "log_fg":      "#7ee787",
    "card":        ("#ffffff", "#1f2230"),
    "field":       ("#f1f5f9", "#2a2d3a"),
}

FONT      = "Segoe UI"
MONO      = "Consolas"


# ══════════════════════════════════════════════════════════════════════════════
class ResumeScreenerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Resume Screening System")
        self.geometry("980x780")
        self.minsize(860, 660)

        self._resume_paths: list[Path] = []
        self._job_file_path: str | None = None
        self._last_html: Path | None = None
        self._running = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_tabs()
        self._build_footer()

    # ── Header ───────────────────────────────────────────────────────────────────

    def _build_header(self):
        hdr = ctk.CTkFrame(self, height=80, corner_radius=0, fg_color=COL["header"])
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_columnconfigure(0, weight=1)

        wrap = ctk.CTkFrame(hdr, fg_color="transparent")
        wrap.pack(side="left", padx=24, pady=12)
        ctk.CTkLabel(
            wrap, text="🧭  Resume Screening System",
            font=ctk.CTkFont(FONT, 22, "bold"), text_color="#ffffff",
        ).pack(anchor="w")
        ctk.CTkLabel(
            wrap, text="Smart candidate screening  •  powered by CrewAI",
            font=ctk.CTkFont(FONT, 12), text_color="#e0e7ff",
        ).pack(anchor="w")

        # appearance toggle
        self._appearance = ctk.CTkSegmentedButton(
            hdr, values=["☀ Light", "🌙 Dark", "Auto"],
            command=self._change_appearance,
            selected_color=COL["primary"], selected_hover_color=COL["primary_h"],
            font=ctk.CTkFont(FONT, 11),
        )
        self._appearance.set("Auto")
        self._appearance.pack(side="right", padx=24)

    def _change_appearance(self, choice):
        mode = {"☀ Light": "Light", "🌙 Dark": "Dark", "Auto": "System"}[choice]
        ctk.set_appearance_mode(mode)

    # ── Tabs ───────────────────────────────────────────────────────────────────────

    def _build_tabs(self):
        self.tabs = ctk.CTkTabview(
            self, corner_radius=12,
            segmented_button_selected_color=COL["primary"],
            segmented_button_selected_hover_color=COL["primary_h"],
            segmented_button_fg_color=COL["field"],
        )
        self.tabs.grid(row=1, column=0, sticky="nsew", padx=16, pady=(14, 0))

        self.tabs.add("📄  Job & Resumes")
        self.tabs.add("⚙  Configuration")
        self.tabs.add("▸  Progress")

        self._build_input_tab(self.tabs.tab("📄  Job & Resumes"))
        self._build_config_tab(self.tabs.tab("⚙  Configuration"))
        self._build_log_tab(self.tabs.tab("▸  Progress"))

    # ── Footer ───────────────────────────────────────────────────────────────────

    def _build_footer(self):
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="ew", padx=16, pady=14)
        footer.grid_columnconfigure(0, weight=1)

        self._run_btn = ctk.CTkButton(
            footer, text="▶   Start Screening",
            command=self._start_screening,
            fg_color=COL["primary"], hover_color=COL["primary_h"],
            font=ctk.CTkFont(FONT, 15, "bold"),
            height=46, width=210, corner_radius=10,
        )
        self._run_btn.grid(row=0, column=0, sticky="w")

        status = ctk.CTkFrame(footer, fg_color="transparent")
        status.grid(row=0, column=1, sticky="e")
        self._status_dot = ctk.CTkLabel(status, text="●", font=ctk.CTkFont(size=16),
                                         text_color=COL["faint"])
        self._status_dot.pack(side="left", padx=(0, 6))
        self._status_lbl = ctk.CTkLabel(status, text="Ready", font=ctk.CTkFont(FONT, 13, "bold"),
                                        text_color=COL["muted"])
        self._status_lbl.pack(side="left")

    # ── Reusable card ───────────────────────────────────────────────────────────

    def _card(self, parent, icon_title, subtitle=""):
        card = ctk.CTkFrame(parent, corner_radius=12, fg_color=COL["card"])
        card.pack(fill="x", padx=14, pady=(14, 0))
        head = ctk.CTkFrame(card, fg_color="transparent")
        head.pack(fill="x", padx=18, pady=(14, 0))
        ctk.CTkLabel(head, text=icon_title, font=ctk.CTkFont(FONT, 15, "bold"),
                     anchor="w").pack(anchor="w")
        if subtitle:
            ctk.CTkLabel(head, text=subtitle, font=ctk.CTkFont(FONT, 11),
                         text_color=COL["faint"], anchor="w").pack(anchor="w")
        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(fill="x", padx=18, pady=(10, 16))
        return body

    def _accent_btn(self, parent, text, command, color="accent", **kw):
        kw.setdefault("height", 34)
        kw.setdefault("corner_radius", 8)
        kw.setdefault("font", ctk.CTkFont(FONT, 12, "bold"))
        return ctk.CTkButton(
            parent, text=text, command=command,
            fg_color=COL[color], hover_color=COL[f"{color}_h"],
            **kw,
        )

    # ── Input Tab ────────────────────────────────────────────────────────────────

    def _build_input_tab(self, parent):
        scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        # Job Description
        jd = self._card(scroll, "📋  Job Description",
                        "Browse a file (its text loads below) or paste it directly")
        jrow = ctk.CTkFrame(jd, fg_color="transparent")
        jrow.pack(fill="x", pady=(0, 8))
        jrow.grid_columnconfigure(0, weight=1)
        self._job_entry = ctk.CTkEntry(jrow, placeholder_text="job_description.txt",
                                       height=36, corner_radius=8)
        self._job_entry.grid(row=0, column=0, sticky="ew")
        self._job_entry.insert(0, os.getenv("JOB_DESCRIPTION_FILE", "job_description.txt"))
        self._accent_btn(jrow, "📁  Browse", self._browse_job).grid(row=0, column=1, padx=(8, 0))

        ctk.CTkLabel(jd, text="Job description text:", font=ctk.CTkFont(FONT, 11),
                     text_color=COL["faint"], anchor="w").pack(anchor="w")
        self._job_text = ctk.CTkTextbox(jd, height=150, corner_radius=8,
                                        font=ctk.CTkFont(MONO, 12), wrap="word")
        self._job_text.pack(fill="x", pady=(4, 0))

        # Resumes
        rc = self._card(scroll, "📑  Resumes",
                        "Add a folder or individual files  (PDF, DOC, DOCX, TXT)")
        brow = ctk.CTkFrame(rc, fg_color="transparent")
        brow.pack(fill="x", pady=(0, 8))
        self._accent_btn(brow, "📂  Add Folder", self._browse_folder).pack(side="left", padx=(0, 8))
        self._accent_btn(brow, "➕  Add Files", self._browse_files).pack(side="left", padx=(0, 8))
        self._accent_btn(brow, "🗑  Clear", self._clear_resumes, color="danger").pack(side="left")
        self._resume_count = ctk.CTkLabel(brow, text="0 files added",
                                          font=ctk.CTkFont(FONT, 11, slant="italic"),
                                          text_color=COL["muted"])
        self._resume_count.pack(side="right")

        self._resume_list = ctk.CTkTextbox(rc, height=150, corner_radius=8,
                                           font=ctk.CTkFont(MONO, 12), wrap="none")
        self._resume_list.pack(fill="x")
        self._resume_list.configure(state="disabled")

        # Screening Settings
        sc = self._card(scroll, "🎚  Screening Settings", "Tune scoring and batching")
        grid = ctk.CTkFrame(sc, fg_color="transparent")
        grid.pack(fill="x")
        self._company_entry  = self._field(grid, "Company name", 0, 0, 24,
                                            os.getenv("COMPANY_NAME", "TechStartup Egypt"))
        self._threshold_entry = self._field(grid, "Min score threshold", 0, 1, 8,
                                             os.getenv("MIN_SCORE_THRESHOLD", "60"))
        self._chunk_entry    = self._field(grid, "Batch size (resumes / LLM call)", 1, 0, 8,
                                            os.getenv("CHUNK_SIZE", "4"))
        ctk.CTkLabel(
            sc, text="💡 Lower batch size is safer for many resumes or small-context models — "
                     "it avoids cross-candidate mix-ups.",
            font=ctk.CTkFont(FONT, 11), text_color=COL["faint"],
            wraplength=780, justify="left", anchor="w",
        ).pack(anchor="w", pady=(8, 0))

    def _field(self, parent, label, row, col, width, value):
        cell = ctk.CTkFrame(parent, fg_color="transparent")
        cell.grid(row=row, column=col, sticky="w", padx=(0, 30), pady=8)
        ctk.CTkLabel(cell, text=label, font=ctk.CTkFont(FONT, 11),
                     text_color=COL["muted"], anchor="w").pack(anchor="w")
        e = ctk.CTkEntry(cell, width=max(width * 9, 90), height=34, corner_radius=8)
        e.pack(anchor="w", pady=(3, 0))
        e.insert(0, value)
        return e

    # ── Config Tab ────────────────────────────────────────────────────────────────

    def _build_config_tab(self, parent):
        scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        # LLM provider
        lc = self._card(scroll, "🤖  LLM Provider", "Choose the engine that scores resumes")
        row = ctk.CTkFrame(lc, fg_color="transparent"); row.pack(fill="x", pady=4)
        ctk.CTkLabel(row, text="Provider", width=150, anchor="w",
                     font=ctk.CTkFont(FONT, 12), text_color=COL["muted"]).pack(side="left")
        self._provider_var = ctk.StringVar(value=os.getenv("LLM_PROVIDER", "ollama"))
        ctk.CTkOptionMenu(
            row, values=["ollama", "openai"], variable=self._provider_var,
            fg_color=COL["primary"], button_color=COL["primary_h"],
            button_hover_color=COL["primary_h"], width=160, corner_radius=8,
            command=self._on_provider_change,
        ).pack(side="left")
        self._ollama_model = self._crow(lc, "Ollama model",
                                        os.getenv("OLLAMA_MODEL", "llama3:instruct"))
        self._ollama_url   = self._crow(lc, "Ollama base URL",
                                        os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))

        # OpenAI
        oc = self._card(scroll, "🔑  OpenAI", "Only needed when the OpenAI provider is selected")
        self._openai_key   = self._crow(oc, "API key", os.getenv("OPENAI_API_KEY", ""), show="•")
        self._openai_model = self._crow(oc, "Model", os.getenv("OPENAI_MODEL", "gpt-4o-mini"))

        # SMTP
        sm = self._card(scroll, "✉  Email / SMTP",
                        "Optional — leave blank to use mailto: links in the report")
        self._smtp_host = self._crow(sm, "SMTP host", os.getenv("SMTP_HOST", ""))
        self._smtp_port = self._crow(sm, "SMTP port", os.getenv("SMTP_PORT", ""))
        self._smtp_user = self._crow(sm, "SMTP user", os.getenv("SMTP_USER", ""))
        self._smtp_pass = self._crow(sm, "SMTP password", os.getenv("SMTP_PASSWORD", ""), show="•")
        self._smtp_from = self._crow(sm, "From name", os.getenv("SMTP_FROM_NAME", ""))

        # Output dir
        od = self._card(scroll, "📂  Output Directory", "Where reports and results are written")
        orow = ctk.CTkFrame(od, fg_color="transparent"); orow.pack(fill="x", pady=4)
        orow.grid_columnconfigure(0, weight=1)
        self._output_entry = ctk.CTkEntry(orow, height=36, corner_radius=8)
        self._output_entry.grid(row=0, column=0, sticky="ew")
        self._output_entry.insert(0, os.getenv("RESULTS_DIR", "results/"))
        self._accent_btn(orow, "📁  Browse", self._browse_output).grid(row=0, column=1, padx=(8, 0))

        # Save
        save_wrap = ctk.CTkFrame(scroll, fg_color="transparent")
        save_wrap.pack(fill="x", padx=14, pady=(14, 18))
        self._accent_btn(save_wrap, "💾  Save Settings to .env", self._save_env,
                         color="success", height=40, width=220).pack(anchor="w")

    def _crow(self, parent, label, value, show=""):
        r = ctk.CTkFrame(parent, fg_color="transparent"); r.pack(fill="x", pady=4)
        ctk.CTkLabel(r, text=label, width=150, anchor="w",
                     font=ctk.CTkFont(FONT, 12), text_color=COL["muted"]).pack(side="left")
        e = ctk.CTkEntry(r, width=360, height=34, corner_radius=8, show=show)
        e.pack(side="left")
        e.insert(0, value)
        return e

    # ── Log Tab ───────────────────────────────────────────────────────────────────

    def _build_log_tab(self, parent):
        top = ctk.CTkFrame(parent, fg_color="transparent")
        top.pack(fill="x", padx=14, pady=(14, 6))
        ctk.CTkLabel(top, text="▸  Progress & Output",
                     font=ctk.CTkFont(FONT, 15, "bold")).pack(side="left")
        self._progress = ctk.CTkProgressBar(top, width=240, progress_color=COL["accent"])
        self._progress.configure(mode="indeterminate")
        self._progress.set(0)
        self._progress.pack(side="right")

        self._log = ctk.CTkTextbox(parent, corner_radius=10, wrap="word",
                                   font=ctk.CTkFont(MONO, 12),
                                   fg_color=COL["log_bg"], text_color=COL["log_fg"])
        self._log.pack(fill="both", expand=True, padx=14, pady=(6, 14))
        self._log.configure(state="disabled")

    # ── Helpers ───────────────────────────────────────────────────────────────────

    def _log_write(self, msg: str):
        self._log.configure(state="normal")
        self._log.insert("end", msg + "\n")
        self._log.see("end")
        self._log.configure(state="disabled")

    def _set_status(self, msg: str, color=COL["muted"]):
        self._status_lbl.configure(text=msg, text_color=color)
        self._status_dot.configure(text_color=color)

    def _refresh_resume_count(self):
        n = len(self._resume_paths)
        self._resume_count.configure(text=f"{n} file{'s' if n != 1 else ''} added")
        self._resume_list.configure(state="normal")
        self._resume_list.delete("1.0", "end")
        for p in self._resume_paths:
            self._resume_list.insert("end", f"  • {p.name}\n")
        self._resume_list.configure(state="disabled")

    # ── File pickers ─────────────────────────────────────────────────────────────

    def _browse_job(self):
        path = filedialog.askopenfilename(
            title="Select Job Description",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return
        self._job_entry.delete(0, "end")
        self._job_entry.insert(0, path)
        self._job_file_path = path
        # Load the file's text straight into the editor
        try:
            text = Path(path).read_text(encoding="utf-8", errors="replace")
            self._job_text.delete("1.0", "end")
            self._job_text.insert("1.0", text)
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file:\n{e}")

    def _browse_folder(self):
        folder = filedialog.askdirectory(title="Select Resumes Folder")
        if folder:
            for f in Path(folder).iterdir():
                if f.suffix.lower() in {".pdf", ".txt", ".doc", ".docx"} and f not in self._resume_paths:
                    self._resume_paths.append(f)
            self._refresh_resume_count()

    def _browse_files(self):
        files = filedialog.askopenfilenames(
            title="Select Resume Files",
            filetypes=[("Resume files", "*.pdf *.txt *.doc *.docx"), ("All files", "*.*")],
        )
        for f in files:
            fp = Path(f)
            if fp not in self._resume_paths:
                self._resume_paths.append(fp)
        self._refresh_resume_count()

    def _clear_resumes(self):
        self._resume_paths.clear()
        self._refresh_resume_count()

    def _browse_output(self):
        folder = filedialog.askdirectory(title="Select Output Directory")
        if folder:
            self._output_entry.delete(0, "end")
            self._output_entry.insert(0, folder)

    def _on_provider_change(self, _choice=None):
        pass

    def _save_env(self):
        if not ENV_FILE.exists():
            ENV_FILE.write_text("")
        mappings = {
            "LLM_PROVIDER":    self._provider_var.get(),
            "OLLAMA_MODEL":    self._ollama_model.get(),
            "OLLAMA_BASE_URL": self._ollama_url.get(),
            "OPENAI_API_KEY":  self._openai_key.get(),
            "OPENAI_MODEL":    self._openai_model.get(),
            "SMTP_HOST":       self._smtp_host.get(),
            "SMTP_PORT":       self._smtp_port.get(),
            "SMTP_USER":       self._smtp_user.get(),
            "SMTP_PASSWORD":   self._smtp_pass.get(),
            "SMTP_FROM_NAME":  self._smtp_from.get(),
            "RESULTS_DIR":     self._output_entry.get(),
            "COMPANY_NAME":    self._company_entry.get(),
            "MIN_SCORE_THRESHOLD": self._threshold_entry.get(),
            "CHUNK_SIZE":          self._chunk_entry.get(),
        }
        for key, val in mappings.items():
            if val:
                set_key(str(ENV_FILE), key, val)
        messagebox.showinfo("Saved", "Settings saved to .env")

    # ── Screening ────────────────────────────────────────────────────────────────

    def _open_report(self):
        if self._last_html and self._last_html.exists():
            webbrowser.open(self._last_html.as_uri())

    def _start_screening(self):
        if self._running:
            return
        self._running = True
        self._run_btn.configure(state="disabled", text="⏳   Screening...")
        self._progress.start()
        self._set_status("Running...", COL["accent"])
        self.tabs.set("▸  Progress")
        threading.Thread(target=self._run_screening, daemon=True).start()

    def _run_screening(self):
        try:
            self._screening_logic()
        except Exception as e:
            self.after(0, lambda: self._log_write(f"\nFatal error: {e}"))
            self.after(0, lambda: self._set_status("Error", COL["danger"]))
        finally:
            self._running = False
            self.after(0, lambda: self._run_btn.configure(state="normal", text="▶   Start Screening"))
            self.after(0, lambda: self._progress.stop())
            self.after(0, lambda: self._progress.set(0))

    def _screening_logic(self):
        import io
        from dotenv import load_dotenv
        load_dotenv(override=True)

        class GUIWriter(io.TextIOBase):
            def __init__(self, callback):
                self._cb = callback
            def write(self, s):
                if s.strip():
                    self._cb(s.rstrip())
                return len(s)
            def flush(self): pass

        old_stdout = sys.stdout
        sys.stdout = GUIWriter(lambda msg: self.after(0, lambda m=msg: self._log_write(m)))

        try:
            from llm_loader    import get_llm
            from resume_loader import load_all_resumes
            from agents        import BatchScreeningCrew, save_html_report

            # Job description — prefer pasted/loaded text, else read path
            pasted = self._job_text.get("1.0", "end").strip()
            if pasted:
                job_description = pasted
            else:
                job_path = Path(self._job_entry.get().strip())
                if not job_path.exists():
                    self.after(0, lambda: messagebox.showerror("Error", f"Job file not found:\n{job_path}"))
                    return
                job_description = job_path.read_text(encoding="utf-8")

            position = "Open Position"
            for line in job_description.splitlines():
                if line.lower().startswith("position:"):
                    position = line.split(":", 1)[1].strip()
                    break

            company    = self._company_entry.get().strip() or "Our Company"
            threshold  = int(self._threshold_entry.get().strip() or 60)
            chunk_size = int(self._chunk_entry.get().strip() or 4)

            sources = self._resume_paths if self._resume_paths else [
                Path(self._output_entry.get().strip()).parent / "resumes"
            ]
            resumes = load_all_resumes(sources)
            if not resumes:
                self.after(0, lambda: messagebox.showerror("Error", "No resumes found. Add resume files first."))
                return

            llm = get_llm(
                provider = self._provider_var.get(),
                model    = self._ollama_model.get() if self._provider_var.get() == "ollama" else self._openai_model.get(),
                api_key  = self._openai_key.get() or None,
                base_url = self._ollama_url.get() or None,
            )

            results_dir = Path(self._output_entry.get().strip())
            output_dir  = results_dir / "outputs"
            results_dir.mkdir(parents=True, exist_ok=True)

            crew = BatchScreeningCrew(
                llm             = llm,
                job_description = job_description,
                position        = position,
                company         = company,
                output_dir      = output_dir,
                chunk_size      = chunk_size,
            )
            advisor_results, email_drafts = crew.screen(resumes)

            html_path = save_html_report(
                candidates   = advisor_results,
                email_drafts = email_drafts,
                position     = position,
                company      = company,
                results_dir  = results_dir,
                threshold    = threshold,
            )
            self._last_html = html_path

            self.after(0, lambda: self._set_status("Done", COL["success"]))
            self.after(0, lambda: self._log_write(f"\nReport: {html_path}"))
            self.after(500, lambda: webbrowser.open(html_path.as_uri()))

        finally:
            sys.stdout = old_stdout


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    app = ResumeScreenerApp()
    
    app.mainloop()


if __name__ == "__main__":
    main()
