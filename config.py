import os
from typing import Any, Dict

def load_config() -> Dict[str, Any]:
    return {
        "ENV": os.getenv("ENV", "dev"),
        "PORT": int(os.getenv("PORT", "8000")),
        "REPAIR_OVERWRITE": os.getenv("REPAIR_OVERWRITE", "1"),
    }
