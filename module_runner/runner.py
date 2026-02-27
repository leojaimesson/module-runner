import json
import logging
import subprocess
from pathlib import Path
from subprocess import CompletedProcess
from typing import Optional

from .exceptions import RunnerExecutionError
from .environment import EnvironmentManager, EnvironmentMode
from .environment.constants import MAIN_PY

logger = logging.getLogger("module_runner")


class Runner:

    def __init__(self, module_path: str | Path, environment: EnvironmentMode | str = EnvironmentMode.AUTO) -> None:
        self.module_path = Path(module_path).resolve()
        self.environment = environment
        self.module_name = self.module_path.name

    def run(
        self,
        payload: Optional[dict] = None,
    ) -> CompletedProcess[str]:
        script_path = self.module_path / MAIN_PY

        if not script_path.exists():
            raise FileNotFoundError(f"Module '{self.module_name}' does not contain {MAIN_PY}")

        env_manager = EnvironmentManager(self.module_path, self.environment)
        executor = env_manager.ensure()

        if str(executor) == "uv":
            cmd = ["uv", "run", "--project", str(self.module_path), "python", str(script_path)]
        else:
            cmd = [str(executor), str(script_path)]

        if payload is not None:
            cmd.append(json.dumps(payload))

        logger.info("[%s] executing: %s", self.module_name, " ".join(cmd))

        process: CompletedProcess[str] = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(self.module_path),
        )

        if process.returncode != 0:
            raise RunnerExecutionError(
                module=self.module_name,
                exit_code=process.returncode,
                stderr=process.stderr,
                stdout=process.stdout,
                cmd=cmd,
            )

        return process
