import numpy as np

from src.sketch import sketch_matches


def _along(expr: str, tol_noise: float = 0.2) -> list[list[float]]:
    import sympy as sp

    x = sp.symbols("x")
    fn = sp.lambdify(x, sp.sympify(expr), modules="numpy")
    xs = np.linspace(-5.0, 5.0, 80)
    ys = np.asarray(fn(xs), dtype=float).reshape(-1) + tol_noise
    keep = np.isfinite(ys) & (np.abs(ys) <= 6)
    return [[float(a), float(b)] for a, b in zip(xs[keep], ys[keep])]


def test_a_line_near_the_curve_passes():
    ok, reason = sketch_matches(_along("x + 1"), "x + 1", tol=0.9)
    assert ok, reason


def test_a_parabola_near_the_curve_passes():
    ok, reason = sketch_matches(_along("x**2 - 2", 0.15), "x**2 - 2", tol=0.95)
    assert ok, reason


def test_a_flat_line_is_not_a_parabola():
    points = [[x, 0.0] for x in np.linspace(-5, 5, 40)]
    ok, _reason = sketch_matches(points, "x**2 - 2", tol=0.95)
    assert not ok


def test_a_shifted_line_fails():
    ok, _reason = sketch_matches(_along("-x + 2"), "x + 1", tol=0.9)
    assert not ok


def test_sine_follows_the_wave():
    ok, reason = sketch_matches(_along("sin(x)", 0.1), "sin(x)", tol=0.7)
    assert ok, reason


def test_a_short_mark_is_not_enough():
    ok, reason = sketch_matches([[0, 1], [1, 2]], "x + 1")
    assert not ok
    assert "short" in reason
