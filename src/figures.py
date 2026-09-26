from __future__ import annotations

from typing import Any

import matplotlib

try:
    matplotlib.use("Agg")
except Exception:
    pass
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

BLUE = "#1d4ed8"
RED = "#dc2626"
GREEN = "#059669"
ORANGE = "#ea580c"
PURPLE = "#7c3aed"
SLATE = "#64748b"
INK = "#0f172a"


def _fig(w: float = 6.4, h: float = 4.3):
    fig, ax = plt.subplots(figsize=(w, h), facecolor="white")
    ax.set_facecolor("#fbfcfe")
    fig.tight_layout(pad=0.6)
    return fig, ax


def _axes(ax, title: str = "", equal: bool = False) -> None:
    ax.axhline(0, color="#94a3b8", lw=0.9, zorder=1)
    ax.axvline(0, color="#94a3b8", lw=0.9, zorder=1)
    ax.grid(True, alpha=0.28)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    if title:
        ax.set_title(title, fontsize=11, color=INK, pad=8)
    if equal:
        ax.set_aspect("equal", adjustable="datalim")


def _arrow(ax, x, y, dx, dy, color=RED, text: str | None = None) -> None:
    ax.annotate(
        "",
        xy=(x + dx, y + dy),
        xytext=(x, y),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=2),
        zorder=5,
    )
    if text:
        ax.text(
            x + dx * 0.55 + 0.08,
            y + dy * 0.55 + 0.08,
            text,
            color=color,
            fontsize=10,
            fontweight="600",
        )


def fig_number_line(d: dict[str, Any]):
    edge = float(d.get("edge", 0))
    greater = bool(d.get("greater", True))
    fig, ax = _fig(6.4, 2.4)
    ax.set_xlim(edge - 6, edge + 6)
    ax.set_ylim(-1.2, 1.4)
    ax.axhline(0, color=SLATE, lw=1.4)
    for x in range(int(edge - 5), int(edge + 6)):
        ax.plot([x, x], [-0.12, 0.12], color=SLATE, lw=1)
        ax.text(x, -0.45, str(x), ha="center", fontsize=9, color=INK)
    if greater:
        ax.annotate(
            "",
            xy=(edge + 5.4, 0),
            xytext=(edge, 0),
            arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=3),
        )
        ax.plot(edge, 0, "o", ms=10, color="white", markeredgecolor=BLUE, markeredgewidth=2, zorder=6)
    else:
        ax.annotate(
            "",
            xy=(edge - 5.4, 0),
            xytext=(edge, 0),
            arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=3),
        )
        ax.plot(edge, 0, "o", ms=10, color="white", markeredgecolor=BLUE, markeredgewidth=2, zorder=6)
    ax.set_title(d.get("title", "Solution on the number line"), fontsize=11)
    ax.axis("off")
    return fig


def fig_two_points(d: dict[str, Any]):
    x1, y1, x2, y2 = map(float, (d["x1"], d["y1"], d["x2"], d["y2"]))
    fig, ax = _fig()
    _axes(ax, d.get("title", "Points in the plane"), equal=True)
    if d.get("segment", True):
        ax.plot([x1, x2], [y1, y2], color=BLUE, lw=2, zorder=2)
        ax.plot([x1, x2], [y1, y1], color=ORANGE, lw=1.4, ls="--")
        ax.plot([x2, x2], [y1, y2], color=GREEN, lw=1.4, ls="--")
    ax.scatter([x1, x2], [y1, y2], s=70, color=RED, zorder=4)
    ax.annotate(f"({int(x1) if x1==int(x1) else x1:g}, {int(y1) if y1==int(y1) else y1:g})", (x1, y1), textcoords="offset points", xytext=(6, 8), fontsize=9)
    ax.annotate(f"({int(x2) if x2==int(x2) else x2:g}, {int(y2) if y2==int(y2) else y2:g})", (x2, y2), textcoords="offset points", xytext=(6, 8), fontsize=9)
    pad = 2
    ax.set_xlim(min(x1, x2) - pad, max(x1, x2) + pad)
    ax.set_ylim(min(y1, y2) - pad, max(y1, y2) + pad)
    return fig


def fig_slope_line(d: dict[str, Any]):
    x1, y1, x2, y2 = map(float, (d["x1"], d["y1"], d["x2"], d["y2"]))
    fig, ax = _fig()
    _axes(ax, "Line through two points")
    xs = np.linspace(min(x1, x2) - 2, max(x1, x2) + 2, 50)
    if x2 != x1:
        m = (y2 - y1) / (x2 - x1)
        ys = y1 + m * (xs - x1)
        ax.plot(xs, ys, color=BLUE, lw=2)
    ax.scatter([x1, x2], [y1, y2], s=70, color=RED, zorder=4)
    ax.annotate("rise", ((x1 + x2) / 2 + 0.2, (y1 + y2) / 2), color=GREEN, fontsize=9)
    return fig


def fig_parabola(d: dict[str, Any]):
    a, h, k = float(d.get("a", 1)), float(d.get("h", 0)), float(d.get("k", 0))
    fig, ax = _fig()
    _axes(ax, r"Parabola $y = a(x-h)^2 + k$")
    xs = np.linspace(h - 4, h + 4, 200)
    ax.plot(xs, a * (xs - h) ** 2 + k, color=BLUE, lw=2.2)
    ax.scatter([h], [k], s=80, color=RED, zorder=4)
    ax.annotate("vertex", (h, k), textcoords="offset points", xytext=(8, 8), color=RED, fontsize=9)
    ax.set_xlim(h - 4.5, h + 4.5)
    lo, hi = min(k, k + a * 16), max(k, k + a * 16)
    ax.set_ylim(lo - 2, hi + 2)
    return fig


def fig_sqrt_shift(d: dict[str, Any]):
    h = float(d.get("h", 2))
    fig, ax = _fig()
    _axes(ax, r"Parent $y=\sqrt{x}$ and shifted graph")
    xs0 = np.linspace(0, 9, 200)
    xs = np.linspace(h, h + 9, 200)
    ax.plot(xs0, np.sqrt(xs0), color=SLATE, lw=1.6, ls="--", label=r"$y=\sqrt{x}$")
    ax.plot(xs, np.sqrt(xs - h), color=BLUE, lw=2.3, label=rf"$y=\sqrt{{x-{h:g}}}$")
    ax.scatter([0, h], [0, 0], s=70, color=RED, zorder=4)
    ax.legend(fontsize=8, loc="upper left")
    ax.set_xlim(-1, h + 8)
    ax.set_ylim(-0.5, 3.4)
    return fig


