from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from app.utils import load_key

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    PORT: int = 8000
    HOST: str = "127.0.0.1"
    ECHO: bool = False
    DB_URL: str
    ALGORITHM: str = "RS256"
    PUBLIC_KEY: bytes = load_key(BASE_DIR / "public.pem")
    PRIVATE_KEY: bytes = load_key(BASE_DIR / "private.pem")

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env", extra="ignore")


settings = Settings()
