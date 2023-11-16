from typing import Final

from losos.token import Token


class LososRuntimeError(Exception):
    def __init__(self, token: Token, message: str) -> None:
        self.token: Final[Token] = token
        self.message: Final[str] = message
