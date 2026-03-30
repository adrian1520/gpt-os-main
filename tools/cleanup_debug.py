# tools/cleanup_debug.py

import os
from pathlib import Path

DEBUG_DIR = Path("memory/debug")
MAX_KEEP = 5


def cleanup_debug():
    files = sorted(
        [f for f in DEBUG_DIR.iterdir() if f.name != ".keep"],
        key=lambda x: x.stat().st_mtime
    )

    if len(files) <= MAX_KEEP:
        return

    to_delete = files[:len(files) - MAX_KEEP]

    for f in to_delete:
        f.unlink()


if __name__ == "__main__":
    cleanup_debug()
