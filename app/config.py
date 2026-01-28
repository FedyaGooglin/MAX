import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    token: str
    db_path: Path


def load_config() -> Config:
    token = os.getenv("TOKEN", "")
    if not token:
        raise RuntimeError("TOKEN is not set in environment")
    db_path = Path(os.getenv("DB_PATH", "data/app.db"))
    return Config(token=token, db_path=db_path)