def fig_abs_v(d: dict[str, Any]):
    h, k = float(d.get("h", 2)), float(d.get("k", 1))
    fig, ax = _fig()
    _axes(ax, r"$y = |x-h| + k$")
    xs = np.linspace(h - 5, h + 5, 400)
    ax.plot(xs, np.abs(xs - h) + k, color=BLUE, lw=2.3)
    ax.scatter([h], [k], s=80, color=RED, zorder=4)
    ax.annotate("vertex", (h, k), textcoords="offset points", xytext=(8, 8), color=RED, fontsize=9)
    ax.set_xlim(h - 5, h + 5)
    ax.set_ylim(k - 1, k + 6)
    return fig


def fig_polynomial(d: dict[str, Any]):
    lead = float(d.get("lead", 1))
    degree = int(d.get("degree", 3))
    fig, ax = _fig()
    _axes(ax, f"End behavior of a degree-{degree} polynomial")
    xs = np.linspace(-2.4, 2.4, 300)
    ys = lead * xs**degree
    ax.plot(xs, ys, color=BLUE, lw=2.2)
    ax.annotate("x → +∞", xy=(2.1, lead * 2.1**degree), color=ORANGE, fontsize=9)
    return fig


def fig_poly_zeros(d: dict[str, Any]):
    roots = [float(r) for r in d.get("roots", [-1, 1, 2])]
    fig, ax = _fig()
    _axes(ax, "Zeros are x-intercepts")
    lo, hi = min(roots) - 2, max(roots) + 2
    xs = np.linspace(lo, hi, 400)
    ys = np.ones_like(xs)
    for r in roots:
        ys *= xs - r
    ax.plot(xs, ys, color=BLUE, lw=2.2)
    ax.scatter(roots, [0] * len(roots), s=70, color=RED, zorder=4)
    ax.set_xlim(lo, hi)
    return fig


def fig_exponential(d: dict[str, Any]):
    base = float(d.get("base", 2))
    fig, ax = _fig()
    _axes(ax, rf"$y = {base:g}^x$")
    xs = np.linspace(-2.5, 4.2, 300)
    ax.plot(xs, base**xs, color=BLUE, lw=2.3)
    ax.set_ylim(-0.2, min(base**4.2, 40))
    n = int(d.get("n", 3))
    ax.scatter([n], [base**n], s=70, color=RED, zorder=4)
    ax.annotate(rf"${base:g}^{{{n}}}$", (n, base**n), textcoords="offset points", xytext=(8, 6), color=RED)
    return fig


def fig_log(d: dict[str, Any]):
    b = float(d.get("base", 2))
    arg = float(d.get("arg", 8))
    fig, ax = _fig()
    _axes(ax, rf"$y = \log_{{{b:g}}} x$")
    xs = np.linspace(0.08, max(arg + 2, 10), 400)
    ax.plot(xs, np.log(xs) / np.log(b), color=BLUE, lw=2.3)
    ax.scatter([arg], [np.log(arg) / np.log(b)], s=70, color=RED, zorder=4)
    ax.set_xlim(-0.5, max(arg + 2, 10))
    return fig


def fig_rational(d: dict[str, Any]):
    q = float(d.get("q", 2))
    p = float(d.get("p", 3))
    fig, ax = _fig()
    _axes(ax, "Vertical asymptote from a zero of the denominator")
    xs_l = np.linspace(q - 6, q - 0.12, 200)
    xs_r = np.linspace(q + 0.12, q + 6, 200)
    ax.plot(xs_l, (xs_l + p) / (xs_l - q), color=BLUE, lw=2)
    ax.plot(xs_r, (xs_r + p) / (xs_r - q), color=BLUE, lw=2)
    ax.axvline(q, color=RED, lw=1.6, ls="--")
    ax.set_ylim(-12, 12)
    ax.annotate(f"x = {q:g}", (q, 8), color=RED, fontsize=10, ha="left")
    return fig


def fig_variation(d: dict[str, Any]):
    k = float(d.get("k", 2))
    fig, ax = _fig()
    _axes(ax, r"Direct variation $y = kx$")
    xs = np.linspace(0, 10, 50)
    ax.plot(xs, k * xs, color=BLUE, lw=2.2)
    x1, y1 = float(d.get("x1", 2)), float(d.get("y1", 2 * k))
    x2, y2 = float(d.get("x2", 6)), float(d.get("y2", 6 * k))
    ax.scatter([x1, x2], [y1, y2], s=70, color=RED, zorder=4)
    return fig


def fig_secant(d: dict[str, Any]):
    a = float(d.get("a", 1))
    b = float(d.get("b", 0))
    x1, x2 = float(d["x1"]), float(d["x2"])
    fig, ax = _fig()
    _axes(ax, "Average rate of change is the secant slope")
    xs = np.linspace(min(x1, x2) - 1, max(x1, x2) + 1, 200)
    ax.plot(xs, a * xs**2 + b, color=BLUE, lw=2.2)
    y1, y2 = a * x1**2 + b, a * x2**2 + b
    ax.plot([x1, x2], [y1, y2], color=ORANGE, lw=2)
    ax.scatter([x1, x2], [y1, y2], s=70, color=RED, zorder=4)
    return fig


def fig_inverse_line(d: dict[str, Any]):
    a = float(d.get("a", 2))
    b = float(d.get("b", 1))
    fig, ax = _fig()
    _axes(ax, r"$f$ and $f^{-1}$ are reflections across $y=x$", equal=True)
    xs = np.linspace(-8, 8, 200)
    ax.plot(xs, a * xs + b, color=BLUE, lw=2, label="f")
    ax.plot(xs, (xs - b) / a, color=ORANGE, lw=2, label=r"$f^{-1}$")
    ax.plot(xs, xs, color=SLATE, lw=1, ls="--", label="y = x")
    ax.legend(fontsize=8)
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    return fig


