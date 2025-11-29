from ..common.logging import get_logger
from ...motherboard.api import append_line, ROOT

log = get_logger("retractor")
RETRACTED_LOG = ROOT / "universe" / "retracted.log"

def retract_fact(fact_id: str, reason: str):
    """Records the retraction of a fact."""
    # In a real system, this would also handle downstream consequences.
    log.warn(f"Retracting fact {fact_id} due to: {reason}")
    append_line(str(RETRACTED_LOG), f"{fact_id} | {reason}")