import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    token: str
    db_path: Path


def load_config() -> Config:
    load_dotenv()
    token = os.getenv("TOKEN", "")
    if not token:
        raise RuntimeError("TOKEN is not set in environment. Add it to the environment or .env")
    db_path = Path(os.getenv("DB_PATH", "data/app.db"))
    return Config(token=token, db_path=db_path)
