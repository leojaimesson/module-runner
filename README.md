# Module Runner

**Structure, isolate, and run local scripts in Python, Node.js, and Shell — without the overhead of containers.**

Module Runner brings discipline to local automation. Instead of monolithic scripts that accumulate dependencies and break silently, you decompose work into explicit modules — each with its own declared environment, its own subprocess, and its own clear boundary. You declare the runner and the package manager. What you read is exactly what runs.

[![PyPI version](https://img.shields.io/pypi/v/module-runner)](https://pypi.org/project/module-runner/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

---

## The Problem

Modern automation pipelines commonly hit one of two failure modes:

- **Dependency hell**: a monolithic script accumulates imports and `pip install` calls until one upgrade silently breaks another, and untangling the mess costs more time than the original task.
- **Container overkill**: reaching for Docker to get isolation when you don't need networking, image management, or orchestration — just a clean, repeatable environment per script.

**Module Runner solves both.** Each module is a self-contained unit with its own declared dependencies. Environment creation is automatic, using the toolchain you already have (`uv`, `pip`, `npm`, `pnpm`, `yarn`). No Docker daemon. No virtual environments to manually activate. No global state contamination between scripts.

---

## How It Works

```
Your orchestrator (Python)
        │
        ├─ PythonRunner  →  uv/pip venv  →  module/main.py
        ├─ NodeRunner    →  npm/pnpm/yarn  →  module/main.js
        └─ ShellRunner   →  bash/sh  →  module/main.sh
```

Each `runner.run(payload)` call:
1. Serializes the payload as JSON.
2. Provisions the module's environment — venv creation is skipped if one already exists; `uv run` delegates caching to uv itself.
3. Spawns an isolated subprocess — no shared interpreter, no shared `node_modules`.
4. Returns a `CompletedProcess` or raises `RunnerExecutionError` with full context.

---

## Key Features

- **Explicit runner selection** — choose `PythonRunner`, `NodeRunner`, or `ShellRunner`. No auto-detection magic, no implicit environment guessing.
- **Swappable package managers** — `UvPackageManager`, `PipPackageManager`, `SystemPackageManager`, `NpmPackageManager`, `YarnPackageManager`, `PnpmPackageManager`.
- **Process-level isolation** — each module runs in its own subprocess with its own working directory. One module's failure cannot corrupt another's state.
- **Automatic environment provisioning** — environments are created and cached on first run; subsequent calls reuse them.
- **Structured error surfacing** — `RunnerExecutionError` carries `exit_code`, `stderr`, `stdout`, and the full command for immediate debuggability.
- **Zero hidden magic** — no payload chaining, no implicit wiring. What a module receives and emits is entirely under your control.
- **Built-in logging** — structured log output via Python's standard `logging` module under the `module_runner` logger.

---

## Installation

```bash
pip install module-runner
# or, with uv
uv add module-runner
```

Requires Python 3.10+. No mandatory runtime dependencies beyond the standard library.

---

## Quick Start

Install the library, define a module directory, and run it in under a minute.

### Run a Python module

```python
from module_runner import PythonRunner, UvPackageManager

runner = PythonRunner(
    module_path="modules/normalize",
    package_manager=UvPackageManager(),  # creates a uv-managed venv automatically
)

process = runner.run(payload={"text": "  hello world  "})
print(process.stdout)
# {"text": "hello world"}
```

### Run a Node.js module

```python
from module_runner import NodeRunner, PnpmPackageManager

runner = NodeRunner(
    module_path="modules/greet",
    package_manager=PnpmPackageManager(),  # runs pnpm install if node_modules is absent
)

process = runner.run(payload={"name": "Alessa"})
print(process.stdout)
# {"message": "Hello, Alessa!"}
```

### Run a Shell script

```python
from module_runner import ShellRunner

runner = ShellRunner(module_path="modules/greet_shell")
process = runner.run(payload={"name": "Alessa"})
print(process.stdout)
# {"message": "Hello, Alessa!"}
```

### Enable logging

```python
import logging

logging.basicConfig()
logging.getLogger("module_runner").setLevel(logging.INFO)
# INFO:module_runner:[normalize] executing: uv run python main.py '{"text": "hello"}'
```

---

## Use Cases

### 1. Hybrid Python / Node.js pipeline

Orchestrate a Python data-cleaning step followed by a Node.js rendering step — each with its own pinned dependencies — from a single Python script, without containers or Makefiles.

```python
import json
from module_runner import PythonRunner, NodeRunner, UvPackageManager, PnpmPackageManager

# Step 1 — normalize text (Python, uv-managed)
normalize = PythonRunner(
    module_path="pipeline/normalize",
    package_manager=UvPackageManager(),
)
result = normalize.run(payload={"text": raw_text})
clean = json.loads(result.stdout)

# Step 2 — render to HTML (Node.js, pnpm-managed)
render = NodeRunner(
    module_path="pipeline/render",
    package_manager=PnpmPackageManager(),
)
output = render.run(payload=clean)
print(output.stdout)
```

### 2. Managing conflicting library versions across modules

Two modules can depend on entirely different — and otherwise incompatible — versions of the same library. Module Runner provisions a separate environment for each.

```text
modules/
├── legacy_etl/    # requires pandas==1.5.3
│   ├── main.py
│   └── requirements.txt
└── modern_etl/    # requires pandas>=2.0
    ├── main.py
    └── pyproject.toml
```

```python
legacy = PythonRunner(module_path="modules/legacy_etl", package_manager=PipPackageManager())
modern = PythonRunner(module_path="modules/modern_etl", package_manager=UvPackageManager())

legacy.run(payload={"file": "old_data.csv"})
modern.run(payload={"file": "new_data.parquet"})
```

No version conflict. No virtual environment juggling. Each process is fully isolated.

### 3. Lightweight local automation without Docker

Use Module Runner as the execution layer for local automation tasks — data migrations, report generation, asset processing — where Docker would add operational overhead without meaningful benefit.

```python
from module_runner import PythonRunner, ShellRunner, SystemPackageManager, UvPackageManager

# No deps — run directly against the system interpreter
health_check = PythonRunner(
    module_path="tasks/check_db",
    package_manager=SystemPackageManager(),
)
health_check.run(payload={"host": "localhost", "port": 5432})

# Shell task — no Python runtime needed at all
notify = ShellRunner(module_path="tasks/send_slack_alert")
notify.run(payload={"message": "Pipeline complete"})
```

---

## Runners Reference

### `PythonRunner`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `module_path` | `str \| Path` | required | Path to the module directory |
| `package_manager` | `BasePythonPackageManager` | `UvPackageManager()` | Package manager to provision the environment |
| `entrypoint` | `str` | `"main.py"` | Script filename to execute |

### `NodeRunner`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `module_path` | `str \| Path` | required | Path to the module directory |
| `package_manager` | `BaseNodePackageManager` | `NpmPackageManager()` | Package manager for `node_modules` |
| `entrypoint` | `str` | `"main.js"` | Script filename to execute |
| `script` | `str \| None` | `None` | `package.json` script name; overrides `entrypoint` when set |

### `ShellRunner`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `module_path` | `str \| Path` | required | Path to the module directory |
| `entrypoint` | `str` | `"main.sh"` | Script filename to execute |
| `shell` | `str \| None` | `None` | Pin to `"bash"` or `"sh"`; auto-detects when `None` |

The payload is serialized as JSON and injected as `$1`. No runtime dependencies are required inside the script:

```sh
#!/bin/sh
PAYLOAD="${1:-{}}"
NAME=$(echo "$PAYLOAD" | sed 's/.*"name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')
printf '{"message": "Hello, %s!"}\n' "$NAME"
```

---

## Package Managers Reference

### Python

| Class | Requires | Behavior |
|---|---|---|
| `UvPackageManager` | `uv` in PATH | Creates a `uv`-managed venv; supports `pyproject.toml` and `requirements.txt` |
| `PipPackageManager` | `venv` module | Creates a standard `venv` and installs with `pip`; supports `pyproject.toml` and `requirements.txt` |
| `SystemPackageManager` | none | Runs against the current interpreter with no environment provisioning |

### Node.js

| Class | Requires | Install command | Run command |
|---|---|---|---|
| `NpmPackageManager` | `npm` in PATH | `npm install` | `npm run <script>` |
| `YarnPackageManager` | `yarn` in PATH | `yarn install` | `yarn <script>` |
| `PnpmPackageManager` | `pnpm` in PATH | `pnpm install` | `pnpm run <script>` |

All Node.js package managers automatically run `install` when `node_modules` is absent.

---

## Error Handling

All module failures raise `RunnerExecutionError`. Missing tooling (`uv` not in PATH, `node` not found) raises a `RuntimeError` at runner construction time — before any subprocess is spawned.

```python
from module_runner import PythonRunner, UvPackageManager, RunnerExecutionError

runner = PythonRunner(module_path="modules/normalize", package_manager=UvPackageManager())

try:
    process = runner.run(payload={"text": "hello"})
    print(process.stdout)
except RunnerExecutionError as e:
    # Structured context — no log-digging required
    print(f"Module : {e.module}")
    print(f"Exit   : {e.exit_code}")
    print(f"Stderr : {e.stderr}")
    print(f"Command: {' '.join(e.cmd)}")
```

---

## Module Layout

```text
modules/
├── normalize/          # Python + uv
│   ├── main.py
│   └── pyproject.toml
├── greet/              # Node.js + pnpm
│   ├── main.js
│   └── package.json
├── report/             # System Python — no deps
│   └── main.py
└── greet_shell/        # Shell script
    └── main.sh
```

Each module is an independent directory. The runner resolves the entrypoint relative to that directory and sets it as the working directory for the subprocess.

---

## Fit / No-Fit

| Fits well | Does not fit |
|---|---|
| Local automation scripts with mixed language steps | Complex DAGs with dynamic branching or fan-out |
| Per-module dependency isolation without containers | Long-running services or background daemons |
| Structured internal tooling and developer utilities | Distributed workers or multi-machine workloads |
| Sequential, readable automation you can reason about locally | Cron-style scheduling or SLA-bound orchestration |

---

## Sandbox Playground

The [sandbox/](sandbox/README.md) directory ships with working examples covering all runners and package managers:

```bash
git clone https://github.com/leojaimesson/module-runner.git
cd module-runner
pip install -e .
python sandbox/run_examples.py
```

---

## Development

```bash
git clone https://github.com/leojaimesson/module-runner.git
cd module-runner
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

---

## License

Module Runner is released under the MIT License. See [LICENSE](LICENSE) for details.

