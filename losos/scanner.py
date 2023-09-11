from typing import Any, Final

import losos.helpers  # error
from losos.helpers import char_at, to_float
from losos.reporter import Reporter
from losos.token import Token
from losos.tokentype import TokenType


class Scanner:
    _keywords: Final[dict[str, TokenType]] = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source: str, *, reporter: Reporter) -> None:
        self._source: str = source
        self._tokens: list[Token] = []
        self._start: int = 0
        self._current: int = 0
        self._line: int = 1
        self._reporter: Reporter = reporter

    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end():
            self._start = self._current
            self._scan_token()

        self._tokens.append(Token(TokenType.EOF, "", None, self._line))

        return self._tokens

    def _scan_token(self) -> None:
        c: str = self._advance()  # TODO CHAR type of `c`

        if c == "(":
            self._add_token(TokenType.LEFT_PAREN)

        elif c == ")":
            self._add_token(TokenType.RIGHT_PAREN)

        elif c == "{":
            self._add_token(TokenType.LEFT_BRACE)

        elif c == "}":
            self._add_token(TokenType.RIGHT_BRACE)

        elif c == ",":
            self._add_token(TokenType.COMMA)

        elif c == ".":
            self._add_token(TokenType.DOT)

        elif c == "-":
            self._add_token(TokenType.MINUS)

        elif c == "+":
            self._add_token(TokenType.PLUS)

        elif c == ";":
            self._add_token(TokenType.SEMICOLON)

        elif c == "*":
            self._add_token(TokenType.STAR)

        elif c == "!":
            self._add_token(
                TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG
            )

        elif c == "=":
            self._add_token(
                TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL
            )

        elif c == "<":
            self._add_token(
                TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS
            )

        elif c == ">":
            self._add_token(
                TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER
            )

        elif c == "/":
            if self._match("/"):
                while (self._peek() != "\n") and (not self._is_at_end()):
                    self._advance()
            else:
                self._add_token(TokenType.SLASH)

        elif c in [" ", "\r", "\t"]:
            pass

        elif c == "\n":
            self._line += 1

        elif c == '"':
            self._string()

        elif self._is_digit(c):
            self._number()

        elif self._is_alpha(c):
            self._identifier()

        else:
            self._reporter.error(self._line, "Unexpected character.")

    def _identifier(self) -> None:
        while self._is_alphanumeric(self._peek()):
            self._advance()

        text: str = self._source[self._start : self._current]
        type: TokenType = TokenType.IDENTIFIER

        if text in self._keywords:
            type = self._keywords[text]

        self._add_token(type)

    def _number(self) -> None:
        while self._is_digit(self._peek()):
            self._advance()

        if self._peek() == "." and self._is_digit(self._peek_next()):
            self._advance()  # Consume the `.`
            while self._is_digit(self._peek()):
                self._advance()

        self._add_token(
            TokenType.NUMBER, to_float(self._source[self._start : self._current])
        )

    def _string(self) -> None:
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == "\n":
                self._line += 1
            self._advance()

        if self._is_at_end():
            self._reporter.error(self._line, "Unterminated string.")
            return

        self._advance()  # Consume closing `"`

        # Trim the surrounding quotes.
        value: str = self._source[self._start + 1 : self._current - 1]

        self._add_token(TokenType.STRING, value)

    def _match(self, expected: str) -> bool:
        """It's like a conditional advance()
        We only consume the current character if it's what we're looking for
        """
        # TODO CHAR type of `expected`

        if self._is_at_end():
            return False

        if char_at(self._source, self._current) != expected:
            return False

        self._current += 1

        return True

    def _peek(self) -> str:
        """
        ``It's sort of like advance(), but doesn't consume the character.
        This is called lookahead. Since it only looks at the current unconsumed
        character, we have one character of lookahead.``
        """
        # TODO CHAR return type

        if self._is_at_end():
            return ""

        return char_at(self._source, self._current)

    def _peek_next(self) -> str:
        # TODO CHAR return type

        if self._current + 1 >= len(self._source):
            return ""

        return char_at(self._source, self._current + 1)

    def _is_alpha(self, c: str) -> bool:
        # TODO CHAR type of `c`
        return c.isalpha() and c.isascii()  # False for empty str

    def _is_alphanumeric(self, c: str) -> bool:
        # TODO CHAR type of `c`
        return self._is_alpha(c) or self._is_digit(c)

    def _is_digit(self, c: str) -> bool:
        # TODO CHAR type of `c`
        return c.isdigit() and c.isascii()

    def _is_at_end(self) -> bool:
        return self._current >= len(self._source)

    def _advance(self) -> str:
        """Consume next character in the source and return it."""
        # TODO CHAR return type

        current: int = self._current
        self._current += 1
        return char_at(self._source, current)

    def _add_token(self, type: TokenType, literal: Any | None = None) -> None:
        text: str = self._source[self._start : self._current]
        self._tokens.append(Token(type, text, literal, self._line))
