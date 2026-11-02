import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR.parent / ".env", override=False)
    load_dotenv(BASE_DIR / ".env", override=False)
except Exception:
    pass

class Settings:
    APP_NAME: str = "AGRO AI"
    APP_TAGLINE: str = "Smart Agriculture. Healthy Lives. Better Future."
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Security
    JWT_SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY", secrets.token_urlsafe(48)
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'agro_ai.db'}"
    )

    # Directories
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    MODELS_DIR: Path = BASE_DIR / "models"

    # CORS
    ALLOWED_ORIGINS: list[str] = [
        origin.strip() for origin in os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000,http://127.0.0.1:8000"
        ).split(",") if origin.strip()
    ]

settings = Settings()

# Ensure required directories exist
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.MODELS_DIR.mkdir(parents=True, exist_ok=True)
