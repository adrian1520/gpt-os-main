import json, sys, os

def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return None

sot = load_json("memory/source_of_truth.json")
session = load_json("memory/session/current.json")

if not sot:
    print("❌ SOT missing – BLOCK")
    sys.exit(1)

mode = "normal"

# PRORITY: session (real-time)
if session and isinstance(session, dict):
    status = session.get("status")

    if status == "failed":
        mode = "debug"
    elif status == "running":
        mode = "running"
    elif status == "success":
        mode = "stable"
    else:
        mode = "normal"
else:
    # FALLBACK: SOT
    focus = sot.get("current_focus")
    if focus == "debug":
        mode = "debug"
    elif focus == "stable":
        mode = "stable"

# global error guard
errors = sot.get("errors", [])
if len(errors) > 5:
    print("✘ too many errors – BLOCK")
    sys.exit(1)

# export MODE
env_path = os.environ.get("GITHUB_ENV", "/dev/null")
with open(env_path, "a") as env:
    env.write(f"MODE={mode}\n")

print(f"✔ Gateway passed | MODE: {mode}")
sys.exit(0)