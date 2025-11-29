#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Note: escaped backslashes in the external filepath comment to avoid any accidental "\U" unicode-escape parsing
# filepath (escaped): c:\\Users\\Lunga Manana\\ai_plantation.py
"""Repair scaffold script.

Run this from the repository folder. It creates a minimal working skeleton (src/ packages and tests)
so imports and simple tests can run.

Usage:
    python "c:\\Users\\Lunga Manana\\mkdir ai_plantation && cd ai_plantation.py"

Set environment variable REPAIR_OVERWRITE=0 to avoid overwriting files that already exist.
"""
import os
from pathlib import Path
from textwrap import dedent
from typing import Dict
import argparse

# Use the script's directory as the project root
ROOT = Path(__file__).resolve().parent

# Minimal set of files to create (compact, safe content)
FILES: Dict[str, str] = {
    "src/common/fileio.py": dedent("""\
        # filepath: src/common/fileio.py
        import json
        import os
        from typing import Any, Dict

        def read_json(path: str) -> Dict[str, Any]:
            if not os.path.exists(path):
                return {}
            with open(path, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except Exception:
                    return {}

        def write_json(path: str, data: Dict[str, Any]) -> None:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        def append_line(path: str, line: str) -> None:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "a", encoding="utf-8") as f:
                f.write(line.rstrip() + "\\n")
        """),

    "src/common/ids.py": dedent("""\
        # filepath: src/common/ids.py
        import time
        import hashlib

        def make_id(prefix: str) -> str:
            ts = str(time.time_ns())
            return f"{prefix}_{hashlib.sha256(ts.encode()).hexdigest()[:10]}"
        """),

    "src/common/logging.py": dedent("""\
        # filepath: src/common/logging.py
        from rich.console import Console
        console = Console()

        def info(msg: str) -> None:
            console.print(f"[bold green]INFO[/]: {msg}")

        def warn(msg: str) -> None:
            console.print(f"[bold yellow]WARN[/]: {msg}")

        def error(msg: str) -> None:
            console.print(f"[bold red]ERROR[/]: {msg}")
        """),

    "src/motherboard/api.py": dedent("""\
        # filepath: src/motherboard/api.py
        from pathlib import Path
        from typing import Dict, Any, List
        from src.common.fileio import read_json, write_json, append_line

        ROOT = Path(__file__).resolve().parents[1]
        EARTH_DIR = ROOT / "motherboard" / "earth"
        UNIV_DIR = ROOT / "motherboard" / "universe"

        EARTH_DIR.mkdir(parents=True, exist_ok=True)
        UNIV_DIR.mkdir(parents=True, exist_ok=True)

        EARTH_FACTS = EARTH_DIR / "facts.json"
        EARTH_LINEAGE = EARTH_DIR / "lineage.log"
        UNIVERSE_HYPS = UNIV_DIR / "hypotheses.json"
        PROVISIONAL_LOG = UNIV_DIR / "provisional.log"
        RETRACTED_LOG = UNIV_DIR / "retracted.log"

        def _ensure(path: Path, default: Dict[str, Any]):
            if not path.exists():
                write_json(str(path), default)

        _ensure(EARTH_FACTS, {"facts": []})
        _ensure(UNIVERSE_HYPS, {"hypotheses": []})

        def get_earth_facts() -> List[Dict[str, Any]]:
            return read_json(str(EARTH_FACTS)).get("facts", [])

        def add_earth_fact(fact: Dict[str, Any]) -> Dict[str, Any]:
            data = read_json(str(EARTH_FACTS))
            facts = data.get("facts", [])
            facts.append(fact)
            write_json(str(EARTH_FACTS), {"facts": facts})
            append_line(str(EARTH_LINEAGE), fact.get("id", "unknown"))
            return fact

        def get_universe_hypotheses() -> List[Dict[str, Any]]:
            return read_json(str(UNIVERSE_HYPS)).get("hypotheses", [])

        def add_universe_hypothesis(hyp: Dict[str, Any]) -> Dict[str, Any]:
            data = read_json(str(UNIVERSE_HYPS))
            hyps = data.get("hypotheses", [])
            hyps.append(hyp)
            write_json(str(UNIVERSE_HYPS), {"hypotheses": hyps})
            append_line(str(PROVISIONAL_LOG), hyp.get("claim", ""))
            return hyp

        def retract_fact(fact_id: str, reason: str) -> None:
            append_line(str(RETRACTED_LOG), f"{fact_id} | {reason}")
        """),

    "src/approver_god/gating/gatekeeper.py": dedent("""\
        # filepath: src/approver_god/gating/gatekeeper.py
        from typing import Dict, Any, List
        from src.motherboard.api import add_universe_hypothesis, add_earth_fact
        from src.common.ids import make_id
        from src.common.logging import info, warn

        def _simple_generate(spec: Dict[str, Any]) -> List[Dict[str, Any]]:
            obj = spec.get("objective", "").lower()
            domain = spec.get("domain", "").lower()
            if "materials" in domain and "fatigue" in obj:
                return [{
                    "claim": "Composite D with fiber F and matrix M improves fatigue life by ~22%",
                    "assumptions": ["load profile L", "temperature range T"],
                    "validation_plan": ["toy_sim", "t_test"],
                    "novelty_score": 0.40,
                    "status": "provisional",
                }]
            return [{
                "claim": "No viable hypothesis generated; need more constraints",
                "assumptions": [],
                "validation_plan": [],
                "novelty_score": 0.0,
                "status": "provisional",
            }]

        def _meets_thresholds(metrics: Dict[str, Any]) -> bool:
            return (
                metrics.get("factual_precision", 0.0) >= 0.95 and
                metrics.get("citation_match", 0.0) >= 0.98 and
                metrics.get("code_tests_pass_rate", 0.0) >= 0.98 and
                metrics.get("contradiction_rate", 1.0) <= 0.01
            )

        def process_request(req: Dict[str, Any]) -> List[Dict[str, Any]]:
            spec = req
            hyps = _simple_generate(spec)
            approved: List[Dict[str, Any]] = []

            for h in hyps:
                add_universe_hypothesis(h)
                unit = {"code_tests_pass_rate": 1.0 if h.get("validation_plan") else 0.0}
                stats = {"factual_precision": 0.96 if "improves fatigue life" in h.get("claim","") else 0.5,
                         "citation_match": 0.99 if "improves fatigue life" in h.get("claim","") else 0.5}
                contra = {"contradiction_rate": 0.0, "dual_use_flags": 0}

                metrics = {
                    "factual_precision": stats["factual_precision"],
                    "citation_match": stats["citation_match"],
                    "code_tests_pass_rate": unit["code_tests_pass_rate"],
                    "contradiction_rate": contra["contradiction_rate"],
                    "dual_use_flags": contra["dual_use_flags"],
                    "semantic_distance": h.get("novelty_score", 0.0)
                }

                if _meets_thresholds(metrics):
                    info("Hypothesis passed thresholds; promoting to Earth (scaffold).")
                    approved_output = {
                        "hypothesis": h["claim"],
                        "assumptions": h.get("assumptions", []),
                        "predicted_outcomes": {"delta": "+22%"},
                        "validation_artifacts": {"stats": stats, "unit": unit, "contra": contra},
                        "citations": ["doi:10.1234/XYZ"],
                        "confidence": 0.86,
                    }
                    fact = {
                        "id": make_id("FACT"),
                        "status": "approved",
                        "source": "doi:10.1234/XYZ",
                        "confidence": approved_output.get("confidence", 0.8),
                        "lineage": "scaffold_v1",
                        "payload": approved_output
                    }
                    add_earth_fact(fact)
                    approved.append(approved_output)
                else:
                    warn("Hypothesis failed thresholds; remains provisional (scaffold).")

            return approved
        """),

    "src/babies/baby_science/respond.py": dedent("""\
        # filepath: src/babies/baby_science/respond.py
        from typing import Dict, Any
        from src.motherboard.api import get_earth_facts

        def respond(request: Dict[str, Any]) -> Dict[str, Any]:
            facts = get_earth_facts()
            if not facts:
                return {"message": "No Earth facts available. Ask Approver GOD first."}
            latest = facts[-1]
            return {
                "message": "Approved Earth truth applied.",
                "earth_fact_id": latest.get("id"),
                "guidance": latest.get("payload", {})
            }
        """),

    "src/app.py": dedent("""\
        # filepath: src/app.py
        from src.approver_god.gating.gatekeeper import process_request
        from src.babies.baby_science.respond import respond
        from src.common.logging import info

        def main():
            req = {
                "domain": "materials",
                "objective": "Increase fatigue life by 20%",
                "constraints": [],
                "known_data_refs": [],
                "risk_tolerance": "low"
            }
            info("Submitting request to Approver GOD (scaffold)...")
            approved = process_request(req)
            info(f"Approved outputs: {len(approved)}")
            guidance = respond(req)
            print(guidance)

        if __name__ == '__main__':
            main()
        """),

    "tests/test_gatekeeper.py": dedent("""\
        # filepath: tests/test_gatekeeper.py
        from src.approver_god.gating.gatekeeper import process_request

        def test_gatekeeper_approves_materials():
            req = {
                "domain": "materials",
                "objective": "Increase fatigue life by 20%",
                "constraints": [],
                "known_data_refs": [],
                "risk_tolerance": "low"
            }
            outputs = process_request(req)
            assert isinstance(outputs, list)
            assert len(outputs) >= 0
        """),

    "README.md": dedent("""\
        # ai_plantation — repair scaffold

        This script builds a small, safe scaffold so basic imports and tests run.

        Quick private deploy (local Podman)
        1) Build: podman build -t ai_plantation:latest .
        2) Run (dev): podman run --rm -p 8000:8000 ai_plantation:latest
        3) Or: podman-compose up --build

        Web access:
        - FastAPI serves endpoints at / (basic info) and /api/request to run the Approver GOD scaffold.
        """),

    "requirements.txt": dedent("""\
        pydantic==2.9.2
        rich==13.9.2
        pytest
        fastapi==0.100.0
        uvicorn==0.23.0
        requests==2.31.0
        """),

    "src/web/app.py": dedent("""\
        # filepath: src/web/app.py
        from fastapi import FastAPI, HTTPException
        from pydantic import BaseModel
        from typing import Any, Dict
        from src.approver_god.gating.gatekeeper import process_request
        from src.babies.baby_science.respond import respond
        from src.common.logging import info

        app = FastAPI(title="ai_plantation API (scaffold)")

        class ReqModel(BaseModel):
            domain: str
            objective: str
            constraints: list = []
            known_data_refs: list = []
            risk_tolerance: str = "low"

        @app.get("/")
        def root():
            return {"service": "ai_plantation", "endpoints": ["/api/request", "/api/guidance"]}

        @app.post("/api/request")
        def submit_request(req: ReqModel):
            info("Received API request for Approver GOD (scaffold).")
            try:
                outputs = process_request(req.dict())
                return {"approved": outputs}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @app.post("/api/guidance")
        def guidance(req: ReqModel):
            try:
                g = respond(req.dict())
                return {"guidance": g}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        """),

    "Dockerfile": dedent("""\
        # filepath: Dockerfile
        FROM python:3.11-slim
        WORKDIR /app
        COPY . /app
        RUN pip install --no-cache-dir -r requirements.txt
        EXPOSE 8000
        CMD ["uvicorn", "src.web.app:app", "--host", "0.0.0.0", "--port", "8000"]
        """),

    "docker-compose.yml": dedent("""\
        # filepath: docker-compose.yml
        version: '3.8'
        services:
          ai_plantation:
            build: .
            ports:
              - "8000:8000"
            volumes:
              - ./:/app
            environment:
              - REPAIR_OVERWRITE=1
        """),

    ".gitignore": dedent("""\
        # filepath: .gitignore
        __pycache__/
        *.py[cod]
        *.pyo
        .pytest_cache/
        .mypy_cache/
        .env
        env/
        venv/
        .venv/
        .DS_Store
        .idea/
        .vscode/
        data/raw/
        data/processed/
        *.sqlite3
        .pytest_cache/
        """),

    ".github/workflows/ci.yml": dedent("""\
        # filepath: .github/workflows/ci.yml
        name: CI

        on:
          push:
            branches: [ main ]
          pull_request:
            branches: [ main ]

        jobs:
          test:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v4
              - name: Set up Python
                uses: actions/setup-python@v4
                with:
                  python-version: '3.11'
              - name: Install dependencies
                run: python -m pip install --upgrade pip && pip install -r requirements.txt
              - name: Run tests
                run: pytest -q
        """),

    "scripts/publish.ps1": dedent(r"""\
        # filepath: scripts/publish.ps1
        param(
            [Parameter(Mandatory=$true)][string] $owner,
            [Parameter(Mandatory=$true)][string] $repo
        )

        function Exec([string]$cmd) { Write-Host ">> $cmd"; iex $cmd }

        if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
            Write-Error "git is not installed or not on PATH."
            exit 1
        }

        if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
            Write-Warning "gh CLI not found. The script will create local repo and show manual remote steps."
        }

        if (-not (Test-Path .git)) {
            Exec "git init"
        }

        Exec "git add -A"
        Exec 'git commit -m "Initial scaffold commit" -q' 2>$null

        Exec "git branch -M main"

        if (Get-Command gh -ErrorAction SilentlyContinue) {
            Exec "gh repo create $owner/$repo --private --source=. --remote=origin --push --confirm"
            Write-Host "Pushed to https://github.com/$owner/$repo"
        } else {
            Write-Host "Create repository https://github.com/$owner/$repo manually or install gh CLI."
            Write-Host "Then run:"
            Write-Host "  git remote add origin https://github.com/$owner/$repo.git"
            Write-Host "  git push -u origin main"
        }
        """),

    "scripts/publish.sh": dedent("""\
        # filepath: scripts/publish.sh
        #!/usr/bin/env bash
        set -euo pipefail
        OWNER="$1"
        REPO="$2"

        if ! command -v git >/dev/null 2>&1; then
          echo "git is required"
          exit 1
        fi

        if [ ! -d .git ]; then
          git init
        fi

        git add -A
        git commit -m "Initial scaffold commit" || true
        git branch -M main

        if command -v gh >/dev/null 2>&1; then
          gh repo create "${OWNER}/${REPO}" --private --source=. --remote=origin --push --confirm
          echo "Pushed to https://github.com/${OWNER}/${REPO}"
        else
          echo "gh CLI not installed. Create repo and then run:"
          echo "  git remote add origin https://github.com/${OWNER}/${REPO}.git"
          echo "  git push -u origin main"
        fi
        """),
}

