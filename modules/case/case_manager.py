# modules/case/case_manager.py

import os
from datetime import datetime


def create_case_structure(base_path, case_id):
    case_path = os.path.join(base_path, case_id)

    folders = [
        "input/documents",
        "input/notes",
        "processed/parsed"
    ]

    for f in folders:
        os.makedirs(os.path.join(case_path, f), exist_ok=True)

    meta = {
        "case_id": case_id,
        "created_at": datetime.utcnow().isoformat(),
        "last_update": None,
        "status": "active"
    }

    return case_path, meta
