#!/usr/bin/env python3.13

import json
import os
import secrets
import shutil
import sys
from pathlib import Path

# When running a Python script, parent directory is added to sys.path
from includes.utils.logs import LOGGER
from includes.utils.subprocess import run_cmd, run_interactive_cmd
from includes.git import get_git_base_url
from fetch_links import fetch_links
from create_github_release import create_github_release

_TARGET_REPOSITORY = "pahowlo/pahowlo.github.io"
_TARGET_BRANCH = "main"

ROOT_DIR = Path(__file__).resolve().parent.parent


def publish() -> None:
    curr_workdir = os.getcwd()
    temp_dir = None
    try:
        # Ensure we are using the same version as specified in links config
        fetch_links()

        # Re-do build to be sure
        shutil.rmtree(ROOT_DIR / "target", ignore_errors=True)
        run_cmd(
            "pnpm install:all",
            "pnpm build:all",
            check=True,
        )
        print()

        # Parse arguments
        with open(ROOT_DIR / "package.json") as f:
            version_number = json.load(f)["version"]

        git_base_url = get_git_base_url()

        temp_dir = (
            Path("/tmp/projects/github-page") / f"publish-{secrets.token_hex(10)}"
        )
        os.makedirs(temp_dir, exist_ok=True)

        print(f"TEMP_DIR       = {temp_dir}")
        print(f"VERSION_NUMBER = {version_number}")
        print(f"TEMP_DIR       = {temp_dir}")
        print()

        os.chdir(temp_dir)

        # Clone target repository and remove old files
        target_repository = f"{git_base_url}{_TARGET_REPOSITORY}.git"
        run_cmd(
            f"git clone --branch {_TARGET_BRANCH!r} --depth 1 {target_repository!r} .",
            check=True,
        )
        for item in temp_dir.iterdir():
            if item.name in {".git", "LICENSE", "README.md"}:
                continue
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

        # Copy new files to the target repository
        for src_item in (ROOT_DIR / "target").iterdir():
            if item.name in {".git", "LICENSE", "README.md"}:
                continue

            dest = temp_dir / src_item.name
            if src_item.is_dir():
                shutil.copytree(src_item, dest)
            else:
                shutil.copy2(src_item, dest)

        print()
        for path in sorted(temp_dir.rglob("*")):
            if ".git" in path.parts:
                continue

            print(str(path.relative_to(temp_dir)))
        print()

        run_cmd("git add -A", check=True)

        # Verify that there are actual changes in target repository to commit
        exit_code, _, _ = run_cmd("git diff --quiet HEAD")
        if exit_code == 0:
            LOGGER.info("No changes to commit.")
            return 0

        # Create tag from source repository
        os.chdir(ROOT_DIR)
        release_tag = f"v{version_number}"
        create_github_release(release_tag)

        # Commit and push changes
        os.chdir(temp_dir)
        new_commit_msg = f"Release {release_tag}"

        _, stdout, _ = run_cmd("git log -1 --pretty=format:%s", quiet=True)

        if new_commit_msg == stdout.strip():
            commit_args = "--amend"
        else:
            commit_args = f" --edit -m {new_commit_msg!r}"

        run_interactive_cmd(
            f"git commit {commit_args} -S",
            "git push --force-with-lease",
            check=True,
        )
    finally:
        # Clean up temp_dir
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)
        # Restore working directory
        os.chdir(curr_workdir)


if __name__ == "__main__":
    sys.exit(publish())
