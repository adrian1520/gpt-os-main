import json, datetime, os

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

files = [item.get("path") for item in data.get("tree", []) if isinstance(item, dict) and "path" in item]

debug_runs = [f for f in files if f and f.startswith("memory/debug/")]
sessions = [f for f in files if f and f.startswith("memory/session/")]

last_error = debug_runs[-1] if debug_runs else None

# 🔥 NEW: load live session
session_current = safe_load("memory/session/current.json")

if session_current:
    current_focus = session_current.get("status", "running")
else:
    if debug_runs:
        current_focus = "debug"
    elif sessions:
        current_focus = "continue"
    else:
        current_focus = "init"

now = datetime.datetime.utcnow().isoformat() + "Z"

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
    "live_session": session_current
}

with open("sot.json", "w") as f:
    json.dump(sot, f, indent=2)