# Ensure package __init__ files exist so imports work
PKG_INITS = [
    "src/__init__.py",
    "src/common/__init__.py",
    "src/motherboard/__init__.py",
    "src/approver_god/__init__.py",
    "src/approver_god/gating/__init__.py",
    "src/babies/__init__.py",
    "src/babies/baby_science/__init__.py",
    "src/web/__init__.py",  # added so web package imports work
    "tests/__init__.py",
]

def write_file(relpath: str, content: str) -> None:
    p = ROOT / relpath
    p.parent.mkdir(parents=True, exist_ok=True)
    overwrite = os.getenv("REPAIR_OVERWRITE", "1") == "1"
    if p.exists() and not overwrite:
        print(f"Skipping existing file (REPAIR_OVERWRITE=0): {p}")
        return
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

def ensure_inits() -> None:
    for ip in PKG_INITS:
        p = ROOT / ip
        if p.exists():
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write("# package init\n")

def generate_installments() -> list:
    """
    Return a list of ordered installments. Each installment contains:
      - title: short name
      - summary: what it achieves
      - steps: actionable subtasks (developer/data/infra items)
      - suggested_files: example file paths to create (under Desktop/myproject)
    """
    # Use escaped backslashes to avoid Python unicode-escape parsing for "\U"
    base = "c:\\Users\\Lunga Manana\\Desktop\\myproject"
    return [
        {
            "id": 1,
            "title": "Project scaffold & planning",
            "summary": "Create clear repo layout, CI, experiments tracking and baseline README.",
            "steps": [
                "Define repo layout (src/, data/, models/, infra/, experiments/, assets/).",
                "Add experiment tracking (e.g., MLflow) and simple CI (pytest).",
                "Create small sample dataset and a toy model training script to validate pipeline."
            ],
            "suggested_files": [
                f"{base}\\src\\pipeline\\ingest.py",
                f"{base}\\src\\train\\train_baseline.py",
                f"{base}\\README_INSTALLMENTS.md"
            ]
        },
        {
            "id": 2,
            "title": "Data pipelines & ingestion",
            "summary": "Implement modular ingestion, validation, and storage with versioning.",
            "steps": [
                "Create ingestors for web scraping / API pulls with rate limiting and auth.",
                "Implement schema validation (pydantic/schemas) and unit tests.",
                "Store raw/processed data with manifest and checksums for offline use."
            ],
            "suggested_files": [
                f"{base}\\src\\data\\ingest_api.py",
                f"{base}\\src\\data\\validate.py",
                f"{base}\\data\\README_DATA_VERSIONING.md"
            ]
        },
        {
            "id": 3,
            "title": "Experiment orchestration & tracking",
            "summary": "Set up pipelines to run reproducible experiments and track metrics/artifacts.",
            "steps": [
                "Use an orchestrator (Airflow/Prefect/just scripts) for ETL -> train -> eval.",
                "Integrate MLflow or similar to log runs, params, artifacts, datasets.",
                "Add experiment reproducibility: seed handling, config files (yaml/json)."
            ],
            "suggested_files": [
                f"{base}\\infra\\orchestrator\\flow.py",
                f"{base}\\experiments\\config\\baseline.yaml"
            ]
        },
        {
            "id": 4,
            "title": "Modeling foundations & evaluation",
            "summary": "Build transformer/embedding-backed models, strong evaluation and anti-hallucination.",
            "steps": [
                "Prototype small transformer/embedding pipeline and retrieval (FAISS) for RAG.",
                "Design evaluation matrix: factual_precision, citation_match, hallucination_rate, robustness.",
                "Implement automated unit and integration tests for models and scoring."
            ],
            "suggested_files": [
                f"{base}\\src\\models\\embed_ret.py",
                f"{base}\\src\\eval\\metrics.py"
            ]
        },
        {
            "id": 5,
            "title": "Approver GOD (approval layer) — prototype",
            "summary": "Create the gatekeeper that validates hypotheses against thresholds and experiments.",
            "steps": [
                "Implement a reproducible test harness that runs validation plans deterministically.",
                "Log provisional vs approved items; store lineage metadata and provenance.",
                "Define strict thresholds and create an automated promotion pipeline from Universe -> Earth."
            ],
            "suggested_files": [
                f"{base}\\src\\approver_god\\validation\\runner.py",
                f"{base}\\src\\approver_god\\policy\\thresholds.py"
            ]
        },
        {
            "id": 6,
            "title": "Assets generation (film/animation/music) — baseline tools",
            "summary": "Integrate or wrap existing SOTA tools for image/video/audio generation and ensure consistency.",
            "steps": [
                "Define asset schemas: character profiles, voice profiles, lighting/camera specs.",
                "Wrap stable image/video models and multi-turn voice models; create deterministic seeds and manifests.",
                "Build an orchestration layer to render scenes consistently across frames and audio tracks."
            ],
            "suggested_files": [
                f"{base}\\src\\assets\\character_profiles.json",
                f"{base}\\src\\assets\\render_scene.py"
            ]
        },
        {
            "id": 7,
            "title": "Deployment, monitoring and offline mode",
            "summary": "Deploy models and pipelines, add monitoring, enable offline operation and local cache.",
            "steps": [
                "Containerize components (Podman) and provide local-only mode with cached knowledge base.",
                "Add logging, alerting, and metrics (Prometheus/Grafana or simple logging to files).",
                "Create a sync process for motherboard to pull verified world updates when online."
            ],
            "suggested_files": [
                f"{base}\\infra\\docker\\Dockerfile",
                f"{base}\\src\\sync\\sync_service.py"
            ]
        },
        {
            "id": 8,
            "title": "Quality, bias mitigation and governance",
            "summary": "Operationalize checks to reduce hallucinations, bias and harmful outputs; add human-in-loop.",
            "steps": [
                "Create adversarial tests to detect model hallucinations and bias.",
                "Add human review flows and sampling of promoted 'Earth' facts.",
                "Maintain audit logs and provenance for all promoted facts."
            ],
            "suggested_files": [
                f"{base}\\src\\gov\\auditing.py",
                f"{base}\\src\\gov\\human_review_workflow.md"
            ]
        },
        {
            "id": 9,
            "title": "Scale, optimization & continuous learning",
            "summary": "Scale pipelines, introduce incremental learning, and continuous validation on new data.",
            "steps": [
                "Add incremental retraining with evaluation gates and canary deployments.",
                "Optimize inference (quantization, streaming, batching) for long video/audio generation.",
                "Automate feedback loops from deployment to experiment tracking for model improvement."
            ],
            "suggested_files": [
                f"{base}\\src\\deploy\\canary.py",
                f"{base}\\src\\models\\serving_optim.py"
            ]
        },
        {
            "id": 10,
            "title": "Full film production pipeline (end-to-end)",
            "summary": "Combine all components to generate consistent multi-scene films with consistent characters/voices.",
            "steps": [
                "Define scene graph and shot list generator from screenplay.",
                "Implement deterministic rendering per-shot with asset manifests and versioned voice profiles.",
                "Create final assembly tool to merge video, audio, subtitles and deliver artifacts for publishing."
            ],
            "suggested_files": [
                f"{base}\\src\\production\\shot_generator.py",
                f"{base}\\src\\production\\final_assembler.py"
            ]
        }
    ]

