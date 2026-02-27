import json
import os
import platform
import sys
from typing import Any, Dict


def load_payload() -> Dict[str, Any]:
    if len(sys.argv) > 1:
        try:
            return json.loads(sys.argv[1])
        except json.JSONDecodeError:
            pass
    return {}


def main() -> None:
    payload = load_payload()
    message = payload.get("message", "Running with system interpreter")

    result = {
        "message": str(message),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "cwd": os.getcwd(),
    }

    print(json.dumps(result))


if __name__ == "__main__":
    main()
