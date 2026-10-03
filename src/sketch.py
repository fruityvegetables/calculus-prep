"""Sketch-the-graph problems. The drawing is the answer."""

from __future__ import annotations

import random

import numpy as np
import sympy as sp

from src.schema import make_problem, steps

_X = sp.symbols("x")
WINDOW = 6.0


def _curve(expr: str):
    return sp.lambdify(_X, sp.sympify(expr), modules="numpy")


def sketch_matches(points, expr: str, tol: float = 0.9) -> tuple[bool, str]:
    """True when the ink follows y = expr across the window."""
    try:
        pts = np.asarray(points, dtype=float)
    except (TypeError, ValueError):
        return False, "Draw the curve on the grid, then check the sketch."
    if pts.ndim != 2 or pts.shape[1] != 2 or pts.shape[0] < 12:
        return False, "Draw more of the curve. A short mark is not enough."

    xs, ys = pts[:, 0], pts[:, 1]
    inside = (np.abs(xs) <= WINDOW) & (np.abs(ys) <= WINDOW) & np.isfinite(xs) & np.isfinite(ys)
    xs, ys = xs[inside], ys[inside]
    if xs.size < 12:
        return False, "Draw the curve inside the window."

    fn = _curve(expr)
    with np.errstate(all="ignore"):
        target = np.asarray(fn(xs), dtype=float).reshape(-1)
    if target.shape != xs.shape:
        return False, "Draw the curve on the grid, then check the sketch."

    on_axis = (np.abs(xs) <= 0.28) | (np.abs(ys) <= 0.28)
    keep = ~on_axis | (np.isfinite(target) & (np.abs(target) <= tol))
    xs, ys, target = xs[keep], ys[keep], target[keep]
    if xs.size < 12:
        return False, "Draw the curve, not only the axes."

    close = np.isfinite(target) & (np.abs(ys - target) <= tol)
    if float(close.mean()) < 0.68:
        return False, "Too much of the ink misses the curve. Stay within about one grid square."

    sample_x = np.linspace(-5.2, 5.2, 14)
    with np.errstate(all="ignore"):
        sample_y = np.asarray(fn(sample_x), dtype=float).reshape(-1)
    visible = np.isfinite(sample_y) & (np.abs(sample_y) <= 5.4)
    if int(visible.sum()) < 3:
        return False, "Draw the curve across the window, not just one piece."
    hits = 0
    for x0, y0 in zip(sample_x[visible], sample_y[visible]):
        near = np.abs(xs - x0) <= 0.95
        if np.any(near) and float(np.min(np.abs(ys[near] - y0))) <= tol:
            hits += 1
    if hits / int(visible.sum()) < 0.55:
        return False, "Draw the curve across the window, not just one piece."
    return True, ""


def sketch_figure(expr: str):
    import matplotlib.pyplot as plt

    fn = _curve(expr)
    grid = np.linspace(-WINDOW, WINDOW, 500)
    with np.errstate(all="ignore"):
        values = np.asarray(fn(grid), dtype=float).reshape(-1)
    values = np.where(np.isfinite(values) & (np.abs(values) <= WINDOW + 1.5), values, np.nan)
    fig, ax = plt.subplots(figsize=(4.4, 4.4))
    ax.set_xlim(-WINDOW, WINDOW)
    ax.set_ylim(-WINDOW, WINDOW)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks(range(-6, 7, 2))
    ax.set_yticks(range(-6, 7, 2))
    ax.grid(True, color="#e2e8f0")
    ax.axhline(0, color="#64748b", lw=1)
    ax.axvline(0, color="#64748b", lw=1)
    ax.plot(grid, values, color="#e11d48", lw=2.2)
    ax.set_title("The curve you were sketching")
    fig.tight_layout()
    return fig


def _prompt(display: str) -> str:
    return (
        f"Sketch {display} on the grid. "
        "Each square is 1. Draw the part of the graph that fits in the window."
    )


def _line_problem(item: dict, skill_id: str, rng: random.Random):
    m, b = item["m"], item["b"]
    down = "down" if m < 0 else "up"
    squares = abs(m)
    unit = "square" if squares == 1 else "squares"
    start = "the origin" if b == 0 else f"(0, {b})"
    return make_problem(
        id=f"{skill_id}-sketch-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=_prompt(item["display"]),
        answer=item["expr"],
        answer_display=item["display"],
        hint=f"Cross the y-axis at {start}. Slope {m} means 1 right and {squares} {down}.",
        common_mistakes=[
            "Using the slope as the intercept.",
            "Moving up when the slope is negative.",
        ],
        exam_tags=["clep_algebra"],
        source="generated",
        cluster="functions",
        plot="sketch",
        plot_data={"expr": item["expr"], "tol": item["tol"]},
        steps=steps(
            (
                "Goal",
                f"Sketch {item['display']} from the left side of the window to the right side.",
            ),
            (
                "Intercept",
                f"When x is 0, y is {b}. Put a point at {start} before you draw the slant.",
            ),
            (
                "Slope",
                f"From that point, go 1 square right and {squares} {unit} {down}. Repeat that step.",
            ),
            (
                "Straight",
                "A line does not bend. Extend the same slant until it leaves the window.",
            ),
        ),
    )


