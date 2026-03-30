def define_objective(parsed):
    doc_type = parsed.get("document_type", {}).get("value")

    if doc_type == "claim":
        return "Uzyskanie korzystnego wyroku"
    if doc_type == "judgment":
        return "Analiza wyroku i ewentualna apelacja"

    return "Ustalenie celu procesowego"


def assess_current_state(events):
    if not events:
        return "Brak danych o przebiegu sprawy"

    last_event = events[-1]
    return f"Ostatnie zdarzenie: {last_event.get('action')} ({last_event.get('date')})"


def extract_key_risks(risk_report):
    return [r["description"] for r in risk_report.get("risks", []) if r.get("level") == "high"]


def recommend_actions(parsed, risk_report):
    actions = []

    for r in risk_report.get("risks", []):
        if r.get("level") == "high":
            if r.get("recommendation"):
                actions.append(r.get("recommendation"))

    if not actions:
        actions.append("Monitorować rozwój sprawy")

    return list(set(actions))


def build_argumentation(parsed):
    legal = parsed.get("legal", [])
    arguments = []

    for ref in legal:
        arguments.append(f"Powiązać argument z: {ref.get('reference')}")

    if not arguments:
        arguments.append("Brak podstaw prawnych — konieczne uzupełnienie")

    return arguments


def define_next_steps(events):
    if not events:
        return ["Zgromadzić dokumenty"]

    return [
        "Przygotować kolejne pismo procesowe",
        "Zebrać dowody",
        "Zweryfikować stanowisko przeciwnika"
    ]


def build_strategy(parsed, risk_report):
    return {
        "case_id": parsed.get("case_id"),
        "objective": define_objective(parsed),
        "current_state": assess_current_state(parsed.get("events", [])),
        "key_risks": extract_key_risks(risk_report),
        "recommended_actions": recommend_actions(parsed, risk_report),
        "argumentation": build_argumentation(parsed),
        "next_steps": define_next_steps(parsed.get("events", []))
    }
