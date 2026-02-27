import logging
import shutil
import subprocess
from pathlib import Path

from .constants import PYPROJECT_TOML, REQUIREMENTS_TXT, VENV_DIR
from .utils import venv_python
from .mode import EnvironmentMode

logger = logging.getLogger("module_runner")


def ensure_uv_environment(module_path: Path, module_name: str) -> Path:
    """Ensure uv is available and provision dependencies in the module directory."""
    uv_bin = shutil.which("uv")
    if uv_bin is None:
        raise RuntimeError(
            f"Environment '{EnvironmentMode.UV.value}' is unavailable for module '{module_name}': uv executable not found in PATH"
        )

    requirements_path = module_path / REQUIREMENTS_TXT
    pyproject_path = module_path / PYPROJECT_TOML

    if requirements_path.exists() and not pyproject_path.exists():
        venv_path = module_path / VENV_DIR
        python_bin = venv_python(venv_path)
        if not venv_path.exists():
            create_cmd = [uv_bin, "venv"]
            logger.info("[%s] creating venv: %s", module_name, " ".join(create_cmd))
            _run_uv_checked(create_cmd, module_path, module_name, "create virtual environment")
        else:
            logger.info("[%s] reusing existing venv at %s", module_name, venv_path)
        install_cmd = [uv_bin, "pip", "install", "-r", str(requirements_path)]
        logger.info("[%s] installing deps: %s", module_name, " ".join(install_cmd))
        _run_uv_checked(install_cmd, module_path, module_name, "install dependencies from requirements.txt")
        return python_bin

    logger.info("[%s] using uv run for pyproject.toml-based module", module_name)
    return Path("uv")


def _run_uv_checked(
    cmd: list[str],
    module_path: Path,
    module_name: str,
    action: str,
) -> None:
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
            f"Environment '{EnvironmentMode.UV.value}' failed to {action} for module '{module_name}': {stderr}"
        ) from exc
