from pathlib import Path
import sys

from .mode import EnvironmentMode
from .resolver import resolve_mode
from .pip_env import ensure_pip_environment
from .uv_env import ensure_uv_environment


class EnvironmentManager:

    def __init__(self, module_path: Path, mode: EnvironmentMode | str = EnvironmentMode.AUTO):
        self.module_path = module_path
        self.module_name = module_path.name
        self.mode = self._coerce_mode(mode)

    def _coerce_mode(self, mode: EnvironmentMode | str) -> EnvironmentMode:
        if isinstance(mode, EnvironmentMode):
            return mode

        try:
            return EnvironmentMode(mode)
        except ValueError as exc:
            raise RuntimeError(
                f"Unsupported environment mode '{mode}' for module '{self.module_name}'"
            ) from exc

    def resolve(self) -> EnvironmentMode:
        return resolve_mode(self.module_path, self.mode, self.module_name)

    def ensure(self) -> Path:
        env_type = self.resolve()

        if env_type is EnvironmentMode.UV:
            return ensure_uv_environment(self.module_path, self.module_name)

        if env_type is EnvironmentMode.PIP:
            return ensure_pip_environment(self.module_path, self.module_name)

        return Path(sys.executable)
