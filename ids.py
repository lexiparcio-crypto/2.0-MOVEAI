import time
import hashlib

def make_id(prefix: str) -> str:
    """Creates a unique ID with a given prefix."""
    ts = str(time.time_ns())
    return f"{prefix.upper()}_{hashlib.sha256(ts.encode()).hexdigest()[:12]}"