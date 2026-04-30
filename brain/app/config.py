from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = "development"
    anthropic_api_key: str
    claude_model: str = "claude-sonnet-4-5"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
