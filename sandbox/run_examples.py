from pathlib import Path
import json

import sys

root = str(Path(__file__).parent.parent.absolute())
if root not in sys.path:
    sys.path.insert(0, root)

from module_runner import Runner

MODULES_PATH = Path(__file__).parent / "modules"


import logging
logging.getLogger("module_runner").setLevel(logging.INFO)
logging.basicConfig()

def run_system_module() -> None:
    runner = Runner(module_path=MODULES_PATH / "system_report")
    process = runner.run(payload={"message": "Hello from system mode!"})
    print("System module stdout:\n", process.stdout.strip())


def run_single_module() -> None:
    runner = Runner(module_path=MODULES_PATH / "normalize")
    process = runner.run(payload={"text": "   AI assistants simplify automation.   "})
    print("Single module stdout:\n", process.stdout.strip())


def manual_chaining() -> None:
    normalize_runner = Runner(module_path=MODULES_PATH / "normalize")
    normalize_process = normalize_runner.run(
        payload={"text": "  Building pipelines is straightforward with Runner.  "}
    )
    normalized_data = json.loads(normalize_process.stdout or "{}")

    stats_runner = Runner(
        module_path=MODULES_PATH / "stats"
    )
    stats_process = stats_runner.run(payload={"text": normalized_data.get("text", "")})

    print("Normalize stdout:\n", normalize_process.stdout.strip())
    print("Stats stdout:\n", stats_process.stdout.strip())


if __name__ == "__main__":
    run_system_module()
    run_single_module()
    manual_chaining()
