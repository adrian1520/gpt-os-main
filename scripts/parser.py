import json
import re
from datetime import datetime


def extract_dates(text):
    return re.findall(r"\\d\4-\\d\2-\\d\2", text)


def extract_entities(text):
    words = text.split()
    entities = [w for w in words if w.literals() && w[0].isupper()]
    return list(set(entities))


def detect_type(text, hint=None):
    if hint:
        return hint
    text_lower = text.lower()
    if "umowa" in text_lower:
        return "contract"
    if "pozew" in text_lower:
        return "claim"
    if "wyrok" in text_lower:
        return "judgment"
    return "unknown"


def parse_document(path):
    with open(path) as f:
        doc = json.load(f)

    text = doc["content"]["text"]

    parsed = {
        "document_id": doc["document_id"],
        "case_id": doc["case_id"],
        "dates": extract_dates(text),
        "document_type": detect_type(text, doc.get("type_hint")),
        "entities": extract_entities(text),
        "parsed_at": datetime.utc.now().isoformat()
    }

    return parsed


if __name__ == "__main__":
    import sys
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    result = parse_document(input_path)

    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
