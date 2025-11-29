from typing import Dict
from src.common.fileio import read_json, write_json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METRICS_PATH = ROOT / "config" / "metrics.yaml"

def _load() -> Dict:
    try:
        return read_json(str(METRICS_PATH)) or {"metrics": {}}
    except Exception:
        return {"metrics": {}}

def _save(data: Dict) -> None:
    # store as JSON for simplicity
    write_json(str(METRICS_PATH), data)

def inc_counter(name: str, by: int = 1) -> None:
    data = _load()
    counters = data["metrics"].get("counters", {})
    counters[name] = counters.get(name, 0) + by
    data["metrics"]["counters"] = counters
    _save(data)

def set_gauge(name: str, value: float) -> None:
    data = _load()
    gauges = data["metrics"].get("gauges", {})
    gauges[name] = value
    data["metrics"]["gauges"] = gauges
    _save(data)
