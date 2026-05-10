from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Always resolve .env relative to brain/ root, not the CWD
_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        env_ignore_empty=True,   # shell empty vars don't override .env values
    )

    env: str = "development"
    anthropic_api_key: str
    claude_model: str = "claude-sonnet-4-5"
    log_level: str = "INFO"


settings = Settings()
