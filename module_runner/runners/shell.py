import json
import shutil
from pathlib import Path
from typing import Literal, Optional

from ..environment.constants import MAIN_SH
from .base import BaseRunner

_SHELLS = ["bash", "sh"]
ShellType = Literal["bash", "sh"]


class ShellRunner(BaseRunner):
    """Runs a shell script, passing the payload as a JSON string in $1."""

    def __init__(
        self,
        module_path: str | Path,
        entrypoint: Optional[str] = None,
        shell: Optional[ShellType] = None,
    ) -> None:
        if shell is not None and shell not in _SHELLS:
            raise ValueError(f"Invalid shell {shell!r}. Must be one of: {', '.join(_SHELLS)}")
        super().__init__(module_path, entrypoint)
        self.shell = shell

    def _build_command(self, payload: Optional[dict]) -> list[str]:
        shell_bin = self._resolve_shell()
        script_path = self._entrypoint_path(MAIN_SH)
        cmd = [shell_bin, str(script_path)]
        if payload is not None:
            cmd.append(json.dumps(payload))
        return cmd

    def _resolve_shell(self) -> str:
        candidates = [self.shell] if self.shell else _SHELLS
        for candidate in candidates:
            found = shutil.which(candidate)
            if found:
                return found
        raise RuntimeError(
            f"ShellRunner could not find a shell executable in PATH "
            f"(tried: {', '.join(candidates)})"
        )
