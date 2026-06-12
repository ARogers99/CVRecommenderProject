from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    adzuna_app_id: str
    adzuna_app_key: str
    anthropic_api_key: str
    jsearch_api_key: str

    class Config:
        env_file = ".env"

settings = Settings()