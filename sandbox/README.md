# Sandbox Examples

This directory illustrates how to use Module Runner with explicit runners and package managers. Any communication between modules (stdout parsing, temp files, queues, etc.) is your responsibility.

## Layout

- `modules/system_report/` — no dependencies, runs with `SystemPackageManager` (current interpreter).
- `modules/normalize/` — trims, lowercases, and removes diacritics from the `text` field (depends on `text-unidecode`), runs with `UvPackageManager`.
- `modules/stats/` — computes simple metrics with `numpy` via `pyproject.toml`, runs with `UvPackageManager`.
- `modules/greet/` — Node.js greeting module, runs with `NodeRunner` (entrypoint or `script`).
- `run_examples.py` — standalone executions, manual chaining, and a Node.js script example.

## Requirements

- Python 3.9+
- Project dependencies installed (`pip install -e .`)
- `uv` in PATH for `UvPackageManager` examples
- `node` and `npm` in PATH for Node.js examples

## Usage

```bash
python sandbox/run_examples.py
```

## Examples

```python
from module_runner import PythonRunner, NodeRunner
from module_runner import UvPackageManager, SystemPackageManager

# system interpreter, no deps
PythonRunner(module_path="modules/system_report", package_manager=SystemPackageManager())

# uv-managed environment
PythonRunner(module_path="modules/normalize", package_manager=UvPackageManager())

# Node.js via entrypoint
NodeRunner(module_path="modules/greet")

# Node.js via package.json script
NodeRunner(module_path="modules/greet", script="start")
```

