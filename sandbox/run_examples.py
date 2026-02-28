from pathlib import Path
import json

import sys

root = str(Path(__file__).parent.parent.absolute())
if root not in sys.path:
    sys.path.insert(0, root)

from module_runner import NodeRunner, PythonRunner, ShellRunner, UvPackageManager, SystemPackageManager, PnpmPackageManager

MODULES_PATH = Path(__file__).parent / "modules"


import logging
logging.getLogger("module_runner").setLevel(logging.INFO)
logging.basicConfig()

def run_system_module() -> None:
    runner = PythonRunner(module_path=MODULES_PATH / "system_report", package_manager=SystemPackageManager())
    process = runner.run(payload={"message": "Hello from system mode!"})
    print("System module stdout:\n", process.stdout.strip())


def run_single_module() -> None:
    runner = PythonRunner(module_path=MODULES_PATH / "normalize", package_manager=UvPackageManager())
    process = runner.run(payload={"text": "   AI assistants simplify automation.   "})
    print("Single module stdout:\n", process.stdout.strip())


def manual_chaining() -> None:
    normalize_runner = PythonRunner(module_path=MODULES_PATH / "normalize", package_manager=UvPackageManager())
    normalize_process = normalize_runner.run(
        payload={"text": "  Building pipelines is straightforward with Runner.  "}
    )
    normalized_data = json.loads(normalize_process.stdout or "{}")

    stats_runner = PythonRunner(module_path=MODULES_PATH / "stats", package_manager=UvPackageManager())
    stats_process = stats_runner.run(payload={"text": normalized_data.get("text", "")})

    print("Normalize stdout:\n", normalize_process.stdout.strip())
    print("Stats stdout:\n", stats_process.stdout.strip())


def run_node_module() -> None:
    runner = NodeRunner(module_path=MODULES_PATH / "greet", package_manager=PnpmPackageManager())
    process = runner.run(payload={"name": "Module Runner"})
    print("Greet (Node.js) stdout:\n", process.stdout.strip())


def run_node_script() -> None:
    runner = NodeRunner(module_path=MODULES_PATH / "greet", script="start")
    process = runner.run(payload={"name": "Module Runner (via script)"})
    print("Greet via npm script stdout:\n", process.stdout.strip())


def run_shell_module() -> None:
    runner = ShellRunner(module_path=MODULES_PATH / "greet_shell")
    process = runner.run(payload={"name": "Module Runner"})
    print("Greet (shell) stdout:\n", process.stdout.strip())


if __name__ == "__main__":
    run_system_module()
    run_single_module()
    manual_chaining()
    run_node_module()
    run_node_script()
    run_shell_module()
