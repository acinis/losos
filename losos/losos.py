from typing import cast
import sys

from losos.astprinter import AstPrinter
from losos.expr import Expr
from losos.helpers import eprint
from losos.parser import Parser
from losos.reporter import Reporter
from losos.scanner import Scanner
from losos.token import Token


class Losos:
    def __init__(self) -> None:
        self._reporter: Reporter = Reporter()

    def run_file(self, path: str) -> None:
        content: str = ""
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except OSError as e:
            raise  # TODO
        except ValueError as e:  # encoding error
            raise  # TODO

        self._run(content)

        if self._reporter:
            sys.exit(65)

    def run_prompt(self) -> None:
        print("Use exit() or Ctrl-Z plus Return to exit\n")

        while True:
            try:
                line: str = input("> ")
            except KeyboardInterrupt:
                print("\nKeyboard Interrupt")
                break
            except EOFError:
                print("EOF")
                break

            self._run(line)

            # ``We need to reset this flag in the interactive loop. If the user makes a mistake, it shouldn't kill their entire session.``
            self._reporter.clear()

    def _run(self, source: str) -> None:
        scanner = Scanner(source, reporter=self._reporter)
        tokens: list[Token] = scanner.scan_tokens()

        parser: Parser = Parser(tokens, reporter=self._reporter)
        expression: Expr | None = parser.parse()

        # Stop if there was a syntax error.
        if self._reporter:
            return

        expression = cast(Expr, expression)
        print(AstPrinter().print(expression))