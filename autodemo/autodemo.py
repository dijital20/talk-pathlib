"""Automating demo."""

# /// script
# requires-python = ">=3.10"
# ///

import argparse
import logging
import os
import platform
import re
import shutil
import textwrap
import time
from collections import UserDict
from collections.abc import Iterator
from enum import StrEnum
from io import StringIO
from pathlib import Path
from pprint import pformat
from typing import Any

LOG = logging.getLogger(__name__)


# region Enumerations, Constants and Utility classes
class Ansi(StrEnum):
    """Ansi escape sequences for controlling terminal output."""

    # Text colors
    black = "\u001b[30m"
    red = "\u001b[31m"
    green = "\u001b[32m"
    yellow = "\u001b[33m"
    blue = "\u001b[34m"
    magenta = "\u001b[35m"
    cyan = "\u001b[36m"
    white = "\u001b[37m"
    bright_black = "\u001b[30;1m"
    bright_red = "\u001b[31;1m"
    bright_green = "\u001b[32;1m"
    bright_yellow = "\u001b[33;1m"
    bright_blue = "\u001b[34;1m"
    bright_magenta = "\u001b[35;1m"
    bright_cyan = "\u001b[36;1m"
    bright_white = "\u001b[37;1m"
    # Background colors
    back_black = "\u001b[40m"
    back_red = "\u001b[41m"
    back_green = "\u001b[42m"
    back_yellow = "\u001b[43m"
    back_blue = "\u001b[44m"
    back_magenta = "\u001b[45m"
    back_cyan = "\u001b[46m"
    back_white = "\u001b[47m"
    back_bright_black = "\u001b[40;1m"
    back_bright_red = "\u001b[41;1m"
    back_bright_green = "\u001b[42;1m"
    back_bright_yellow = "\u001b[43;1m"
    back_bright_blue = "\u001b[44;1m"
    back_bright_magenta = "\u001b[45;1m"
    back_bright_cyan = "\u001b[46;1m"
    back_bright_white = "\u001b[47;1m"
    # Text styling
    reset = "\u001b[0m"
    bold = "\u001b[1m"
    dim = "\u001b[2m"
    italic = "\u001b[3m"
    underline = "\u001b[4m"
    slow_blink = "\u001b[5m"
    fast_blink = "\u001b[6m"
    reversed = "\u001b[7m"
    hide = "\u001b[8m"
    strikethrough = "\u001b[9m"
    # Cursor operations
    cursor_up = "\u001b[1A"
    cursor_down = "\u001b[1B"
    cursor_right = "\u001b[1C"
    cursor_left = "\u001b[1D"
    cursor_pos_save = "\u001b[s"
    cursor_pos_restore = "\u001b[u"
    # Clear operations
    clear_screen_cursor_to_end = "\u001b[0J"
    clear_screen_cursor_to_begin = "\u001b[1J"
    clear_screen = "\u001b[2J"
    clear_line_cursor_to_begin = "\u001b[0K"
    clear_line_cursor_to_end = "\u001b[1K"
    clear_line = "\u001b[2K"


PROMPT = f"{Ansi.green}(q for quit, any other value to continue):{Ansi.reset} "


class LocalScope(UserDict):
    """Variant of a dictionary that tracks which keys have been set/modified.

    Attributes:
        updated_keys: Set of keys that have been updated.
    """

    def __init__(self, *args, **kwargs):
        """Prepare a LocalScope for use."""
        super().__init__(*args, **kwargs)
        self.updated_keys = set()

    def __setitem__(self, key: Any, item: Any) -> None:
        """Log when we update an item."""
        self.updated_keys.add(key)
        return super().__setitem__(key, item)

    def clear(self):
        LOG.debug("Clearing local scope")
        return super().clear()


# endregion


# region Private functions
def _get_width() -> int:
    """Get the terminal width."""
    return shutil.get_terminal_size()[0]


def _canonical_path(val: str) -> Path:
    """Convert string path into a canonical path object.

    Args:
        val: Input value as a string.

    Returns:
        A canonical Path object.
    """
    return Path(val).resolve()


def get_content(path: Path) -> StringIO:
    """Get the content from the file into a StringIO object.

    Args:
        path: Path of the file.

    Returns:
        StringIO object to read from.

    Notes:
        For markdown, read all of the lines inside `python` or `py` code fences.
        For all other files, read the file in whole.
    """
    match path.suffix:
        case ".md":
            LOG.debug("Loading markdown %s", path)
            # Extract code fences
            return StringIO(
                "\n# --- \n".join(
                    t.strip()
                    for t in re.findall(
                        r"(?:```(?:python|py)(.*?)```)",
                        path.read_text(encoding="UTF-8"),
                        flags=re.DOTALL,
                    )
                )
            )

        case _:
            LOG.debug("Loading text %s", path)
            # Just return the whole file
            return StringIO(path.read_text(encoding="UTF-8"))


def _find_executable_lines(path: Path) -> Iterator[str]:
    """Perform a buffered read through the file until we run out of content.

    Args:
        path: File path.

    Yields:
        Each executable line.
    """
    with get_content(path) as f:
        buffer = f.read(1)
        while True:
            # Handle EOF
            if not (char := f.read(1)):
                yield buffer.strip()
                break

            buffer += char
            if buffer[-2] == "\n" and buffer[-1] not in " \t\n\r":
                yield buffer[:-1].strip()
                buffer = buffer[-1]


