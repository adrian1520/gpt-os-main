import json
import re
from datetime import datetime

# --- DATE ENGINE ---

def extract_dates(text):
    patterns = [
        r"\d{4}-\d{2}-\d{2}",
        r"\d{2}\.\d{2}\.\d{4}"
    ]
    dates = []
    for p in patterns:
        dates += re.findall(p, text)
    return list(set(dates))

def normalize_date(date_str):
    try:
        if "-" in date_str:
            return datetime.strptime(date_str, "%Y-%m-%d").date().isoformat()
        if "." in date_str:
            return datetime.strptime(date_str, "%d.%m.%Y").date().isoformat()
    except:
        return None

# --- NLP ---

def extract_sentences(text):
    return [s.strip() for s in re.split(r'[?.!]+', text) if s.strip()]

# --- ENTITY ENGINE ---

def extract_entities(text):
    words = text.split()
    persons, orgs, legal = [], [], []

    for i in range(len(words)-1):
        if words[i].istitle() and words[i+1].istitle():
            persons.append(words[i] + " " + words[i+1])

    for w in words:
        wl = w.lower()
        if "sąd" in wl or "urząd" in wl or "spółka" in wl:
            orgs.append(w)
        if "art." in wl or "§" in wl:
            legal.append(w)

    return {
        "persons": list(set(persons)),
        "organizations": list(set(orgs)),
        "legal_refs": list(set(legal))
    }

# --- TYPE ---

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

# --- EVENTS ---

ACTION_KEYWORDS = {
    "złożył": "filed",
    "wniósł": "filed",
    "zawarł": "contract_signed",
    "odmówił": "refused",
    "wezwał": "summoned",
    "zapłacił": "paid",
    "nie zapłacił": "defaulted",
}

def extract_events(text, entities):
    sentences = extract_sentences(text)
    events = []

    for s in sentences:
        s_lower = s.lower()

        action = None
        for key in ACTION_KEYWORDS:
            if key in s_lower:
                action = ACTION_KEYWORDS[key]
                break

        if not action:
            continue

        dates = extract_dates(s)
        date = normalize_date(dates[0]) if dates else None

        actor = None
        for p in entities.get("persons", []):
            if p in s:
                actor = p
                break

        events.append({
            "date": date,
            "actor": actor,
            "action": action,
            "type": "procedural",
            "source": s
        })

    return events

# --- ROLES ---

def detect_roles(text):
    roles = {"plaintiff": None, "defendant": None}
    for line in text.split("\n"):
        l = line.lower()
        if "powód" in l:
            roles["plaintiff"] = line
        if "pozwany" in l:
            roles["defendant"] = line
    return roles

# --- LEGAL ---

def extract_legal_context(text):
    refs = []
    for s in extract_sentences(text):
        if "art." in s.lower():
            refs.append({"reference": s, "context": s})
    return refs

# --- CORE ---

def parse_document(doc):
    text = doc["content"]["text"]

    entities = extract_entities(text)

    parsed = {
        "document_id": doc["document_id"],
        "case_id": doc["case_id"],
        "dates": [normalize_date(d) for d in extract_dates(text) if normalize_date(d)],
        "document_type": detect_type(text, doc.get("type_hint")),
        "entities": entities,
        "events": extract_events(text, entities),
        "roles": detect_roles(text),
        "legal": extract_legal_context(text),
        "parsed_at": datetime.utcnow().isoformat()
    }

    return parsed
