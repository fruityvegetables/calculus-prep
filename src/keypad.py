"""Insert calculator keys into an answer string."""

from __future__ import annotations

import re
from typing import NamedTuple

_UNARY_BEFORE = set("+-*/^(,")
_INSIDE = set("0123456789.x") | {"pi"}
_OPERATORS = set("+-*/^,<>( )")
_FUNCTIONS = ("sqrt", "sin", "cos", "tan")
_NUMBER_OR_NAME = re.compile(r"(-?(?:\d+(?:\.\d*)?|\.\d+|[A-Za-z]\w*))$")


class KeypadEdit(NamedTuple):
    text: str
    fill: bool


def apply_key(text: str, token: str, *, fill: bool = False) -> KeypadEdit:
    """Apply one keypad token.

    ``fill`` is true while the next digits, decimal point, ``x``, or ``pi``
    should land inside a trailing ``()``.
    """
    current = text or ""
    if token == "backspace":
        return _backspace(current, fill)
    if token in _FUNCTIONS:
        return _apply_function(current, token)
    if token in _INSIDE and fill and current.endswith(")"):
        return KeypadEdit(current[:-1] + token + ")", True)
    if token == ")" and fill and current.endswith(")"):
        return KeypadEdit(current, False)
    if token in _OPERATORS or token in _INSIDE:
        return KeypadEdit(current + token, False)
    return KeypadEdit(current, fill)


def _backspace(text: str, fill: bool) -> KeypadEdit:
    if not text:
        return KeypadEdit("", False)
    if fill and text.endswith(")") and len(text) >= 2:
        if text[-2] != "(":
            return KeypadEdit(text[:-2] + ")", True)
        return KeypadEdit(text[:-1], False)
    return KeypadEdit(text[:-1], False)


def _apply_function(text: str, name: str) -> KeypadEdit:
    span = _wrap_span(text)
    if span is None:
        return KeypadEdit(f"{text}{name}()", True)
    start, end = span
    return KeypadEdit(f"{text[:start]}{name}({text[start:end]}){text[end:]}", False)


def _wrap_span(text: str) -> tuple[int, int] | None:
    if not text:
        return None
    if text.endswith(")"):
        span = _paren_group(text)
        if span is None:
            return None
        start, end = span
        if text[start:end] == "()":
            return None
        return _with_unary_minus(text, start, end)
    match = _NUMBER_OR_NAME.search(text)
    if match is None:
        return None
    return _with_unary_minus(text, match.start(1), match.end(1))


def _paren_group(text: str) -> tuple[int, int] | None:
    depth = 0
    for index in range(len(text) - 1, -1, -1):
        char = text[index]
        if char == ")":
            depth += 1
        elif char == "(":
            depth -= 1
            if depth == 0:
                return index, len(text)
    return None


def _with_unary_minus(text: str, start: int, end: int) -> tuple[int, int] | None:
    if start < end and text[start] == "-":
        if start > 0 and text[start - 1] not in _UNARY_BEFORE:
            start += 1
    elif (
        start > 0
        and text[start - 1] == "-"
        and (start == 1 or text[start - 2] in _UNARY_BEFORE)
    ):
        start -= 1
    if start >= end or text[start:end] in {"-", "()"}:
        return None
    return start, end
