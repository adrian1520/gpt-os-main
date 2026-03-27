import json
import re
from datetime import datetime


def extract_dates(text):
    patterns = [
        r"\\d{4}-\\d{2}-\\d{2}",
        r"\\d{2}\\.\\d{2}\\.\\d{4}"
    ]
    dates = []
    for p in patterns:
        dates += re.findall(p, text)
    return list(set(dates))


def extract_sentences(text):
    return [s.strip() for s in re.split(r'[?!.]+', text) if s.strip()]


def extract_entities(text):
    words = text.split()
    persons = []
    orgs = []
    legal = []

    for i in range(len(words)-1):
        if words[i].istitle() and words[i+1].istitle():
            persons.append(words[i] + " " + words[i+1])

    for w in words:
        wl = w.lower()
        if "sád" in wl or "urzę" in wl or "spółka" in wl:
            orgs.append(w)
        if "art." in wl or "§" in wl:
            legal.append(w)

    return {
        "persons": list(set(persons)),
        "organizations": list(set(orgs)),
        "legal_refs": list(set(legal))
    }


def detect_type(text, hint=None):
    text_lower = text.lower()
    if hint:
        return {"value": hint, "confidence": 1.0}
    if "pozew" in text_lower:
        return {"value": "claim", "confidence": 0.9}
    if "wyrok" in text_lower:
        return {"value": "judgment", "confidence": 0.9}
    if "umowa" in text_lower:
        return {"value": "contract", "confidence": 0.8}
    return {"value": "unknown", "confidence": 0.5}


def parse_document(path):
    with open(path) as f:
        doc = json.load(f)

    text = doc["content"]["text"]

    sentences = extract_sentences(text)
    entities = extract_entities(text)

    parsed = {
        "document_id": doc["document_id"],
        "case_id": doc["case_id"],
        "dates": extract_dates(text),
        "document_type": detect_type(text, doc.get("type_hint")),
        "entities": entities,
        "nlp": {
            "sentences": sentences,
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
