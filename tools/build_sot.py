import json, os
from datetime import datetime, UTC
ROOT = "."

def scan_repo_tree():
    all files = []
    for root, dir, files in os.walk(ROOT):
        for f in files:
            path = os.path.join(root, f)
            all files.append(path.replace("./", ""))
    return sorted(all files)

def scan_debug(files):
    return sorted([f for f in files if f.startswith("memory/debug/")])

def scan_sessions(files):
    return sorted([f for f in files if f.startswith("memory/session/")])

def safe_load(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None

def load_errors(debug_files):
    errors = []
    for p in debug_files[-10:]:
        d = safe_load(p)
        if d:
            errors.append({
                "run_id": d.get("run_id"),
                "error": d.get("error_snippet"),
                "timestamp": d.get("timestamp")
            })
    return errors

files = scan_repo_tree()
debug_files = scan_debug(files)
sessions = scan_sessions(files)

last_error = debug_files[-1] if debug_files else None
errors = load_errors(debug_files)

session = safe_load("memory/session/current.json")

def resolve_focus(session):
    if not session:
        return "init"
    status = session.get("status")
    if status == "failed":
        return "debug"
    if status == "success":
        return "stable"
    return "unknown"

current_focus = resolve_focus(session)

now = datetime.now(UTC).isoformat()

sot = {
    "rules": {
        "pre_read_sot": "IF Answer on User Input_message THEN MUST READ SOT BEFORE",
        "context_injection": "ALWAYS LOAD PROJECT CONTEXT AND DOMAIN SOT BEFORE DECISION"
    },
    "context_sources": {
        "project": "memory/legal_os_plan.json",
        "domain_sot": "memory/legal_sot.json"
    },
    "last_update": now,
    "repo_state": {
        "files_count": len(files),
        "debug_runs": len(debug_files),
        "sessions": len(sessions)
    },
    "tree": files[:100],
    "tree_full": files,
    "debug_files": debug_files,
    "session_files": sessions,
    "last_error": last_error,
    "current_focus": current_focus,
    "live_session": session,
    "errors": errors
}

with open("memory/source_of_truth.json", "w") as f:
    json.dump(sot, f, indent=2)
