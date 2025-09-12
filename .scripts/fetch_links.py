#!/usr/bin/env python3.13

import os
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from includes.git import get_git_base_url  # noqa: E402
from includes.utils.logs import LOGGER  # noqa: E402
from includes.utils.subprocess import run_cmd  # noqa: E402

ROOT_DIR = SCRIPTS_DIR.parent


def _fetch_link(
    link_path: Path, repo_name: str, repo_ref: str, git_base_url: str
) -> None:
    target_repo_url = f"{git_base_url}{repo_name}.git"
    if not link_path.name.endswith(".link"):
        link_path = link_path.with_name(f"{link_path.name}.link")

    print(f"LINK_PATH  = {link_path}")
    print(f"REPO_URL   = {target_repo_url}")
    print(f"REPO_REF   = {repo_ref}\n")

    # Check and handle if something already exists at that path
    if link_path.is_symlink():
        link_path.unlink()
    elif link_path.exists():
        answer = input(
            f"Path already exists and is not a symlink. Override {link_path}? (y/N) "
        ).lower()
        match answer:
            case "y":
                if link_path.is_dir():
                    import shutil

                    shutil.rmtree(link_path)
                else:
                    link_path.unlink()
            case _:
                raise InterruptedError("User aborted.")

    LOGGER.info(f"Cloning {repo_name} (ref: {repo_ref}) in link directory: {link_path}")
    os.makedirs(link_path, exist_ok=True)
    cwd = os.getcwd()
    try:
        os.chdir(link_path)
        run_cmd(
            f"""
            git init -q;
            git remote add origin {target_repo_url!r};
            git fetch --depth 1 origin {repo_ref!r};
            git checkout {repo_ref!r} -q
            """
        )
    finally:
        os.chdir(cwd)


def fetch_links():
    links_file = ROOT_DIR / ".links_conf"
    if not links_file.is_file():
        print(f"ERROR: Links config file not found: {links_file}")
        exit(1)

    git_base_url = get_git_base_url()

    with links_file.open() as f:
        for line in f:
            line = line.split("#")[0].strip()
            if not line:
                continue

            try:
                link_dest, repo_org_name, repo_ref, *_ = line.split()
            except Exception:
                print(f"ERROR: Invalid line in links config file: {line}")
                continue

            link_path = ROOT_DIR / f"{link_dest}.link"
            _fetch_link(link_path, repo_org_name, repo_ref, git_base_url)


if __name__ == "__main__":
    fetch_links()
