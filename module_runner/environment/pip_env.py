import importlib.util
import logging
import subprocess
import sys
from pathlib import Path

from .constants import PYPROJECT_TOML, REQUIREMENTS_TXT, VENV_DIR
from .utils import venv_python
from .mode import EnvironmentMode

logger = logging.getLogger("module_runner")


def ensure_pip_environment(module_path: Path, module_name: str) -> Path:
    """Provision and return the Python interpreter inside a venv."""
    if importlib.util.find_spec("venv") is None:
        detail = "pip mode requires the standard library venv module, but it is unavailable"
        raise RuntimeError(
            f"Environment '{EnvironmentMode.PIP.value}' is unavailable for module '{module_name}': {detail}"
        )

    venv_path = module_path / VENV_DIR
    python_bin = venv_python(venv_path)

    if not venv_path.exists():
        create_cmd = [sys.executable, "-m", "venv", str(venv_path)]
        logger.info("[%s] creating venv: %s", module_name, " ".join(create_cmd))
        _run_checked(create_cmd, module_path, module_name, "create virtual environment")

        pyproject = module_path / PYPROJECT_TOML
        req = module_path / REQUIREMENTS_TXT

        if pyproject.exists():
            install_cmd = [str(python_bin), "-m", "pip", "install", "."]
            logger.info("[%s] installing deps: %s", module_name, " ".join(install_cmd))
            _run_checked(install_cmd, module_path, module_name, "install dependencies from pyproject.toml")
        elif req.exists():
            install_cmd = [str(python_bin), "-m", "pip", "install", "-r", str(req)]
            logger.info("[%s] installing deps: %s", module_name, " ".join(install_cmd))
            _run_checked(install_cmd, module_path, module_name, "install requirements")
    else:
        logger.info("[%s] reusing existing venv at %s", module_name, venv_path)

    return python_bin


def _run_checked(cmd: list[str], module_path: Path, module_name: str, action: str) -> None:
    try:
        subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            cwd=str(module_path),
        )
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip() if exc.stderr else str(exc)
        raise RuntimeError(
            f"Environment '{EnvironmentMode.PIP.value}' failed to {action} for module '{module_name}': {stderr}"
        ) from exc
