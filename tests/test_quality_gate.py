from __future__ import annotations

from src.check import answers_match
from src.curriculum import COURSES, TRACKS, all_skills, skill_by_id, track_by_id
from src.diagnostic_bank import DIAGNOSTIC_PROBLEMS
from src.generate import GENERATORS, ensure_all_generators, generate_problem
from src.schema import MIN_STEPS


def test_diagnostic_problems_all_have_full_solutions():
    from src.diagnostic_bank import DIAGNOSTIC_SETS, SET_ORDER, set_by_id
    from src.load import problems_for_stage

    assert len(DIAGNOSTIC_PROBLEMS) == 68
    ids = [problem.id for problem in DIAGNOSTIC_PROBLEMS]
    assert len(ids) == len(set(ids))
    for problem in DIAGNOSTIC_PROBLEMS:
        problem.validate()
        assert len(problem.steps) >= MIN_STEPS
        assert problem.stage in (1, 2, 3, 4)
        assert skill_by_id(problem.skill_id) is not None
    assert SET_ORDER == ("placement", "midway", "end", "anytime")
    assert set(DIAGNOSTIC_SETS) == set(SET_ORDER)
    placement = set_by_id("placement")
    assert placement.n_per_stage == 8
    assert len(placement.problems) == 32
    for set_id in ("midway", "end", "anytime"):
        dset = set_by_id(set_id)
        assert dset.n_per_stage == 3
        assert len(dset.problems) == 12
        for stage in (1, 2, 3, 4):
            assert len(dset.problems_for_stage(stage)) == 3
    assert len(problems_for_stage(1)) == 8
    assert len(problems_for_stage(1, "midway")) == 3
    assert problems_for_stage(2, "end")[0].id.startswith("diag-e-2")


def test_every_skill_has_a_generator():
    gens = ensure_all_generators()
    missing = []
    coming = []
    for skill in all_skills():
        if skill.status != "ready":
            coming.append(skill.id)
        if skill.generator not in gens:
            missing.append(skill.id)
    assert coming == []
    assert missing == []


def test_generated_problems_validate_and_self_check():
    gens = ensure_all_generators()
    for name in gens:
        problem = generate_problem(name, skill_id=f"test-{name}", seed=42)
        problem.validate()
        assert answers_match(problem.answer, problem.answer)


def test_answer_checker_equivalences():
    assert answers_match("1/2", "0.5")
    assert answers_match("sqrt(3)/2", "sqrt(3)/2")
    assert answers_match("5*pi/6", "5*pi/6")
    assert answers_match("-3, 5", "5, -3")
    assert answers_match("x>-2", "x > -2")
    assert not answers_match("22", "16")


def test_curriculum_has_three_courses():
    ids = [c.id for c in COURSES]
    assert ids == ["algebra", "trig", "precalc", "physics"]
    assert len(all_skills()) >= 70


def test_precalc_track_is_the_full_course():
    track = track_by_id("precalc")
    assert track is not None
    skill_ids = [sid for unit in track.units for sid in unit.skill_ids]
    assert len(skill_ids) >= 50
    assert "alg-3-1" in skill_ids
    assert "trig-7-3" in skill_ids
    assert "pc-10-3" in skill_ids
    assert "pc-limit-2" in skill_ids
    missing = [sid for sid in skill_ids if skill_by_id(sid) is None]
    assert missing == []
    assert [t.id for t in TRACKS] == ["algebra", "trig", "precalc", "physics"]


def test_trig_track_is_complete():
    track = track_by_id("trig")
    assert track is not None
    skill_ids = [sid for unit in track.units for sid in unit.skill_ids]
    assert len(skill_ids) >= 24
    for needed in (
        "trig-7-5",
        "trig-7-8",
        "trig-8-4",
        "trig-8-5",
        "trig-9-6",
        "trig-10-3",
        "trig-10-4",
        "pc-10-3",
        "pc-10-8",
    ):
        assert needed in skill_ids
        assert skill_by_id(needed) is not None
    assert any(u.id == "trig-polar" for u in track.units)


