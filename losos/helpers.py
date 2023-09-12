import sys  # stderr
from typing import Any


class Char(str):
    """Custom type for single character.
    Allows also empty string as equivalent of null character
    (like '\0' in Java, C++ and others).
    """

    def __new__(cls, s: str) -> "Char":
        if len(s) > 1:
            raise ValueError("Only one character or empty string")
        return super(Char, cls).__new__(cls, s)


def eprint(*args: Any, **kwargs: Any) -> None:
    print(*args, file=sys.stderr, **kwargs)


def char_at(string: str, index: int) -> Char:
    try:
        return Char(string[index])
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
