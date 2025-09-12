#!/usr/bin/env python3.13
import re
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from includes.utils.logs import LOGGER # noqa: E402
from includes.utils.subprocess import run_cmd # noqa: E402
 
_VERSION_REGEX = re.compile(r"^[0-9]+\.[0-9]+(\.[0-9]+)?$")


def check_version(package: str, min_version: str) -> bool:
    """Validate that the package version is greater or equal than the provided number.

    Args:
        package: The package name to check, must be available in PATH.
        min_version: The minimal version required. E.g. "X.Y.Z" or "X.Y".
    """
    base_msg = f"Required: {package!r} must be installed with greater version than {min_version!r}"

    process = run_cmd(f"$(which {package!r}) --version", quiet=True)
    if not process.successful() or not process.stdout:
        LOGGER.error(
            f"{base_msg}, but was not found or could not read version",
        )
        return False

    m = _VERSION_REGEX.search(process.stdout[0])
    if not m:
        LOGGER.error(
            f"{base_msg}, but was not found or could not read version",
        )
        return False
    version = m.group(0)

    min_version_tup = tuple(map(int, min_version.split(".")))
    version_tup = tuple(map(int, version.split(".")))

    if min_version_tup > version_tup:
        LOGGER.error(
            f"{base_msg}, but found version {version!r} for $(which {package!r})",
        )
        return False

    return True