def test_trig_high_leverage_skills_are_tagged():
    track = track_by_id("trig")
    assert track is not None
    # SSA is a real trig topic but not a Calc 1 / EE / ME workhorse.
    skip = {"trig-10-4"}
    missing = []
    for sid in [s for u in track.units for s in u.skill_ids]:
        if sid in skip:
            continue
        skill = skill_by_id(sid)
        assert skill is not None
        if not skill.relevance:
            missing.append(sid)
    assert missing == []
    # Spot-check the three disciplines on the trig track.
    by_id = {s.id: s for s in all_skills()}
    assert "calc" in by_id["trig-7-1"].relevance
    assert "ee" in by_id["trig-8-5"].relevance
    assert "me" in by_id["trig-10-2"].relevance
    assert "ee" in by_id["pc-10-5"].relevance


def test_relevance_tags_are_selective_and_complete():
    tagged = [s for s in all_skills() if s.relevance]
    assert 40 <= len(tagged) <= 110
    allowed = {"calc", "ee", "me"}
    unknown = [t for s in tagged for t in s.relevance if t not in allowed]
    assert unknown == []
    missing_why = [s.id for s in tagged if len(s.why_relevant) < 20]
    assert missing_why == []
    ids = {s.id for s in tagged}
    assert "trig-7-1" in ids
    assert "trig-8-1" in ids
    assert "pc-limit-2" in ids
    assert "pc-10-5" in ids
    assert "pc-10-8" in ids
    assert "alg-2-4" in ids
    assert "alg-13-7" not in ids
    assert "pc-12-4" not in ids
    calc = [s for s in tagged if "calc" in s.relevance]
    ee = [s for s in tagged if "ee" in s.relevance]
    me = [s for s in tagged if "me" in s.relevance]
    assert len(calc) >= 20
    assert len(ee) >= 12
    assert len(me) >= 12


def test_inverse_trig_prompt_says_inverse_not_forward():
    for seed in range(50):
        problem = generate_problem("inverse_trig", skill_id="trig-8-3", seed=seed)
        assert r"\arccos" in problem.prompt or r"\arcsin" in problem.prompt or r"\arctan" in problem.prompt
        assert r"\sin^{-1}" in problem.prompt or r"\cos^{-1}" in problem.prompt or r"\tan^{-1}" in problem.prompt
        assert "**Domain:**" in problem.prompt
        assert "**Range:**" in problem.prompt
        assert r"\ccos" not in problem.prompt
        assert "not cosine" in problem.prompt or "not sine" in problem.prompt or "not tangent" in problem.prompt
        assert any("arccos" in m.lower() or "inverse" in m.lower() for m in problem.common_mistakes)


def test_unit_circle_diagram_is_fully_labeled():
    from src.plots import SPECIAL_ANGLES, unit_circle_figure, unit_circle_practice_html

    assert len(SPECIAL_ANGLES) == 16
    degrees = [pt.deg for pt in SPECIAL_ANGLES]
    assert degrees == [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]
    fig = unit_circle_figure(labeled=True)
    texts = " ".join(t.get_text() for t in fig.axes[0].texts)
    assert "30°" in texts
    assert "π/6" in texts
    assert r"\sqrt{3}" in texts or "√3" in texts or "sqrt(3)" in texts
    assert "(1," in texts or r"(1," in texts
    html = unit_circle_practice_html("coordinates")
    assert html.count('class="station"') == 16
    assert html.count('class="hit"') == 16
    assert 'id="uc-drill"' in html
    assert 'id="editor"' in html
    assert "data-k=\"cos\"" in html
    assert "Check" in html
    blank = unit_circle_practice_html("all")
    assert blank.count('class="station"') == 16
    assert "<input" not in blank
    assert 'placeholder=' not in blank
    assert blank.count('data-k="deg"') >= 17
    assert blank.count('data-k="rad"') >= 17
    assert blank.count('data-k="cos"') >= 17
    assert blank.count('data-k="sin"') >= 17
    assert "Choose…" in blank
    assert 'value="30"' in blank
    assert 'value="pi/6"' in blank
    assert 'value="sqrt(3)/2"' in blank
    assert 'value="-sqrt(2)/2"' in blank


