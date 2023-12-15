# Losos

[![Version](https://img.shields.io/badge/version-0.1.4-blue)](https://github.com/acinis/losos/releases)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Mypy strict](https://img.shields.io/badge/mypy-strict-2a6db2)](https://mypy.readthedocs.io/en/stable/)
[![Code style black](https://img.shields.io/badge/code_style-black-black)](https://black.readthedocs.io/en/stable/)

Losos is implementation of [Lox](https://craftinginterpreters.com/) language in [Python 3](https://www.python.org/).

## Goals

- Python implementation should be as close as possible to Java version in book ([see below](#differences))

- [ ] Losos 1.0 - working Python implementation of tree-walk interpreter
- [ ] Losos 1.x - extend Losos so next goals are possible
- [ ] Losos 2.0 - bytecode compiler written in Lox itself
- [ ] Use v1.x to run v2.0 to compile v2.0 source to bytecode
- [ ] Losos VM written in C++

## Differences

- No tool for generating syntax tree classes (tool/GenerateAst.java).
- \[expr.py\] `Visitor` abstract class and all expression classes are not nested inside `Expr`: `BinaryExpr` instead of `Expr.Binary`, `ExprVisitor` instead of `Expr.Visitor`, etc.
- \[parser.py\] `_ParseError` class is not nested inside `Parser` class.
- \[helpers.py\] Whole new file with handy helpers.
- \[losos.py\] `Losos` class is instantiable and all methods are non-static.
- \[losos.py\] `Reporter` instance instead of `_had_error` property (see below).
- \[losos.py\] `main` responsibility is to parse args and call `run_*` methods, so I made them public and moved `main` to `__main__.py`.
- \[losos.py\] `run_prompt` method prints welcome message and will exit after `CTRL+Z` followed by `RETURN`.
- \[losos.py\] `error`, `_report`, `runtimeError`, etc moved to `Reporter` (see below).
- \[reporter.py\] In book, there was `hadError` static boolean flag inside top-level `Lox` class. We have instantiable `Losos` class, and we just cannot call static error method from it. This is minimal error reporter class. It's instance will be passed around, so classes used inside `Losos` (like `Parser` and `Scanner`) can report errors back. Later it may be turned into interface for swapping different error-reporting implementations. For now it's just a way to pass around basic information about encountered errors (just like mentioned flag in book).
- Java's `char` type: I added class `Char` (in `helpers.py`) for type-hinting single character (see [#2](/../../issues/2) for reasoning).
- \[runtimeerror.py\] `RuntimeError` in Losos is named `LososRuntimeError` to avoid name collision with Python's built-in exception.
- Possibly other minor differences.
