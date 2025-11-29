from fastapi import FastAPI, Depends, Body
from src.security.auth import get_role
from src.security.rbac import require
from src.security.rate_limit import check_rate
from src.security.validators import validate_payload, CharacterPayload, BatchPayload

# ... existing imports and app startup ...

@app.post("/project/update")
def update_project_info(config: Dict[str, Any], role: str = Depends(get_role)):
    check_rate(role, "/project/update")
    require(role, "manage_project")
    update_project(config)
    return {"status": "updated"}

@app.post("/registry/character")
def add_character(payload: Dict[str, Any] = Body(...), role: str = Depends(get_role)):
    check_rate(role, "/registry/character")
    require(role, "manage_registry")
    data = validate_payload(CharacterPayload, payload)
    char = register_character(data["char_id"], data["face_id"], data["voice_id"], data["outfit_id"])
    char.update({"traits": data["traits"], "phys": data["phys"], "voice": data["voice"]})
    return char

@app.post("/batch")
def run_batch(payload: Dict[str, Any] = Body(...), role: str = Depends(get_role)):
    check_rate(role, "/batch")
    require(role, "run_batch")
    data = validate_payload(BatchPayload, payload)
    result = orchestrate_batch(start=data["start"], end=data["end"], retry_limit=data["retry_limit"])
    pkg_path = export_project_package(get_project(), {"details": result["details"]})
    return {"summary": result, "package_export": pkg_path}

@app.get("/evaluate")
def evaluate(role: str = Depends(get_role)):
    check_rate(role, "/evaluate")
    require(role, "evaluate")
    return run_all_suites()

@app.post("/retrain/embeddings")
def retrain(role: str = Depends(get_role)):
    check_rate(role, "/retrain/embeddings")
    require(role, "retrain")
    result = retrain_embeddings()
    log_training("embeddings", result)
    return result

@app.post("/longform")
def export_longform(role: str = Depends(get_role)):
    check_rate(role, "/longform")
    require(role, "export")
    return build_longform_package()
from src.marketplace.registry import add_market_asset, list_market_assets
from src.marketplace.licensing import check_license

@app.post("/marketplace/asset")
def register_asset(asset: Dict[str, Any], role: str = Depends(get_role)):
    check_rate(role, "/marketplace/asset")
    require(role, "manage_registry")
    add_market_asset(asset)
    record("marketplace_asset_add", role, {"asset_id": asset.get("asset_id")})
    return {"status": "registered"}

@app.get("/marketplace/assets")
def get_assets(role: str = Depends(get_role)):
    check_rate(role, "/marketplace/assets")
    require(role, "evaluate")
    return {"assets": list_market_assets()}
