from typing import Dict, Any
from ...motherboard.api import add_earth_fact
from ..common.logging import get_logger

log = get_logger("promoter")

def promote_to_earth(approved_hypothesis: Dict[str, Any], lineage: str, source: str) -> Dict[str, Any]:
    """Promotes a validated hypothesis to an Earth Fact."""
    confidence = approved_hypothesis.get("confidence_score", 0.98)
    trust_tier = "approved_simulation"
    
    fact = add_earth_fact(approved_hypothesis, source, lineage, trust_tier, confidence)
    log.info(f"Promoted to Earth Fact: {fact['fact_id']}")
    return fact