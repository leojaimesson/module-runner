from importlib.metadata import version, PackageNotFoundError

from .runners import (
    NodeRunner, PythonRunner,
    UvPackageManager, PipPackageManager, SystemPackageManager,
    NpmPackageManager, YarnPackageManager, PnpmPackageManager,
)
from .exceptions import RunnerExecutionError
from .environment import EnvironmentMode

try:
    __version__ = version("module-runner")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = [
    "NodeRunner",
    "PythonRunner",
    "UvPackageManager",
    "PipPackageManager",
    "SystemPackageManager",
    "NpmPackageManager",
    "YarnPackageManager",
    "PnpmPackageManager",
    "RunnerExecutionError",
    "EnvironmentMode",
    "__version__",
]
