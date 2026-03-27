import yaml
import base64
import sys

def prepare_content(raw_content: str) -> str:
    # basic normalization
    content = raw_content.replace('\t', '  ')
    content = "\n".join(line.rstrip() for line in content.splitlines())
    return content + "\n"

def validate_yaml(content: str) -> bool:
    try:
        yaml.safe_load(content)
        return True
    except Exception as e:
        print(f"YAML VALIDATION ERROR: {e}", file=sys.stderr)
        return False

def encode_base64(content: str) -> str:
    return base64.b64encode(content.encode()).decode()

def main():
    raw = sys.stdin.read()
    prepared = prepare_content(raw)

    if not validate_yaml(prepared):
        sys.exit(1)

    encoded = encode_base64(prepared)
    print(encoded)

if __name__ == "__main__":
    main()