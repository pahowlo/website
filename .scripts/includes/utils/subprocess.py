#!/usr/bin/env python3.13

import subprocess
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import IO


@dataclass
class ShellProcess:
    cmd: str
    exit_code: int
    stdout: list[str]
    stderr: list[str]

    def successful(self) -> bool:
        return self.exit_code == 0


class ShellProcessError(Exception):
    """Failed to successfully run a shell command."""


def run_cmd(
    *cmds: str,
    shell: str = "/bin/sh",
    quiet: bool = False,
    raise_on_error: bool = False,
) -> ShellProcess:
    """Run provided command(s) in a non-interactive shell."""
    pool = ThreadPoolExecutor(max_workers=2)

    cmd = " && ".join(cmds)
    proc = subprocess.Popen(
        cmd,
        shell=True,
        executable=shell,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    stdout_stream = pool.submit(_tee_stream, proc.stdout, quiet=quiet)
    stderr_stream = pool.submit(_tee_stream, proc.stderr, quiet=quiet)

    proc.wait()
    pool.shutdown()
    stdout_lines = stdout_stream.result()
    stderr_lines = stderr_stream.result()

    if raise_on_error and proc.returncode != 0:
        raise ShellProcessError(
            f"Command failed with exit code {proc.returncode}: {cmd!r}\n"
            + "\n".join(stderr_lines)
        )
    return ShellProcess(
        cmd=cmd,
        exit_code=proc.returncode,
        stdout=stdout_lines,
        stderr=stderr_lines,
    )


def run_interactive_cmd(
    *cmds: str,
    shell: str = "/bin/sh",
    raise_on_error: bool = False,
) -> int:
    """Run provided command(s) in an interactive shell.

    Stdout/stderr outputs cannot be captured.
    """
    cmd = " && ".join(cmds)
    proc = subprocess.Popen(
        cmd,
        shell=True,
        executable=shell,
        text=True,
        bufsize=1,
    )
    proc.wait()

    if raise_on_error and proc.returncode != 0:
        raise ShellProcessError(
            f"Command failed with exit code {proc.returncode}: {cmd!r}\n"
        )
    exit_code = proc.returncode
    return exit_code


def _tee_stream(stream: IO[str], quiet: bool = False) -> list[str]:
    out = []
    eof = ""
    for line in iter(stream.readline, eof):
        if not line:
            continue
        if not quiet:
            print(line, end="")
        out.append(line)
    stream.close()
    return out
