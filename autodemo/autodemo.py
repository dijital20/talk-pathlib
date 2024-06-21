import argparse
import os
import shutil
import traceback as tb
from pathlib import Path


def _canonical_path(val: str) -> Path:
    """Convert string path into a canonical path object."""
    return Path(val).resolve()


def _get_width() -> int:
    """Get the width of the terminal."""
    return shutil.get_terminal_size()[0]


def process_file(__path: Path):
    """Process a script file, line by line.

    Args:
        script_path: Path of a text file containing lines to execute.
    """
    with __path.open(mode="r", encoding="UTF-8") as __f:
        __locals = {}
        for __idx, __expression in enumerate(__f, start=1):
            print(f"[{__idx:>3}] >>> {__expression.rstrip()}")

            try:
                __result = eval(__expression, globals(), __locals)
            except SyntaxError:
                exec(__expression, globals(), __locals)
            except Exception as e:
                tb.print_exception(e)
            else:
                if __result:
                    print(f"{__result!r}")

            if __locals:
                print(
                    "\nLocals:\n"
                    f"{"\n".join(f"  {k} = {v!r}" for k, v in __locals.items())}",
                )

            if (
                input("(q for quit, any other key to continue): ").strip().lower()
                == "q"
            ):
                break

            print(f'\033[A\r{' ' * _get_width()}\r')


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
        print(f"Changing directory to {args.work_dir}")
        os.chdir(args.work_dir)

    process_file(args.file_path)
