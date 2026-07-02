"""
llm_loader.py — Load an LLM for CrewAI from .env config.
Supports: Ollama (local), OpenAI.
"""

from crewai import LLM


def get_llm(
    provider: str,
    model: str,
    api_key: str | None = None,
    base_url: str | None = None,
) -> LLM:
    provider = (provider or "").lower().strip()

    if provider == "openai":
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required for OpenAI provider.")
        return LLM(model=f"openai/{model}", api_key=api_key)

    elif provider == "ollama":
        return LLM(
            model=f"ollama/{model}",
            base_url=base_url or "http://localhost:11434",
            temperature=0,          # deterministic for consistent scoring
        )

    else:
        raise ValueError(
            f"Unknown LLM provider: '{provider}'. "
            "Supported: 'openai', 'ollama'"
        )


def get_llm_from_env() -> LLM:
    """Convenience: build LLM entirely from environment variables."""
    import os
    print("Loading LLM from environment variables...")
    return get_llm(
        provider = os.getenv("LLM_PROVIDER", "ollama"),
        model    = os.getenv("OLLAMA_MODEL") or os.getenv("OPENAI_MODEL", "llama3:instruct"),
        api_key  = os.getenv("OPENAI_API_KEY"),
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    )

