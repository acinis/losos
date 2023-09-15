from functools import singledispatchmethod

from losos.helpers import eprint
from losos.token import Token
from losos.tokentype import TokenType


class Reporter:
    def __init__(self) -> None:
        self._had_error = False

    def _report(self, line: int, where: str, message: str) -> None:
        eprint("[line ", line, "] Error", where, ": ", message, sep="")
        self._had_error = True

    def clear(self) -> None:
        self._had_error = False

    def had_error(self) -> bool:
        return self._had_error

    def __bool__(self) -> bool:
        return self._had_error

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
