# tools/input_uploader.py

import os
from datetime import datetime


def generate_filename(prefix="pismo"):
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{ts}.txt"


def build_case_path(case_id, filename):
    return os.path.join(
        "cases",
        case_id,
        "input",
        "documents",
        filename
    )


def build_raw_document(text):
    return text.strip() + "\n"


def create_input_payload(case_id, text):
    filename = generate_filename()
    path = build_case_path(case_id, filename)

    return {
        "path": path,
        "content": build_raw_document(text),
        "message": f"add document to {case_id}"
    }
