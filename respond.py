from typing import Dict, Any
from ...motherboard.api import get_earth_facts
from ..common.logging import get_logger

log = get_logger("baby_science")

def respond(request: Dict[str, Any]) -> Dict[str, Any]:
    """Responds to a request using only approved Earth knowledge."""
    facts = get_earth_facts()
    if not facts:
        return {"response": "I have no approved knowledge to answer this request."}
    
    log.info(f"Responding with guidance from {len(facts)} Earth facts.")
    return {"response": "Based on approved Earth knowledge, here is a novel insight:", "guidance": facts[-1]}