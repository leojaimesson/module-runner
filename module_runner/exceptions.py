from typing import Optional


class RunnerExecutionError(Exception):
    def __init__(
        self,
        module: str,
        exit_code: int,
        stderr: str,
        stdout: str = "",
        cmd: Optional[list[str]] = None,
    ):
        self.module = module
        self.exit_code = exit_code
        self.stderr = stderr
        self.stdout = stdout
        self.cmd = cmd

        parts = [f"Module '{module}' failed with exit code {exit_code}"]

        if cmd:
            parts.append(f"  command : {' '.join(cmd)}")

        if stderr.strip():
            parts.append(f"  stderr  : {stderr.strip()}")

        if stdout.strip():
            parts.append(f"  stdout  : {stdout.strip()}")

        if not stderr.strip() and not stdout.strip():
            parts.append("  (no output captured)")

        super().__init__("\n".join(parts))
