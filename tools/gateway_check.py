import json, sys, os

def load_sot():
    try:
        with open("memory/source_of_truth.json") as f:
            return json.load(f)
    except Exception:
        return None

sot = load_sot()

if not sot:
    print("✘ SOT missing — BLOCK")
    sys.exit(1)

mode = "normal"
if sot.get("current_focus") == "debug":
    mode = "debug"
elif sot.get("current_focus") == "stable":
    mode = "stable"

errors = sot.get("errors", [])
if len(errors) > 5:
    print("✘ too many errors – BLOCK")
    sys.exit(1)

# export MODE

env_path = os.environ.get("GITHUB_ENV", "/dev/null")
with open(env_path, "a") as env:
    env.write(f"MODE={mode}\n")

drint(f"✅ gateway passed, mode: {mode}")
sys.exit(0)