def fig_sine(d: dict[str, Any]):
    A = float(d.get("A", 1))
    b = float(d.get("b", 1))
    k = float(d.get("k", 0))
    kind = d.get("kind", "sin")
    shift = float(d.get("shift", 0))
    fig, ax = _fig(6.8, 4.0)
    ax.set_facecolor("#fbfcfe")
    ax.axhline(k, color=ORANGE, lw=1.2, ls="--", label="midline")
    ax.axhline(0, color="#94a3b8", lw=0.7)
    ax.grid(True, alpha=0.28)
    xs = np.linspace(-0.2, 2 * np.pi + 0.4, 500)
    inside = b * (xs - shift)
    ys = A * (np.sin(inside) if kind == "sin" else np.cos(inside)) + k
    ax.plot(xs, ys, color=BLUE, lw=2.3)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(d.get("title", "Sinusoid"), fontsize=11)
    ax.set_xlim(-0.2, 2 * np.pi + 0.3)
    ax.legend(fontsize=8, loc="upper right")
    return fig


def fig_tan(d: dict[str, Any]):
    b = float(d.get("b", 1))
    fig, ax = _fig(6.8, 4.0)
    ax.set_facecolor("#fbfcfe")
    ax.axhline(0, color="#94a3b8", lw=0.8)
    ax.grid(True, alpha=0.28)
    period = np.pi / abs(b)
    xs = np.linspace(-period * 1.4, period * 1.4, 800)
    ys = np.tan(b * xs)
    ys[np.abs(ys) > 6] = np.nan
    ax.plot(xs, ys, color=BLUE, lw=2)
    for n in (-1, 0, 1):
        ax.axvline((n + 0.5) * period, color=RED, lw=1, ls="--")
    ax.set_ylim(-5, 5)
    ax.set_title(rf"$y=\tan({b:g}x)$, period $\pi/|{b:g}|$", fontsize=11)
    return fig


def fig_right_triangle(d: dict[str, Any]):
    a, b, c = float(d["opp"]), float(d["adj"]), float(d["hyp"])
    fig, ax = _fig(5.6, 4.6)
    ax.set_aspect("equal")
    scale = 3.4 / max(a, b)
    A, B = a * scale, b * scale
    ax.fill([0, B, B, 0], [0, 0, A, 0], color="#dbeafe", zorder=1)
    ax.plot([0, B, B, 0], [0, 0, A, 0], color=BLUE, lw=2.2)
    ax.add_patch(Rectangle((B - 0.28, 0), 0.28, 0.28, fill=False, ec=SLATE, lw=1.2))
    ax.text(B / 2, -0.35, f"adj {d['adj']:g}", ha="center", fontsize=10)
    ax.text(B + 0.2, A / 2, f"opp {d['opp']:g}", va="center", fontsize=10)
    ax.text(B / 2 - 0.15, A / 2 + 0.15, f"hyp {d['hyp']:g}", rotation=np.degrees(np.arctan2(A, B)), fontsize=10)
    ax.text(0.35, 0.28, r"$\theta$", fontsize=12, color=RED)
    ax.set_xlim(-0.6, B + 1.4)
    ax.set_ylim(-0.8, A + 0.8)
    ax.axis("off")
    ax.set_title("Right triangle", fontsize=11)
    return fig


def fig_elevation(d: dict[str, Any]):
    dist = float(d["dist"])
    height = float(d["height"])
    fig, ax = _fig(6.2, 4.2)
    ax.set_aspect("equal")
    scale = 4.2 / max(dist, height)
    D, H = dist * scale, height * scale
    ax.fill([0, D, D], [0, 0, H], color="#dbeafe")
    ax.plot([0, D, D, 0], [0, 0, H, 0], color=BLUE, lw=2)
    ax.plot([D, D], [0, H], color=GREEN, lw=2.4)
    ax.text(D / 2, -0.35, f"{dist:g}", ha="center")
    ax.text(D + 0.2, H / 2, f"{height:g}", va="center", color=GREEN)
    ax.text(0.45, 0.22, d.get("angle", r"$45^\circ$"), color=RED, fontsize=11)
    ax.set_xlim(-0.5, D + 1.3)
    ax.set_ylim(-0.8, H + 0.7)
    ax.axis("off")
    ax.set_title("Angle of elevation", fontsize=11)
    return fig


def fig_polar_point(d: dict[str, Any]):
    r = float(d["r"])
    deg = float(d["deg"])
    fig, ax = _fig(5.4, 5.4)
    ax.set_aspect("equal")
    circ = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(circ), np.sin(circ), color="#cbd5e1", lw=1)
    ax.plot(2 * np.cos(circ), 2 * np.sin(circ), color="#e2e8f0", lw=1)
    _axes(ax, "Polar point", equal=True)
    rad = np.deg2rad(deg)
    ax.plot([0, r * np.cos(rad)], [0, r * np.sin(rad)], color=BLUE, lw=2)
    ax.scatter([r * np.cos(rad)], [r * np.sin(rad)], s=80, color=RED, zorder=4)
    ax.set_xlim(-r - 1, r + 1)
    ax.set_ylim(-r - 1, r + 1)
    return fig


def fig_polar_circle(d: dict[str, Any]):
    a = float(d.get("a", 3))
    fig, ax = _fig(5.4, 5.4)
    _axes(ax, rf"$r = {a:g}$", equal=True)
    t = np.linspace(0, 2 * np.pi, 300)
    ax.plot(a * np.cos(t), a * np.sin(t), color=BLUE, lw=2.3)
    ax.set_xlim(-a - 1, a + 1)
    ax.set_ylim(-a - 1, a + 1)
    return fig


def fig_ellipse(d: dict[str, Any]):
    a, b = float(d.get("a", 4)), float(d.get("b", 2))
    fig, ax = _fig(6.2, 4.4)
    _axes(ax, "Ellipse", equal=True)
    t = np.linspace(0, 2 * np.pi, 300)
    ax.plot(a * np.cos(t), b * np.sin(t), color=BLUE, lw=2.2)
    ax.scatter([a, -a], [0, 0], s=50, color=RED)
    ax.set_xlim(-a - 1, a + 1)
    ax.set_ylim(-max(b, 2) - 1, max(b, 2) + 1)
    return fig


