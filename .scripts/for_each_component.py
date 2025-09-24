#!/usr/bin/env python3.13

import os
import sys
from pathlib import Path

# When running a Python script, parent directory is added to sys.path
from includes.utils.subprocess import run_cmd
from includes.utils.logs import LOGGER, Color


ROOT_DIR = Path(__file__).resolve().parent.parent


def for_each_component(cmd: str) -> None:
    LOGGER.info(f"Runing command for each component: {Color.ORANGE}{cmd}{Color.NC}")

    components = sorted(d for d in (ROOT_DIR / "components").iterdir() if d.is_dir())

    current_workdir = os.getcwd()
    try:
        for c_dir in components:
            os.chdir(c_dir)
            print(f"{Color.BLUE}./{c_dir.name}{Color.NC}")
            run_cmd(cmd)
            print()
    finally:
        # Restore working directory
        os.chdir(current_workdir)


if __name__ == "__main__":
    cmd = " ".join(sys.argv[1:]).strip() + "\n"
    for_each_component(cmd)
