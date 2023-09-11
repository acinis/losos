from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import sys  # version_info
from typing import Final, Generic, TypeVar, Any

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

from losos.token import Token

R = TypeVar("R")


class ExprVisitor(ABC, Generic[R]):
    @abstractmethod
    def visit_binary_expr(self, expr: BinaryExpr) -> R:
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr: GroupingExpr) -> R:
        pass

    @abstractmethod
    def visit_literal_expr(self, expr: LiteralExpr) -> R:
        pass

    @abstractmethod
    def visit_unary_expr(self, expr: UnaryExpr) -> R:
        pass


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: ExprVisitor[R]) -> R:
        pass


# NOTE Assigning `field` descriptor is a workaround for mypy bug, see:
# https://github.com/python/mypy/issues/10688#issuecomment-866039452


@dataclass
class BinaryExpr(Expr):
    left: Final[Expr] = field()
    operator: Final[Token] = field()
    right: Final[Expr] = field()

    @override
    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_binary_expr(self)


@dataclass
class GroupingExpr(Expr):
    expression: Final[Expr] = field()

    @override
    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_grouping_expr(self)


@dataclass
class LiteralExpr(Expr):
    value: Final[Any] = field()

    @override
    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_literal_expr(self)


@dataclass
class UnaryExpr(Expr):
    operator: Final[Token] = field()
    right: Final[Expr] = field()

    @override
    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_unary_expr(self)
