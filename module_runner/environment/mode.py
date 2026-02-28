from enum import Enum


class EnvironmentMode(str, Enum):
    AUTO = "auto"
    UV = "uv"
    PIP = "pip"
    NODE = "node"
    SYSTEM = "system"
