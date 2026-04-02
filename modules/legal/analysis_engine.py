import json
import os
from datetime import datetime

RUNTIME_PATH = "memory/legal_runtime"
KNOWLEDGE_PATH = "memory/legal_knowledge"
CASES_PATH = "memory/legal_cases"

def load_knowledge():
    with open(f"{KNOWLEDGE_PATH}/kro.json") as f:
        return json.load(f)

def extract_facts(case_id):
    folder = case_id.replace("/", "_")
    path = os.path.join(CASES_PATH, folder)

    facts = {
        "has_documents": False,
        "events_count": 0,
        "case_type": None,
        "has_initial_document": False,
        "activity_level": "low"
    }

    # metadata
    metadata_path = os.path.join(path, "metadata.json")
    if os.path.exists(metadata_path):
        with open(metadata_path) as f:
            metadata = json.load(f)
            facts["case_type"] = metadata.get("type")

    # timeline
    timeline_path = os.path.join(path, "timeline.json")

    if os.path.exists(timeline_path):
        with open(timeline_path) as f:
            timeline = json.load(f)
            count = len(timeline)
            facts["events_count"] = count

            if count > 0:
                facts["has_documents"] = True
                facts["has_initial_document"] = True

            if count > 3:
                facts["activity_level"] = "medium"
            elif count > 5:
                facts["activity_level"] = "high"

    return facts

def run_analysis(case_id):
    knowledge = load_knowledge()
    facts = extract_facts(case_id)

    legal_basis = list(knowledge.keys())

    risks = []
    strategy = []

    # logika bazelowa
    if not facts["has_initial_document"]:
        risks.append({
            "type": "brak_pozwu",
            "severity": "high",
            "description": "Brak poczatkowego pisma"
        })
        strategy.append({
            "action": "zloazenia pozdwu",
            "priority": "high"
        })

    if facts["activity_level"] == "low":
        strategy.append({
            "action": "zwiekszyc aktywnosc sprawy",
            "priority": "medium"
        })

    snapshot = {
        "case_id": case_id,
        "timestamp": datetime.utcnow().isoformat(),
        "facts": facts,
        "process_position": {
            "role": "unknown",
            "strength": "weak",
            "score": 0.3
        },
        "risks": risks,
        "strategy": strategy,
        "legal_basis": legal_basis,
        "procedural_compliance": {
            "status": facts["has_documents"],
            "issues": [] if facts["has_documents"] or ["brak dokumentów"]
        },
        "next_steps": [
            "upelnienia akt sprawy"
        ]
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