def fig_hyperbola(d: dict[str, Any]):
    fig, ax = _fig()
    _axes(ax, r"$x^2/9 - y^2/4 = 1$ (opens left-right)", equal=True)
    xs = np.linspace(3.02, 8, 200)
    ys = 2 * np.sqrt((xs**2) / 9 - 1)
    ax.plot(xs, ys, color=BLUE, lw=2)
    ax.plot(xs, -ys, color=BLUE, lw=2)
    ax.plot(-xs, ys, color=BLUE, lw=2)
    ax.plot(-xs, -ys, color=BLUE, lw=2)
    ax.plot([-8, 8], [-8 * 2 / 3, 8 * 2 / 3], color=SLATE, ls="--", lw=1)
    ax.plot([-8, 8], [8 * 2 / 3, -8 * 2 / 3], color=SLATE, ls="--", lw=1)
    ax.set_xlim(-8, 8)
    ax.set_ylim(-6, 6)
    return fig


def fig_conic_parabola(d: dict[str, Any]):
    p = float(d.get("p", 2))
    fig, ax = _fig()
    _axes(ax, rf"Focus at $(0,{p:g})$", equal=True)
    xs = np.linspace(-4 * p, 4 * p, 300)
    ax.plot(xs, xs**2 / (4 * p), color=BLUE, lw=2.2)
    ax.scatter([0], [p], s=70, color=RED, zorder=4)
    ax.axhline(-p, color=ORANGE, ls="--", lw=1.4)
    ax.annotate("focus", (0, p), textcoords="offset points", xytext=(8, 4), color=RED, fontsize=9)
    ax.annotate("directrix", (3 * p, -p), textcoords="offset points", xytext=(0, 6), color=ORANGE, fontsize=9)
    ax.set_xlim(-4 * p, 4 * p)
    ax.set_ylim(-p - 1.5, 4 * p)
    return fig


def fig_vector(d: dict[str, Any]):
    a, b = float(d["a"]), float(d["b"])
    fig, ax = _fig(5.4, 4.8)
    _axes(ax, "Vector from the origin", equal=True)
    _arrow(ax, 0, 0, a, b, BLUE)
    ax.plot([a, a], [0, b], color=SLATE, ls=":", lw=1)
    ax.plot([0, a], [b, b], color=SLATE, ls=":", lw=1)
    ax.set_xlim(-1, a + 2)
    ax.set_ylim(-1, b + 2)
    return fig


def fig_complex(d: dict[str, Any]):
    a, b = float(d["a"]), float(d["b"])
    fig, ax = _fig(5.4, 4.8)
    _axes(ax, "Complex plane", equal=True)
    ax.set_xlabel("real")
    ax.set_ylabel("imaginary")
    _arrow(ax, 0, 0, a, b, BLUE, f"{d['a']:g}+{d['b']:g}i")
    ax.set_xlim(-1, a + 2)
    ax.set_ylim(-1, b + 2)
    return fig


def fig_unit_param(d: dict[str, Any]):
    fig, ax = _fig(5.2, 5.2)
    _axes(ax, r"$x=\cos t,\ y=\sin t$", equal=True)
    t = np.linspace(0, 2 * np.pi, 300)
    ax.plot(np.cos(t), np.sin(t), color=BLUE, lw=2.3)
    ax.scatter([1], [0], s=60, color=RED, zorder=4)
    ax.annotate("t = 0", (1, 0), textcoords="offset points", xytext=(8, 6), fontsize=9)
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    return fig


def fig_limit_hole(d: dict[str, Any]):
    a = float(d.get("a", 2))
    fig, ax = _fig()
    _axes(ax, "A hole: the limit can still exist")
    xs = np.linspace(a - 4, a + 4, 300)
    ys = xs + a
    ax.plot(xs, ys, color=BLUE, lw=2.2)
    ax.plot(a, 2 * a, "o", ms=11, color="white", markeredgecolor=BLUE, markeredgewidth=2, zorder=5)
    ax.axvline(a, color=SLATE, ls=":", lw=1)
    ax.annotate("hole", (a, 2 * a), textcoords="offset points", xytext=(8, 8), color=RED)
    return fig


def fig_oblique_triangle(d: dict[str, Any]):
    fig, ax = _fig(5.6, 4.4)
    ax.set_aspect("equal")
    ax.fill([0, 4.2, 1.4], [0, 0, 2.6], color="#dbeafe")
    ax.plot([0, 4.2, 1.4, 0], [0, 0, 2.6, 0], color=BLUE, lw=2)
    ax.text(2.1, -0.28, "c", ha="center")
    ax.text(2.9, 1.45, "a", color=RED)
    ax.text(0.45, 1.4, "b")
    ax.text(1.45, 2.75, "C", color=ORANGE)
    ax.axis("off")
    ax.set_title("Oblique triangle (Law of Sines / Cosines)", fontsize=11)
    ax.set_xlim(-0.5, 4.8)
    ax.set_ylim(-0.7, 3.3)
    return fig


def fig_projectile(d: dict[str, Any]):
    v = float(d.get("v", 20))
    g = float(d.get("g", 10))
    fig, ax = _fig(6.6, 3.8)
    ax.set_facecolor("#fbfcfe")
    ax.grid(True, alpha=0.28)
    t_f = 2 * (v / np.sqrt(2)) / g
    t = np.linspace(0, t_f, 80)
    vx = vy = v / np.sqrt(2)
    x = vx * t
    y = vy * t - 0.5 * g * t**2
    ax.plot(x, np.maximum(y, 0), color=BLUE, lw=2.3)
    ax.scatter([0, x[-1]], [0, 0], s=40, color=RED)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title(rf"Projectile at $45^\circ$, $v={v:g}$ m/s", fontsize=11)
    ax.set_ylim(-0.5, max(y) + 2)
    return fig


def fig_motion_1d(d: dict[str, Any]):
    x0, x = float(d["x0"]), float(d["x"])
    fig, ax = _fig(6.6, 2.3)
    ax.axhline(0.15, color=SLATE, lw=1.5)
    ax.plot(x0, 0.15, "s", ms=14, color=BLUE)
    ax.plot(x, 0.15, "s", ms=14, color=RED)
    ax.annotate("", xy=(x, 0.15), xytext=(x0, 0.15), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2))
    ax.text(x0, -0.25, f"start {x0:g} m", ha="center", fontsize=9)
    ax.text(x, -0.25, f"end {x:g} m", ha="center", fontsize=9)
    ax.set_xlim(min(x0, x) - 3, max(x0, x) + 3)
    ax.set_ylim(-0.7, 0.8)
    ax.axis("off")
    ax.set_title("Displacement along a line", fontsize=11)
    return fig


