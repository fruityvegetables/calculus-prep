from __future__ import annotations

from src.curriculum import COURSES, Skill, all_skills, skill_by_id
from src.diagnostic_bank import DIAGNOSTIC_PROBLEMS
from src.generate import ensure_all_generators, generate_problem
from src.schema import Problem

PASS_RATIO = 0.70

STAGES = [
    {
        "stage": 1,
        "title": "Algebra foundations",
        "why": (
            "This is the arithmetic-and-algebra toolbox: order of operations, exponents, "
            "factoring, fractions of polynomials, linear and quadratic equations, inequalities. "
            "If this stage is weak, later 'function' work will feel like gibberish."
        ),
    },
    {
        "stage": 2,
        "title": "College algebra and functions",
        "why": (
            "Functions, domain, composition, transformations, inverses, parabolas, logs "
            "and exponentials. This is the heart of CLEP College Algebra and AP Precalculus Units 1–2."
        ),
    },
    {
        "stage": 3,
        "title": "Trigonometry",
        "why": (
            "Radians, the unit circle, right triangles, graphs, a basic identity, solving "
            "sin x = 1/2, and triangle angle sum. This is usually the rusty spot for returning students."
        ),
    },
    {
        "stage": 4,
        "title": "Precalculus extras",
        "why": (
            "A quick sample of systems, conics, polar coordinates, sequences, binomial "
            "coefficients, a limit, a vector magnitude, and a matrix entry. Missing these "
            "does not block starting algebra or trig — it tells us what to visit later."
        ),
    },
]


def problems_for_stage(stage: int) -> list[Problem]:
    return [p for p in DIAGNOSTIC_PROBLEMS if p.stage == stage]


def generate_for_skill(skill: Skill, seed: int) -> Problem | None:
    gens = ensure_all_generators()
    name = skill.generator
    if not name or name not in gens:
        return None
    return generate_problem(name, skill.id, seed=seed)


def ready_skills() -> list[Skill]:
    return [s for s in all_skills() if s.status == "ready"]


def score_stage(results: list[bool]) -> float:
    if not results:
        return 0.0
    return sum(results) / len(results)


def recommend(stage_results: dict[int, list[tuple[Problem, bool]]]) -> dict:
    """Return placement from completed stages.

    stage_results maps stage number to a list of (problem, correct) in order.
    """
    weak_skills: list[str] = []
    first_fail_stage: int | None = None
    first_fail_skill: str | None = None

    for stage in range(1, 5):
        pairs = stage_results.get(stage) or []
        if not pairs:
            continue
        marks = [ok for _, ok in pairs]
        ratio = score_stage(marks)
        missed = [p.skill_id for p, ok in pairs if not ok]
        weak_skills.extend(missed)
        if ratio < PASS_RATIO and first_fail_stage is None:
            first_fail_stage = stage
            first_fail_skill = missed[0] if missed else pairs[0][0].skill_id

    if first_fail_stage is None and 4 in stage_results:
        start_id = "trig-7-1"
        headline = (
            "The diagnostic did not find a blocking gap. Start trigonometry in depth "
            "(unit circle first) if that still feels rusty, or browse Precalculus extras."
        )
        ready_for_calc_caution = True
    elif first_fail_stage is None:
        start_id = "alg-1-1"
        headline = "Finish the diagnostic to get a placement."
        ready_for_calc_caution = False
    else:
        start_id = first_fail_skill or "alg-1-1"
        titles = {1: "algebra foundations", 2: "functions / college algebra", 3: "trigonometry", 4: "precalculus extras"}
        headline = (
            f"Stop and study {titles[first_fail_stage]} first. "
            f"You were below {int(PASS_RATIO*100)}% on that stage, so later stages would be guessing."
        )
        ready_for_calc_caution = False

    skill = skill_by_id(start_id)
    return {
        "start_skill_id": start_id,
        "start_title": skill.title if skill else start_id,
        "headline": headline,
        "weak_skills": list(dict.fromkeys(weak_skills)),
        "first_fail_stage": first_fail_stage,
        "ready_for_calc_caution": ready_for_calc_caution,
        "stage_scores": {
            stage: score_stage([ok for _, ok in pairs])
            for stage, pairs in stage_results.items()
        },
    }


def extra_practice_catalog() -> list[dict]:
    rows = []
    for course in COURSES:
        for unit in course.units:
            for skill in unit.skills:
                rows.append(
                    {
                        "course": course.title,
                        "unit": unit.title,
                        "skill": skill.title,
                        "url": skill.openstax_url,
                        "note": skill.extra_note,
                        "status": skill.status,
                    }
                )
    return rows
