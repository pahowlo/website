#!/usr/bin/env python3.13
import sys
from typing import Literal


class Color:
    NC = "\033[0m"  # color reset

    BLUE = "\033[0;34m"
    BOLD = "\033[1m"
    BOLD_ORANGE = "\033[1;33m"
    DARKGRAY = "\033[1;30m"
    GREEN = "\033[0;32m"
    ORANGE = "\033[0;33m"
    RED = "\033[0;31m"


class Symbol:
    OK = f"{Color.GREEN}✔{Color.NC}"
    FAIL = f"{Color.RED}✘{Color.NC}"


class _Logger:
    @staticmethod
    def info(msg: str, *msg_details: str) -> None:
        _log("INFO", msg, *msg_details)

    @staticmethod
    def warning(msg: str, *msg_details: str) -> None:
        _log("WARNING", msg, *msg_details)

    @staticmethod
    def error(msg: str, *msg_details: str) -> None:
        _log("ERROR", msg, *msg_details)

    @staticmethod
    def success(msg: str, *msg_details: str) -> None:
        _log("SUCCESS", msg, *msg_details)


LOGGER = _Logger()


def _log(
    level: Literal["INFO", "WARNING", "ERROR", "SUCCESS"], msg: str, *msg_details: str
) -> None:
    max_padding = 8  # max_length_log_level + 1

    match level:
        case "INFO":
            color = Color.BLUE
        case "WARNING":
            color = Color.ORANGE
        case "ERROR":
            color = Color.RED
        case "SUCCESS":
            color = Color.GREEN
        case _:
            raise ValueError(f"Undefined log level: {level}")

    padding = " "
    padding_length = max_padding - len(level)
    sys.stdout.write(f"[{color}{level}{Color.NC}]{padding * padding_length}{msg}\n")
    if not msg_details:
        return
    for line in msg_details:
        sys.stdout.write(f"{' ' * (max_padding + 2)}{line}\n")
