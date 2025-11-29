from pathlib import Path
from typing import Dict, Any, List
from src.common.fileio import read_json, write_json, append_line
from src.common.ids import make_id
from src.common.logging import get_logger
import time

log = get_logger("motherboard_api")

ROOT = Path(__file__).resolve().parent
EARTH_DIR = ROOT / "earth"
UNIVERSE_DIR = ROOT / "universe"

EARTH_FACTS = EARTH_DIR / "facts.json"
EARTH_LINEAGE = EARTH_DIR / "lineage.log"
UNIVERSE_HYPS = UNIVERSE_DIR / "hypotheses.json"

def get_earth_facts() -> List[Dict[str, Any]]:
    """Retrieves all approved facts from the Motherboard."""
    return read_json(str(EARTH_FACTS)).get("facts", [])

def add_earth_fact(content: Dict[str, Any], source: str, lineage: str, trust_tier: str, confidence: float) -> Dict[str, Any]:
    """
    Adds a new, approved fact to the Motherboard.
    This is the primary function for promoting knowledge from the Approver GOD.
    """
    data = read_json(str(EARTH_FACTS))
    facts = data.get("facts", [])

    fact = {
        "fact_id": make_id("FACT"),
        "version": 1,
        "status": "approved",
        "trust_tier": trust_tier,
        "source": source,
        "confidence": confidence,
        "lineage": lineage,
        "content": content,
        "timestamp": int(time.time())
    }

    facts.append(fact)
    write_json(str(EARTH_FACTS), {"facts": facts})
    append_line(str(EARTH_LINEAGE), f"{fact['fact_id']} | {lineage}")
    log.info(f"Added Earth Fact: {fact['fact_id']} (Source: {source})")
    return fact

def add_universe_hypothesis(hyp: Dict[str, Any]) -> Dict[str, Any]:
    """Adds a provisional hypothesis to the Universe for later testing."""
    data = read_json(str(UNIVERSE_HYPS))
    hyps = data.get("hypotheses", [])
    hyps.append(hyp)
    write_json(str(UNIVERSE_HYPS), {"hypotheses": hyps})
    log.info(f"Added Universe Hypothesis: {hyp.get('hypothesis_id')}")
    return hyp