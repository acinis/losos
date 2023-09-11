import sys  # stderr
from typing import Any


def eprint(*args: Any, **kwargs: Any) -> None:
    print(*args, file=sys.stderr, **kwargs)


def char_at(string: str, index: int) -> str:
    # TODO CHAR return type
    try:
        return string[index]
    except IndexError as e:
        raise
        # `char_at` is used like in book - always when index is valid.


def to_float(s: str) -> float:
    try:
        return float(s)
    except ValueError as e:
        raise
    except OverflowError as e:
        # TODO And what now? Underlying limitation...
        raise
