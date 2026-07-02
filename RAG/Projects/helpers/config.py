from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str

    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    MONGODB_URL: str
    MONGODB_DATABASE: str

    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    OPENAI_API_KEY: str | None = None
    OPENAI_API_URL: str | None = None

    OLLAMA_API_URL: str | None = None
    OLLAMA_API_KEY: str | None = None

    COHERE_API_KEY: str | None = None

    GENERATION_MODEL_ID: str | None = None
    EMBEDDING_MODEL_ID: str | None = None
    EMBEDDING_MODEL_SIZE: int | None = None

    INPUT_DAFAULT_MAX_CHARACTERS: int | None = None
    GENERATION_DAFAULT_MAX_TOKENS: int | None = None
    GENERATION_DAFAULT_TEMPERATURE: float | None = None

    VECTOR_DB_BACKEND: str
    VECTOR_DB_PATH: str
    VECTOR_DB_DISTANCE_METHOD: str | None = None

    PRIMARY_LANG: str = "en"
    DEFAULT_LANG: str = "en"

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()