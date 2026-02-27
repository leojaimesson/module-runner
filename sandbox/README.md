# Sandbox Examples

This directory illustrates how to use Module Runner's `Runner` class to execute isolated modules. Any communication between modules is your responsibility (stdout parsing, temp files, queues, etc.).

## Layout

- `modules/system_report/` – no `requirements.txt` or `pyproject.toml`, so it runs with the system interpreter and prints host metadata.
- `modules/normalize/` – trims, lowercases, and removes diacritics from the `text` field (depends on `text-unidecode`).
- `modules/stats/` – computes simple metrics with `numpy`, showcasing a module driven by `pyproject.toml`/`uv`.
- `run_examples.py` – script with standalone executions plus a manual chaining example that reuses stdout.

## Module Dependencies

- Modules with `requirements.txt` (e.g., `modules/normalize/`) are provisioned using `uv` when available (`uv venv` + `uv pip install -r`), falling back to `venv`/`pip` otherwise.
- Modules with `pyproject.toml` (e.g., `modules/stats/`) run through `uv run`, so dependencies are resolved automatically without a separate `venv`.

If `uv` is missing from `PATH` or the running Python lacks `venv` support, Module Runner raises a descriptive `RuntimeError` explaining that declared dependencies cannot be provisioned automatically.

## Requirements

- Python 3.9+
- Project dependencies installed (e.g., `pip install -e .`).

## Usage

1. From the repository root, run:

   ```bash
   python sandbox/run_examples.py
   ```

2. Inspect the terminal output. The script first runs `system_report` using the current interpreter, then shows a virtual-environment-backed module, and finally demonstrates manual chaining with the `stats` module.

Feel free to duplicate modules in `sandbox/modules/` to explore other scenarios (e.g., `pyproject.toml` for `uv`, `requirements.txt` for dedicated virtual environments).