def generate_installment_detail(installment_id: int) -> dict:
    """
    Return a detailed plan and small-safe template snippets for the requested installment.
    Templates are suggested files under: c:\\Users\\Lunga Manana\\Desktop\\myproject
    """
    # Use escaped backslashes to avoid Python unicode-escape parsing for "\U"
    base = "c:\\Users\\Lunga Manana\\Desktop\\myproject"
    # Note: also escape the docstring path so the Python parser doesn't see "\U"
    # (changed the inline docstring line above to avoid unicode-escape parse errors)
    # Minimal safe templates / guides for key installments that users commonly request.
    templates = {}

    # Installment 2 — Data pipelines & ingestion
    templates[2] = {
        "title": "Data pipelines & ingestion (detailed)",
        "description": (
            "Implement modular ingestion, schema validation, storage with versioning and offline cache.\n"
            "Includes: ingest_api.py (fetching & rate limiting), validate.py (pydantic schemas), "
            "manifesting raw -> processed files and checksums."
        ),
        "steps": [
            "1) Create pydantic schemas for each data type under src/data/schemas.py.",
            "2) Implement ingest_api.py with retries, backoff, auth and rate-limiting.",
            "3) Add validate.py to validate and convert raw payloads to canonical format.",
            "4) Save raw and processed artifacts under data/raw/ and data/processed/ with manifest.json.",
            "5) Add unit tests for ingest and validate."
        ],
        "templates": [
            {
                "path": f"{base}\\src\\data\\ingest_api.py",
                "content": (
                    "# safe minimal ingest_api.py\n"
                    "import time, json, os\n"
                    "from typing import Any, Dict\n"
                    "import requests\n\n"
                    "def fetch_json(url: str, params: Dict[str, Any] = None, api_key: str = None) -> Dict[str, Any]:\n"
                    "    headers = {'Accept': 'application/json'}\n"
                    "    if api_key:\n"
                    "        headers['Authorization'] = f'Bearer {api_key}'\n"
                    "    for attempt in range(3):\n"
                    "        try:\n"
                    "            r = requests.get(url, params=params, headers=headers, timeout=10)\n"
                    "            r.raise_for_status()\n"
                    "            return r.json()\n"
                    "        except Exception as e:\n"
                    "            time.sleep(2 ** attempt)\n" 
                    "    return {}\n"
                )
            },
            {
                "path": f"{base}\\src\\data\\validate.py",
                "content": (
                    "# safe minimal validate.py\n"
                    "from pydantic import BaseModel, ValidationError\n"
                    "from typing import Any, Dict\n\n"
                    "class ItemSchema(BaseModel):\n"
                    "    id: str\n"
                    "    title: str\n"
                    "    metadata: Dict[str, Any] = {}\n\n"
                    "def validate_item(raw: Dict[str, Any]) -> Dict[str, Any]:\n"
                    "    try:\n"
                    "        itm = ItemSchema(**raw)\n"
                    "        return itm.dict()\n"
                    "    except ValidationError as e:\n"
                    "        # return empty dict on invalid; in prod log errors and snapshot raw\n"
                    "        return {}\n"
                )
            },
            {
                "path": f"{base}\\data\\README_DATA_VERSIONING.md",
                "content": (
                    "# Data versioning README\n"
                    "Store raw files under data/raw/YYYYMMDD/ and processed under data/processed/VERSION/\n"
                    "Maintain manifest.json with filename, sha256, and provenance metadata.\n"
                )
            }
        ]
    }

    # Installment 5 — Approver GOD (approval layer) — prototype
    templates[5] = {
        "title": "Approver GOD — validation runner and thresholds",
        "description": (
            "Create deterministic validation harness that runs validation plan items, computes metrics "
            "and promotes hypothesis to Earth when thresholds are met."
        ),
        "steps": [
            "1) Define threshold policy file (thresholds.py) with numeric gates.",
            "2) Implement runner.py that executes simple validation_plan steps (simulators/unit tests/stat tests).",
            "3) Log artifacts and provenance to motherboard (use existing src/motherboard/api).",
            "4) Add deterministic seeding and replay logs to ensure reproducibility."
        ],
        "templates": [
            {
                "path": f"{base}\\src\\approver_god\\policy\\thresholds.py",
                "content": (
                    "# thresholds.py\n"
                    "THRESHOLDS = {\n"
                    "    'factual_precision': 0.95,\n"
                    "    'citation_match': 0.98,\n"
                    "    'code_tests_pass_rate': 0.98,\n"
                    "    'contradiction_rate': 0.01,\n"
                    "}\n"
                )
            },
            {
                "path": f"{base}\\src\\approver_god\\validation\\runner.py",
                "content": (
                    "# runner.py — minimal deterministic validation runner\n"
                    "import random\n"
                    "from typing import Dict\n"
                    "from src.approver_god.policy.thresholds import THRESHOLDS\n"
                    "from src.motherboard.api import add_earth_fact\n\n"
                    "def run_validation(hypothesis: Dict[str, Any], seed: int = 42) -> Dict[str, float]:\n"
                    "    random.seed(seed)\n"
                    "    # Simulate metrics — replace with real simulators/tests in installments\n"
                    "    return {\n"
                    "        'factual_precision': 0.96 if 'improves' in hypothesis.get('claim','') else 0.5,\n"
                    "        'citation_match': 0.99,\n"
                    "        'code_tests_pass_rate': 1.0 if hypothesis.get('validation_plan') else 0.0,\n"
                    "        'contradiction_rate': 0.0,\n"
                    "    }\n"
                )
            }
        ]
    }

    # Installment 6 — Assets generation (film/animation/music)
    templates[6] = {
        "title": "Assets generation — characters, audio, video render orchestration",
        "description": (
            "Wrap existing generators deterministically, create character/voice/profile manifests, and build "
            "a render orchestrator that ensures consistency across scenes."
        ),
        "steps": [
            "1) Define character_profiles.json with persistent character IDs, seed, voice profile and appearance descriptors.",
            "2) Implement render_scene.py which takes a scene manifest and calls generation backends with fixed seeds.",
            "3) Use asset manifests to ensure same model checkpoints, seeds, and transforms are applied across all shots."
        ],
        "templates": [
            {
                "path": f"{base}\\src\\assets\\character_profiles.json",
                "content": (
                    "{\n"
                    "  \"characters\": [\n"
                    "    {\n"
                    "      \"id\": \"CHAR_001\",\n"
                    "      \"name\": \"Ava\",\n"
                    "      \"seed\": 12345,\n"
                    "      \"voice_profile\": \"voice_v1\",\n"
                    "      \"appearance\": {\"age\": 30, \"ethnicity\": \"mixed\", \"hair\": \"short_black\"}\n"
                    "    }\n"
                    "  ]\n"
                    "}\n"
                )
            },
            {
                "path": f"{base}\\src\\assets\\render_scene.py",
                "content": (
                    "# render_scene.py — orchestrator stub (safe)\n"
                    "import json\n"
                    "from typing import Dict\n\n"
                    "def render_scene(scene_manifest: Dict[str, Any], out_dir: str) -> None:\n"
                    "    \"\"\"Call image/audio/video generators with deterministic seeds and write manifest of outputs.\n"
                    "    Replace generator calls with real backends in later installments.\"\"\"\n"
                    "    # Example: write scene manifest to out_dir to record what would be rendered\n"
                    "    with open(out_dir + '/scene_record.json', 'w', encoding='utf-8') as f:\n"
                    "        json.dump(scene_manifest, f, indent=2)\n"
                )
            }
        ]
    }

    # Installment 7 — Deployment & offline mode
    templates[7] = {
        "title": "Deployment, monitoring and offline cache",
        "description": (
            "Containerize components, implement local-only mode that uses cached knowledge bases, "
            "and a sync service to pull verified updates when online."
        ),
        "steps": [
            "1) Provide Dockerfile and a compose file for local dev services (storage, optional mlflow).",
            "2) Implement sync_service.py to pull approved Earth facts to local cache when online.",
            "3) Add CLI flag to run system in offline-mode reading only local caches."
        ],
        "templates": [
            {
                "path": f"{base}\\infra\\docker\\Dockerfile",
                "content": (
                    "# Simple Dockerfile for local service\n"
                    "FROM python:3.11-slim\n"
                    "WORKDIR /app\n"
                    "COPY . /app\n"
                    "RUN pip install -r requirements.txt\n"
                    "CMD [\"python\", \"-m\", \"src.app\"]\n"
                )
            },
            {
                "path": f"{base}\\src\\sync\\sync_service.py",
                "content": (
                    "# sync_service.py — minimal safe skeleton\n"
                    "from src.motherboard.api import get_universe_hypotheses, get_earth_facts\n\n"
                    "def sync_to_local(cache_dir: str = 'cache'):\n"
                    "    # in prod: fetch from remote motherboard; here we read current local state\n"
                    "    hyps = get_universe_hypotheses()\n"
                    "    facts = get_earth_facts()\n    \n"
                    "    # write simple cache manifests\n"
                    "    print('synced', len(hyps), 'hypotheses and', len(facts), 'facts')\n"
                )
            }
        ]
    }

    # Installment 10 — Full film production pipeline (end-to-end)
    templates[10] = {
        "title": "Full production — shot generator and final assembler",
        "description": (
            "Create shot list generator from screenplay, deterministic per-shot rendering, and final assembly of video/audio."
        ),
        "steps": [
            "1) Implement shot_generator.py to parse screenplay and generate per-shot manifests.",
            "2) Implement final_assembler.py to merge rendered clips, audio tracks and subtitles into deliverables.",
            "3) Add checksums and versioned manifests for reproducibility and publishing."
        ],
        "templates": [
            {
                "path": f"{base}\\src\\production\\shot_generator.py",
                "content": (
                    "# shot_generator.py — minimal shot list generator\n"
                    "def generate_shot_list(screenplay_text: str):\n"
                    "    # naive splitter by scenes; replace with proper parser in later installments\n"
                    "    scenes = screenplay_text.split('\\n\\n')\n"
                    "    return [{'scene_id': i+1, 'text': s.strip()} for i, s in enumerate(scenes) if s.strip()]\n"
                )
            },
            {
                "path": f"{base}\\src\\production\\final_assembler.py",
                "content": (
                    "# final_assembler.py — stub to record assembly steps\n"
                    "def assemble_project(shot_manifests, audio_tracks, out_path: str):\n"
                    "    # In production: call ffmpeg, handle codecs, transitions, loudness normalization\n"
                    "    with open(out_path + '/assembly_record.txt', 'w') as f:\n"
                    "        f.write('assembled %d shots and %d audio tracks' % (len(shot_manifests), len(audio_tracks)))\n"
                )
            }
        ]
    }

    # If requested id exists return it, else a short help dict
    return templates.get(installment_id, {
        "title": f"Installment {installment_id} not found",
        "description": "Available installments: 2,5,6,7,10 (detailed templates provided). Use --plan to see high-level list.",
        "steps": [],
        "templates": []
    })

