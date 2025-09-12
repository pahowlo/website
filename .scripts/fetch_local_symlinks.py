#!/usr/bin/env python3.13

import os
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPTS_DIR.parent


def fetch_local_symlinks():
    links_file = ROOT_DIR / ".links_conf"
    if not links_file.is_file():
        print(f"ERROR: Links config file not found: {links_file}")
        exit(1)

    try:
        with (ROOT_DIR / ".links_relpath").open() as f:
            links_relpath = f.readline().strip()
    except Exception as e:
        print(f"ERROR: Links config file not found: {links_file}\n\n" + e.__traceback__)
        exit(1)

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

            link_name = os.path.basename(link_dest)
            link_local_target = (ROOT_DIR / links_relpath / link_name).resolve()

            print(f"Creating symlink: {link_path} -> {link_local_target}\n")

            # Check and handle if something already exists at that path
            if link_path.is_symlink():
                link_path.unlink()
            elif link_path.exists():
                match input(
                    f"Path already exists and is not a symlink. Override {link_path}? (y/N) "
                ).lower():
                    case "y":
                        if link_path.is_dir():
                            import shutil

                            shutil.rmtree(link_path)
                        else:
                            link_path.unlink()
                    case _:
                        raise InterruptedError("User aborted.")

            os.makedirs(link_path.parent, exist_ok=True)
            link_path.symlink_to(link_local_target)


if __name__ == "__main__":
    fetch_local_symlinks()
