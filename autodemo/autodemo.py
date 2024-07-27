"""Automating demo."""

import argparse
import os
import platform
import shutil
import textwrap
from collections import UserDict
from collections.abc import Iterator
from enum import StrEnum
from pathlib import Path
from pprint import pformat
from typing import Any, TextIO


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

    def reset_updated_keys(self):
        """Reset the set of updated keys."""
        self.updated_keys.clear()


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


def _find_executable_lines(f: TextIO) -> Iterator[str]:
    """Perform a buffered read through the file until we run out of content.

    Args:
        f: File object.

    Yields:
        Each executable line.
    """
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
            line = line.replace("#", f"{Ansi.bright_white}{Ansi.italic}#") + Ansi.reset
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


def _print_local_scope(local_scope: LocalScope[str, Any]):
    """Write the local scope to the console.

    Args:
        local_scope: Local scope dictionary.
        changed: Items that have changed since the last state.
    """
    if local_scope:
        print(
            f"{Ansi.white}{Ansi.dim}{Ansi.underline}{' ' * _get_width()}{Ansi.reset}\n"
            f"{Ansi.bright_blue}Locals{Ansi.reset}"
        )
        for name, value in local_scope.items():
            value_width = _get_width() - len(name) - 3
            value_repr = repr(value)
            value = textwrap.shorten(value_repr, value_width, placeholder="...")
            new_mark = f"{Ansi.bold}*" if name in local_scope.updated_keys else " "
            print(f"{new_mark}{Ansi.red}{name}{Ansi.reset} = {value}")

        local_scope.reset_updated_keys()


# endregion


# region Public functions
def process_file(path: Path):
    """Process a script file, line by line.

    Args:
        script_path: Path of a text file containing lines to execute.
    """
    with path.open(mode="r", encoding="UTF-8") as f:
        local_scope = LocalScope()
        print(
            f"{Ansi.white}{Ansi.italic}Python {platform.python_version()} "
            f"on {platform.platform()}\n"
            f"{Ansi.underline}{Ansi.dim}{' ' * _get_width()}{Ansi.reset}"
        )
        for code in _find_executable_lines(f):
            match code:
                case "# ---":
                    print(
                        f"{Ansi.white}{Ansi.underline}{Ansi.dim}{' ' * _get_width()}{Ansi.reset}"
                    )
                    continue
                case "#":
                    print("")
                    continue
                case _:
                    _print_expression(code)

            if (result := _execute_line(code, local_scope)) is not None:
                print(f"{Ansi.blue}{pformat(result, width=_get_width())}{Ansi.reset}")

            _print_local_scope(local_scope)

            if input(PROMPT).strip().lower() == "q":
                break

            print(
                (
                    Ansi.cursor_up
                    + Ansi.cursor_up * ((len(local_scope) + 2) if local_scope else 0)
                    + Ansi.clear_screen_cursor_to_end
                ),
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
    args = parser.parse_args()

    if args.work_dir:
        args.work_dir = args.work_dir.resolve()
        print(
            f"{Ansi.white}{Ansi.italic}Changing directory to {args.work_dir}{Ansi.reset}"
        )
        os.chdir(args.work_dir)

    process_file(args.file_path)
# endregion
