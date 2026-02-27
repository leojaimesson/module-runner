import json
import sys
from typing import Any, Dict

from text_unidecode import unidecode


def load_payload() -> Dict[str, Any]:
    if len(sys.argv) > 1:
        try:
            return json.loads(sys.argv[1])
        except json.JSONDecodeError:
            pass
    return {}


def normalize_text(text: str) -> str:
    normalized = unidecode(text)
    return normalized.strip().lower()


def main() -> None:
    payload = load_payload()
    original_text = str(payload.get("text", ""))
    normalized = normalize_text(original_text)

    result = {
        "text": normalized,
        "original_text": original_text,
    }

    print(json.dumps(result))


if __name__ == "__main__":
    main()