def fig_vt(d: dict[str, Any]):
    v0, a, t = float(d["v0"]), float(d["a"]), float(d["t"])
    fig, ax = _fig(6.4, 3.6)
    ax.set_facecolor("#fbfcfe")
    ax.grid(True, alpha=0.28)
    ts = np.array([0, t])
    ax.plot(ts, v0 + a * ts, color=BLUE, lw=2.3)
    ax.set_xlabel("t (s)")
    ax.set_ylabel("v (m/s)")
    ax.set_title("Velocity vs time (constant a)", fontsize=11)
    ax.set_xlim(-0.1, t + 0.4)
    return fig


def fig_freefall(d: dict[str, Any]):
    h = float(d.get("h", 20))
    fig, ax = _fig(3.6, 5.2)
    ax.add_patch(Rectangle((-0.4, 0), 0.8, h, color="#e2e8f0"))
    ax.plot(0, h, "o", ms=14, color=ORANGE)
    ax.annotate("", xy=(0, 0.4), xytext=(0, h - 0.3), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
    ax.text(0.55, h / 2, f"{h:g} m", color=RED)
    ax.set_xlim(-1.6, 2.2)
    ax.set_ylim(-1, h + 2)
    ax.axis("off")
    ax.set_title("Dropped from rest", fontsize=11)
    return fig


def fig_fbd(d: dict[str, Any]):
    kind = d.get("kind", "net")
    fig, ax = _fig(5.2, 4.6)
    ax.add_patch(FancyBboxPatch((-0.7, -0.5), 1.4, 1.0, boxstyle="round,pad=0.05", fc="#93c5fd", ec=BLUE, lw=2))
    ax.text(0, 0, "m", ha="center", va="center", fontsize=12, fontweight="600")
    if kind == "net":
        _arrow(ax, 0.7, 0, 1.4, 0, RED, r"$F_{\mathrm{net}}$")
    elif kind == "friction":
        _arrow(ax, 0.7, 0, 1.3, 0, GREEN, r"$F$")
        _arrow(ax, -0.7, 0, -1.3, 0, ORANGE, r"$f_k$")
        _arrow(ax, 0, 0.5, 0, 1.1, BLUE, "n")
        _arrow(ax, 0, -0.5, 0, -1.1, SLATE, "mg")
    else:
        _arrow(ax, 0, 0.5, 0, 1.2, BLUE, "n")
        _arrow(ax, 0, -0.5, 0, -1.2, RED, "mg")
        ax.axhline(-0.5, color="#78716c", lw=6)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-2.6, 2.4)
    ax.axis("off")
    ax.set_title("Free-body diagram", fontsize=11)
    return fig


def fig_ramp(d: dict[str, Any]):
    h = float(d.get("h", 5))
    fig, ax = _fig(6.2, 4.0)
    ax.fill([0, 4.5, 4.5], [h * 0.35, 0, h * 0.35], color="#e2e8f0")
    ax.plot([0, 4.5], [h * 0.35, 0], color=SLATE, lw=3)
    ax.plot(0.35, h * 0.35 + 0.12, "s", ms=16, color=BLUE)
    ax.plot(4.2, 0.18, "s", ms=16, color=RED)
    ax.annotate("", xy=(4.15, 0.25), xytext=(0.5, h * 0.35), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.6))
    ax.text(4.7, h * 0.18, f"drop {h:g} m", color=GREEN)
    ax.set_xlim(-0.4, 6.2)
    ax.set_ylim(-0.4, h * 0.35 + 1.2)
    ax.axis("off")
    ax.set_title("Frictionless ramp", fontsize=11)
    return fig


def fig_carts(d: dict[str, Any]):
    fig, ax = _fig(6.6, 2.6)
    ax.axhline(0.2, color=SLATE, lw=3)
    ax.add_patch(Rectangle((0.4, 0.2), 1.2, 0.7, fc="#93c5fd", ec=BLUE, lw=2))
    ax.add_patch(Rectangle((3.6, 0.2), 1.4, 0.7, fc="#fdba74", ec=ORANGE, lw=2))
    _arrow(ax, 1.7, 0.55, 1.1, 0, RED, r"$v$")
    ax.text(1.0, 1.1, f"m₁ = {d.get('m1', '?')}", ha="center", fontsize=9)
    ax.text(4.3, 1.1, f"m₂ = {d.get('m2', '?')} at rest", ha="center", fontsize=9)
    ax.set_xlim(0, 6.4)
    ax.set_ylim(-0.2, 1.7)
    ax.axis("off")
    ax.set_title("Inelastic collision (they stick)", fontsize=11)
    return fig


def fig_circle_motion(d: dict[str, Any]):
    r = float(d.get("r", 4))
    fig, ax = _fig(5.2, 5.2)
    ax.set_aspect("equal")
    t = np.linspace(0, 2 * np.pi, 200)
    ax.plot(r * np.cos(t), r * np.sin(t), color=BLUE, lw=2)
    ax.plot(0, 0, "o", color=SLATE)
    ax.plot([0, r], [0, 0], color=SLATE, ls="--")
    ax.plot(r, 0, "o", ms=10, color=RED)
    _arrow(ax, r, 0, 0, 1.6, ORANGE, r"$\vec v$")
    _arrow(ax, r, 0, -1.4, 0, GREEN, r"$\vec a_c$")
    ax.set_xlim(-r - 2, r + 2.4)
    ax.set_ylim(-r - 2, r + 2.4)
    ax.axis("off")
    ax.set_title("Uniform circular motion", fontsize=11)
    return fig


def fig_spring(d: dict[str, Any]):
    fig, ax = _fig(6.4, 2.6)
    xs = np.linspace(0.4, 3.2, 40)
    ys = 0.18 * np.sin(xs * 12)
    ax.plot(xs, ys + 0.4, color=SLATE, lw=2)
    ax.add_patch(Rectangle((3.2, 0.15), 0.9, 0.55, fc="#93c5fd", ec=BLUE, lw=2))
    ax.axvline(0.35, color="#57534e", lw=8)
    ax.set_xlim(0, 5.2)
    ax.set_ylim(-0.4, 1.3)
    ax.axis("off")
    ax.set_title("Mass on a spring (SHM)", fontsize=11)
    return fig


