from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ..common.logging import info, warn

router = APIRouter()

@router.get("/api/health")
def health() -> Dict[str, str]:
    info("Health check")
    return {"status": "ok"}

@router.post("/api/request")
def submit_request(payload: Dict[str, Any]):
    info("Received request to /api/request")
    try:
        # try to use the scaffold gatekeeper if available in PYTHONPATH / project workspace
        from src.approver_god.gating.gatekeeper import process_request  # type: ignore
        outputs = process_request(payload)
        return {"approved": outputs}
    except Exception as e:
        warn("Gatekeeper not available or errored; returning provisional response")
        # minimal safe fallback
        return {"approved": [], "note": "gatekeeper unavailable", "error": str(e)}
