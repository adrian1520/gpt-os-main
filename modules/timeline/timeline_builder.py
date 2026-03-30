from datetime import datetime

def sort_events(events):
    def parse_date(e):
        try:
            return datetime.fromisoformat(e["date"]) if e.get("date") else datetime.max
        except:
            return datetime.max

    return sorted(events, key=parse_date)

def format_event(event):
    date = event.get("date") or "???"
    actor = event.get("actor") or "Nieznany"
    action = event.get("action") or "zdarzenie"
    source = event.get("source") or ""

    return f"- [{date}] {actor} → {action}\n  ↳ {source}"

def build_timeline(events):
    if not events:
        return "# Oś czasu sprawy\n\nBrak zdarzeń."

    events_sorted = sort_events(events)

    lines = ["# Oś czasu sprawy\n"]

    for e in events_sorted:
        lines.append(format_event(e))

    return "\n".join(lines)
