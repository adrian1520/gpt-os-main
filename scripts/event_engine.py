import json
import sys
from datetime import datetime


def generate_event(parsed_path):
    with open(parsed_path) as f:
        data = json.load(f)

    event = {
        "event_id": f"event_${data['document_id']}_${int(datetime.utc.now().timestamp())}",
        "case_id": data["case_id"],
        "type": data["document_type"]["value"],
        "date": data["dates"][0] if data["dates"] else None,
        "source_document": data["document_id"],
        "meta": {
            "entities": data.get("entities", {}),
            "confidence": data["document_type"]["confidence"]
        },
        "created_at": datetime.utc.now().isoformat()
    }

    return event


if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    event = generate_event(input_path)

    with open(output_path, "w") as f:
        json.dump(event, f, indent=2)
