import os
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[2]

def get_env(key: str, default: str = "") -> str:
    """Return environment variable or default."""
    return os.getenv(key, default)

def project_root() -> Path:
    """Return the local myproject root path (two levels up from this file)."""
    return ROOT
