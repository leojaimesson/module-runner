# Module Runner

Module Runner sits in the gap between ad-hoc scripts and heavyweight orchestration frameworks. It gives each module a predictable, isolated environment without asking you to bolt on extra infrastructure, schedulers, or workflow engines. The project stays intentionally lightweight and focuses on two responsibilities:

1. Detect the proper execution strategy (system Python, `venv`, or `uv`).
2. Launch the module with an optional JSON payload, returning the `subprocess.CompletedProcess` so you can decide how to consume `stdout`, `stderr`, or exit codes.

Any higher-level orchestration (pipelines, RPC, shared storage, etc.) is an application concern, keeping this library small and predictable.

## Features

- ⚙️ **Automatic environment discovery**: detects `pyproject.toml` or `requirements.txt` (→ `uv` when available, `venv` as fallback), or falls back to the current interpreter.
- 📦 **Per-module dependencies**: each module lives in its own folder with its own toolchain, avoiding cross-contamination.
- 🧱 **Opinionated boundary**: no implicit payload chaining—what a module prints, writes, or exposes is entirely up to you.
- 🪪 **Clear error surface**: `RunnerExecutionError` captures module failures while missing tooling raises descriptive `RuntimeError`s, keeping debugging straightforward.
- 🔍 **Built-in logging**: uses Python's standard `logging` module under the `module_runner` logger — enable `DEBUG` to see the resolved strategy, every setup command, and the final execution command.

## Logging

Module Runner emits `INFO`-level log records under the `module_runner` logger. To see them:

```python
import logging
logging.getLogger("module_runner").setLevel(logging.INFO)
logging.basicConfig()
```

Example output:
```
[normalize] strategy=pip  (requirements.txt detected, uv unavailable — fallback to venv+pip)
[normalize] creating venv: /usr/bin/python3 -m venv .venv
[normalize] installing deps: .venv/bin/python -m pip install -r requirements.txt
[normalize] executing: .venv/bin/python main.py {"text": " Hello World "}
```

## Why This Exists

Module Runner is the missing middle layer between one-off helper scripts and enterprise orchestrators. It gives you just enough structure to keep automation tidy while remaining lightweight, infrastructure-free, and dependency-light.

## When to Use

Use Module Runner when you:

- Need simple local automation or scripting glue with a lightweight footprint
- Have dependency conflicts between scripts and want per-module isolation
- Want predictable, sequential execution you can reason about
- Prefer to stay container-free for lightweight tasks
- Do not need a workflow engine or task scheduler

## When Not to Use

Reach for other tooling if you require:

- Complex DAG dependencies or branching workflows
- Scheduling, cron-style orchestration, or SLAs
- Distributed workers or autoscaling fleets
- Monitoring dashboards, retries, or alerting UI
- Enterprise workflow/orchestration guarantees

## Philosophy

- Small, explicit, predictable, and lightweight
- Infrastructure-free: relies on the Python already on your machine
- Focused on one problem—launching modules in clean environments

It is not meant to be a workflow engine; it simply keeps isolated scripts manageable.

## Installation

```bash
# using pip
pip install module_runner

# using uv
uv add module_runner

```

You only need Python 3.9+ and whichever tooling your modules request (e.g., `uv`, `venv`, system packages).

## Quick Start

```python
from module_runner import Runner

runner = Runner(module_path="modules/normalize_text")

process = runner.run(
    payload={"text": " Hello World "},
)

print(process.stdout)  # or json.loads(process.stdout)
```

Your module layout needs a `main.py` entry point. Any payload you pass is serialized as JSON and delivered as the last CLI argument. How you emit results (stdout, files, sockets) is entirely your call.

## Environment Selection

| Signal in module folder | Mode used     | Requirement |
| ----------------------- | ------------- | ----------- |
| `pyproject.toml`        | `uv run ...`  | `uv` available in `PATH` |
| `pyproject.toml` (no `uv`) | `python -m venv` + `pip install .` | `venv` module available |
| `requirements.txt`      | `uv venv` + `uv pip install -r requirements.txt` | `uv` available in `PATH` |
| `requirements.txt` (no `uv`) | `python -m venv` + `pip install -r requirements.txt` | `venv` module available |
| none of the above       | current interpreter (`sys.executable`) | none |

- Auto-detection always checks whether the required tooling is installed. When `uv` is available it is preferred for both `pyproject.toml` and `requirements.txt` modules. If `uv` is not available, both `pyproject.toml` and `requirements.txt` modules fall back to `venv`/`pip`.
- If a module signals that it needs `uv` or `venv` but the corresponding tooling is missing, Module Runner raises a descriptive `RuntimeError` explaining what needs to be installed.
- Runtime failures propagate as `RunnerExecutionError`, exposing the module name, exit code, captured `stderr`, captured `stdout`, and the exact `cmd` list that was executed — making it straightforward to reproduce or log failures.

## Sandbox Playground

The [sandbox](sandbox/README.md) directory ships with two toy modules (`normalize` and `stats`) that showcase:

- How `requirements.txt` triggers a module-specific virtual environment.
- How `pyproject.toml` causes execution via `uv run`.
- How you can manually chain modules by parsing the `stdout` from the first run and feeding it into the next.

Run everything with:

```bash
python sandbox/run_examples.py
```

Use this folder as a template to create your own modules or to test different deployment scenarios.

## Development

```bash
git clone https://github.com/leojaimesson/module-runner.git
cd module_runner
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

Feel free to open issues or pull requests with improvements. The scope intentionally stays small: reliable environment setup and process execution.

## License

Module Runner is released under the MIT License. See [LICENSE](LICENSE) for details.
