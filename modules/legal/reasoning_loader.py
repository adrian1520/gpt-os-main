import os
import json

def load_reasoning(case_id):
    folder = case_id.replace("/", "_")
    path = f"memory/legal_cases/{folder}/reasoning"

    data = []

    if not os.path.exists(path):
        return data

    for file in sorted(os.listdir(path)):
        file_path = os.path.join(path, file)

        if os.path.isfile(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data.append(json.load(f))
            except:
                continue

    return data