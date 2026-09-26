from __future__ import annotations

import html
import json
import random
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, FancyArrowPatch


@dataclass(frozen=True)
class CirclePoint:
    deg: int
    rad: str
    cos: str
    sin: str

    @property
    def rad_disp(self) -> str:
        if self.rad == "0":
            return "0 rad"
        return self.rad.replace("*", "").replace("pi", "π")

    @property
    def rad_tex(self) -> str:
        if self.rad == "0":
            return r"$0$"
        body = self.rad.replace("*", "").replace("pi", r"\pi")
        return rf"${body}$"

    @property
    def coord_disp(self) -> str:
        def pretty(value: str) -> str:
            return value.replace("sqrt", "√").replace("*", "")

        return f"({pretty(self.cos)}, {pretty(self.sin)})"

    @property
    def coord_tex(self) -> str:
        def piece(value: str) -> str:
            neg = value.startswith("-")
            core = value[1:] if neg else value
            mapping = {
                "0": "0",
                "1": "1",
                "1/2": r"1/2",
                "sqrt(2)/2": r"\sqrt{2}/2",
                "sqrt(3)/2": r"\sqrt{3}/2",
            }
            body = mapping.get(core, core)
            return rf"-{body}" if neg else body

        return rf"$({piece(self.cos)},\ {piece(self.sin)})$"

    def rad_accept(self) -> list[str]:
        raw = self.rad
        compact = raw.replace("*", "")
        pretty = compact.replace("pi", "π")
        return [raw, compact, pretty, f"{compact}rad", f"{pretty} rad"]

    def deg_accept(self) -> list[str]:
        return [str(self.deg), f"{self.deg}°", f"{self.deg} deg"]

    def coord_accept(self, value: str) -> list[str]:
        alts = [value, value.replace("sqrt", "√"), value.replace("*", "")]
        if value.replace("-", "") == "sqrt(2)/2":
            sign = "-" if value.startswith("-") else ""
            alts.extend(
                [
                    f"{sign}1/sqrt(2)",
                    f"{sign}√2/2",
                    f"{sign}1/√2",
                ]
            )
        if value in ("1", "-1", "0"):
            alts.append(f"{value}.0")
        return alts


SPECIAL_ANGLES: tuple[CirclePoint, ...] = (
    CirclePoint(0, "0", "1", "0"),
    CirclePoint(30, "pi/6", "sqrt(3)/2", "1/2"),
    CirclePoint(45, "pi/4", "sqrt(2)/2", "sqrt(2)/2"),
    CirclePoint(60, "pi/3", "1/2", "sqrt(3)/2"),
    CirclePoint(90, "pi/2", "0", "1"),
    CirclePoint(120, "2*pi/3", "-1/2", "sqrt(3)/2"),
    CirclePoint(135, "3*pi/4", "-sqrt(2)/2", "sqrt(2)/2"),
    CirclePoint(150, "5*pi/6", "-sqrt(3)/2", "1/2"),
    CirclePoint(180, "pi", "-1", "0"),
    CirclePoint(210, "7*pi/6", "-sqrt(3)/2", "-1/2"),
    CirclePoint(225, "5*pi/4", "-sqrt(2)/2", "-sqrt(2)/2"),
    CirclePoint(240, "4*pi/3", "-1/2", "-sqrt(3)/2"),
    CirclePoint(270, "3*pi/2", "0", "-1"),
    CirclePoint(300, "5*pi/3", "1/2", "-sqrt(3)/2"),
    CirclePoint(315, "7*pi/4", "sqrt(2)/2", "-sqrt(2)/2"),
    CirclePoint(330, "11*pi/6", "sqrt(3)/2", "-1/2"),
)


_LABEL_NUDGE = {
    30: -7,
    60: 8,
    120: -8,
    150: 7,
    210: -7,
    240: 8,
    300: -8,
    330: 7,
}


