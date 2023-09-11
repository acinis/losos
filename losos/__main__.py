import sys
from losos.losos import Losos


def main(args: list[str]) -> int:
    """Return system exit code. `args` is list of cli arguments."""

    if len(args) > 2:
        print("Usage: losos [script]")
        return 64

    losos: Losos = Losos()
    if len(args) == 2:
        losos.run_file(args[1])
    else:
        losos.run_prompt()

    return 0


try:
    sys.exit(main(sys.argv))

except Exception as e:
    raise
