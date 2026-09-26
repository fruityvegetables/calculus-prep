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
    PASS_RATIO,
    STAGES,
    generate_for_skill,
    problems_for_stage,
    recommend,
)
from src.identities import (
    FAMILY_LABEL,
    FAMILY_ORDER,
    identities_for,
    identities_practice_html,
    grouped_identities,
)
from src.figures import figure_for
from src.plots import (
    unit_circle_figure,
    unit_circle_practice_html,
    unit_circle_value_table,
)
from src.progress import empty_progress, record_attempt, to_json
from src.schema import Problem

ensure_all_generators()

st.set_page_config(
    page_title="Algebra · Trig · Precalculus",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "progress" not in st.session_state:
    st.session_state.progress = empty_progress()
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "diag" not in st.session_state:
    st.session_state.diag = {
        "stage": 1,
        "index": 0,
        "results": {},
        "finished": False,
        "recommendation": None,
        "awaiting": True,
        "last_correct": None,
    }
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
    "Extra practice",
    "Progress",
]

MOBILE_CSS = """
<style>
  .stApp { overflow-x: hidden; }
  [data-testid="stMainBlockContainer"] {
    padding-top: 0.6rem;
    padding-left: max(0.7rem, env(safe-area-inset-left));
    padding-right: max(0.7rem, env(safe-area-inset-right));
    padding-bottom: max(1.2rem, env(safe-area-inset-bottom));
    max-width: 100%;
  }
  @media (min-width: 768px) {
    [data-testid="stMainBlockContainer"] {
      padding-left: 2rem;
      padding-right: 2rem;
    }
  }
  h1 { font-size: 1.55rem !important; line-height: 1.25 !important; }
  h2 { font-size: 1.25rem !important; }
  h3 { font-size: 1.1rem !important; }
  @media (min-width: 768px) {
    h1 { font-size: 2.15rem !important; }
    h2 { font-size: 1.5rem !important; }
  }
  .stButton button, .stDownloadButton button, .stFormSubmitButton button {
    min-height: 44px;
    width: 100%;
    font-size: 1rem !important;
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
  @media (max-width: 768px) {
    [data-testid="stHeader"],
    [data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapseButton"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding-top: 0.75rem; }
  }
  [data-testid="stButtonGroup"] { flex-wrap: wrap !important; }
  .stMarkdown, .stCaption, .stAlert { overflow-wrap: anywhere; word-break: break-word; }
  [data-testid="stExpander"] summary { min-height: 44px; }
</style>
"""


def inject_mobile_css() -> None:
    st.markdown(MOBILE_CSS, unsafe_allow_html=True)


def render_nav() -> None:
    with st.sidebar:
        st.title("Calc 1 prep")
        for name in PAGES:
            if st.button(
                name,
                key=f"navbtn-{name}",
                use_container_width=True,
                type="primary" if st.session_state.page == name else "secondary",
            ):
                st.session_state.page = name
                st.session_state["main-nav"] = name
                st.rerun()

    if "main-nav" not in st.session_state:
        st.session_state["main-nav"] = st.session_state.page

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


def _go(name: str) -> None:
    st.session_state.page = name
    st.session_state["main-nav"] = name


def _start_diagnostic() -> None:
    st.session_state.page = "Diagnostic"
    st.session_state["main-nav"] = "Diagnostic"
    st.session_state.diag = {
        "stage": 1,
        "index": 0,
        "results": {},
        "finished": False,
        "recommendation": None,
        "awaiting": True,
        "last_correct": None,
    }


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
    with st.expander("Lesson — read this before you try", expanded=True):
        st.markdown(skill.lesson)
        if openstax and skill.openstax_url:
            st.markdown(f"[Optional textbook reading: OpenStax]({skill.openstax_url})")


def show_solution(problem: Problem) -> None:
    st.markdown(f"**Final answer:** {problem.answer_display}")
    for i, step in enumerate(problem.steps, start=1):
        st.markdown(f"**Step {i} — {step.title}**")
        st.markdown(step.text)
    if problem.common_mistakes:
        st.markdown("**Common mistakes**")
        for miss in problem.common_mistakes:
            st.markdown(f"- {miss}")


