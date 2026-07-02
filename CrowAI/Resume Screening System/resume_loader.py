"""
resume_loader.py — Load resumes from files/directories.

Returns a single dict:  { "Candidate Name": "full resume text" }

Supported formats: .txt, .pdf, .doc, .docx
Candidate name is derived from the filename (underscores → spaces, title-cased).
"""

from pathlib import Path

try:
    from langchain_community.document_loaders import (
        TextLoader,
        PyMuPDFLoader,
        UnstructuredWordDocumentLoader,
    )
    _HAS_LANGCHAIN = True
except ImportError:
    _HAS_LANGCHAIN = False

SUPPORTED = {".txt", ".pdf", ".doc", ".docx"}


def _load_file(filepath: Path) -> str:
    """Load a single resume file and return its text content."""
    suffix   = filepath.suffix.lower()
    path_str = str(filepath)

    if not _HAS_LANGCHAIN:
        if suffix == ".txt":
            return filepath.read_text(encoding="utf-8", errors="ignore")
        raise ImportError(
            "langchain_community is required for PDF/DOCX support. "
            "Run: pip install langchain-community pymupdf unstructured"
        )

    try:
        if suffix == ".txt":
            docs = TextLoader(path_str, encoding="utf-8", autodetect_encoding=True).load()
        elif suffix == ".pdf":
            docs = PyMuPDFLoader(path_str).load()
        elif suffix in (".doc", ".docx"):
            docs = UnstructuredWordDocumentLoader(path_str).load()
        else:
            return ""

        return "\n".join(d.page_content for d in docs if d.page_content).strip()

    except Exception as e:
        print(f"  ⚠  Failed to load {filepath.name}: {e}")
        return ""


def load_all_resumes(sources: "str | Path | list[str | Path]") -> dict[str, str]:
    """
    Load all resumes from a directory, a single file, or a list of either.

    Returns:
        {"Candidate Name": "full resume text", ...}
    """
    if not isinstance(sources, list):
        sources = [sources]

    files: list[Path] = []
    for src in sources:
        src = Path(src)
        if src.is_dir():
            files.extend(
                f for f in sorted(src.iterdir())
                if f.suffix.lower() in SUPPORTED
            )
        elif src.is_file():
            if src.suffix.lower() in SUPPORTED:
                files.append(src)
            else:
                print(f"  ⚠  Skipping unsupported file: {src.name}")
        else:
            print(f"  ⚠  Path not found: {src}")

    # Deduplicate while preserving order
    seen: set[Path] = set()
    unique = [f for f in files if not (f in seen or seen.add(f))]

    resumes: dict[str, str] = {}
    for f in unique:
        name = f.stem.replace("_", " ").replace("-", " ").title()
        text = _load_file(f)
        if text.strip():
            resumes[name] = text
        else:
            print(f"  ⚠  Empty content — skipping: {f.name}")

    return resumes