def fig_wave(d: dict[str, Any]):
    lam = float(d.get("lam", 4))
    fig, ax = _fig(6.6, 3.2)
    xs = np.linspace(0, 3 * lam, 400)
    ax.plot(xs, np.sin(2 * np.pi * xs / lam), color=BLUE, lw=2.2)
    ax.annotate(
        "",
        xy=(lam, -1.15),
        xytext=(0, -1.15),
        arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=1.4),
    )
    ax.text(lam / 2, -1.45, rf"$\lambda = {lam:g}$ m", ha="center", color=ORANGE)
    ax.set_title("Snapshot of a traveling wave", fontsize=11)
    ax.set_xlabel("x (m)")
    ax.set_ylim(-1.8, 1.5)
    return fig


def fig_circuit(d: dict[str, Any]):
    kind = d.get("kind", "ohm")
    fig, ax = _fig(6.0, 3.6)
    ax.plot([1, 4.5, 4.5, 1, 1], [2.2, 2.2, 0.7, 0.7, 2.2], color=INK, lw=2)
    ax.add_patch(Circle((1, 1.45), 0.28, fill=False, ec=INK, lw=2))
    ax.text(1, 1.45, "+ −", ha="center", va="center", fontsize=8)
    ax.text(0.2, 1.45, f"{d.get('V', 'V')}", fontsize=10)
    if kind == "ohm":
        ax.plot([2.4, 2.55, 2.7, 2.85, 3.0, 3.15, 3.3], [2.2, 2.45, 1.95, 2.45, 1.95, 2.45, 2.2], color=RED, lw=2)
        ax.text(2.7, 2.65, f"R = {d.get('R', '?')} Ω", color=RED, fontsize=10)
    elif kind == "series":
        ax.plot([2.0, 2.15, 2.3, 2.45, 2.6], [2.2, 2.4, 2.0, 2.4, 2.2], color=RED, lw=2)
        ax.plot([3.1, 3.25, 3.4, 3.55, 3.7], [2.2, 2.4, 2.0, 2.4, 2.2], color=ORANGE, lw=2)
        ax.text(2.1, 2.6, f"{d.get('R1', '')} Ω", fontsize=9, color=RED)
        ax.text(3.2, 2.6, f"{d.get('R2', '')} Ω", fontsize=9, color=ORANGE)
    else:
        ax.plot([2.6, 2.6], [2.2, 0.7], color=INK, lw=2)
        ax.plot([2.35, 2.5, 2.65, 2.8, 2.95], [2.2, 2.4, 2.0, 2.4, 2.2], color=RED, lw=2)
        ax.plot([2.35, 2.5, 2.65, 2.8, 2.95], [0.7, 0.9, 0.5, 0.9, 0.7], color=ORANGE, lw=2)
    ax.set_xlim(0, 5.3)
    ax.set_ylim(0.2, 3.1)
    ax.axis("off")
    ax.set_title("Circuit", fontsize=11)
    return fig


def fig_piston(d: dict[str, Any]):
    fig, ax = _fig(4.4, 4.6)
    ax.add_patch(Rectangle((1, 0.4), 1.6, 2.4, fill=False, ec=INK, lw=2))
    ax.add_patch(Rectangle((1.05, 1.8), 1.5, 0.18, fc="#94a3b8"))
    _arrow(ax, 1.8, 2.0, 0, 0.9, RED, "F")
    ax.text(1.8, 1.1, "A", ha="center")
    ax.set_xlim(0.3, 3.6)
    ax.set_ylim(0, 3.4)
    ax.axis("off")
    ax.set_title("Pressure = F / A", fontsize=11)
    return fig


def fig_buoyancy(d: dict[str, Any]):
    fig, ax = _fig(5.0, 4.6)
    ax.add_patch(Rectangle((0.6, 0.4), 3.2, 2.4, fc="#bae6fd", ec=BLUE, lw=1.5))
    ax.add_patch(Rectangle((1.6, 1.0), 1.1, 0.9, fc="#78716c", ec=INK, lw=1.5))
    _arrow(ax, 2.15, 1.9, 0, 0.9, GREEN, r"$F_b$")
    _arrow(ax, 2.15, 1.0, 0, -0.7, RED, "mg")
    ax.set_xlim(0.2, 4.2)
    ax.set_ylim(0, 3.4)
    ax.axis("off")
    ax.set_title("Fully submerged object", fontsize=11)
    return fig


def fig_pipe(d: dict[str, Any]):
    fig, ax = _fig(6.6, 3.2)
    ax.fill([0.3, 2.6, 2.6, 0.3], [0.7, 0.7, 2.3, 2.3], color="#bae6fd", ec=BLUE)
    ax.fill([2.6, 5.8, 5.8, 2.6], [1.05, 1.05, 1.95, 1.95], color="#7dd3fc", ec=BLUE)
    _arrow(ax, 0.7, 1.5, 1.3, 0, RED, r"$v_1$")
    _arrow(ax, 3.2, 1.5, 1.6, 0, ORANGE, r"$v_2$")
    ax.set_xlim(0, 6.4)
    ax.set_ylim(0.2, 2.8)
    ax.axis("off")
    ax.set_title("Continuity: narrower → faster", fontsize=11)
    return fig


def fig_charges(d: dict[str, Any]):
    fig, ax = _fig(5.6, 3.6)
    ax.add_patch(Circle((1.3, 1.5), 0.35, fc="#fecaca", ec=RED, lw=2))
    ax.add_patch(Circle((4.2, 1.5), 0.35, fc="#fecaca", ec=RED, lw=2))
    ax.text(1.3, 1.5, "+", ha="center", va="center", fontsize=16, color=RED)
    ax.text(4.2, 1.5, "+", ha="center", va="center", fontsize=16, color=RED)
    ax.annotate("", xy=(1.3 - 0.9, 1.5), xytext=(1.3 - 0.35, 1.5), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2))
    ax.annotate("", xy=(4.2 + 0.9, 1.5), xytext=(4.2 + 0.35, 1.5), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2))
    ax.text(2.75, 1.95, f"r = {d.get('r', '?')} m", ha="center")
    ax.set_xlim(0, 6)
    ax.set_ylim(0.4, 2.6)
    ax.axis("off")
    ax.set_title("Like charges repel", fontsize=11)
    return fig


