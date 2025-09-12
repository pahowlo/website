#!/usr/bin/env python3.13

import re
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from includes.utils.logs import LOGGER  # noqa: E402
from includes.utils.subprocess import run_cmd  # noqa: E402


_GIT_REMOVE_URL_RE = re.compile(r"^(.*[.]com[/:])([^/:]+)/([^/]+)[.]git$")


def get_git_base_url() -> str:
    process = run_cmd("git config --get remote.origin.url", quiet=True)
    if not process.successful():
        LOGGER.error("Could not determine git base url", *sys.stderr)
        exit(1)

    url = process.stdout[0].strip()
    m = _GIT_REMOVE_URL_RE.match(url)
    if m:
        return m.group(1)

    raise ValueError(f"Could not parse git base url from: {url!r}")


def get_git_repository() -> tuple[str, str]:
    """Return (owner, repo_name) of the current git repository."""
    process = run_cmd("git config --get remote.origin.url", quiet=True)
    if not process.successful():
        LOGGER.error("Could not determine git repository", *sys.stderr)
        exit(1)

    url = process.stdout[0].strip()
    m = _GIT_REMOVE_URL_RE.match(url)
    if m:
        return m.group(2), m.group(3)

    raise ValueError(f"Could not parse git repository from: {url!r}")
