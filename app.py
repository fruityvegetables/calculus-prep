from __future__ import annotations

import random

import streamlit as st
import streamlit.components.v1 as components

from src.check import answers_match
from src.curriculum import (
    TRACKS,
    all_skills,
    format_skill_title,
    locate_skill_on_track,
    physics_skill_ids,
    precalc_skill_ids,
    relevance_line,
    skill_by_id,
    skills_with_tag,
    track_by_id,
    track_skill_ids,
)
from src.generate import ensure_all_generators
from src.load import (
    STAGES,
    generate_for_skill,
    problems_for_stage,
    recommend,
)
from src.diagnostic_bank import SET_ORDER, set_by_id  # four diagnostic forms
from src.flashcards import (
    FAMILY_LABEL as CARD_FAMILY_LABEL,
    FAMILY_ORDER as CARD_FAMILY_ORDER,
    flashcards_for,
    shuffled_ids,
)
from src.identities import (
    FAMILY_LABEL,
    FAMILY_ORDER,
    identities_for,
    identities_practice_html,
    grouped_identities,
)
from src.figures import figure_for
from src.handwriting import handwriting_pad
from src.keypad import apply_key
from src.plots import (
    unit_circle_figure,
    unit_circle_practice_html,
    unit_circle_value_table,
)
from src.progress import empty_progress, record_attempt, record_diagnostic, to_json
from src.schema import Problem

ensure_all_generators()

