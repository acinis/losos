import sys  # version_info
from typing import Any

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

from losos.expr import *
from losos.reporter import Reporter
from losos.runtimeerror import LososRuntimeError
from losos.token import Token
from losos.tokentype import TokenType


class Interpreter(ExprVisitor[Any]):
    def __init__(self, *, reporter: Reporter) -> None:
        self._reporter: Reporter = reporter

    def interpret(self, expression: Expr) -> None:
        try:
            value: Any = self._evaluate(expression)
            print(self._stringify(value))
        except LososRuntimeError as error:
            self._reporter.runtime_error(error)

    @override
    def visit_literal_expr(self, expr: LiteralExpr) -> Any:
        return expr.value

    @override
    def visit_unary_expr(self, expr: UnaryExpr) -> Any:
        right: Any = self._evaluate(expr.right)

        if expr.operator.type == TokenType.BANG:
            return not self._is_truthy(right)
        elif expr.operator.type == TokenType.MINUS:
            self._check_number_operand(expr.operator, right)
            return -float(right)

        # Unreachable
        return None

    def _check_number_operand(self, operator: Token, operand: Any) -> None:
        if type(operand) is float:
            return
        raise LososRuntimeError(operator, "Operand must be a number.")

    def _check_number_operands(self, operator: Token, left: Any, right: Any) -> None:
        if (type(left) is float) and (type(right) is float):
            return
        raise LososRuntimeError(operator, "Operands must be numbers.")

    # ``false and nil are falsey, and everything else is truthy``
    def _is_truthy(self, obj: Any) -> bool:
        if obj is None:
            return False
        if type(obj) is bool:
            return bool(obj)
        return True

    def _is_equal(self, a: Any, b: Any) -> bool:
        if a is None and b is None:
            return True
        if a is None:
            return False
        return bool(a == b)

    def _stringify(self, obj: Any) -> str:
        if obj is None:
            return "nil"

        if type(obj) is float:
            text: str = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text

        return str(obj)

    @override
    def visit_grouping_expr(self, expr: GroupingExpr) -> Any:
        return self._evaluate(expr.expression)

    def _evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)

    @override
    def visit_binary_expr(self, expr: BinaryExpr) -> Any:
        left: Any = self._evaluate(expr.left)
        right: Any = self._evaluate(expr.right)

        if expr.operator.type == TokenType.GREATER:
            self._check_number_operands(expr.operator, left, right)
            return float(left) > float(right)

        elif expr.operator.type == TokenType.GREATER_EQUAL:
            self._check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)

        elif expr.operator.type == TokenType.LESS:
            self._check_number_operands(expr.operator, left, right)
            return float(left) < float(right)

        elif expr.operator.type == TokenType.LESS_EQUAL:
            self._check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)

        elif expr.operator.type == TokenType.MINUS:
            self._check_number_operands(expr.operator, left, right)
            return float(left) - float(right)

        elif expr.operator.type == TokenType.PLUS:
            if (type(left) is float) and (type(right) is float):
                return left + right

            if (type(left) is str) and (type(right) is str):
                return left + right

            raise LososRuntimeError(
                expr.operator, "Operands must be two numbers or two strings."
            )

        elif expr.operator.type == TokenType.SLASH:
            self._check_number_operands(expr.operator, left, right)
            return float(left) / float(right)

        elif expr.operator.type == TokenType.STAR:
            self._check_number_operands(expr.operator, left, right)
            return float(left) * float(right)

        elif expr.operator.type == TokenType.BANG_EQUAL:
            return not self._is_equal(left, right)

        elif expr.operator.type == TokenType.EQUAL_EQUAL:
            return self._is_equal(left, right)

        # Unreachable
        return None