def test_trig_identities_catalog_and_drill():
    from src.identities import IDENTITIES, FIELD_ORDER, identities_for, identities_practice_html

    ids = [item.id for item in IDENTITIES]
    assert len(ids) == len(set(ids))
    assert len(IDENTITIES) >= 60
    allowed = set(FIELD_ORDER)
    for item in IDENTITIES:
        assert item.fields
        assert set(item.fields) <= allowed
        assert item.answer
        assert len(item.why) >= 20
        assert item.lhs_tex
        assert item.rhs_tex
    assert len(identities_for(field="math")) >= 40
    assert len(identities_for(field="physics")) >= 20
    assert len(identities_for(field="ee")) >= 18
    assert len(identities_for(field="me")) >= 10
    html = identities_practice_html(field="all")
    assert 'id="id-drill"' in html
    assert "<input" not in html
    assert "Choose…" in html
    assert html.count("<select") >= len(IDENTITIES)
    assert "Check" in html and "Reveal" in html
    for item in IDENTITIES:
        assert item.answer in html
    ee = identities_practice_html(field="ee")
    assert "Euler" in ee
    assert "Law of Sines" not in ee
    me = identities_practice_html(field="me")
    assert "Law of Cosines" in me
    assert "Euler" not in me
    empty = identities_practice_html(field="ee", family="triangles")
    assert "No identities" in empty
    pyth = identities_practice_html(field="math", family="pythagorean")
    assert "sin²(θ) + cos²(θ)" in pyth
    assert pyth.count('data-id="pyth-1"') == 2
    by_id = {item.id: item for item in IDENTITIES}
    for required in (
        "rec-sin",
        "rec-cos",
        "rec-tan",
        "per-cot",
        "per-cot-w",
        "inv-alias-sin",
        "inv-dom-sin",
        "inv-dom-cos",
        "inv-dom-tan",
        "inv-def-sin",
        "tri-cos-a",
        "tri-cos-b",
        "tri-cos-c",
        "tri-tan-ab",
        "tri-tan-bc",
        "tri-tan-ac",
        "tri-mollweide",
    ):
        assert required in by_id, required
    assert by_id["rec-sin"].answer == "1 / csc(θ)"
    assert by_id["per-cot"].answer == "cot(θ)"
    assert by_id["inv-def-sin"].answer == "x = sin(y)"
    assert by_id["inv-dom-sin"].answer == "−1 ≤ x ≤ 1"
    assert by_id["inv-sin-rng"].answer == "−π/2 ≤ y ≤ π/2"
    assert by_id["inv-cos-rng"].answer == "0 ≤ y ≤ π"
    assert by_id["inv-dom-tan"].answer == "−∞ < x < ∞"
    assert by_id["inv-tan-rng"].answer == "−π/2 < y < π/2"
    assert by_id["inv-cos"].answer == "x"
    assert by_id["inv-acos-cos"].answer == "θ"
    assert by_id["inv-alias-sin"].answer == "arcsin(x)"
    assert by_id["inv-def-sin"].labeled_markdown() == r"$y=\sin^{-1}(x)$ is equivalent to $x=\sin(y)$"
    assert "Domain" in by_id["inv-dom-sin"].labeled_markdown()
    assert r"-1\le x\le 1" in by_id["inv-dom-sin"].labeled_markdown()
    assert "sin(γ)/c" in by_id["tri-sines"].answer
    assert "2bc cos" in by_id["tri-cos-a"].answer
    math_html = identities_practice_html(field="math")
    assert "y = sin⁻¹(x) is equivalent to" in math_html
    assert "sin⁻¹(x) = arcsin(x)" in math_html
    assert "−1 ≤ x ≤ 1" in math_html
    assert "Mollweide" in math_html
    assert "Cotangent period" in math_html


def test_flashcards_cover_formulas_and_identities():
    from src.flashcards import (
        FAMILY_ORDER,
        FORMULAS,
        all_flashcards,
        flashcards_for,
    )
    from src.identities import FIELD_ORDER, IDENTITIES

    cards = all_flashcards()
    ids = [card.id for card in cards]
    assert len(ids) == len(set(ids))
    assert len(FORMULAS) >= 40
    assert len(cards) == len(FORMULAS) + len(IDENTITIES)
    allowed = set(FIELD_ORDER)
    for card in cards:
        assert card.fields
        assert set(card.fields) <= allowed
        assert card.family in FAMILY_ORDER
        assert card.name.strip()
        assert card.front.strip()
        assert card.back_tex.strip()
        assert len(card.why) >= 20
    by_id = {card.id: card for card in cards}
    assert "alg-slope-int" in by_id
    assert "y = mx + b" in by_id["alg-slope-int"].back_tex
    assert "kin-g" in by_id
    assert r"10\,\mathrm{m/s^2}" in by_id["kin-g"].back_tex
    assert "id-rec-sin" in by_id
    assert by_id["id-rec-sin"].back_tex == r"1/\csc\theta"
    assert "id-per-cot" in by_id
    assert "id-inv-alias-sin" in by_id
    assert "id-tri-cos-c" in by_id
    assert "id-tri-mollweide" in by_id
    assert "fn-cot-period" in by_id
    assert flashcards_for(field="math")
    assert flashcards_for(field="physics")
    assert flashcards_for(field="ee")
    assert flashcards_for(field="me")
    assert len(flashcards_for(family="trig")) == len(IDENTITIES)
    assert all("math" in c.fields or "physics" in c.fields for c in flashcards_for(field="physics"))
    empty = flashcards_for(field="ee", family="fluids")
    assert empty == ()


