# tools/run_pipeline.py

import sys
import os

sys.path.append(os.getcwd())

import json
import time
import traceback

from tools.process_case import process_file


def main(file_path):
    ts = int(time.time())

    os.makedirs("memory/debug", exist_ok=True)
    debug_path = f"memory/debug/run_{ts}.json"

    with open(debug_path, "w", encoding="utf-8") as f:
        json.dump({"status": "started", "timestamp": ts}, f)

    try:
        process_file(file_path)

        log = {
            "status": "success",
            "timestamp": ts
        }

    except BaseException as e:
        log = {
            "status": "failure",
            "timestamp": ts,
            "error": str(e),
            "traceback": traceback.format_exc()
        }

    with open(debug_path, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())


if __name__ == "__main__":
    main(sys.argv[1])