def _align(deg: int) -> tuple[str, str]:
    rad = np.deg2rad(deg)
    c, s = np.cos(rad), np.sin(rad)
    ha = "center" if abs(c) < 0.2 else ("left" if c > 0 else "right")
    va = "center" if abs(s) < 0.2 else ("bottom" if s > 0 else "top")
    return ha, va


def _label_radius(deg: int) -> tuple[float, float]:
    """Angle-measure radius, then coordinate radius."""
    if deg % 90 == 0:
        return 1.12, 1.28
    if deg % 45 == 0:
        return 1.42, 1.68
    return 1.16, 1.36


def unit_circle_figure(
    highlight_degrees: float | None = None,
    *,
    labeled: bool = True,
    size: float = 8.6,
):
    fig, ax = plt.subplots(figsize=(size, size), facecolor="white")
    ax.set_facecolor("#fbfcfe")
    theta = np.linspace(0, 2 * np.pi, 500)
    ax.plot(np.cos(theta), np.sin(theta), color="#1d4ed8", lw=2.2, zorder=2)
    ax.axhline(0, color="#64748b", lw=0.9, zorder=1)
    ax.axvline(0, color="#64748b", lw=0.9, zorder=1)
    ax.annotate(
        "",
        xy=(2.05, 0),
        xytext=(-2.05, 0),
        arrowprops=dict(arrowstyle="<->", color="#64748b", lw=0.9),
        zorder=1,
    )
    ax.annotate(
        "",
        xy=(0, 2.05),
        xytext=(0, -2.05),
        arrowprops=dict(arrowstyle="<->", color="#64748b", lw=0.9),
        zorder=1,
    )

    for pt in SPECIAL_ANGLES:
        rad = np.deg2rad(pt.deg)
        c, s = np.cos(rad), np.sin(rad)
        ax.plot([0, c], [0, s], color="#cbd5e1", lw=0.8, zorder=1)
        ax.scatter([c], [s], color="#0f172a", s=18, zorder=3)
        if labeled:
            ha, va = _align(pt.deg)
            r_ang, r_xy = _label_radius(pt.deg)
            label_rad = np.deg2rad(pt.deg + _LABEL_NUDGE.get(pt.deg, 0))
            lc, ls = np.cos(label_rad), np.sin(label_rad)
            if pt.deg in (0, 180):
                x = 1.22 * c
                ax.text(
                    x,
                    0.12,
                    f"{pt.deg}°  {pt.rad_disp}",
                    ha=ha,
                    va="bottom",
                    fontsize=8.0,
                    color="#0f172a",
                    fontweight="bold",
                    zorder=4,
                    family="DejaVu Sans",
                )
                ax.text(
                    x,
                    -0.12,
                    pt.coord_tex,
                    ha=ha,
                    va="top",
                    fontsize=7.6,
                    color="#1e3a8a",
                    zorder=4,
                )
            else:
                ax.text(
                    r_ang * lc,
                    r_ang * ls,
                    f"{pt.deg}°  {pt.rad_disp}",
                    ha=ha,
                    va=va,
                    fontsize=8.0,
                    color="#0f172a",
                    fontweight="bold",
                    zorder=4,
                    family="DejaVu Sans",
                )
                ax.text(
                    r_xy * lc,
                    r_xy * ls,
                    pt.coord_tex,
                    ha=ha,
                    va=va,
                    fontsize=7.6,
                    color="#1e3a8a",
                    zorder=4,
                )

    if highlight_degrees is not None:
        rad = np.deg2rad(highlight_degrees)
        ax.scatter([np.cos(rad)], [np.sin(rad)], color="#dc2626", s=48, zorder=5)
        ax.plot([0, np.cos(rad)], [0, np.sin(rad)], color="#dc2626", lw=2, zorder=4)

    if labeled:
        ax.text(0.42, 0.42, "I  ALL +", color="#94a3b8", fontsize=8, ha="center")
        ax.text(-0.42, 0.42, "II  SIN +", color="#94a3b8", fontsize=8, ha="center")
        ax.text(-0.42, -0.42, "III  TAN +", color="#94a3b8", fontsize=8, ha="center")
        ax.text(0.42, -0.42, "IV  COS +", color="#94a3b8", fontsize=8, ha="center")
        arc = Arc((0, 0), 0.62, 0.62, theta1=6, theta2=48, color="#64748b", lw=1.1)
        ax.add_patch(arc)
        tip = np.deg2rad(48)
        ax.add_patch(
            FancyArrowPatch(
                (0.31 * np.cos(tip - 0.08), 0.31 * np.sin(tip - 0.08)),
                (0.31 * np.cos(tip), 0.31 * np.sin(tip)),
                arrowstyle="-|>",
                mutation_scale=9,
                color="#64748b",
                lw=1.1,
            )
        )
        ax.text(0.46, 0.14, "positive", color="#64748b", fontsize=7.5)
        ax.text(2.10, -0.14, r"$x=\cos\theta$", fontsize=9, color="#0f172a", ha="right")
        ax.text(0.08, 2.10, r"$y=\sin\theta$", fontsize=9, color="#0f172a", va="top")

    ax.set_aspect("equal")
    ax.set_xlim(-2.15, 2.15)
    ax.set_ylim(-2.15, 2.15)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(r"Unit circle  ·  radius 1  ·  $P=(\cos\theta,\ \sin\theta)$")
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.subplots_adjust(left=0.04, right=0.98, top=0.94, bottom=0.04)
    return fig