def _print_expression(expression: str):
    """Write the expression to the console.

    Args:
        expression: Expression to write.
    """
    for idx, line in enumerate(expression.split("\n")):
        prompt = (
            f"{Ansi.bright_magenta}>>>{Ansi.reset}"
            if idx == 0
            else f"{Ansi.bright_magenta}...{Ansi.reset}"
        )
        if "#" in line:
            line = line.replace("#", f"{Ansi.dim}{Ansi.italic}#") + Ansi.reset
        print(f"{prompt} {line}")


def _execute_line(code: str, local_scope: dict[str, Any]) -> Any:
    """Execute code.

    Args:
        code: Code to execute.
        local_scope: Dictionary to use for local scope.

    Returns:
        Return value of the operation.
    """
    # Try to compile this as an eval expression
    try:
        code = compile(code, "<string>", "eval")

    # Whoops, wasn't an expression, just exec it.
    except SyntaxError:
        try:
            exec(code, globals(), local_scope)
        except Exception as e:
            print(f"{Ansi.red}{type(e).__name__}: {e}{Ansi.reset}")

    # Ah HA!, we have an expression!
    else:
        try:
            return eval(code, globals(), local_scope)
        except Exception as e:
            print(f"{Ansi.red}{type(e).__name__}: {e}{Ansi.reset}")


def _print_local_scope(local_scope: LocalScope[str, Any]) -> int:
    """Write the local scope to the console.

    Args:
        local_scope: Local scope dictionary.
        changed: Items that have changed since the last state.

    Returns:
        Number of lines written.
    """
    LOG.debug("Printing local scope with %d items", len(local_scope))
    lines = 0
    if local_scope:
        print(
            f"{Ansi.white}{Ansi.dim}{Ansi.underline}{' ' * _get_width()}{Ansi.reset}\n"
            f"{Ansi.bright_blue}Locals{Ansi.reset}"
        )
        width = _get_width()
        lines += 2
        for name, value in local_scope.items():
            value_width = width - len(name) - 3
            value = textwrap.shorten(repr(value), value_width, placeholder="...")
            new_mark = f"{Ansi.bold}*" if name in local_scope.updated_keys else " "
            print(f"{new_mark}{Ansi.red}{name}{Ansi.reset} = {value}")
            lines += 1

        local_scope.updated_keys.clear()
    return lines


# endregion


# region Public functions
def process_file(path: Path, timer: float | None = None):
    """Process a script file, line by line.

    Args:
        script_path: Path of a text file containing lines to execute.
        timer: Advance on this timer instead of input. Defaults to None.
    """

    local_scope = LocalScope()
    print(
        f"{Ansi.white}{Ansi.italic}Python {platform.python_version()} "
        f"on {platform.platform()}\n"
        f"{Ansi.underline}{Ansi.dim}{' ' * _get_width()}{Ansi.reset}"
    )
    for code in _find_executable_lines(path):
        LOG.debug("Line: %r", code)

        match code:
            case "# ^^^ clear ^^^":  # Clear locals without a line
                local_scope.clear()
                continue

            case "# --- clear ---":  # Clear locals with a line
                local_scope.clear()
                print(
                    f"{Ansi.white}{Ansi.underline}{Ansi.dim}{' ' * _get_width()}{Ansi.reset}"
                )
                continue

            case "# ---":  # Line, keep locals
                print(
                    f"{Ansi.white}{Ansi.underline}{Ansi.dim}{' ' * _get_width()}{Ansi.reset}"
                )
                continue

            case "#":  # Empty comment
                print("")
                continue

            case _:  # Code!!
                _print_expression(code)

        if (result := _execute_line(code, local_scope)) is not None:
            print(f"{Ansi.blue}{pformat(result, width=_get_width())}{Ansi.reset}")

        cursor_up = _print_local_scope(local_scope)

        # Wait for advancement
        if timer is not None:
            time.sleep(timer)
        else:
            cursor_up += 1
            if input(PROMPT).strip().lower() == "q":
                break

        # Clear local scope and update.
        LOG.debug("Cursoring up %d lines and clearing", cursor_up)
        print(
            (Ansi.cursor_up * (cursor_up) + Ansi.clear_screen_cursor_to_end),
            end="",
        )
    else:  # No break
        _print_local_scope(local_scope)


# endregion

# region Main block
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute steps in a file.")
    parser.add_argument(
        "file_path",
        type=_canonical_path,
        help="Path to execute.",
    )
    parser.add_argument(
        "--work-dir",
        "-w",
        type=_canonical_path,
        help="Working directory.",
    )
    parser.add_argument(
        "--timer",
        "-t",
        type=float,
        help="Advance on this interval rather than taking input.",
    )
    parser.add_argument(
        "--log-path",
        "-l",
        type=_canonical_path,
        help="Path to save the log to. If provided, logging will be done at DEBUG level.",
    )
    args = parser.parse_args()

    if args.log_path:
        logging.basicConfig(level=logging.DEBUG, filename=args.log_path, filemode="w")

    if args.work_dir:
        args.work_dir = args.work_dir.resolve()
        print(
            f"{Ansi.white}{Ansi.italic}Changing directory to {args.work_dir}{Ansi.reset}"
        )
        os.chdir(args.work_dir)

    process_file(args.file_path, args.timer)
# endregion
