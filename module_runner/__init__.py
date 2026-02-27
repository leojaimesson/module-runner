from importlib.metadata import version, PackageNotFoundError

from .runner import Runner
from .exceptions import RunnerExecutionError
from .environment import EnvironmentMode

try:
    __version__ = version("module-runner")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["Runner", "RunnerExecutionError", "EnvironmentMode", "__version__"]