def _station_offset_pct(deg: int) -> float:
    if deg % 90 == 0:
        return 9.0
    if deg % 45 == 0:
        return 15.5
    return 11.5


def unit_circle_value_table() -> str:
    lines = [
        "| Degrees | Radians | cos θ (x) | sin θ (y) |",
        "| ---: | ---: | --- | --- |",
    ]
    for pt in SPECIAL_ANGLES:
        lines.append(f"| {pt.deg}° | {pt.rad_disp} | `{pt.cos}` | `{pt.sin}` |")
    return "\n".join(lines)


def _pretty_coord(value: str) -> str:
    return value.replace("sqrt(", "√").replace(")", "").replace("*", "")


_COORD_ORDER = (
    "1",
    "sqrt(3)/2",
    "sqrt(2)/2",
    "1/2",
    "0",
    "-1/2",
    "-sqrt(2)/2",
    "-sqrt(3)/2",
    "-1",
)

_DEG_CHOICES = [(str(pt.deg), f"{pt.deg}°") for pt in SPECIAL_ANGLES]
_RAD_CHOICES = [(pt.rad.replace("*", ""), pt.rad_disp) for pt in SPECIAL_ANGLES]
_COORD_CHOICES = [(value, _pretty_coord(value)) for value in _COORD_ORDER]
_FIELD_CHOICES = {
    "deg": _DEG_CHOICES,
    "rad": _RAD_CHOICES,
    "cos": _COORD_CHOICES,
    "sin": _COORD_CHOICES,
}


def _select_html(kind: str, seed: str, *, select_id: str = "", aria: str = "") -> str:
    items = list(_FIELD_CHOICES[kind])
    random.Random(seed).shuffle(items)
    opts = ['<option value="">Choose…</option>']
    for value, label in items:
        opts.append(
            f'<option value="{html.escape(value)}">{html.escape(label)}</option>'
        )
    id_attr = f' id="{html.escape(select_id)}"' if select_id else ""
    aria_attr = f' aria-label="{html.escape(aria)}"' if aria else ""
    return (
        f'<select data-k="{kind}"{id_attr}{aria_attr}>{"".join(opts)}</select>'
    )