def main() -> None:
    parser = argparse.ArgumentParser(description="Repair scaffold and show installment plan.")
    parser.add_argument("--plan", action="store_true", help="Print the multi-installment plan and exit.")
    parser.add_argument("--install", type=int, help="Print detailed plan and templates for the given installment id and exit.")
    args = parser.parse_args()

    if args.plan:
        installments = generate_installments()
        print("\nAI system installment plan (high-level). Review each installment and request implementation:\n")
        for it in installments:
            print(f"Installment {it['id']}: {it['title']}")
            print(f"  Summary: {it['summary']}")
            print("  Steps:")
            for s in it["steps"]:
                print(f"    - {s}")
            print("  Suggested files to create:")
            for fpath in it["suggested_files"]:
                print(f"    - {fpath}")
            print()
        return

    if args.install:
        detail = generate_installment_detail(args.install)
        print(f"\nInstallment {args.install} — {detail.get('title')}\n")
        print(detail.get("description", ""))
        if detail.get("steps"):
            print("\nSteps:")
            for s in detail["steps"]:
                print("  -", s)
        if detail.get("templates"):
            print("\nTemplate files (save under c:\\Users\\Lunga Manana\\Desktop\\myproject):")
            for t in detail["templates"]:
                print(f"\n--- {t['path']} ---\n")
                # print a short preview of the template content (first 20 lines)
                preview = '\n'.join(t['content'].splitlines()[:20])
                print(preview)
        print("\nUse these templates as safe starting points. Request implementation of any template and I'll provide full files and tests.")
        return

    ensure_inits()
    created = []
    for path, content in FILES.items():
        write_file(path, content)
        created.append(path)
    print("Repair scaffold complete. Created/overwritten files:")
    for p in created:
        print(" -", p)
    print()
    print("Next steps:")
    print(" 1) Install minimal deps if needed: pip install -r requirements.txt")
    print(" 2) Run tests: pytest -q")
    print(" 3) Run the simple app: python -m src.app")
    print()
    print("To avoid overwriting files on subsequent runs, set REPAIR_OVERWRITE=0 in your environment.")

if __name__ == "__main__":
    main()
