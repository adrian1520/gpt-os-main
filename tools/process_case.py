# tools/process_case.py

import sys
import os

# FIX: ensure repo root is in PYTHONPATH
sys.path.append(os.getcwd())

import json

from modules.parser.legal_parser import parse_document
from modules.timeline.timeline_builder import build_timeline
from modules.risk.risk_engine import build_risk_report
from modules.strategy.strategy_engine import build_strategy
from modules.dashboard.dashboard_builder import build_dashboard


def load_document(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    return {
        "document_id": os.path.basename(path),
        "case_id": extract_case_id(path),
        "content": {"text": text}
    }


def extract_case_id(path):
    parts = path.split(os.sep)
    for i, p in enumerate(parts):
        if p.startswith("NSM_"):
            if i + 1 < len(parts) and parts[i+1].isdigit():
                return f"{p}_{parts[i+1]}"
            return p
    return "UNKNOWN"


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_text(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def process_file(file_path):
    doc = load_document(file_path)

    parsed = parse_document(doc)

    timeline = build_timeline(parsed["events"])
    risk = build_risk_report(parsed)
    strategy = build_strategy(parsed, risk)
    dashboard = build_dashboard(parsed, timeline, risk, strategy)

    base = os.path.join("cases", doc["case_id"], "processed")

    os.makedirs(os.path.join(base, "parsed"), exist_ok=True)

    save_json(os.path.join(base, "parsed", doc["document_id"] + ".json"), parsed)
    save_text(os.path.join(base, "timeline.md"), timeline)
    save_json(os.path.join(base, "risk.json"), risk)
    save_json(os.path.join(base, "strategy.json"), strategy)

    save_json(os.path.join("cases", doc["case_id"], "dashboard.json"), dashboard)


if __name__ == "__main__":
    import sys
    file_path = sys.argv[1]
    process_file(file_path)