def unit_circle_practice_html(mode: str = "coordinates") -> str:
    """Responsive unit-circle drill. Phones tap a ray; wider screens fill around the circle."""
    cx = cy = 50.0
    radius = 32.0
    show_deg = mode in ("coordinates", "radians")
    show_rad = mode in ("coordinates", "degrees")
    show_xy = mode in ("radians", "degrees")
    stations = []
    hits = []
    key = []
    options = []
    for pt in SPECIAL_ANGLES:
        rad = np.deg2rad(pt.deg)
        extra = _station_offset_pct(pt.deg)
        left = cx + (radius + extra) * np.cos(rad)
        top = cy - (radius + extra) * np.sin(rad)
        hx = cx + radius * np.cos(rad)
        hy = cy - radius * np.sin(rad)
        deg_html = (
            f'<div class="given">{pt.deg}°</div>'
            if show_deg
            else _select_html("deg", f"{pt.deg}-deg", aria=f"degrees at {pt.deg} degrees")
        )
        rad_html = (
            f'<div class="given">{html.escape(pt.rad_disp)}</div>'
            if show_rad
            else _select_html("rad", f"{pt.deg}-rad", aria=f"radians at {pt.deg} degrees")
        )
        if show_xy:
            xy_html = f'<div class="given xy">{html.escape(pt.coord_disp)}</div>'
        else:
            xy_html = (
                '<div class="xy-inputs">'
                + _select_html("cos", f"{pt.deg}-cos", aria=f"cosine at {pt.deg} degrees")
                + _select_html("sin", f"{pt.deg}-sin", aria=f"sine at {pt.deg} degrees")
                + "</div>"
            )
        stations.append(
            f'<div class="station" data-deg="{pt.deg}" style="left:{left:.2f}%;top:{top:.2f}%">'
            f"{deg_html}{rad_html}{xy_html}</div>"
        )
        hits.append(
            f'<circle class="status" data-deg="{pt.deg}" cx="{hx:.2f}" cy="{hy:.2f}" r="2.3"/>'
            f'<circle class="dot" cx="{hx:.2f}" cy="{hy:.2f}" r="1.15"/>'
            f'<circle class="hit" data-deg="{pt.deg}" cx="{hx:.2f}" cy="{hy:.2f}" r="6.5" '
            f'tabindex="0" role="button" aria-label="{pt.deg} degrees"/>'
        )
        options.append(f'<option value="{pt.deg}">{pt.deg}° · {html.escape(pt.rad_disp)}</option>')
        key.append(
            {
                "deg": pt.deg,
                "degAccept": pt.deg_accept(),
                "radAccept": pt.rad_accept(),
                "cosAccept": pt.coord_accept(pt.cos),
                "sinAccept": pt.coord_accept(pt.sin),
                "radDisp": pt.rad_disp,
                "coordDisp": pt.coord_disp,
                "degValue": str(pt.deg),
                "radValue": pt.rad.replace("*", ""),
                "cosValue": pt.cos,
                "sinValue": pt.sin,
            }
        )
    editor_bits = []
    if not show_deg:
        editor_bits.append(
            "<label>Degrees"
            + _select_html("deg", "ed-deg", select_id="ed-deg", aria="degrees")
            + "</label>"
        )
    else:
        editor_bits.append('<div class="ed-given" id="ed-deg-given"></div>')
    if not show_rad:
        editor_bits.append(
            "<label>Radians"
            + _select_html("rad", "ed-rad", select_id="ed-rad", aria="radians")
            + "</label>"
        )
    else:
        editor_bits.append('<div class="ed-given" id="ed-rad-given"></div>')
    if not show_xy:
        editor_bits.append(
            '<div class="xy-inputs">'
            "<label>x = cos"
            + _select_html("cos", "ed-cos", select_id="ed-cos", aria="cosine")
            + "</label>"
            "<label>y = sin"
            + _select_html("sin", "ed-sin", select_id="ed-sin", aria="sine")
            + "</label>"
            "</div>"
        )
    else:
        editor_bits.append('<div class="ed-given" id="ed-xy-given"></div>')

    key_json = json.dumps(key)
    return f"""
<div id="uc-drill">
<style>
  html, body {{ margin: 0; background: #0e1117; color: #e8eef8; }}
  #uc-drill {{ color: #e8eef8; font-family: inherit; max-width: 100%; }}
  #uc-drill * {{ box-sizing: border-box; }}
  #uc-drill .hint {{ font-size: 0.95rem; color: #9aa8bc; margin: 0 0 0.6rem; }}
  #uc-drill .bar, #uc-drill .editor-nav {{
    display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap; margin: 0 0 0.7rem;
  }}
  #uc-drill button {{
    background: #1f2a3d; color: #e8eef8; border: 1px solid #3d4b61; border-radius: 10px;
    padding: 0.65rem 0.9rem; min-height: 44px; font-size: 1rem; cursor: pointer;
    touch-action: manipulation; flex: 1 1 auto;
  }}
  #uc-drill button.primary {{ background: #e11d48; border-color: #e11d48; font-weight: 600; }}
  #uc-drill #score {{ min-height: 1.3em; font-size: 0.95rem; color: #cbd5e1; flex: 1 1 100%; }}
  #uc-drill .jump {{
    display: flex; flex-direction: column; gap: 0.25rem; margin: 0 0 0.7rem; font-size: 0.95rem;
  }}
  #uc-drill .jump select, #uc-drill select, #uc-drill label {{
    font-size: 16px; min-height: 44px;
  }}
  #uc-drill .jump select, #uc-drill select {{
    width: 100%; padding: 0.55rem 0.5rem; border-radius: 8px; border: 1px solid #3d4b61;
    background: #111827; color: #f8fafc; color-scheme: dark;
  }}
  #uc-drill .board {{
    position: relative; width: 100%; max-width: min(100%, 720px); aspect-ratio: 1 / 1;
    margin: 0 auto; touch-action: manipulation;
  }}
  #uc-drill svg {{ width: 100%; height: 100%; display: block; }}
  #uc-drill .circle {{ fill: none; stroke: #6ea8fe; stroke-width: 0.7; }}
  #uc-drill .axis {{ stroke: #8b9bb0; stroke-width: 0.35; }}
  #uc-drill .ray {{ stroke: #3d4b61; stroke-width: 0.28; }}
  #uc-drill .dot {{ fill: #e8eef8; pointer-events: none; }}
  #uc-drill .status {{ fill: none; stroke: #3d4b61; stroke-width: 0.45; pointer-events: none; }}
  #uc-drill .status.ok {{ stroke: #3dd68c; }}
  #uc-drill .status.bad {{ stroke: #f87171; }}
  #uc-drill .status.sel {{ stroke: #6ea8fe; stroke-width: 0.7; }}
  #uc-drill .hit {{ fill: transparent; cursor: pointer; }}
  #uc-drill .axis-label, #uc-drill .quad {{ fill: #9aa8bc; font-size: 3.2px; }}
  #uc-drill .station {{
    position: absolute; transform: translate(-50%, -50%); width: 7.6rem; text-align: center;
    display: none;
  }}
  #uc-drill .given {{ font-size: 0.75rem; color: #dbe7f6; line-height: 1.25; }}
  #uc-drill .given.xy {{ color: #9fb0c5; font-size: 0.7rem; }}
  #uc-drill .station select {{ min-height: 36px; margin: 2px 0; font-size: 13px; padding: 0.2rem 0.2rem; }}
  #uc-drill .xy-inputs {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0.4rem; }}
  #uc-drill .ok select {{ border-color: #3dd68c; background: #052e16; }}
  #uc-drill select.mismatch {{ border-color: #f87171; background: #3f0d12; }}
  #uc-drill .editor {{
    display: block; margin-top: 0.85rem; padding: 0.9rem; border: 1px solid #3d4b61;
    border-radius: 12px; background: #111827;
  }}
  #uc-drill .editor h3 {{ margin: 0 0 0.6rem; font-size: 1.05rem; }}
  #uc-drill .editor label {{ display: flex; flex-direction: column; gap: 0.25rem; margin: 0 0 0.55rem; }}
  #uc-drill .ed-given {{ font-size: 1.05rem; margin: 0 0 0.45rem; color: #dbe7f6; }}
  @media (min-width: 900px) {{
    #uc-drill .station {{ display: block; }}
    #uc-drill .editor {{ display: none; }}
    #uc-drill .jump {{ display: none; }}
    #uc-drill #score {{ flex: 1 1 auto; }}
    #uc-drill button {{ flex: 0 0 auto; }}
  }}
</style>
<p class="hint">Cosine is <b>x</b>, sine is <b>y</b>. Pick the matching value from each menu. On a phone, tap a point (or pick it from the list), then choose from the menus in the card below.</p>
<div class="bar">
  <button type="button" class="primary" id="uc-check">Check</button>
  <button type="button" id="uc-reveal">Reveal</button>
  <button type="button" id="uc-clear">Clear</button>
  <span id="score"></span>
</div>
<label class="jump">Angle
  <select id="jump">{"".join(options)}</select>
</label>
<div class="board">
  <svg viewBox="0 0 100 100" role="img" aria-label="Unit circle. Tap a special angle to fill it in.">
    <line x1="8" y1="50" x2="92" y2="50" class="axis"/>
    <line x1="50" y1="8" x2="50" y2="92" class="axis"/>
    <circle cx="50" cy="50" r="{radius}" class="circle"/>
    {"".join(f'<line x1="50" y1="50" x2="{50 + radius * np.cos(np.deg2rad(pt.deg)):.2f}" y2="{50 - radius * np.sin(np.deg2rad(pt.deg)):.2f}" class="ray"/>' for pt in SPECIAL_ANGLES)}
    {"".join(hits)}
    <text x="90" y="54.5" class="axis-label" text-anchor="end">x = cos θ</text>
    <text x="51.5" y="7.2" class="axis-label">y = sin θ</text>
    <text x="62" y="38" class="quad">I ALL +</text>
    <text x="24" y="38" class="quad">II SIN +</text>
    <text x="23" y="66" class="quad">III TAN +</text>
    <text x="62" y="66" class="quad">IV COS +</text>
  </svg>
  {"".join(stations)}
</div>
<div class="editor" id="editor">
  <h3 id="ed-title">0°</h3>
  {"".join(editor_bits)}
  <div class="editor-nav">
    <button type="button" id="uc-prev">Previous</button>
    <button type="button" id="uc-next">Next</button>
  </div>
</div>
<script>
(function () {{
  const root = document.getElementById("uc-drill");
  if (!root) return;
  const KEY = {key_json};
  const DEGS = KEY.map((row) => row.deg);
  let selected = 0;
  function station(deg) {{ return root.querySelector('.station[data-deg="' + deg + '"]'); }}
  function fields(scope) {{
    return {{
      deg: scope.querySelector('[data-k="deg"]'),
      rad: scope.querySelector('[data-k="rad"]'),
      cos: scope.querySelector('[data-k="cos"]'),
      sin: scope.querySelector('[data-k="sin"]'),
    }};
  }}
  function norm(s) {{
    return (s || "").trim().toLowerCase()
      .replace(/°/g, "").replace(/degrees?/g, "").replace(/radians?/g, "")
      .replace(/π/g, "pi").replace(/√/g, "sqrt").replace(/\\s+/g, "").replace(/\\*/g, "");
  }}
  function matches(val, accept) {{
    const n = norm(val);
    return accept.some((a) => norm(a) === n);
  }}
  function syncEditorFromStation() {{
    const st = station(selected);
    const k = KEY.find((row) => row.deg === selected);
    const src = fields(st);
    const ed = fields(root.querySelector("#editor"));
    const title = root.querySelector("#ed-title");
    if (title) title.textContent = selected + "°";
    const jump = root.querySelector("#jump");
    if (jump) jump.value = String(selected);
    root.querySelectorAll(".status").forEach((el) => el.classList.toggle("sel", Number(el.dataset.deg) === selected));
    ["deg", "rad", "cos", "sin"].forEach((name) => {{
      if (ed[name] && src[name]) {{
        ed[name].value = src[name].value;
        ed[name].classList.toggle("mismatch", src[name].classList.contains("mismatch"));
      }}
    }});
    const dg = root.querySelector("#ed-deg-given");
    const rg = root.querySelector("#ed-rad-given");
    const xg = root.querySelector("#ed-xy-given");
    if (dg) dg.textContent = selected + "°";
    if (rg) rg.textContent = k.radDisp;
    if (xg) xg.textContent = k.coordDisp;
  }}
  function syncStationFromEditor() {{
    const st = station(selected);
    const src = fields(root.querySelector("#editor"));
    const dst = fields(st);
    ["deg", "rad", "cos", "sin"].forEach((k) => {{
      if (src[k] && dst[k]) dst[k].value = src[k].value;
    }});
  }}
  function selectAngle(deg) {{
    selected = Number(deg);
    syncEditorFromStation();
  }}
  root.querySelectorAll(".hit").forEach((el) => {{
    const go = () => selectAngle(el.dataset.deg);
    el.addEventListener("click", go);
    el.addEventListener("keydown", (ev) => {{
      if (ev.key === "Enter" || ev.key === " ") {{ ev.preventDefault(); go(); }}
    }});
  }});
  const jump = root.querySelector("#jump");
  if (jump) jump.addEventListener("change", () => selectAngle(jump.value));
  const editor = root.querySelector("#editor");
  editor.addEventListener("change", syncStationFromEditor);
  editor.addEventListener("input", syncStationFromEditor);
  root.querySelector("#uc-prev").addEventListener("click", () => {{
    const i = DEGS.indexOf(selected);
    selectAngle(DEGS[(i - 1 + DEGS.length) % DEGS.length]);
  }});
  root.querySelector("#uc-next").addEventListener("click", () => {{
    const i = DEGS.indexOf(selected);
    selectAngle(DEGS[(i + 1) % DEGS.length]);
  }});
  root.querySelector("#uc-check").addEventListener("click", () => {{
    syncStationFromEditor();
    let need = 0, good = 0;
    KEY.forEach((k) => {{
      const st = station(k.deg);
      const f = fields(st);
      st.classList.remove("ok", "bad");
      const status = root.querySelector('.status[data-deg="' + k.deg + '"]');
      if (status) status.classList.remove("ok", "bad");
      let stationOk = true;
      let used = false;
      const grade = (input, accept) => {{
        if (!input) return;
        used = true;
        need += 1;
        input.classList.remove("mismatch");
        if (matches(input.value, accept)) {{ good += 1; }}
        else {{ stationOk = false; input.classList.add("mismatch"); }}
      }};
      grade(f.deg, k.degAccept);
      grade(f.rad, k.radAccept);
      grade(f.cos, k.cosAccept);
      grade(f.sin, k.sinAccept);
      if (used) {{
        st.classList.add(stationOk ? "ok" : "bad");
        if (status) status.classList.add(stationOk ? "ok" : "bad");
      }}
    }});
    root.querySelector("#score").textContent = need ? (good + " / " + need + " blanks correct") : "";
    syncEditorFromStation();
  }});
  root.querySelector("#uc-reveal").addEventListener("click", () => {{
    KEY.forEach((k) => {{
      const st = station(k.deg);
      const f = fields(st);
      if (f.deg) f.deg.value = k.degValue;
      if (f.rad) f.rad.value = k.radValue;
      if (f.cos) f.cos.value = k.cosValue;
      if (f.sin) f.sin.value = k.sinValue;
      st.classList.remove("bad");
      st.classList.add("ok");
      Object.values(f).forEach((el) => el && el.classList.remove("mismatch"));
      const status = root.querySelector('.status[data-deg="' + k.deg + '"]');
      if (status) {{ status.classList.remove("bad"); status.classList.add("ok"); }}
    }});
    root.querySelector("#score").textContent = "Revealed. Clear and try again without looking.";
    syncEditorFromStation();
  }});
  root.querySelector("#uc-clear").addEventListener("click", () => {{
    root.querySelectorAll("select[data-k]").forEach((el) => {{
      el.value = "";
      el.classList.remove("mismatch");
    }});
    root.querySelectorAll(".station, .status").forEach((el) => el.classList.remove("ok", "bad"));
    root.querySelector("#score").textContent = "";
    syncEditorFromStation();
  }});
  selectAngle(0);
}})();
</script>
</div>
"""
