from typing import Dict, Any
from hashlib import sha256
from time import time
from pathlib import Path
from src.common.fileio import append_line, read_json, write_json

ROOT = Path(__file__).resolve().parents[1]
AUDIT_LOG = ROOT / "approver_god" / "logs" / "audit_chain.log"
AUDIT_STATE = ROOT / "approver_god" / "logs" / "audit_state.json"

def _head_hash() -> str:
    data = read_json(str(AUDIT_STATE)) or {}
    return data.get("head", "")

def _set_head(h: str) -> None:
    write_json(str(AUDIT_STATE), {"head": h})

def record(event: str, actor: str, payload: Dict[str, Any]) -> str:
    ts = int(time())
    prev = _head_hash()
    raw = f"{ts}|{actor}|{event}|{payload}|{prev}"
    h = sha256(raw.encode("utf-8")).hexdigest()
    append_line(str(AUDIT_LOG), f"{raw}|{h}")
    _set_head(h)
    return h
from typing import Dict, Any
from hashlib import sha256
from time import time
from pathlib import Path
from src.common.fileio import append_line, read_json, write_json

ROOT = Path(__file__).resolve().parents[1]
AUDIT_LOG = ROOT / "approver_god" / "logs" / "audit_chain.log"
AUDIT_STATE = ROOT / "approver_god" / "logs" / "audit_state.json"

def _head_hash() -> str:
    data = read_json(str(AUDIT_STATE)) or {}
    return data.get("head", "")

def _set_head(h: str) -> None:
    write_json(str(AUDIT_STATE), {"head": h})

def record(event: str, actor: str, payload: Dict[str, Any]) -> str:
    ts = int(time())
    prev = _head_hash()
    raw = f"{ts}|{actor}|{event}|{payload}|{prev}"
    h = sha256(raw.encode("utf-8")).hexdigest()
    append_line(str(AUDIT_LOG), f"{raw}|{h}")
    _set_head(h)
    return h
