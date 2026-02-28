import json
import shutil
from pathlib import Path
from typing import Optional

from ..environment.constants import MAIN_JS
from .base import BaseRunner
from .package_managers import NodePackageManager, NpmPackageManager


class NodeRunner(BaseRunner):
    """Runs a Node.js module via a script entrypoint or a package.json script."""

    def __init__(
        self,
        module_path: str | Path,
        entrypoint: Optional[str] = None,
        script: Optional[str] = None,
        package_manager: NodePackageManager = None,
    ) -> None:
        super().__init__(module_path, entrypoint)
        self.script = script
        self.package_manager = package_manager or NpmPackageManager()

    def _build_command(self, payload: Optional[dict]) -> list[str]:
        node_bin = shutil.which("node")
        if node_bin is None:
            raise RuntimeError(
                f"Environment 'node' is unavailable for module '{self.module_name}': "
                "node executable not found in PATH"
            )

        self.package_manager.install(self.module_path, self.module_name)

        if self.script is not None:
            return self.package_manager.run_script(self.script, payload)

        script_path = self._entrypoint_path(MAIN_JS)
        cmd = [node_bin, str(script_path)]
        if payload is not None:
            cmd.append(json.dumps(payload))
        return cmd
