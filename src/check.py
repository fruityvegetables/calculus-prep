from __future__ import annotations

import re

from sympy import Eq, N, simplify, sympify
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application,)


def _parse(expr: str):
    cleaned = expr.strip()
    cleaned = cleaned.replace("^", "**")
    cleaned = cleaned.replace("√", "sqrt")
    cleaned = cleaned.replace("π", "pi")
    return parse_expr(cleaned, transformations=TRANSFORMATIONS, evaluate=True)


def _split_solutions(text: str) -> list[str]:
    text = text.strip()
    text = text.strip("{}[]()")
    text = re.sub(r"x\s*=\s*", "", text, flags=re.I)
    parts = re.split(r"\s*(?:,|;|or|and)\s*", text)
    return [p for p in parts if p]


def answers_match(student: str, correct: str) -> bool:
    """Return True if student and correct represent the same math object."""
    if student is None:
        return False
    s_raw = student.strip()
    c_raw = str(correct).strip()
    if not s_raw:
        return False
    if s_raw.lower() == c_raw.lower():
        return True

    s_compact = re.sub(r"\s+", "", s_raw.lower())
    c_compact = re.sub(r"\s+", "", c_raw.lower())
    if s_compact == c_compact:
        return True

    s_parts = _split_solutions(s_raw)
    c_parts = _split_solutions(c_raw)
    if len(s_parts) > 1 or len(c_parts) > 1:
        try:
            s_vals = sorted((_parse(p) for p in s_parts), key=lambda v: str(v))
            c_vals = sorted((_parse(p) for p in c_parts), key=lambda v: str(v))
            if len(s_vals) != len(c_vals):
                return False
            return all(simplify(a - b) == 0 for a, b in zip(s_vals, c_vals))
        except Exception:
            return False

    try:
        s_expr = _parse(s_raw)
        c_expr = _parse(c_raw)
        if s_expr == c_expr:
            return True
        if simplify(s_expr - c_expr) == 0:
            return True
        if Eq(s_expr, c_expr) is True:
            return True
        try:
            if abs(complex(N(s_expr)) - complex(N(c_expr))) < 1e-6:
                return True
        except Exception:
            pass
    except Exception:
        try:
            return simplify(sympify(s_raw) - sympify(c_raw)) == 0
        except Exception:
            return False
    return False
