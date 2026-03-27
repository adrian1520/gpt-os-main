import json, datetime

with open("tree.json") as f:
    data = json.load(f)

files = [item["path"] for item in data.get("tree", [])]

debug_runs = [f for f in files if f.startswith("memory/debug/")]
sessions = [f for f in files if f.startswith("memory/session/")]

last_error = debug_runs[-1] if debug_runs else None

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
    "current_focus": current_focus
}

open("sot.json", "w").write(json.dumps(sot))
