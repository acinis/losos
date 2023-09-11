from dataclasses import dataclass
from typing import Any
import sys  # version_info

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

from losos.tokentype import TokenType


@dataclass
class Token:
    type: TokenType
    lexeme: str
    literal: Any | None
    line: int

    @override
    def __str__(self) -> str:
        return f"{self.type.name} {self.lexeme} {self.literal}"
