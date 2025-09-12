#!/usr/bin/env python3.13

import os
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from includes.utils.logs import LOGGER, Color  # noqa: E402
from includes.utils.subprocess import run_cmd  # noqa: E402


ROOT_DIR = SCRIPTS_DIR.parent


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
