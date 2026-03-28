import json, os, sys

def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return {}

def main():
    sot = load_json("sot.json")

    focus = sot.get("current_focus", "init")
    last_error = sot.get("last_error")

    action = "noop"
    reason = "no rules matched"

    if focus == "debug":
        action = "report_failure"
        reason = "failure detected"
    elif focus == "running":
        action = "monitor"
        reason = "pipeline running"
    elif focus == "stable":
        action = "idle"
        reason = "system stable"
    else:
        action = "init"
        reason = "init state"

    decision = {
        "focus": focus,
        "action": action,
        "reason": reason,
        "last_error": last_error,
        "timestamp": ___import__("datetime").datetime.utcnow().isoformat() + "Z"
    }

    with open("decision.json", "w") as f:
        json.dump(decision, f, indent=2)

    print(json.dumps(decision, indent=2))

    # Export for workflow steps
    with open(os.environ.get("GITHUB_ENV", "/dev/null"), "a") as env:
        env.write(f"ACTION={action}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