def problem_card(problem: Problem, key_prefix: str, on_check, skill=None) -> None:
    if skill is not None:
        show_skill_lesson(skill, openstax=True)
    st.markdown(problem.prompt)
    fig = figure_for(problem.plot, problem.plot_data)
    if fig is not None:
        st.pyplot(fig, clear_figure=True, width="stretch")
    if problem.steps:
        st.info(
            f"**How to start this problem — {problem.steps[0].title}.** "
            f"{problem.steps[0].text}"
        )
    student = st.text_input(
        "Your answer",
        key=f"{key_prefix}-answer",
        placeholder="Fractions, sqrt(), pi, and lists like -3, 5 are all OK",
    )
    cols = st.columns(3)
    with cols[0]:
        if st.button("Check", key=f"{key_prefix}-check", use_container_width=True):
            ok = answers_match(student, problem.answer)
            on_check(ok, student)
    with cols[1]:
        show_hint = st.button("Hint", key=f"{key_prefix}-hint", use_container_width=True)
    with cols[2]:
        show_sol = st.button(
            "Show step-by-step",
            key=f"{key_prefix}-sol",
            use_container_width=True,
        )
    if show_hint:
        st.info(problem.hint)
    if show_sol:
        with st.expander("Complete solution (meant for a long time away from math)", expanded=True):
            show_solution(problem)


def page_home() -> None:
    st.title("Algebra, trigonometry, and precalculus")
    st.markdown(
        "Built for people coming back to math after a long break — including "
        "returning engineering students aiming at Calculus 1. Every in-app "
        "problem has a final answer **and** a walkthrough that names the goal, "
        "explains *why*, shows each algebra line, and flags a common mistake."
    )
    st.subheader("How the diagnostic decides where you start")
    st.markdown(
        """
The diagnostic is a **placement test**, not a grade. It looks for the
*earliest* gap so you do not waste weeks redoing algebra you still have,
and so you do not jump into trig while factoring is still shaky.

1. **Four stages, eight questions each**, shown one at a time. Type an
   answer; you can request a hint or a full solution after you try.
2. **Stage 1 — Algebra foundations.** Order of operations, exponents,
   radicals, factoring, rational expressions, linear and quadratic
   equations, inequalities. If this stage is weak, stop here.
3. **Stage 2 — College algebra and functions.** Function notation,
   domain, composition, transformations, inverses, parabolas, logs and
   exponentials (CLEP College Algebra / AP Precalculus Units 1–2).
4. **Stage 3 — Trigonometry.** Radians, the unit circle, right triangles,
   period, inverse sine, identities, solving, triangle angles. This is
   the usual rusty spot.
5. **Stage 4 — Precalculus extras.** Systems, conics, polar coordinates,
   sequences, binomial theorem, a limit, vectors, matrices.

You need about **70% on a stage to unlock the next one**. Below that, the
app **stops** and places you at the first missed skill in that stage.
Passing a stage still records every miss, so one rusty topic does not
disappear.

There is no AP Algebra or AP Trigonometry exam. After you rebuild these
three courses, the credit exams are **CLEP College Algebra**, **CLEP
Precalculus**, and **AP Precalculus**.
"""
    )
    st.button(
        "Start the diagnostic",
        type="primary",
        on_click=_start_diagnostic,
        use_container_width=True,
    )
    st.subheader("Study without the test")
    st.markdown(
        "Jump straight into in-app problems. **Precalculus (full course)** is the "
        "complete path (functions, polynomials, exp/log, trig, polar, conics, "
        "sequences, limits) — not only the leftover extras."
    )
    st.markdown(
        "Skills marked **Calc 1**, **EE**, and **ME** are the ones that show up "
        "constantly in calculus and in electrical or mechanical coursework — "
        "not every topic, only the high-leverage ones. Extra practice can drill "
        "those pools on their own."
    )
    st.button(
        "Open Study — pick a skill and get a problem",
        on_click=_go,
        args=("Study",),
        use_container_width=True,
    )
    st.button(
        "Physics 1 & 2 practice — AP algebra-based, with hints and solutions",
        on_click=_go,
        args=("Physics",),
        use_container_width=True,
    )
    st.button(
        "Memorize the unit circle — labeled diagram + fill-in drill",
        on_click=_go,
        args=("Unit circle",),
        use_container_width=True,
    )
    st.button(
        "Memorize trig identities — Math, Physics, EE, or ME",
        on_click=_go,
        args=("Identities",),
        use_container_width=True,
    )
    st.button(
        "Open Extra practice — mixed drill with answers",
        on_click=_go,
        args=("Extra practice",),
        use_container_width=True,
    )


