#!/usr/bin/env python3.13

import re
import sys

# When running a Python script, parent directory is added to sys.path
from includes.utils.logs import LOGGER
from includes.utils.subprocess import run_cmd


_GIT_REMOVE_URL_RE = re.compile(r"^(.*[.]com[/:])([^/:]+)/([^/]+)[.]git$")


def get_git_base_url() -> str:
    exit_code, stdout, _ = run_cmd("git config --get remote.origin.url", quiet=True)
    if exit_code != 0:
        LOGGER.error("Could not determine git base url", *sys.stderr)
        exit(1)

    url = stdout.strip()
    m = _GIT_REMOVE_URL_RE.match(url)
    if m:
        return m.group(1)

    raise ValueError(f"Could not parse git base url from: {url!r}")


def get_git_repository() -> tuple[str, str]:
    """Return (owner, repo_name) of the current git repository."""
    exit_code, stdout, _ = run_cmd("git config --get remote.origin.url", quiet=True)
    if exit_code != 0:
        LOGGER.error("Could not determine git repository", *sys.stderr)
        exit(1)

    url = stdout.strip()
    m = _GIT_REMOVE_URL_RE.match(url)
    if m:
        return m.group(2), m.group(3)

    raise ValueError(f"Could not parse git repository from: {url!r}")