st.set_page_config(
    page_title="Algebra · Trig · Precalculus",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def _empty_diag() -> dict:
    return {
        "set_id": None,
        "stage": 1,
        "index": 0,
        "results": {},
        "finished": False,
        "recommendation": None,
        "awaiting": True,
        "last_correct": None,
    }


if "progress" not in st.session_state:
    st.session_state.progress = empty_progress()
if "page" not in st.session_state:
    st.session_state.page = "Home"
elif st.session_state.page == "Formula flashcards":
    st.session_state.page = "Flashcards"
elif st.session_state.page == "Extra practice":
    st.session_state.page = "Extra"
if st.session_state.get("main-nav") == "Formula flashcards":
    st.session_state["main-nav"] = "Flashcards"
if st.session_state.get("main-nav") == "Extra practice":
    st.session_state["main-nav"] = "Extra"
if "diag" not in st.session_state:
    st.session_state.diag = _empty_diag()
if "study" not in st.session_state:
    st.session_state.study = {
        "course": "precalc",
        "unit": "pc-fn",
        "skill_id": "alg-3-1",
        "seed": 1,
        "problem": None,
        "checked": False,
        "correct": None,
    }
if "extra" not in st.session_state:
    st.session_state.extra = {
        "course": "All courses",
        "seed": 1,
        "problem": None,
        "skill_id": None,
        "checked": False,
        "correct": None,
    }
if "physics" not in st.session_state:
    st.session_state.physics = {
        "pool": "Physics 1",
        "seed": 1,
        "problem": None,
        "skill_id": None,
        "checked": False,
        "correct": None,
    }


PAGES = [
    "Home",
    "Diagnostic",
    "Study",
    "Physics",
    "Unit circle",
    "Identities",
    "Flashcards",
    "Extra",
    "Progress",
]

APP_CSS = """
<style>
  .stApp { overflow-x: clip; }
  [data-testid="stSidebar"],
  [data-testid="stSidebarCollapsedControl"],
  [data-testid="stSidebarCollapseButton"] { display: none !important; }
  [data-testid="stHeader"] {
    display: flex !important;
    background: var(--background-color, #0e1117) !important;
    z-index: 1000;
  }
  [data-testid="stMainBlockContainer"] {
    padding-top: 0.9rem;
    padding-left: max(0.85rem, env(safe-area-inset-left));
    padding-right: max(0.85rem, env(safe-area-inset-right));
    padding-bottom: max(1.4rem, env(safe-area-inset-bottom));
    max-width: min(960px, 100%);
    margin-left: auto;
    margin-right: auto;
  }
  [data-testid="stElementContainer"]:has(.app-nav),
  [data-testid="stVerticalBlockBorderWrapper"]:has(.app-nav) { display: none; }
  [data-testid="stElementContainer"]:has(.app-nav) + [data-testid="stElementContainer"],
  [data-testid="stVerticalBlockBorderWrapper"]:has(.app-nav) + [data-testid="stVerticalBlockBorderWrapper"] {
    position: sticky;
    top: 4.25rem;
    z-index: 999;
    background: var(--background-color, #0e1117);
    padding-top: 0.7rem;
    padding-bottom: 0.5rem;
    margin-bottom: 0.15rem;
    border-bottom: 1px solid #243044;
    overflow: visible;
  }
  @media (min-width: 768px) {
    [data-testid="stMainBlockContainer"] {
      padding-left: 1.5rem;
      padding-right: 1.5rem;
    }
  }
  h1 { font-size: 1.7rem !important; line-height: 1.2 !important; letter-spacing: -0.02em; margin-bottom: 0.35rem !important; }
  h2 { font-size: 1.2rem !important; }
  h3 { font-size: 1.05rem !important; }
  @media (min-width: 768px) {
    h1 { font-size: 1.95rem !important; }
  }
  [data-testid="stCaptionContainer"] { color: #9aa8bc !important; }
  .stButton button, .stDownloadButton button, .stFormSubmitButton button {
    min-height: 44px;
    width: 100%;
    font-size: 0.98rem !important;
    touch-action: manipulation;
  }
  .stTextInput input, .stNumberInput input, .stSelectbox input,
  .stTextArea textarea, [data-baseweb="select"] input {
    min-height: 44px !important;
    font-size: 16px !important;
  }
  [data-testid="stPyplot"], [data-testid="stImage"] {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    max-width: 100%;
  }
  [data-testid="stPyplot"] img {
    min-width: min(100%, 560px);
    height: auto !important;
  }
  @media (min-width: 700px) {
    [data-testid="stPyplot"] img { min-width: 0; width: 100%; }
  }
  @media (max-width: 640px) {
    div[data-testid="stHorizontalBlock"] {
      flex-wrap: wrap !important;
      gap: 0.45rem !important;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
      min-width: 100% !important;
      flex: 1 1 100% !important;
    }
  }
  [data-testid="stButtonGroup"] {
    flex-wrap: wrap !important;
    gap: 0.35rem !important;
    justify-content: flex-start !important;
    overflow: visible !important;
  }
  [data-testid="stButtonGroup"] button { min-height: 38px; width: auto !important; flex: 0 0 auto !important; }
  .stMarkdown, .stCaption, .stAlert { overflow-wrap: anywhere; word-break: break-word; }
  [data-testid="stExpander"] summary { min-height: 44px; }
  [data-testid="stAlert"] { margin-top: 0.4rem; margin-bottom: 0.4rem; }
  .st-key-answer-keypad {
    max-width: 22rem;
    margin-top: 0.15rem;
  }
  .st-key-answer-keypad [data-testid="stVerticalBlock"] {
    gap: 0.35rem !important;
  }
  .st-key-answer-keypad [data-testid="stHorizontalBlock"] {
    flex-wrap: nowrap !important;
    gap: 0.35rem !important;
  }
  .st-key-answer-keypad [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
    min-width: 0 !important;
    width: auto !important;
    flex: 1 1 0 !important;
  }
  .st-key-answer-keypad .stButton button {
    min-height: 44px;
    padding-left: 0.15rem;
    padding-right: 0.15rem;
    font-size: 1.05rem !important;
  }
  .st-key-answer-actions {
    max-width: 22rem;
  }
  .st-key-answer-actions [data-testid="stVerticalBlock"] {
    gap: 0.35rem !important;
  }
  .st-key-answer-actions [data-testid="stHorizontalBlock"] {
    flex-wrap: nowrap !important;
    gap: 0.35rem !important;
  }
  .st-key-answer-actions [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
    min-width: 0 !important;
    width: auto !important;
    flex: 1 1 0 !important;
  }
  .stElementContainer[class*="st-key-"][class*="-check"] button,
  .stElementContainer[class*="st-key-"][class*="-hint"] button,
  .stElementContainer[class*="st-key-"][class*="-sol"] button,
  .stElementContainer[class*="st-key-"][class*="-new"] button {
    position: relative;
    overflow: hidden;
    padding-right: 1.65rem !important;
  }
  .stElementContainer[class*="st-key-"][class*="-check"] button::before,
  .stElementContainer[class*="st-key-"][class*="-hint"] button::before,
  .stElementContainer[class*="st-key-"][class*="-sol"] button::before,
  .stElementContainer[class*="st-key-"][class*="-new"] button::before {
    position: absolute;
    right: 0.22rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1.35rem;
    line-height: 1;
    opacity: 0.92;
    pointer-events: none;
    z-index: 0;
    font-family: "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", sans-serif;
  }
  .stElementContainer[class*="st-key-"][class*="-check"] button > *,
  .stElementContainer[class*="st-key-"][class*="-hint"] button > *,
  .stElementContainer[class*="st-key-"][class*="-sol"] button > *,
  .stElementContainer[class*="st-key-"][class*="-new"] button > * {
    position: relative;
    z-index: 1;
  }
  .stElementContainer[class*="st-key-"][class*="-check"] button::before { content: "⬇️"; }
  .stElementContainer[class*="st-key-"][class*="-hint"] button::before { content: "💡"; }
  .stElementContainer[class*="st-key-"][class*="-sol"] button::before { content: "🪜"; }
  .stElementContainer[class*="st-key-"][class*="-new"] button::before { content: "➡️"; }
  .stButton button:focus-visible,
  .stDownloadButton button:focus-visible,
  [data-testid="stButtonGroup"] button:focus-visible {
    outline: 3px solid #f8fafc !important;
    outline-offset: 2px !important;
    box-shadow: 0 0 0 5px #111111 !important;
  }
  [data-testid="stLayoutWrapper"]:has(.st-key-app-bar) {
    position: sticky;
    top: 4.25rem;
    z-index: 999;
    background: var(--background-color, #0e1117);
  }
  .st-key-app-bar {
    background: var(--background-color, #0e1117);
    padding-top: 0.15rem;
    padding-bottom: 0.35rem;
    border-bottom: 1px solid #243044;
  }
  .st-key-app-bar [data-testid="stVerticalBlock"] { gap: 0.45rem !important; }
  .st-key-color-vision-menu { max-width: 16rem; margin-bottom: 0.1rem; }
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      transition-duration: 0.01ms !important;
    }
  }
</style>
"""


# bg, border, text, hover background, hover border, border style
_Swatch = tuple[str, str, str, str, str, str]

# Palettes stay apart for that kind of vision. They are not simulations.
# Green-blind and red-blind share the red/green confusion, but red-blind also
# darkens reds, so those two sets use different lightness.
_COLOR_VISION: dict[str, dict[str, _Swatch]] = {
    "Standard": {
        "check": ("#14643a", "#1b7a48", "#ffffff", "#1a7a48", "#229456", "solid"),
        "new": ("#8a1e2d", "#a3283a", "#ffffff", "#a32638", "#bc3146", "solid"),
        "sol": ("#1a4f92", "#2464b0", "#ffffff", "#215eab", "#2d74c9", "solid"),
        "hint": ("#e2b000", "#c99700", "#1c1404", "#f0c21a", "#d7a800", "solid"),
        "key": ("#2f5f86", "#3d729c", "#f4f8fc", "#3a719c", "#4d86b4", "solid"),
        "key_down": ("#274f70", "#32648a", "#ffffff", "#274f70", "#32648a", "solid"),
        "ok": ("#123d28", "#3dcea0", "#e9fff2", "#123d28", "#3dcea0", "solid"),
        "bad": ("#4a1520", "#ff8fa0", "#ffe8ec", "#4a1520", "#ff8fa0", "solid"),
    },
    "Green-blind": {
        "check": ("#0b4f9c", "#1a66c2", "#ffffff", "#1464c0", "#2a78d4", "solid"),
        "new": ("#c45c00", "#e07012", "#ffffff", "#d66a08", "#f08420", "solid"),
        "sol": ("#5b2c8a", "#7340a8", "#ffffff", "#6c38a4", "#8554bc", "solid"),
        "hint": ("#f0c400", "#d7ae00", "#1c1404", "#ffd24a", "#e0b800", "solid"),
        "key": ("#1c4558", "#2c647c", "#f4f8fc", "#27586e", "#3a7a94", "solid"),
        "key_down": ("#163644", "#245066", "#ffffff", "#163644", "#245066", "solid"),
        "ok": ("#0c2f55", "#7eb6ff", "#e7f1ff", "#0c2f55", "#7eb6ff", "solid"),
        "bad": ("#4a2a08", "#ffb15a", "#fff1e0", "#4a2a08", "#ffb15a", "solid"),
    },
    "Red-blind": {
        "check": ("#0e5f78", "#16809e", "#ffffff", "#14748f", "#1e96b8", "solid"),
        "new": ("#f0a202", "#ffc14d", "#1c1404", "#ffb423", "#ffd06a", "solid"),
        "sol": ("#1d4ed8", "#3b6ef0", "#ffffff", "#2a5ce0", "#4d7ef5", "solid"),
        "hint": ("#ffe56a", "#f5d000", "#1c1404", "#fff09a", "#ffe56a", "solid"),
        "key": ("#3a4a63", "#516380", "#f4f8fc", "#4a5d7a", "#647898", "solid"),
        "key_down": ("#2c384c", "#42506a", "#ffffff", "#2c384c", "#42506a", "solid"),
        "ok": ("#08343f", "#7ee0f2", "#e7fbff", "#08343f", "#7ee0f2", "solid"),
        "bad": ("#4a3808", "#ffd36a", "#fff6dc", "#4a3808", "#ffd36a", "solid"),
    },
    "Blue-yellow": {
        "check": ("#0f6b3c", "#188a4e", "#ffffff", "#16854a", "#22a35c", "solid"),
        "new": ("#9b1c2c", "#c12a3e", "#ffffff", "#b42334", "#d43b50", "solid"),
        "sol": ("#2a2a2e", "#d4d4d8", "#ffffff", "#3a3a40", "#f4f4f5", "solid"),
        "hint": ("#f4f0e8", "#d6d0c4", "#1c1404", "#fffdf8", "#e7e1d6", "solid"),
        "key": ("#4b5563", "#6b7280", "#ffffff", "#5c6775", "#9ca3af", "solid"),
        "key_down": ("#374151", "#4b5563", "#ffffff", "#374151", "#4b5563", "solid"),
        "ok": ("#0d3320", "#4ade80", "#e9fff2", "#0d3320", "#4ade80", "solid"),
        "bad": ("#4a1218", "#fb7185", "#ffe4ea", "#4a1218", "#fb7185", "solid"),
    },
    "Grayscale": {
        "check": ("#f4f4f5", "#ffffff", "#111111", "#ffffff", "#e4e4e7", "solid"),
        "new": ("#18181b", "#d4d4d8", "#ffffff", "#27272a", "#f4f4f5", "dashed"),
        "sol": ("#52525b", "#a1a1aa", "#ffffff", "#3f3f46", "#d4d4d8", "solid"),
        "hint": ("#d4d4d8", "#e4e4e7", "#111111", "#e4e4e7", "#f4f4f5", "solid"),
        "key": ("#3f3f46", "#71717a", "#ffffff", "#52525b", "#a1a1aa", "solid"),
        "key_down": ("#27272a", "#52525b", "#ffffff", "#27272a", "#52525b", "solid"),
        "ok": ("#f4f4f5", "#111111", "#111111", "#f4f4f5", "#111111", "solid"),
        "bad": ("#18181b", "#f4f4f5", "#ffffff", "#18181b", "#f4f4f5", "dashed"),
    },
}


def _color_mode() -> str:
    mode = st.session_state.get("color-vision-menu") or st.session_state.get("color-vision") or "Standard"
    return mode if mode in _COLOR_VISION else "Standard"


def _swatch_button(selector: str, swatch: _Swatch) -> str:
    bg, border, fg, hover_bg, hover_border, style = swatch
    return f"""
    {selector} {{
      background: {bg} !important;
      border-color: {border} !important;
      border-style: {style} !important;
      color: {fg} !important;
    }}
    {selector}:hover, {selector}:focus {{
      background: {hover_bg} !important;
      border-color: {hover_border} !important;
      color: {fg} !important;
    }}
    {selector} p {{ color: inherit !important; }}
    """


def _color_css(mode: str) -> str:
    palette = _COLOR_VISION[mode]
    parts = [
        "<style>",
        _swatch_button(
            '.stElementContainer[class*="st-key-"][class*="-check"] button',
            palette["check"],
        ),
        _swatch_button(
            '.stElementContainer[class*="st-key-"][class*="-new"] button',
            palette["new"],
        ),
        _swatch_button(
            '.stElementContainer[class*="st-key-"][class*="-sol"] button',
            palette["sol"],
        ),
        _swatch_button(
            '.stElementContainer[class*="st-key-"][class*="-hint"] button',
            palette["hint"],
        ),
        _swatch_button(".st-key-answer-keypad .stButton button", palette["key"]),
        _swatch_button(
            ".st-key-answer-keypad .stButton button:active",
            palette["key_down"],
        ),
    ]
    for kind, key in (("ok", "verdict-ok"), ("bad", "verdict-bad")):
        bg, border, fg, _, _, style = palette[kind]
        parts.append(
            f"""
            .st-key-{key} [data-testid="stAlert"],
            .st-key-{key} [data-testid="stAlert"] * {{
              color: {fg} !important;
            }}
            .st-key-{key} [data-testid="stAlert"] {{
              background: {bg} !important;
              border: 3px {style} {border} !important;
            }}
            .st-key-{key} [data-testid="stAlertContainer"] {{
              background: transparent !important;
            }}
            """
        )
    parts.append("</style>")
    return "\n".join(parts)


def inject_app_css() -> None:
    st.markdown(APP_CSS + _color_css(_color_mode()), unsafe_allow_html=True)


def render_color_vision() -> None:
    if "color-vision-menu" not in st.session_state:
        previous = st.session_state.get("color-vision")
        st.session_state["color-vision-menu"] = previous if previous in _COLOR_VISION else "Standard"
    st.selectbox(
        "Color vision",
        list(_COLOR_VISION),
        key="color-vision-menu",
        help="Green-blind and red-blind are the common kinds. Blue-yellow is rare. Grayscale uses brightness only. The symbols on the buttons stay the same.",
    )


def render_nav() -> None:
    if "main-nav" not in st.session_state:
        st.session_state["main-nav"] = st.session_state.page

    st.markdown('<div class="app-nav"></div>', unsafe_allow_html=True)
    with st.container(key="app-bar"):
        picked = st.pills(
            "Page",
            PAGES,
            key="main-nav",
            selection_mode="single",
            required=True,
            wrap=True,
            width="stretch",
            label_visibility="collapsed",
        )
        if picked != st.session_state.page:
            st.session_state.page = picked
            st.rerun()
        render_color_vision()


def _go(name: str) -> None:
    st.session_state.page = name
    st.session_state["main-nav"] = name


def _start_diagnostic(set_id: str = "placement") -> None:
    st.session_state.page = "Diagnostic"
    st.session_state["main-nav"] = "Diagnostic"
    st.session_state.diag = _empty_diag()
    st.session_state.diag["set_id"] = set_id


def _abandon_diagnostic() -> None:
    st.session_state.diag = _empty_diag()


def _go_recommended() -> None:
    rec = st.session_state.diag.get("recommendation") or {}
    skill_id = rec.get("start_skill_id", "alg-1-1")
    track_id, unit_id = locate_skill_on_track(skill_id)
    st.session_state.study["course"] = track_id
    st.session_state.study["unit"] = unit_id
    st.session_state.study["skill_id"] = skill_id
    st.session_state.study["problem"] = None
    st.session_state.study["checked"] = False
    st.session_state.study["correct"] = None
    st.session_state.page = "Study"
    st.session_state["main-nav"] = "Study"


def _safe_problem(skill, seed):
    try:
        problem = generate_for_skill(skill, seed=seed)
        if problem is None:
            gens = []
            try:
                from src.generate import ensure_all_generators

                gens = sorted(ensure_all_generators())
            except Exception:
                pass
            st.error(
                f"Could not find a problem generator for **{skill.title}** "
                f"(`{skill.id}`, generator `{skill.generator}`)."
            )
            if gens:
                st.caption(f"Loaded generators: {len(gens)}")
            return None
        return problem
    except Exception as exc:
        st.exception(exc)
        return None


def show_skill_lesson(skill, *, openstax: bool = False) -> None:
    with st.expander("Lesson"):
        st.markdown(skill.lesson)
        if openstax and skill.openstax_url:
            st.markdown(f"[OpenStax reading]({skill.openstax_url})")


def show_solution(problem: Problem) -> None:
    st.markdown(f"**Final answer:** {problem.answer_display}")
    for i, step in enumerate(problem.steps, start=1):
        st.markdown(f"**Step {i} — {step.title}**")
        st.markdown(step.text)
    if problem.common_mistakes:
        st.markdown("**Common mistakes**")
        for miss in problem.common_mistakes:
            st.markdown(f"- {miss}")


_KEYPAD_ROWS: tuple[tuple[tuple[str, str], ...], ...] = (
    (("7", "7"), ("8", "8"), ("9", "9"), ("÷", "/"), ("⌫", "backspace")),
    (("4", "4"), ("5", "5"), ("6", "6"), ("×", "*"), ("(", "(")),
    (("1", "1"), ("2", "2"), ("3", "3"), ("−", "-"), (")", ")")),
    (("0", "0"), (".", "."), ("x", "x"), ("+", "+"), ("^", "^")),
    (("√", "sqrt"), ("π", "pi"), (",", ","), ("<", "<"), (">", ">")),
    (("sin", "sin"), ("cos", "cos"), ("tan", "tan")),
)


def _keypad_press(answer_key: str, token: str) -> None:
    fill_key = f"{answer_key}-fill"
    sync_key = f"{answer_key}-sync"
    edit = apply_key(
        st.session_state.get(answer_key, "") or "",
        token,
        fill=bool(st.session_state.get(fill_key, False)),
    )
    st.session_state[answer_key] = edit.text
    st.session_state[fill_key] = edit.fill
    st.session_state[sync_key] = edit.text


def _sync_answer_edit(answer_key: str) -> None:
    """Drop the inside-parentheses flag when the box was edited by hand."""
    fill_key = f"{answer_key}-fill"
    sync_key = f"{answer_key}-sync"
    current = st.session_state.get(answer_key, "") or ""
    if sync_key in st.session_state and st.session_state[sync_key] != current:
        st.session_state[fill_key] = False
    st.session_state[sync_key] = current


def _answer_keypad(answer_key: str, key_prefix: str) -> None:
    with st.container(key="answer-keypad"):
        for row_index, row in enumerate(_KEYPAD_ROWS):
            columns = st.columns(len(row), gap="small")
            for col_index, (label, token) in enumerate(row):
                columns[col_index].button(
                    label,
                    key=f"{key_prefix}-key-{row_index}-{col_index}",
                    on_click=_keypad_press,
                    args=(answer_key, token),
                    use_container_width=True,
                )


def _show_verdict(ok: bool, message: str) -> None:
    mark = "✓" if ok else "✕"
    with st.container(key="verdict-ok" if ok else "verdict-bad"):
        if ok:
            st.success(f"{mark} {message}")
        else:
            st.error(f"{mark} {message}")


def _answer_verdict(checked: bool, correct: bool | None, wrong: str) -> tuple[bool, str] | None:
    if not checked:
        return None
    if correct:
        return True, "Correct."
    return False, wrong


def problem_card(
    problem: Problem,
    key_prefix: str,
    on_check,
    skill=None,
    *,
    verdict: tuple[bool, str] | None = None,
    on_new=None,
) -> None:
    if skill is not None:
        show_skill_lesson(skill, openstax=True)
    st.markdown(problem.prompt)
    answer_key = f"{key_prefix}-answer"
    nonce_key = f"{key_prefix}-ink-nonce"
    fill_key = f"{answer_key}-fill"
    answer_slot = st.container()
    action_slot = st.container()
    keypad_slot = st.container()
    pad_slot = st.container()
    if problem.plot != "sketch":
        with pad_slot:
            st.caption("Write the answer, then **Read as answer**. Edit the box if the reading is off.")
            ink = handwriting_pad(key=f"{key_prefix}-ink")
            if ink and ink.get("expression"):
                nonce = ink.get("nonce")
                if nonce != st.session_state.get(nonce_key):
                    st.session_state[nonce_key] = nonce
                    st.session_state[answer_key] = ink["expression"]
                    st.session_state[fill_key] = False
    _sync_answer_edit(answer_key)
    with answer_slot:
        student = st.text_input(
            "Your answer",
            key=answer_key,
            placeholder="Type here, use the keys below, or write and tap Read as answer",
        )
    with action_slot:
        if verdict is not None:
            ok, message = verdict
            _show_verdict(ok, message)
        if on_new is None:
            cols = st.columns(3)
            with cols[0]:
                if st.button("Submit", key=f"{key_prefix}-check", use_container_width=True):
                    ok = answers_match(student, problem.answer)
                    on_check(ok, student)
                    st.rerun()
            with cols[1]:
                show_hint = st.button("Hint", key=f"{key_prefix}-hint", use_container_width=True)
            with cols[2]:
                show_sol = st.button("Steps", key=f"{key_prefix}-sol", use_container_width=True)
        else:
            with st.container(key="answer-actions"):
                left, right = st.columns(2, gap="small")
                with left:
                    if st.button("Submit", key=f"{key_prefix}-check", use_container_width=True):
                        ok = answers_match(student, problem.answer)
                        on_check(ok, student)
                        st.rerun()
                    show_hint = st.button("Hint", key=f"{key_prefix}-hint", use_container_width=True)
                with right:
                    show_sol = st.button("Steps", key=f"{key_prefix}-sol", use_container_width=True)
                    if st.button("New problem", key=f"{key_prefix}-new", use_container_width=True):
                        on_new()
                        st.rerun()
    with keypad_slot:
        _answer_keypad(answer_key, key_prefix)
    fig = figure_for(problem.plot, problem.plot_data)
    if fig is not None:
        st.pyplot(fig, clear_figure=True, width="stretch")
    if show_hint:
        st.info(problem.hint)
    if show_sol:
        with st.expander("Solution", expanded=True):
            show_solution(problem)


def page_home() -> None:
    st.title("Calc 1 prep")
    st.caption(
        "Algebra, trig, and precalculus for coming back after a long break. "
        "Every problem has a checkable answer and a walkthrough."
    )

    start, practice = st.columns(2)
    with start:
        st.markdown("**Place yourself**")
        st.button(
            "Placement test",
            type="primary",
            on_click=_go,
            args=("Diagnostic",),
            use_container_width=True,
        )
        st.caption("Finds the earliest gap. Not a grade.")
    with practice:
        st.markdown("**Practice**")
        st.button("Study a skill", on_click=_go, args=("Study",), use_container_width=True)
        st.button("Extra drill", on_click=_go, args=("Extra",), use_container_width=True)
        st.button("Physics 1 & 2", on_click=_go, args=("Physics",), use_container_width=True)

    st.markdown("**Memorize**")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.button("Unit circle", on_click=_go, args=("Unit circle",), use_container_width=True)
    with c2:
        st.button("Identities", on_click=_go, args=("Identities",), use_container_width=True)
    with c3:
        st.button("Flashcards", on_click=_go, args=("Flashcards",), use_container_width=True)

    with st.expander("How placement works"):
        st.markdown(
            """
The diagnostic looks for the **earliest** gap so you do not redo algebra you
still have, and so you do not jump into trig with shaky factoring.

- **Placement** — 8 questions per stage (32 total). Take this first.
- **Midway / End / Anytime** — 3 new questions per stage. Same levels, different items.
- **Pass a stage** to continue: about 70% on Placement, or 2 of 3 on a retake.
- If a stage is below that, it **stops** and places you at the first missed skill.

Credit exams after this rebuild: **CLEP College Algebra**, **CLEP Precalculus**,
and **AP Precalculus**.
"""
        )


def _diag_history_lines() -> None:
    history = st.session_state.progress.get("diagnostic_history") or []
    if not history:
        return
    st.markdown("**Previous takes in this session**")
    for rec in reversed(history):
        title = rec.get("set_title") or rec.get("set_id") or "Placement"
        start = rec.get("start_title") or "—"
        scores = rec.get("stage_scores") or {}
        bits = ", ".join(
            f"S{stage} {int(ratio * 100)}%" for stage, ratio in scores.items()
        )
        st.caption(f"{title}: placed at {start}" + (f" · {bits}" if bits else ""))


def _save_diagnostic(diag: dict, rec: dict) -> None:
    dset = set_by_id(diag.get("set_id"))
    rec = {**rec, "set_id": dset.id, "set_title": dset.title}
    diag["finished"] = True
    diag["recommendation"] = rec
    record_diagnostic(st.session_state.progress, rec)
    st.session_state.diag = diag


def page_diagnostic() -> None:
    st.title("Diagnostic")
    diag = st.session_state.diag
    if not diag.get("set_id") and not diag.get("finished"):
        st.caption(
            "Placement first (8 per stage). The others are shorter retakes with new questions."
        )
        _diag_history_lines()
        for row in (SET_ORDER[:2], SET_ORDER[2:]):
            cols = st.columns(2)
            for set_id, col in zip(row, cols):
                dset = set_by_id(set_id)
                with col:
                    with st.container(border=True):
                        st.markdown(f"**{dset.title}**")
                        st.caption(f"{dset.n_per_stage} per stage · {dset.when}")
                        st.button(
                            "Start",
                            key=f"diag-start-{set_id}",
                            type="primary" if set_id == "placement" else "secondary",
                            on_click=_start_diagnostic,
                            args=(set_id,),
                            use_container_width=True,
                        )
        return

    dset = set_by_id(diag.get("set_id"))
    pass_ratio = dset.pass_ratio

    if diag["finished"] and diag["recommendation"]:
        rec = diag["recommendation"]
        st.success(rec["headline"])
        st.caption(f"Form: **{dset.title}** · {dset.when}")
        st.markdown(f"**Recommended start:** {rec['start_title']}")
        scores = rec["stage_scores"]
        if scores:
            st.markdown("**Stage scores**")
            for stage, ratio in scores.items():
                title = next(s["title"] for s in STAGES if s["stage"] == stage)
                st.markdown(f"- Stage {stage} · {title}: {int(ratio*100)}%")
        if rec["weak_skills"]:
            st.markdown("**Skills to revisit**")
            for sid in rec["weak_skills"]:
                sk = skill_by_id(sid)
                st.markdown(f"- {sk.title if sk else sid}")
        st.button(
            "Go to recommended skill",
            type="primary",
            on_click=_go_recommended,
            use_container_width=True,
        )
        _diag_history_lines()
        st.button(
            "Choose another form",
            on_click=_abandon_diagnostic,
            use_container_width=True,
        )
        return

    stage = diag["stage"]
    items = problems_for_stage(stage, dset.id)
    index = diag["index"]
    meta = next(s for s in STAGES if s["stage"] == stage)
    st.progress((stage - 1) / 4, text=f"{dset.title} · Stage {stage} of 4")
    st.caption(f"{meta['title']} · {int(pass_ratio * 100)}% to continue · {index + 1} of {len(items)}")
    if index >= len(items):
        st.stop()
    problem = items[index]

    def on_check(ok: bool, _student: str) -> None:
        diag["awaiting"] = False
        diag["last_correct"] = ok
        record_attempt(st.session_state.progress, problem.skill_id, ok, problem.id)
        pairs = diag["results"].setdefault(stage, [])
        if len(pairs) == index:
            pairs.append((problem, ok))
        else:
            pairs[index] = (problem, ok)
        st.session_state.diag = diag

    if diag["awaiting"]:
        problem_card(problem, f"diag-{dset.id}-{stage}-{index}", on_check)
        st.button(
            "Quit this form",
            on_click=_abandon_diagnostic,
            use_container_width=True,
        )
    else:
        if diag["last_correct"]:
            _show_verdict(True, "Correct.")
        else:
            _show_verdict(False, f"Not quite. Target form: {problem.answer_display}")
        with st.expander("Solution", expanded=not diag["last_correct"]):
            show_solution(problem)
        if st.button("Next", type="primary", use_container_width=True):
            next_index = index + 1
            if next_index < len(items):
                diag["index"] = next_index
                diag["awaiting"] = True
                diag["last_correct"] = None
            else:
                marks = [ok for _, ok in diag["results"].get(stage, [])]
                ratio = (sum(marks) / len(marks)) if marks else 0
                passed = ratio >= pass_ratio
                if passed and stage < 4:
                    diag["stage"] = stage + 1
                    diag["index"] = 0
                    diag["awaiting"] = True
                    diag["last_correct"] = None
                    st.info(
                        f"Stage {stage} score {int(ratio*100)}% — continuing to stage {stage + 1}."
                    )
                else:
                    rec = recommend(diag["results"], pass_ratio=pass_ratio)
                    _save_diagnostic(diag, rec)
            st.session_state.diag = diag
            st.rerun()


def page_study() -> None:
    st.title("Study")
    if "course" not in st.session_state.study:
        skill_id = st.session_state.study.get("skill_id") or "alg-3-1"
        track_id, unit_id = locate_skill_on_track(skill_id)
        st.session_state.study["course"] = track_id
        st.session_state.study["unit"] = unit_id

    track_ids = [t.id for t in TRACKS]
    col_c, col_u, col_s = st.columns(3)
    with col_c:
        course_id = st.selectbox(
            "Course",
            track_ids,
            index=track_ids.index(st.session_state.study["course"])
            if st.session_state.study.get("course") in track_ids
            else 2,
            format_func=lambda tid: track_by_id(tid).title if track_by_id(tid) else tid,
        )
    if course_id != st.session_state.study.get("course"):
        track = track_by_id(course_id)
        st.session_state.study["course"] = course_id
        st.session_state.study["unit"] = track.units[0].id if track else ""
        st.session_state.study["skill_id"] = track.units[0].skill_ids[0] if track else ""
        st.session_state.study["problem"] = None
        st.session_state.study["checked"] = False
        st.rerun()

    track = track_by_id(course_id)
    if track is None:
        st.stop()

    unit_ids = [u.id for u in track.units]
    current_unit = st.session_state.study.get("unit")
    if current_unit not in unit_ids:
        current_unit = unit_ids[0]
    with col_u:
        unit_id = st.selectbox(
            "Unit",
            unit_ids,
            index=unit_ids.index(current_unit),
            format_func=lambda uid: next(u.title for u in track.units if u.id == uid),
        )
    if unit_id != st.session_state.study.get("unit"):
        unit = next(u for u in track.units if u.id == unit_id)
        st.session_state.study["unit"] = unit_id
        st.session_state.study["skill_id"] = unit.skill_ids[0]
        st.session_state.study["problem"] = None
        st.session_state.study["checked"] = False
        st.rerun()

    unit = next(u for u in track.units if u.id == unit_id)
    skill_ids = unit.skill_ids
    current = st.session_state.study["skill_id"]
    if current not in skill_ids:
        track_id, found_unit = locate_skill_on_track(current, preferred_track=course_id)
        if found_unit != unit_id or track_id != course_id:
            st.session_state.study["course"] = track_id
            st.session_state.study["unit"] = found_unit
            st.rerun()
        current = skill_ids[0]
    with col_s:
        chosen = st.selectbox(
            "Skill",
            skill_ids,
            index=skill_ids.index(current),
            format_func=lambda sid: (
                format_skill_title(skill_by_id(sid)) if skill_by_id(sid) else sid
            ),
        )
    if chosen != st.session_state.study["skill_id"]:
        st.session_state.study["skill_id"] = chosen
        st.session_state.study["problem"] = None
        st.session_state.study["checked"] = False
        st.rerun()

    skill = skill_by_id(chosen)
    if skill is None:
        st.stop()

    why = relevance_line(skill)
    if why:
        st.caption(why)

    if st.session_state.study["problem"] is None:
        st.session_state.study["problem"] = _safe_problem(
            skill, st.session_state.study["seed"]
        )
    problem = st.session_state.study["problem"]
    if problem is None:
        if st.button("Try again", use_container_width=True):
            st.session_state.study["seed"] = random.randint(1, 10**9)
            st.rerun()
        return

    def on_check(ok: bool, _student: str) -> None:
        st.session_state.study["checked"] = True
        st.session_state.study["correct"] = ok
        record_attempt(st.session_state.progress, skill.id, ok, problem.id)

    def on_new() -> None:
        st.session_state.study["seed"] = random.randint(1, 10**9)
        st.session_state.study["problem"] = None
        st.session_state.study["checked"] = False
        st.session_state.study["correct"] = None

    problem_card(
        problem,
        f"study-{skill.id}-{st.session_state.study['seed']}",
        on_check,
        skill=skill,
        verdict=_answer_verdict(
            st.session_state.study["checked"],
            st.session_state.study["correct"],
            f"Not quite. A correct form is {problem.answer_display}",
        ),
        on_new=on_new,
    )


def page_extra() -> None:
    st.title("Extra")
    st.caption("Random problems from the pool you pick. Same Submit / Hint / Steps as Study.")
    course = st.selectbox(
        "Pool",
        [
            "All courses",
            "College Algebra",
            "Trigonometry",
            "Precalculus",
            "Physics 1 & 2",
            "Physics 1",
            "Physics 2",
            "Calc 1 priority",
            "Electrical engineering",
            "Mechanical engineering",
        ],
        key="extra-course",
    )
    if course != st.session_state.extra.get("course"):
        st.session_state.extra["course"] = course
        st.session_state.extra["seed"] = random.randint(1, 10**9)
        st.session_state.extra["problem"] = None
        st.session_state.extra["checked"] = False

    pool = all_skills()
    if course == "College Algebra":
        wanted = track_skill_ids("algebra")
        pool = [s for s in pool if s.id in wanted]
    elif course == "Trigonometry":
        wanted = track_skill_ids("trig")
        pool = [s for s in pool if s.id in wanted]
    elif course == "Precalculus":
        wanted = precalc_skill_ids()
        pool = [s for s in pool if s.id in wanted]
    elif course == "Physics 1 & 2":
        wanted = physics_skill_ids()
        pool = [s for s in pool if s.id in wanted]
    elif course == "Physics 1":
        wanted = physics_skill_ids(exam="ap_physics1")
        pool = [s for s in pool if s.id in wanted]
    elif course == "Physics 2":
        wanted = physics_skill_ids(exam="ap_physics2")
        pool = [s for s in pool if s.id in wanted]
    elif course == "Calc 1 priority":
        pool = skills_with_tag("calc")
    elif course == "Electrical engineering":
        pool = skills_with_tag("ee")
    elif course == "Mechanical engineering":
        pool = skills_with_tag("me")

    if st.session_state.extra["problem"] is None:
        rng = random.Random(st.session_state.extra["seed"])
        skill = rng.choice(pool)
        st.session_state.extra["skill_id"] = skill.id
        st.session_state.extra["problem"] = _safe_problem(
            skill, st.session_state.extra["seed"]
        )

    skill = skill_by_id(st.session_state.extra["skill_id"])
    problem = st.session_state.extra["problem"]
    if skill is None or problem is None:
        st.error("Could not load a problem.")
        return

    st.caption(format_skill_title(skill))
    why = relevance_line(skill)
    if why:
        st.caption(why)

    def on_check(ok: bool, _student: str) -> None:
        st.session_state.extra["checked"] = True
        st.session_state.extra["correct"] = ok
        record_attempt(st.session_state.progress, skill.id, ok, problem.id)

    def on_new() -> None:
        st.session_state.extra["seed"] = random.randint(1, 10**9)
        st.session_state.extra["problem"] = None
        st.session_state.extra["checked"] = False
        st.session_state.extra["correct"] = None

    problem_card(
        problem,
        f"extra-{st.session_state.extra['seed']}",
        on_check,
        skill=skill,
        verdict=_answer_verdict(
            st.session_state.extra["checked"],
            st.session_state.extra["correct"],
            f"Not quite. A correct form is {problem.answer_display}",
        ),
        on_new=on_new,
    )


def page_physics() -> None:
    st.title("Physics")
    st.caption(
        "Algebra-based AP 1 & 2. Use $g = 10\\,\\mathrm{m/s^2}$ when gravity appears."
    )
    pool_label = st.pills(
        "Pool",
        ["Physics 1", "Physics 2", "Mixed"],
        default="Physics 1",
        key="phy-pool",
        wrap=True,
        width="stretch",
    )
    label = pool_label or "Physics 1"
    if label != st.session_state.physics.get("pool"):
        st.session_state.physics["pool"] = label
        st.session_state.physics["seed"] = random.randint(1, 10**9)
        st.session_state.physics["problem"] = None
        st.session_state.physics["checked"] = False
        st.session_state.physics["correct"] = None

    if label == "Physics 1":
        wanted = physics_skill_ids(exam="ap_physics1")
    elif label == "Physics 2":
        wanted = physics_skill_ids(exam="ap_physics2")
    else:
        wanted = physics_skill_ids()
    pool = [s for s in all_skills() if s.id in wanted]

    if st.session_state.physics["problem"] is None:
        rng = random.Random(st.session_state.physics["seed"])
        skill = rng.choice(pool)
        st.session_state.physics["skill_id"] = skill.id
        st.session_state.physics["problem"] = _safe_problem(
            skill, st.session_state.physics["seed"]
        )

    skill = skill_by_id(st.session_state.physics["skill_id"])
    problem = st.session_state.physics["problem"]
    if skill is None or problem is None:
        st.error("Could not load a physics problem.")
        return

    st.caption(format_skill_title(skill))
    why = relevance_line(skill)
    if why:
        st.caption(why)

    def on_check(ok: bool, _student: str) -> None:
        st.session_state.physics["checked"] = True
        st.session_state.physics["correct"] = ok
        record_attempt(st.session_state.progress, skill.id, ok, problem.id)

    def on_new() -> None:
        st.session_state.physics["seed"] = random.randint(1, 10**9)
        st.session_state.physics["problem"] = None
        st.session_state.physics["checked"] = False
        st.session_state.physics["correct"] = None

    problem_card(
        problem,
        f"phy-{st.session_state.physics['seed']}",
        on_check,
        skill=skill,
        verdict=_answer_verdict(
            st.session_state.physics["checked"],
            st.session_state.physics["correct"],
            f"Not quite. A correct form is {problem.answer_display}",
        ),
        on_new=on_new,
    )


def page_flashcards() -> None:
    st.title("Flashcards")
    st.caption("Recall the right-hand side, then Flip. Filter by field or family.")
    field_label = st.pills(
        "Field",
        ["All fields", "Math", "Physics", "EE", "ME"],
        default="All fields",
        key="fc-field",
        wrap=True,
        width="stretch",
    )
    field = {
        "All fields": "all",
        "Math": "math",
        "Physics": "physics",
        "EE": "ee",
        "ME": "me",
    }.get(field_label or "All fields", "all")
    family_label = st.pills(
        "Family",
        ["All families", *[CARD_FAMILY_LABEL[fid] for fid in CARD_FAMILY_ORDER]],
        default="All families",
        key="fc-family",
        wrap=True,
        width="stretch",
    )
    family_from_label = {label: fid for fid, label in CARD_FAMILY_LABEL.items()}
    family = (
        "all"
        if (family_label or "All families") == "All families"
        else family_from_label.get(family_label or "All families", "all")
    )
    cards = flashcards_for(field=field, family=family)
    st.caption(f"{len(cards)} cards in this filter.")
    if not cards:
        st.info("Nothing in this mix. Try All fields or another family.")
        return

    filt = f"{field}:{family}"
    flash = st.session_state.setdefault(
        "flash",
        {"filter": None, "ids": [], "i": 0, "flipped": False},
    )
    if flash.get("filter") != filt or set(flash.get("ids") or []) != {c.id for c in cards}:
        flash["filter"] = filt
        flash["ids"] = shuffled_ids(cards)
        flash["i"] = 0
        flash["flipped"] = False

    ids = flash["ids"]
    index = flash["i"] % len(ids)
    flash["i"] = index
    by_id = {card.id: card for card in cards}
    card = by_id[ids[index]]
    tags = " · ".join(f"**{label}**" for label in card.field_labels())

    st.markdown(f"**{index + 1} / {len(ids)}** · {card.family_label}")
    st.caption(tags)
    with st.container(border=True):
        st.markdown(f"### {card.name}")
        if not flash["flipped"]:
            st.markdown(card.front)
            st.caption("Then Flip.")
        else:
            st.latex(card.back_tex)
            st.markdown(card.why)

    cols = st.columns(4)
    with cols[0]:
        if st.button("Flip", key="fc-flip", use_container_width=True):
            flash["flipped"] = not flash["flipped"]
            st.rerun()
    with cols[1]:
        if st.button("Previous", key="fc-prev", use_container_width=True):
            flash["i"] = (index - 1) % len(ids)
            flash["flipped"] = False
            st.rerun()
    with cols[2]:
        if st.button("Next", key="fc-next", use_container_width=True):
            flash["i"] = (index + 1) % len(ids)
            flash["flipped"] = False
            st.rerun()
    with cols[3]:
        if st.button("Shuffle", key="fc-shuffle", use_container_width=True):
            flash["ids"] = shuffled_ids(cards)
            flash["i"] = 0
            flash["flipped"] = False
            st.rerun()


def page_progress() -> None:
    st.title("Progress")
    data = st.session_state.progress
    rec = data.get("diagnostic")
    history = data.get("diagnostic_history") or []
    if rec:
        form = rec.get("set_title") or rec.get("set_id") or "Placement"
        st.markdown(f"**Last diagnostic ({form}):** {rec.get('start_title')}")
        st.markdown(rec.get("headline", ""))
    else:
        st.caption("No diagnostic in this session yet.")
    if len(history) > 1:
        st.markdown("**All takes this session**")
        for item in reversed(history):
            form = item.get("set_title") or item.get("set_id") or "Placement"
            st.caption(f"{form}: {item.get('start_title')} — {item.get('headline', '')}")
    st.markdown(f"**Attempts this session:** {len(data.get('attempts', []))}")
    st.download_button(
        "Download progress JSON",
        data=to_json(data),
        file_name="calc1-prep-progress.json",
        mime="application/json",
        use_container_width=True,
    )
    if st.button("Reset session progress", use_container_width=True):
        st.session_state.progress = empty_progress()
        st.rerun()


def page_unit_circle() -> None:
    st.title("Unit circle")
    st.caption("Cosine is x, sine is y. Sixteen special angles.")
    tab_ref, tab_practice = st.tabs(["Look", "Fill in"])
    with tab_ref:
        st.pyplot(
            unit_circle_figure(labeled=True, size=6.8),
            clear_figure=True,
            width="stretch",
        )
        with st.expander("Table"):
            st.markdown(unit_circle_value_table())
    with tab_practice:
        mode_label = st.pills(
            "What to fill in",
            [
                "Coordinates",
                "Radians",
                "Degrees",
                "Everything",
            ],
            default="Coordinates",
            key="uc-mode",
            wrap=True,
            width="stretch",
        )
        mode = {
            "Coordinates": "coordinates",
            "Radians": "radians",
            "Degrees": "degrees",
            "Everything": "all",
        }.get(mode_label or "Coordinates", "coordinates")
        components.html(
            unit_circle_practice_html(mode),
            height=980,
            scrolling=True,
        )


def page_identities() -> None:
    st.title("Identities")
    st.caption(
        "Filter by field, then read or fill in the right-hand side. "
        "Catalog follows [Paul’s cheat sheet](https://tutorial.math.lamar.edu/pdf/Trig_Cheat_Sheet.pdf)."
    )
    field_label = st.pills(
        "Field",
        ["All fields", "Math", "Physics", "EE", "ME"],
        default="All fields",
        key="id-field",
        wrap=True,
        width="stretch",
    )
    field = {
        "All fields": "all",
        "Math": "math",
        "Physics": "physics",
        "EE": "ee",
        "ME": "me",
    }.get(field_label or "All fields", "all")
    tab_ref, tab_practice = st.tabs(["Look", "Fill in"])
    with tab_ref:
        for family_name, rows in grouped_identities(field):
            with st.expander(f"{family_name} · {len(rows)}"):
                for item in rows:
                    st.markdown(item.labeled_markdown())
                    st.caption(item.why)
    with tab_practice:
        family_label = st.pills(
            "Family",
            ["All families", *[FAMILY_LABEL[fid] for fid in FAMILY_ORDER]],
            default="All families",
            key="id-family",
            wrap=True,
            width="stretch",
        )
        family_from_label = {label: fid for fid, label in FAMILY_LABEL.items()}
        family = "all" if (family_label or "All families") == "All families" else family_from_label.get(
            family_label or "All families", "all"
        )
        n_shown = len(identities_for(field=field, family=family))
        st.caption(f"{n_shown} to fill. Check the list, or Reveal to study.")
        components.html(
            identities_practice_html(field=field, family=family),
            height=920,
            scrolling=True,
        )


inject_app_css()
render_nav()

page = st.session_state.page
if page == "Home":
    page_home()
elif page == "Diagnostic":
    page_diagnostic()
elif page == "Study":
    page_study()
elif page == "Physics":
    page_physics()
elif page == "Unit circle":
    page_unit_circle()
elif page == "Identities":
    page_identities()
elif page == "Flashcards":
    page_flashcards()
elif page == "Extra":
    page_extra()
else:
    page_progress()