def test_physics_course_is_algebra_based_ap_level():
    from src.curriculum import physics_skill_ids, track_by_id
    from src.generate import generate_problem

    track = track_by_id("physics")
    assert track is not None
    p1 = physics_skill_ids(exam="ap_physics1")
    p2 = physics_skill_ids(exam="ap_physics2")
    both = physics_skill_ids()
    assert len(p1) >= 16
    assert len(p2) >= 12
    assert p1 | p2 == both
    assert "phy-1-2" in p1
    assert "phy-10-1" in p2
    assert "phy-7-1" in p1 and "phy-7-1" in p2
    for sid in ("phy-1-2", "phy-3-3", "phy-7-1", "phy-10-1", "phy-14-1"):
        skill = skill_by_id(sid)
        assert skill is not None
        assert skill.status == "ready"
        assert skill.generator
        assert "Remember:" in skill.lesson
        problem = generate_problem(skill.generator, skill_id=sid, seed=42)
        problem.validate()
        assert answers_match(problem.answer, problem.answer)
        assert len(problem.hint) >= 20
        assert problem.steps[0].title


def test_graph_skills_ship_a_matching_figure():
    import matplotlib.pyplot as plt

    from src.figures import FIGURES, figure_for

    samples = [
        ("parabola", "alg-parab"),
        ("transformations", "alg-tf"),
        ("rational_fn", "pre-rat"),
        ("period_amp", "trig-wave"),
        ("ellipse", "pre-ell"),
        ("hyperbola", "pre-hyp"),
        ("phy_projectile", "phy-1-4"),
        ("phy_n2", "phy-2-1"),
        ("phy_snell", "phy-14-1"),
        ("unit_circle", "trig-uc"),
        ("polar_graphs", "pre-polar"),
        ("limit_numeric", "pre-lim"),
    ]
    for name, sid in samples:
        problem = generate_problem(name, skill_id=sid, seed=7)
        assert problem.plot, f"{name} should include a graph or diagram"
        fig = figure_for(problem.plot, problem.plot_data)
        assert fig is not None, f"{name} plot {problem.plot!r} did not render"
        plt.close(fig)

    dummy = {
        "edge": 2,
        "greater": True,
        "x1": 0,
        "y1": 1,
        "x2": 4,
        "y2": 5,
        "a": 1,
        "h": 2,
        "k": 1,
        "lead": 2,
        "degree": 3,
        "roots": [-1, 2],
        "base": 2,
        "n": 3,
        "arg": 8,
        "c": -3,
        "q": 40,
        "p": 3,
        "b": 1,
        "A": 2,
        "kind": "sin",
        "opp": 3,
        "adj": 4,
        "hyp": 5,
        "dist": 10,
        "height": 10,
        "r": 3,
        "deg": 90,
        "a1": 1,
        "b1": 1,
        "c1": 5,
        "a2": 1,
        "b2": -1,
        "c2": -1,
        "x": 2,
        "y": 3,
        "d": 2,
        "lam": 4,
        "V": 12,
        "R": 3,
        "n2": 1.5,
        "w": 10,
        "du": 30,
        "factor": 2,
        "v0": 2,
        "t": 3,
        "v": 20,
        "g": 10,
        "m1": 2,
        "m2": 4,
        "R1": 2,
        "R2": 4,
        "x0": 0,
        "a1": 1,
    }
    dummy["q"] = 40
    for kind in FIGURES:
        fig = figure_for(kind, dummy)
        assert fig is not None, kind
        plt.close(fig)
    assert figure_for(None) is None
    assert len(FIGURES) >= 40

