import json
import os
from datetime import datetime
from modules.legal.document_parser import load_documents, extract_facts_from_documents
from modules.legal.reasoning_loader import load_reasoning

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

    metadata_path = os.path.join(path, "metadata.json")
    if os.path.exists(metadata_path):
        with open(metadata_path) as f:
            metadata = json.load(f)
            facts["case_type"] = metadata.get("type")

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

    documents = load_documents(case_id)
    document_facts = extract_facts_from_documents(documents)

    reasoning_data = load_reasoning(case_id)

    legal_basis = list(knowledge.keys())

    snapshot = {
        "case_id": case_id,
        "timestamp": datetime.utcnow().isoformat(),
        "facts": facts,
        "document_facts": document_facts,
        "reasoning": reasoning_data,
        "legal_basis": legal_basis
    }

    save_snapshot(case_id, snapshot)
    return snapshot


def save_snapshot(case_id, snapshot):
    folder = case_id.replace("/", "_"
    path = os.path.join(RUNTIME_PATH, folder)
    os.makedirs(path, exist_ok=True)

    file_path = os.path.join(path, "latest.json")

    with open(file_path, "w") as f:
        json.dump(snapshot, f, indent=2)
