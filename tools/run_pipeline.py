# tools/run_pipeline.py

import json
import time
import traceback

from tools.process_case import process_file


def main(file_path):
    ts = int(time.time())

    try:
        process_file(file_path)

        log = {
            "status": "success",
            "timestamp": ts
        }

    except Exception as e:
        log = {
            "status": "failure",
            "timestamp": ts,
            "error": str(e),
            "traceback": traceback.format_exc()
        }

    with open(f"memory/debug/run_{ts}.json", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