def _parabola_problem(item: dict, skill_id: str, rng: random.Random):
    h, k = item["h"], item["k"]
    return make_problem(
        id=f"{skill_id}-sketch-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=_prompt(item["display"]),
        answer=item["expr"],
        answer_display=item["display"],
        hint=f"The vertex is ({h}, {k}). One square left or right of it, the graph is 1 higher.",
        common_mistakes=[
            "Putting the vertex on the origin when it has moved.",
            "Drawing a V instead of a U.",
        ],
        exam_tags=["clep_algebra"],
        source="generated",
        cluster="functions",
        plot="sketch",
        plot_data={"expr": item["expr"], "tol": item["tol"]},
        steps=steps(
            (
                "Goal",
                f"Sketch the parabola {item['display']}. Only the part inside the window needs to be drawn.",
            ),
            (
                "Vertex",
                f"The lowest point is ({h}, {k}). Mark that before the arms.",
            ),
            (
                "Nearby points",
                f"One square left or right of x = {h}, y is {k + 1}. Two squares away, y is {k + 4}.",
            ),
            (
                "Shape",
                "Connect those points with a symmetric U. Both arms open upward and get steeper.",
            ),
        ),
    )


def _abs_problem(item: dict, skill_id: str, rng: random.Random):
    h, k, a = item["h"], item["k"], item["a"]
    opening = "down" if a < 0 else "up"
    return make_problem(
        id=f"{skill_id}-sketch-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=_prompt(item["display"]),
        answer=item["expr"],
        answer_display=item["display"],
        hint=f"The corner is ({h}, {k}), and the V opens {opening}.",
        common_mistakes=[
            "Rounding the corner into a parabola.",
            "Opening the V the wrong direction.",
        ],
        exam_tags=["clep_algebra"],
        source="generated",
        cluster="functions",
        plot="sketch",
        plot_data={"expr": item["expr"], "tol": item["tol"]},
        steps=steps(
            (
                "Goal",
                f"Sketch {item['display']}. Absolute value graphs are straight arms with a sharp corner.",
            ),
            (
                "Corner",
                f"The corner is the point ({h}, {k}). Everything else is measured from there.",
            ),
            (
                "Arms",
                f"Each arm changes height by 1 square for each square of x. This V opens {opening}.",
            ),
            (
                "Sharp",
                "Do not round the corner. The two arms meet at a point and then run straight.",
            ),
        ),
    )


def _sine_problem(item: dict, skill_id: str, rng: random.Random):
    return make_problem(
        id=f"{skill_id}-sketch-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=_prompt(item["display"]),
        answer=item["expr"],
        answer_display=item["display"],
        hint="It passes through the origin, tops out at 1, and bottoms at -1. One full wave is about 6.3 squares wide.",
        common_mistakes=[
            "Drawing a straight line through the origin.",
            "Letting the wave climb past y = 1.",
        ],
        exam_tags=["clep_precalc"],
        source="generated",
        cluster="functions",
        plot="sketch",
        plot_data={"expr": item["expr"], "tol": item["tol"]},
        steps=steps(
            (
                "Goal",
                "Sketch y = sin x. On this grid, x is in radians and each square is 1.",
            ),
            (
                "Anchors",
                "The wave crosses the origin. It is about 1 at x = 1.6 and back to 0 near x = 3.1.",
            ),
            (
                "Other side",
                "Left of the origin it falls to about -1 near x = -1.6, then returns toward 0 near x = -3.1.",
            ),
            (
                "Smooth",
                "Draw a smooth wave between those heights. It never goes above 1 or below -1.",
            ),
        ),
    )


_BANK = [
    {"kind": "line", "m": 1, "b": 1, "expr": "x + 1", "display": r"$y = x + 1$", "tol": 0.9},
    {"kind": "line", "m": -1, "b": 2, "expr": "-x + 2", "display": r"$y = -x + 2$", "tol": 0.9},
    {"kind": "line", "m": 2, "b": -1, "expr": "2*x - 1", "display": r"$y = 2x - 1$", "tol": 1.05},
    {"kind": "parabola", "h": 0, "k": -2, "expr": "x**2 - 2", "display": r"$y = x^2 - 2$", "tol": 0.95},
    {"kind": "parabola", "h": 2, "k": 0, "expr": "(x - 2)**2", "display": r"$y = (x - 2)^2$", "tol": 0.95},
    {"kind": "parabola", "h": -1, "k": 1, "expr": "(x + 1)**2 + 1", "display": r"$y = (x + 1)^2 + 1$", "tol": 0.95},
    {"kind": "abs", "h": 0, "k": -1, "a": 1, "expr": "Abs(x) - 1", "display": r"$y = |x| - 1$", "tol": 0.9},
    {"kind": "abs", "h": 1, "k": 3, "a": -1, "expr": "-Abs(x - 1) + 3", "display": r"$y = -|x - 1| + 3$", "tol": 0.95},
    {"kind": "sine", "expr": "sin(x)", "display": r"$y = \sin x$", "tol": 0.7},
]


def sketch_graph(rng: random.Random, skill_id: str):
    item = rng.choice(_BANK)
    kind = item["kind"]
    if kind == "line":
        return _line_problem(item, skill_id, rng)
    if kind == "parabola":
        return _parabola_problem(item, skill_id, rng)
    if kind == "abs":
        return _abs_problem(item, skill_id, rng)
    return _sine_problem(item, skill_id, rng)
