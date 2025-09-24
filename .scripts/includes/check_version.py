#!/usr/bin/env python3.13
import re

# When running a Python script, parent directory is added to sys.path
from includes.utils.subprocess import run_cmd

_VERSION_REGEX = re.compile(r"[0-9]+\.[0-9]+(\.[0-9]+)?")


def check_version(package: str, min_version: str) -> tuple[bool, str | None]:
    """Validate that the package version is greater or equal than the provided number.

    Args:
        package: The package name to check, must be available in PATH.
        min_version: The minimal version required. E.g. "X.Y.Z" or "X.Y".

    Returns:
        - True if the package was found and its version greater or equal.
        - The version found for package even if lower.
            None only if package was not found, or has no version option.
    """
    exit_code, stdout, _ = run_cmd(f"$(which {package!r}) --version", quiet=True)
    if exit_code != 0 or not stdout:
        return False, None  # Package not found, or has no version option

    m = _VERSION_REGEX.search(stdout)
    if not m:
        return False, None  # Could not parse version
    version = m.group(0)

    min_version_tup = list(map(int, min_version.split(".")))
    version_tup = list(map(int, version.split(".")))

    version_tup.extend([0] * (len(min_version_tup) - len(version_tup)))

    for v, min_v in zip(version_tup, min_version_tup):
        if v > min_v:
            return True, version
        if v < min_v:
            return False, version

    return True, version
