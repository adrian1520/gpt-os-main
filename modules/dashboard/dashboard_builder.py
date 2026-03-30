def build_dashboard(parsed, timeline_md, risk_report, strategy):
    return {
        "case_id": parsed.get("case_id"),

        "summary": {
            "document_type": parsed.get("document_type"),
            "entities": parsed.get("entities"),
            "dates": parsed.get("dates")
        },

        "timeline": timeline_md,

        "risk": {
            "count": risk_report.get("risk_count"),
            "items": risk_report.get("risks")
        },

        "strategy": strategy,

        "status": build_status(parsed, risk_report)
    }


def build_status(parsed, risk_report):
    high_risks = [
        r for r in risk_report.get("risks", [])
        if r.get("level") == "high"
    ]

    if high_risks:
        return {
            "state": "critical",
            "reason": "Wysokie ryzyko w sprawie"
        }

    if not parsed.get("events"):
        return {
            "state": "incomplete",
            "reason": "Brak zdarzeń"
        }

    return {
        "state": "active",
        "reason": "Sprawa w toku"
    }
