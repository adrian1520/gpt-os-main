import json
import os
from datetime import datetime

RUNTIME_PATH = "memory/legal_runtime"

def run_analysis(case_id):
    snapshot = {
        "case_id": case_id,
        "timestamp": datetime.utcnow().isoformat(),
        "process_position": {
            "role": "unknown",
            "strength": "weak",
            "score": 0.3
        },
        "risks": [],
        "strategy": [],
        "legal_basis": [],
        "procedural_compliance": {
            "status": False,
            "issues": []
        },
        "next_steps": []
    }

    save_snapshot(case_id, snapshot)
    return snapshot

def save_snapshot(case_id, snapshot):
    folder = case_id.replace("/", "_")
    path = os.path.join(RUNTIME_PATH, folder)
    os.makedirs(path, exist_ok=True)

    file_path = os.path.join(path, "latest.json")

    with open(file_path, "w") as f:
        json.dump(snapshot, f, indent=2)