def page_diagnostic() -> None:
    st.title("Placement diagnostic")
    diag = st.session_state.diag

    if diag["finished"] and diag["recommendation"]:
        rec = diag["recommendation"]
        st.success(rec["headline"])
        skill = skill_by_id(rec["start_skill_id"])
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
        st.button(
            "Retake diagnostic",
            on_click=_start_diagnostic,
            use_container_width=True,
        )
        return

    stage = diag["stage"]
    items = problems_for_stage(stage)
    index = diag["index"]
    meta = next(s for s in STAGES if s["stage"] == stage)
    st.progress((stage - 1) / 4, text=f"Stage {stage} of 4 — {meta['title']}")
    st.caption(meta["why"])
    if index >= len(items):
        st.stop()
    problem = items[index]
    st.markdown(f"**Question {index + 1} of {len(items)}** · skill: `{problem.skill_id}`")
    diag_skill = skill_by_id(problem.skill_id)

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
        problem_card(problem, f"diag-{stage}-{index}", on_check, skill=diag_skill)
    else:
        if diag["last_correct"]:
            st.success("Correct.")
        else:
            st.error(f"Not quite. Target form: {problem.answer_display}")
        with st.expander("Complete solution", expanded=not diag["last_correct"]):
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
                passed = ratio >= PASS_RATIO
                if passed and stage < 4:
                    diag["stage"] = stage + 1
                    diag["index"] = 0
                    diag["awaiting"] = True
                    diag["last_correct"] = None
                    st.info(
                        f"Stage {stage} score {int(ratio*100)}% — continuing to stage {stage + 1}."
                    )
                else:
                    rec = recommend(diag["results"])
                    diag["finished"] = True
                    diag["recommendation"] = rec
                    st.session_state.progress["diagnostic"] = rec
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
    st.caption(track.blurb)
    st.caption(
        "Tags: **Calc 1** = used constantly in calculus. **EE** = electrical. "
        "**ME** = mechanical. Untagged skills are still useful prerequisites."
    )

    unit_ids = [u.id for u in track.units]
    current_unit = st.session_state.study.get("unit")
    if current_unit not in unit_ids:
        current_unit = unit_ids[0]
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
        st.info(why)

    st.subheader("Practice problem")
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

    problem_card(problem, f"study-{skill.id}-{st.session_state.study['seed']}", on_check, skill=skill)
    if st.session_state.study["checked"]:
        if st.session_state.study["correct"]:
            st.success("Correct.")
        else:
            st.error(f"Not quite. A correct form is {problem.answer_display}")
    if st.button("New problem", use_container_width=True):
        st.session_state.study["seed"] = random.randint(1, 10**9)
        st.session_state.study["problem"] = None
        st.session_state.study["checked"] = False
        st.session_state.study["correct"] = None
        st.rerun()


def page_extra() -> None:
    st.title("Extra practice")
    st.markdown(
        "Mixed in-app problems with the same Check / Hint / step-by-step tools. "
        "Pick a course or shuffle everything. **Precalculus** is the full AP/CLEP "
        "path (functions, polynomials, exp/log, trig, polar, conics, sequences, "
        "limits), not only polar and matrices. **Physics 1** and **Physics 2** are "
        "algebra-based AP-level intro physics. **Calc 1 priority**, **Electrical "
        "engineering**, and **Mechanical engineering** drill only the tagged skills."
    )
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

    st.caption(f"Skill: {format_skill_title(skill)}")
    why = relevance_line(skill)
    if why:
        st.info(why)

    def on_check(ok: bool, _student: str) -> None:
        st.session_state.extra["checked"] = True
        st.session_state.extra["correct"] = ok
        record_attempt(st.session_state.progress, skill.id, ok, problem.id)

    problem_card(problem, f"extra-{st.session_state.extra['seed']}", on_check, skill=skill)
    if st.session_state.extra["checked"]:
        if st.session_state.extra["correct"]:
            st.success("Correct.")
        else:
            st.error(f"Not quite. A correct form is {problem.answer_display}")
    if st.button("New problem", key="extra-new", use_container_width=True):
        st.session_state.extra["seed"] = random.randint(1, 10**9)
        st.session_state.extra["problem"] = None
        st.session_state.extra["checked"] = False
        st.session_state.extra["correct"] = None
        st.rerun()


