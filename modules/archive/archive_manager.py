# modules/archive/archive_manager.py

import os
import shutil
import json
import hashlib
from datetime import datetime


def compute_hash(directory):
    sha = hashlib.sha256()

    for root, _, files in os.walk(directory):
        for f in sorted(files):
            path = os.path.join(root, f)
            with open(path, "rb") as file:
                sha.update(file.read())

    return sha.hexdigest()


def build_diff(prev_path, current_path):
    diff = {
        "added": [],
        "modified": [],
        "removed": []
    }

    prev_files = set()
    curr_files = set()

    for root, _, files in os.walk(prev_path):
        for f in files:
            prev_files.add(os.path.relpath(os.path.join(root, f), prev_path))

    for root, _, files in os.walk(current_path):
        for f in files:
            curr_files.add(os.path.relpath(os.path.join(root, f), current_path))

    diff["added"] = list(curr_files - prev_files)
    diff["removed"] = list(prev_files - curr_files)

    return diff


def archive_case(case_id, source_file=None):
    now = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")

    case_path = os.path.join("cases", case_id)
    archive_path = os.path.join("archive", case_id, now)

    snapshot_path = os.path.join(archive_path, "snapshot")

    os.makedirs(snapshot_path, exist_ok=True)

    shutil.copytree(case_path, snapshot_path, dirs_exist_ok=True)

    hash_value = compute_hash(snapshot_path)

    with open(os.path.join(archive_path, "hash.txt"), "w", encoding="utf-8") as f:
        f.write(hash_value)

    meta = {
        "timestamp": now,
        "case_id": case_id,
        "source_file": source_file
    }

    with open(os.path.join(archive_path, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    case_archive_root = os.path.join("archive", case_id)

    snapshots = sorted(os.listdir(case_archive_root))

    if len(snapshots) > 1:
        prev = os.path.join(case_archive_root, snapshots[-2], "snapshot")
        diff = build_diff(prev, snapshot_path)

        with open(os.path.join(archive_path, "diff.json"), "w", encoding="utf-8") as f:
            json.dump(diff, f, ensure_ascii=False, indent=2)
