# Module Runner

**Explicit, isolated task execution for Python and Node.js.**

Module Runner sits in the gap between ad-hoc scripts and heavyweight orchestration frameworks. You explicitly choose the runner and the package manager for each module — no magic auto-detection, no hidden behavior. What you read is exactly what runs.

## Features

- 🎯 **Explicit runners**: choose `PythonRunner`, `NodeRunner`, or `ShellRunner` — no hidden detection logic.
- 📦 **Swappable package managers**: plug in `UvPackageManager`, `PipPackageManager`, `NpmPackageManager`, `YarnPackageManager`, `PnpmPackageManager`, or `SystemPackageManager`.
- 🧱 **Opinionated boundary**: no implicit payload chaining — what a module prints or writes is entirely up to you.
- 🛡️ **Atomic workflows**: fail fast, clear error surfaces, and easy cleanup — each module runs in its own isolated process.
- 🪪 **Clear error surface**: `RunnerExecutionError` captures module failures while missing tooling raises descriptive `RuntimeError`s, keeping debugging straightforward.
- 🔍 **Built-in logging**: uses Python's standard `logging` module under the `module_runner` logger.

## Logging

```python
import logging
logging.getLogger("module_runner").setLevel(logging.INFO)
logging.basicConfig()
```

## When to Use

- Simple local automation or scripting glue with a lightweight footprint
- Per-module dependency isolation without cross-contamination
- Predictable, sequential execution you can reason about
- Container-free lightweight tasks

## When Not to Use

- Complex DAG dependencies or branching workflows
- Scheduling, cron-style orchestration, or SLAs
- Distributed workers or autoscaling fleets
- Enterprise workflow/orchestration guarantees

## Installation

```bash
pip install module_runner
# or
uv add module_runner
```

## Quick Start

### Python module

```python
from module_runner import PythonRunner, UvPackageManager

runner = PythonRunner(
    module_path="modules/normalize",
    package_manager=UvPackageManager(),
)
process = runner.run(payload={"text": " Hello World "})
print(process.stdout)
```

### Node.js module — entrypoint

```python
from module_runner import NodeRunner

runner = NodeRunner(module_path="modules/greet")
process = runner.run(payload={"name": "Alice"})
print(process.stdout)
```

### Node.js module — package.json script

```python
from module_runner import NodeRunner, YarnPackageManager

runner = NodeRunner(
    module_path="modules/greet",
    script="start",
    package_manager=YarnPackageManager(),
)
process = runner.run(payload={"name": "Alice"})
print(process.stdout)
```

> If no `package_manager` is specified, `NpmPackageManager` is used by default for Node.js modules.

### Shell script module

```python
from module_runner import ShellRunner

runner = ShellRunner(module_path="modules/greet_shell")
process = runner.run(payload={"name": "Alice"})
print(process.stdout)
```

The payload is serialized as JSON and passed as `$1` inside the script. The default entrypoint is `main.sh`. By default `bash` is tried first, falling back to `sh`. You can pin a specific shell with the `shell` parameter (`"bash"` or `"sh"`).

## Python Package Managers

| Class | Tooling required | Use case |
|---|---|---|
| `UvPackageManager` | `uv` in PATH | `pyproject.toml` or `requirements.txt` modules |
| `PipPackageManager` | `venv` module | `pyproject.toml` or `requirements.txt` modules, no `uv` |
| `SystemPackageManager` | none | no dependencies, runs with the current interpreter |

```python
from module_runner import PythonRunner, PipPackageManager, SystemPackageManager

# venv + pip
PythonRunner(module_path="modules/normalize", package_manager=PipPackageManager())

# system interpreter, no setup
PythonRunner(module_path="modules/report", package_manager=SystemPackageManager())
```

## Shell Runner

```python
from module_runner import ShellRunner

# auto-detect shell (bash → sh)
ShellRunner(module_path="modules/greet_shell")

# pin to sh
ShellRunner(module_path="modules/greet_shell", shell="sh")

# custom entrypoint
ShellRunner(module_path="modules/greet_shell", entrypoint="run.sh")
```

The shell module receives the JSON payload as `$1`. Reading it is plain shell — no runtime dependencies required:

```sh
#!/bin/sh
PAYLOAD="${1:-{}}"
NAME=$(echo "$PAYLOAD" | sed 's/.*"name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')
printf '{"message": "Hello, %s!"}\n' "$NAME"
```

## Node.js Package Managers

| Class | Tooling required | Script command built |
|---|---|---|
| `NpmPackageManager` | `npm` in PATH | `npm run <script>` |
| `YarnPackageManager` | `yarn` in PATH | `yarn <script>` |
| `PnpmPackageManager` | `pnpm` in PATH | `pnpm run <script>` |

All three call `install` automatically on first run if `node_modules` is absent.

## Custom Entrypoint

Both runners accept an `entrypoint` parameter to override the default (`main.py` / `main.js`):

```python
PythonRunner(module_path="modules/normalize", entrypoint="run.py", package_manager=UvPackageManager())
NodeRunner(module_path="modules/greet", entrypoint="index.js")
```

## Module Layout

```text
modules/
├── normalize/          # Python + uv
│   ├── main.py
│   └── pyproject.toml
├── greet/              # Node.js
│   ├── main.js
│   └── package.json
├── report/             # System Python, no deps
│   └── main.py
└── greet_shell/        # Shell script
    └── main.sh
```

## Sandbox Playground

The [sandbox](sandbox/README.md) directory ships with toy modules that showcase all scenarios:

```bash
python sandbox/run_examples.py
```

## Development

```bash
git clone https://github.com/leojaimesson/module-runner.git
cd module-runner
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

## License

Module Runner is released under the MIT License. See [LICENSE](LICENSE) for details.