def page_physics() -> None:
    st.title("Physics 1 & 2")
    st.markdown(
        "Algebra-based **AP Physics 1** (mechanics, waves, simple circuits) and "
        "**AP Physics 2** (fluids, thermo, E&M, optics, photons). Same depth as a "
        "one-year college intro sequence — no calculus. Every problem has a lesson, "
        "a hint, and a full walkthrough. Take $g = 10\\,\\mathrm{m/s^2}$ when a "
        "problem uses gravity. Enter the number the prompt asks for; units are in the question."
    )
    st.caption(
        "Optional reading: [OpenStax College Physics 2e](https://openstax.org/books/college-physics-2e/). "
        "You can also open **Study**, pick course **Physics 1 & 2**, and drill one skill at a time."
    )
    pool_label = st.pills(
        "Exam slice",
        ["Physics 1", "Physics 2", "Mixed P1 + P2"],
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
    st.caption(f"{len(pool)} skills in this slice. Check / Hint / Show step-by-step work the same as Study.")

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

    st.caption(f"Skill: {format_skill_title(skill)}")
    why = relevance_line(skill)
    if why:
        st.info(why)

    def on_check(ok: bool, _student: str) -> None:
        st.session_state.physics["checked"] = True
        st.session_state.physics["correct"] = ok
        record_attempt(st.session_state.progress, skill.id, ok, problem.id)

    problem_card(
        problem,
        f"phy-{st.session_state.physics['seed']}",
        on_check,
        skill=skill,
    )
    if st.session_state.physics["checked"]:
        if st.session_state.physics["correct"]:
            st.success("Correct.")
        else:
            st.error(f"Not quite. A correct form is {problem.answer_display}")
    if st.button("New problem", key="phy-new", use_container_width=True):
        st.session_state.physics["seed"] = random.randint(1, 10**9)
        st.session_state.physics["problem"] = None
        st.session_state.physics["checked"] = False
        st.session_state.physics["correct"] = None
        st.rerun()


def page_progress() -> None:
    st.title("Progress")
    data = st.session_state.progress
    rec = data.get("diagnostic")
    if rec:
        st.markdown(f"**Last diagnostic placement:** {rec.get('start_title')}")
        st.markdown(rec.get("headline", ""))
    else:
        st.markdown("No diagnostic saved in this session yet.")
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
    st.markdown(
        "On the unit circle, **cosine is the x-coordinate** and **sine is the y-coordinate**. "
        "Memorize the 16 special angles: degrees, radians, and the point "
        r"$(\cos\theta,\ \sin\theta)$. Signs follow **ASTC** (All Students Take Calculus): "
        "all positive in Q1, sine in Q2, tangent in Q3, cosine in Q4."
    )
    tab_ref, tab_practice = st.tabs(["Labeled reference", "Fill it in"])
    with tab_ref:
        st.caption("Every standard angle with degrees, radians, and coordinates. Scroll sideways on a phone if the labels feel small.")
        st.pyplot(
            unit_circle_figure(labeled=True, size=6.8),
            clear_figure=True,
            width="stretch",
        )
        with st.expander("The same 16 points as a table (easy on a phone)", expanded=True):
            st.markdown(unit_circle_value_table())
    with tab_practice:
        st.caption(
            "Hide a piece of the diagram and pick the matching value from each menu. On a phone, "
            "tap a point or pick it from the list, then use the dropdowns in the card below. "
            "Check grades your choices; Reveal fills them so you can study, then Clear and try again."
        )
        mode_label = st.pills(
            "What to fill in",
            [
                "Coordinates (x = cos, y = sin)",
                "Radians",
                "Degrees",
                "Everything",
            ],
            default="Coordinates (x = cos, y = sin)",
            key="uc-mode",
            wrap=True,
            width="stretch",
        )
        mode = {
            "Coordinates (x = cos, y = sin)": "coordinates",
            "Radians": "radians",
            "Degrees": "degrees",
            "Everything": "all",
        }.get(mode_label or "Coordinates (x = cos, y = sin)", "coordinates")
        components.html(
            unit_circle_practice_html(mode),
            height=980,
            scrolling=True,
        )


def page_identities() -> None:
    st.title("Trig identities")
    st.markdown(
        "Memorize the identities you will actually use in **calculus**, **physics**, "
        "**electrical engineering**, and **mechanical engineering**. Each formula is "
        "tagged by field — filter the list, then fill the right-hand side from a menu "
        "the same way as the unit-circle drill."
    )
    st.caption(
        "Coverage matches the standard trig identity list "
        "([Paul's Online Notes cheat sheet](https://tutorial.math.lamar.edu/pdf/Trig_Cheat_Sheet.pdf)). "
        "The layout, field tags, and drill are ours. Euler’s formula and vector components "
        "are included because they are the everyday EE / physics / ME forms of cosine and sine."
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
    n_field = len(identities_for(field=field))
    st.caption(f"{n_field} identities in this field filter.")
    tab_ref, tab_practice = st.tabs(["Labeled reference", "Fill it in"])
    with tab_ref:
        st.caption("Read the formula, the field tags, and why it shows up in that work.")
        for family_name, rows in grouped_identities(field):
            with st.expander(f"{family_name} · {len(rows)}", expanded=True):
                for item in rows:
                    tags = " · ".join(f"**{label}**" for label in item.field_labels())
                    st.markdown(rf"${item.lhs_tex} = {item.rhs_tex}$")
                    st.caption(f"{tags} — {item.why}")
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
        st.caption(
            f"{n_shown} blanks in this filter. Pick each right-hand side from the menu. "
            "Check grades the whole list; Reveal fills them so you can study, then Clear."
        )
        components.html(
            identities_practice_html(field=field, family=family),
            height=920,
            scrolling=True,
        )


inject_mobile_css()
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
elif page == "Extra practice":
    page_extra()
else:
    page_progress()
