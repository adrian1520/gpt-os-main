import json
import re
from datetime import datetime


def extract_dates(text):
    pattern = r"\\d{4}-\\d{2}-\\d{2}"
    return re.findall(pattern, text)


def extract_sentences(text):
    return re.split(r'[?!.]+\s*', text)


def extract_entities(text):
    words = text.split()
    persons = []
    for i in range(len(words)-1):
        if words[i].istitle() and words[i+1].istitle():
            persons.append(words[i] + " " + words[i+1])
    return {"persons": list(set(persons))}


def detect_type(text, hint=None):
    if hint:
        return {"value": hint, "confidence": 1.0}
    if "pozew" in text.lower():
        return {"value": "claim", "confidence": 0.9}
    return {"value": "unknown", "confidence": 0.5}


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
        "nlp": {
            "sentences": extract_sentences(text),
            "tokens_count": len(text.split())
        },
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
