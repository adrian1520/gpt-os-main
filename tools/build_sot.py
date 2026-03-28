import json, os
from datetime import datetime, UTC

def safe_load(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return None

try:
    with open("tree.json") as f:
        data = json.load(f)
except Exception:
    data = {}

files = [
    item.get("path")
    for item in data.get("tree", [])
    if isinstance(item, dict) and "path" in item
]

debug_runs = sorted(
    [f for f in files if f and f.startswith("memory/debug/")]
)

sessions = sorted(
    [f for f in files if f and f.startswith("memory/session/")]
)

last_error = debug_runs[-1] if debug_runs else None

def load_errors(debug_files):
    errors = []
    for path in reversed(debug_files[-10:]):
        data = safe_load(path)
        if data:
            errors.append({
                "run_id": data.get("run_id"),
                "error": data.get("error_snippet"),
                "timestamp": data.get("timestamp")
            })
    return errors

error_list = load_errors(debug_runs)

session_current = safe_load("memory/session/current.json")

def resolve_focus(session, debug_runs, sessions):
    if session and isinstance(session, dict):
        status = session.get("status")
        if status == "failed":
            return "debug"
        elif status == "success":
            return "stable"
        elif status == "running":
            return "running"
        else:
            return "unknown"
    if debug_runs:
        return "debug"
    if sessions:
        return "continue"
    return "init"

current_focus = resolve_focus(session_current, debug_runs, sessions)

now = datetime.now(UTC).isoformat()

sot = {
    "last_update": now,
    "repo_state": {
        "files_count": len(files),
        "debug_runs": len(debug_runs),
        "sessions": len(sessions)
    },
    "debug_files": debug_runs[:10],
    "session_files": sessions[:10],
    "last_error": last_error,
    "current_focus": current_focus,
    "live_session": session_current,
    "errors": error_list
}

with open("sot.json", "w") as f:
    json.dump(sot, f, indent=2)