def fig_efield(d: dict[str, Any]):
    fig, ax = _fig(6.2, 3.4)
    for y in (0.7, 1.5, 2.3):
        ax.annotate("", xy=(5.4, y), xytext=(0.6, y), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.5))
    ax.plot(2.4, 1.5, "o", ms=16, color=RED)
    _arrow(ax, 2.4, 1.5, 1.3, 0, RED, r"$\vec F = q\vec E$")
    ax.set_xlim(0.2, 6)
    ax.set_ylim(0.2, 2.9)
    ax.axis("off")
    ax.set_title("Uniform electric field", fontsize=11)
    return fig


def fig_magnetic(d: dict[str, Any]):
    fig, ax = _fig(5.6, 4.2)
    for x in np.linspace(1, 4.5, 6):
        for y in np.linspace(0.8, 3.0, 5):
            ax.plot(x, y, "x", color=SLATE, ms=7)
    ax.annotate("", xy=(3.3, 1.9), xytext=(1.4, 1.9), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2))
    ax.text(2.2, 2.15, r"$\vec v$", color=BLUE)
    ax.text(3.6, 3.15, r"$\vec B$ (× into page)", color=SLATE)
    ax.annotate("", xy=(2.4, 3.1), xytext=(2.4, 1.9), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
    ax.text(2.55, 2.6, r"$\vec F$", color=RED)
    ax.set_xlim(0.5, 5.4)
    ax.set_ylim(0.4, 3.6)
    ax.axis("off")
    ax.set_title(r"$F = qvB$ (v ⟂ B)", fontsize=11)
    return fig


def fig_snell(d: dict[str, Any]):
    fig, ax = _fig(5.6, 4.8)
    ax.axhline(2, color=SLATE, lw=2)
    ax.fill([-0.2, 5, 5, -0.2], [2, 2, -0.2, -0.2], color="#e0f2fe")
    ax.text(4.1, 3.1, "air", fontsize=10)
    ax.text(4.1, 0.7, f"n = {d.get('n2', '?')}", fontsize=10)
    ax.plot([2.4, 2.4], [0, 4], color=SLATE, ls=":", lw=1)
    ax.plot([1.1, 2.4], [3.6, 2], color=RED, lw=2)
    ax.plot([2.4, 3.2], [2, 0.3], color=ORANGE, lw=2)
    ax.text(1.2, 3.2, r"$\theta_1$", color=RED)
    ax.text(2.55, 1.3, r"$\theta_2$", color=ORANGE)
    ax.set_xlim(-0.2, 5)
    ax.set_ylim(-0.2, 4.1)
    ax.axis("off")
    ax.set_title("Snell's law", fontsize=11)
    return fig


def fig_lens(d: dict[str, Any]):
    fig, ax = _fig(6.6, 3.8)
    ax.axhline(1.6, color=SLATE, lw=1)
    ax.plot([3.2, 3.2], [0.3, 2.9], color=BLUE, lw=3)
    ax.plot(3.2, 1.6, "o", color=BLUE, ms=4)
    ax.plot(1.2, 2.3, "s", color=ORANGE, ms=8)
    ax.plot(4.7, 0.95, "o", color=RED, ms=8)
    ax.plot([1.2, 3.2, 4.7], [2.3, 1.6, 0.95], color=GREEN, lw=1.4)
    ax.plot([1.2, 3.2, 4.7], [2.3, 2.3, 0.95], color=PURPLE, lw=1.4)
    ax.text(1.2, 2.55, "object", fontsize=8)
    ax.text(4.5, 0.55, "image", fontsize=8, color=RED)
    ax.set_xlim(0.5, 6.2)
    ax.set_ylim(0.2, 3.2)
    ax.axis("off")
    ax.set_title("Converging lens", fontsize=11)
    return fig


def fig_energy_bars(d: dict[str, Any]):
    q, w, du = float(d["q"]), float(d["w"]), float(d["du"])
    fig, ax = _fig(5.6, 4.0)
    ax.bar([0, 1, 2], [q, w, du], color=[GREEN, ORANGE, BLUE], width=0.55)
    ax.set_xticks([0, 1, 2], ["Q heat in", "W work by gas", r"$\Delta U$"])
    ax.set_ylabel("joules")
    ax.set_title("First law: ΔU = Q − W", fontsize=11)
    ax.axhline(0, color=SLATE, lw=0.8)
    return fig


def fig_quadratic_abc(d: dict[str, Any]):
    a, b, c = float(d["a"]), float(d["b"]), float(d["c"])
    x0 = d.get("x0")
    roots = [float(r) for r in (d.get("roots") or [])]
    vertex = -b / (2 * a) if a else 0.0
    marks = [vertex, *roots]
    if x0 is not None:
        marks.append(float(x0))
    lo, hi = min(marks) - 4, max(marks) + 4
    fig, ax = _fig()
    _axes(ax, r"$y = ax^2 + bx + c$")
    xs = np.linspace(lo, hi, 300)
    ys = a * xs**2 + b * xs + c
    ax.plot(xs, ys, color=BLUE, lw=2.2)
    if x0 is not None:
        x0 = float(x0)
        y0 = a * x0**2 + b * x0 + c
        ax.scatter([x0], [y0], s=80, color=RED, zorder=4)
        ax.annotate(f"({x0:g}, {y0:g})", (x0, y0), textcoords="offset points", xytext=(8, 8), fontsize=9)
    if roots:
        ax.scatter(roots, [0] * len(roots), s=70, color=ORANGE, zorder=4)
    ax.set_xlim(lo, hi)
    pad = max(3.0, 0.15 * (float(np.max(ys)) - float(np.min(ys))))
    ax.set_ylim(float(np.min(ys)) - pad, float(np.max(ys)) + pad)
    return fig


def fig_system(d: dict[str, Any]):
    a1, b1, c1 = float(d["a1"]), float(d["b1"]), float(d["c1"])
    a2, b2, c2 = float(d["a2"]), float(d["b2"]), float(d["c2"])
    xs = np.linspace(-2, 8, 80)
    fig, ax = _fig()
    _axes(ax, "Two lines — the solution is the intersection")
    if b1 != 0:
        ax.plot(xs, (c1 - a1 * xs) / b1, color=BLUE, lw=2)
    if b2 != 0:
        ax.plot(xs, (c2 - a2 * xs) / b2, color=ORANGE, lw=2)
    if "x" in d and "y" in d:
        ax.scatter([d["x"]], [d["y"]], s=80, color=RED, zorder=4)
    ax.set_xlim(-1, 8)
    ax.set_ylim(-1, 10)
    return fig


def fig_seq(d: dict[str, Any]):
    a1 = float(d["a1"])
    n = int(d["n"])
    kind = d.get("kind", "arith")
    fig, ax = _fig()
    xs = np.arange(1, n + 1)
    if kind == "arith":
        diff = float(d["d"])
        ys = a1 + (xs - 1) * diff
        ax.set_title("Arithmetic sequence", fontsize=11)
    else:
        r = float(d["r"])
        ys = a1 * (r ** (xs - 1))
        ax.set_title("Geometric sequence", fontsize=11)
    ax.scatter(xs, ys, s=70, color=BLUE, zorder=4)
    ax.plot(xs, ys, color=BLUE, lw=1.2, alpha=0.5)
    ax.set_xlabel("n")
    ax.set_ylabel(r"$a_n$")
    ax.grid(True, alpha=0.28)
    ax.set_xticks(list(xs))
    return fig


def fig_sector(d: dict[str, Any]):
    r = float(d.get("r", 4))
    frac = float(d.get("frac", 0.25))
    fig, ax = _fig(5.0, 5.0)
    ax.set_aspect("equal")
    t = np.linspace(0, 2 * np.pi, 300)
    ax.plot(r * np.cos(t), r * np.sin(t), color="#cbd5e1", lw=1.4)
    wedge = np.linspace(0, 2 * np.pi * frac, 80)
    xs = np.concatenate([[0], r * np.cos(wedge), [0]])
    ys = np.concatenate([[0], r * np.sin(wedge), [0]])
    ax.fill(xs, ys, color="#bfdbfe", ec=BLUE, lw=2)
    ax.set_xlim(-r - 1, r + 1)
    ax.set_ylim(-r - 1, r + 1)
    ax.axis("off")
    ax.set_title("Arc / sector", fontsize=11)
    return fig


def fig_gravity(d: dict[str, Any]):
    factor = float(d.get("factor", 2))
    fig, ax = _fig(6.4, 4.0)
    ax.set_aspect("equal")
    ax.add_patch(Circle((1.6, 1.6), 0.85, fc="#93c5fd", ec=BLUE, lw=2))
    ax.add_patch(Circle((4.6, 1.6), 0.85 * min(factor, 2.2) / 1.4, fc="#fdba74", ec=ORANGE, lw=2))
    ax.text(1.6, 1.6, "same M\nsmaller R", ha="center", va="center", fontsize=8)
    ax.text(4.6, 1.6, f"same M\n{factor:g}× R", ha="center", va="center", fontsize=8)
    ax.set_xlim(0.2, 6.4)
    ax.set_ylim(0.1, 3.2)
    ax.axis("off")
    ax.set_title(r"$g = GM/R^2$", fontsize=11)
    return fig


def fig_wrench(d: dict[str, Any]):
    fig, ax = _fig(6.2, 3.2)
    ax.plot([0.6, 5.2], [1.3, 1.3], color="#57534e", lw=10, solid_capstyle="round")
    ax.add_patch(Circle((0.7, 1.3), 0.28, fc="#a8a29e", ec=INK, lw=2))
    _arrow(ax, 4.6, 1.3, 0, 1.3, RED, r"$\vec F$")
    ax.text(2.6, 0.7, f"r = {d.get('d', '?')} m", ha="center")
    ax.set_xlim(0, 6)
    ax.set_ylim(0.2, 3)
    ax.axis("off")
    ax.set_title("Torque τ = r F (perpendicular)", fontsize=11)
    return fig


FIGURES = {
    "number_line": fig_number_line,
    "two_points": fig_two_points,
    "slope_line": fig_slope_line,
    "parabola": fig_parabola,
    "sqrt_shift": fig_sqrt_shift,
    "abs_v": fig_abs_v,
    "polynomial": fig_polynomial,
    "poly_zeros": fig_poly_zeros,
    "exponential": fig_exponential,
    "log": fig_log,
    "rational": fig_rational,
    "variation": fig_variation,
    "secant": fig_secant,
    "inverse_line": fig_inverse_line,
    "sine": fig_sine,
    "tan": fig_tan,
    "right_triangle": fig_right_triangle,
    "elevation": fig_elevation,
    "polar_point": fig_polar_point,
    "polar_circle": fig_polar_circle,
    "ellipse": fig_ellipse,
    "hyperbola": fig_hyperbola,
    "conic_parabola": fig_conic_parabola,
    "vector": fig_vector,
    "complex": fig_complex,
    "unit_param": fig_unit_param,
    "limit_hole": fig_limit_hole,
    "oblique_triangle": fig_oblique_triangle,
    "projectile": fig_projectile,
    "motion_1d": fig_motion_1d,
    "vt": fig_vt,
    "freefall": fig_freefall,
    "fbd": fig_fbd,
    "ramp": fig_ramp,
    "carts": fig_carts,
    "circle_motion": fig_circle_motion,
    "spring": fig_spring,
    "wave": fig_wave,
    "circuit": fig_circuit,
    "piston": fig_piston,
    "buoyancy": fig_buoyancy,
    "pipe": fig_pipe,
    "charges": fig_charges,
    "efield": fig_efield,
    "magnetic": fig_magnetic,
    "snell": fig_snell,
    "lens": fig_lens,
    "energy_bars": fig_energy_bars,
    "wrench": fig_wrench,
    "quadratic_abc": fig_quadratic_abc,
    "system": fig_system,
    "seq": fig_seq,
    "sector": fig_sector,
    "gravity": fig_gravity,
}


def figure_for(kind: str | None, data: dict[str, Any] | None = None):
    """Return a matplotlib Figure for a problem, or None."""
    if not kind:
        return None
    if kind == "unit_circle":
        from src.plots import unit_circle_figure

        deg = (data or {}).get("deg")
        return unit_circle_figure(highlight_degrees=deg, labeled=True, size=6.2)
    fn = FIGURES.get(kind)
    if fn is None:
        return None
    return fn(data or {})
