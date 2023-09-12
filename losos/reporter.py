from functools import singledispatchmethod
from typing import Iterator

from losos.helpers import eprint
from losos.token import Token
from losos.tokentype import TokenType


class Reporter:
    def __init__(self) -> None:
        self._messages: list[str] = []

    def _report(self, line: int, where: str, message: str) -> None:
        full_message: str = f"[line {line}] Error{where}: {message}"
        self._messages.append(full_message)
        eprint(full_message)

    def clear(self) -> None:
        self._messages = []

    def __iter__(self) -> Iterator[str]:
        return iter(self._messages)

    def __bool__(self) -> bool:
        return bool(self._messages)

    def __len__(self) -> int:
        return len(self._messages)

    # singledispatchmethod cos it's a way priettier than overload
    @singledispatchmethod
    def error(self, arg: object, message: str) -> None:
        raise NotImplementedError(
            "INTERNAL_ERROR: Reporter.error(): Unknown argument type(s)"
        )
        # From docs: original function is used if no better implementation is found.
        # So throw internal error here, cos it just mean that bug is somewhere.
        # Do not rely on catch all behaviour.

    @error.register
    def _(self, line: int, message: str) -> None:
        self._report(line, "", message)

    @error.register
    def _(self, token: Token, message: str) -> None:
        if token.type == TokenType.EOF:
            self._report(token.line, " at end", message)
        else:
            self._report(token.line, " at '" + token.lexeme + "'", message)
