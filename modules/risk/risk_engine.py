def detect_missing_actions(events):
    risks = []

    filed = any(e.get("action") == "filed" for e in events)
    response = any(e.get("action") in ["responded", "defended"] for e in events)

    if filed and not response:
        risks.append({
            "type": "procedural",
            "level": "high",
            "description": "Brak odpowiedzi na pozew",
            "source": "events",
            "recommendation": "Złożyć odpowiedź na pozew"
        })

    return risks


def detect_missing_dates(events):
    risks = []

    for e in events:
        if not e.get("date"):
            risks.append({
                "type": "procedural",
                "level": "medium",
                "description": "Zdarzenie bez daty",
                "source": e.get("source"),
                "recommendation": "Uzupełnić datę zdarzenia"
            })

    return risks


def detect_no_legal_basis(legal_refs):
    if not legal_refs:
        return [{
            "type": "legal",
            "level": "high",
            "description": "Brak podstawy prawnej",
            "source": "document",
            "recommendation": "Dodać podstawę prawną"
        }]
    return []


def detect_role_issues(roles):
    risks = []

    if not roles.get("plaintiff"):
        risks.append({
            "type": "procedural",
            "level": "high",
            "description": "Brak powoda",
            "source": "roles",
            "recommendation": "Ustalić stronę inicjującą"
        })

    if not roles.get("defendant"):
        risks.append({
            "type": "procedural",
            "level": "high",
            "description": "Brak pozwanego",
            "source": "roles",
            "recommendation": "Ustalić stronę przeciwną"
        })

    return risks


def detect_inconsistencies(events):
    risks = []

    dates = [e.get("date") for e in events if e.get("date")]

    if dates != sorted(dates):
        risks.append({
            "type": "factual",
            "level": "medium",
            "description": "Niespójna chronologia",
            "source": "events",
            "recommendation": "Zweryfikować kolejność zdarzeń"
        })

    return risks


def build_risk_report(parsed):
    events = parsed.get("events", [])
    roles = parsed.get("roles", {})
    legal = parsed.get("legal", [])

    risks = []

    risks += detect_missing_actions(events)
    risks += detect_missing_dates(events)
    risks += detect_no_legal_basis(legal)
    risks += detect_role_issues(roles)
    risks += detect_inconsistencies(events)

    return {
        "case_id": parsed.get("case_id"),
        "risk_count": len(risks),
        "risks": risks
    }
