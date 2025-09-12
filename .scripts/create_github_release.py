#!/usr/bin/env python3.13

import argparse
import re
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from includes.git import get_git_repository  # noqa: E402
from includes.utils.logs import LOGGER  # noqa: E402
from includes.utils.subprocess import run_cmd  # noqa: E402

ROOT_DIR = SCRIPTS_DIR.parent

_VERSION_RE = re.compile(r"^[v]\d+[.]\d+[.]\d+([-][0-9A-Za-z.-]+)?$")
_GITHUB_CONFIG_RE = re.compile(r"^.*[.]com[/:]([^/:]+)/([^/]+)[.]git$")


# == Main function
def create_github_release(version: str) -> None:
    org, repo_name = get_git_repository()
    github_repository = f"{org}/{repo_name}"
    print(f"REPOSITORY  = {github_repository}")
    print(f"VERSION     = {version}")
    print()

    m = _VERSION_RE.match(version)
    if not m:
        LOGGER.error(
            f"Given version does not match expected format vX.Y.Z(-suffix)?: {version!r}"
        )
        exit(1)

    process = run_cmd(
        f"gh release view {version!r} --repo {github_repository!r}", quiet=True
    )
    if process.successful():
        match input(
            f"Do you want to delete the existing release of {version!r} in {github_repository!r}? (y/N)"
        ).lower():
            case "y":
                # Delete previous release and tag of same version
                run_cmd(
                    f"gh release delete {version!r} --repo {github_repository!r} -y --cleanup-tag",
                    raise_on_error=True,
                )
                print()
            case _:
                raise InterruptedError("User aborted.")

    # Delete previous tag of same version if it exists
    run_cmd(f"git tag  --delete {version!r}")

    # Create and push new tag
    run_cmd(
        f"git tag -s {version!r} -m ''",
        f"git push origin {version!r} --force",
        raise_on_error=True,
    )

    # Create a release on GitHub
    run_cmd(
        f"gh release create {version!r} --repo {github_repository!r} --title {version!r}",
        raise_on_error=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a new GitHub release for the current repository.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "version",
        type=str,
        help="Version for the new release. Format: vX.Y.Z(-suffix)?",
    )
    args = parser.parse_args()

    create_github_release(args.version)
