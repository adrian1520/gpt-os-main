import json, datetime, os

def safe_load(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return None

# Load repo tree
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

# Detect memory files
debug_runs = sorted(
    [f for f in files if f and f.startswith("memory/debug/")]
)

sessions = sorted(
    [f for f in files if f and f.startswith("memory/session/")]
)

# Last error (deterministic)
last_error = debug_runs[-1] if debug_runs else None

# Load live session
session_current = safe_load("memory/session/current.json")

# 🔥 INTERPRET STATE (IMPORTANT)
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

# Timestamp
now = datetime.datetime.utcnow().isoformat() + "Z"

# Build SOT
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

# Save
with open("sot.json", "w") as f:
    json.dump(sot, f, indent=2)