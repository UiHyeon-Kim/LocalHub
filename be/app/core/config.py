from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)


# Database
raw_database_url = os.getenv(
    "DATABASE_URL",
    "sqlite:///./database/localhub.db",
)

if raw_database_url.startswith("sqlite:///./"):
    relative_path = raw_database_url.replace(
        "sqlite:///./",
        "",
        1,
    )
    DATABASE_URL = (
        f"sqlite:///{(BASE_DIR / relative_path).resolve()}"
    )
else:
    DATABASE_URL = raw_database_url