import importlib.util
import logging
import shutil
from pathlib import Path

from .constants import PYPROJECT_TOML, REQUIREMENTS_TXT
from .mode import EnvironmentMode

logger = logging.getLogger("module_runner")


def resolve_mode(module_path: Path, requested: EnvironmentMode, module_name: str) -> EnvironmentMode:
    """Determine which environment mode should be used for the module."""
    if requested is not EnvironmentMode.AUTO:
        return requested

    has_pyproject = (module_path / PYPROJECT_TOML).exists()
    has_requirements = (module_path / REQUIREMENTS_TXT).exists()
    uv_available = shutil.which("uv") is not None
    pip_available = importlib.util.find_spec("venv") is not None

    if has_pyproject:
        if uv_available:
            logger.info("[%s] strategy=uv  (pyproject.toml detected, uv available)", module_name)
            return EnvironmentMode.UV

        if pip_available:
            logger.info("[%s] strategy=pip  (pyproject.toml detected, uv unavailable — fallback to venv+pip)", module_name)
            return EnvironmentMode.PIP

        detail = f"{PYPROJECT_TOML} detected but neither uv nor venv is available"
        raise RuntimeError(
            f"Environment setup failed for module '{module_name}': {detail}"
        )

    if has_requirements:
        if uv_available:
            logger.info("[%s] strategy=uv  (requirements.txt detected, uv available)", module_name)
            return EnvironmentMode.UV
        if pip_available:
            logger.info("[%s] strategy=pip  (requirements.txt detected, uv unavailable — fallback to venv+pip)", module_name)
            return EnvironmentMode.PIP

        detail = f"{REQUIREMENTS_TXT} detected but pip is unavailable"
        raise RuntimeError(
            f"Environment '{EnvironmentMode.PIP.value}' is unavailable for module '{module_name}': {detail}"
        )

    logger.info("[%s] strategy=system  (no dependency file found, using current interpreter)", module_name)
    return EnvironmentMode.SYSTEM
