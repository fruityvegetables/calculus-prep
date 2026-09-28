from __future__ import annotations

from math import gcd
import random

from src.schema import make_problem as _prob
from src.schema import steps as _steps

UNIT_CIRCLE = [
    (0, "0", "0", "1"),
    (30, "pi/6", "1/2", "sqrt(3)/2"),
    (45, "pi/4", "sqrt(2)/2", "sqrt(2)/2"),
    (60, "pi/3", "sqrt(3)/2", "1/2"),
    (90, "pi/2", "1", "0"),
    (120, "2*pi/3", "sqrt(3)/2", "-1/2"),
    (135, "3*pi/4", "sqrt(2)/2", "-sqrt(2)/2"),
    (150, "5*pi/6", "1/2", "-sqrt(3)/2"),
    (180, "pi", "0", "-1"),
    (210, "7*pi/6", "-1/2", "-sqrt(3)/2"),
    (225, "5*pi/4", "-sqrt(2)/2", "-sqrt(2)/2"),
    (240, "4*pi/3", "-sqrt(3)/2", "-1/2"),
    (270, "3*pi/2", "-1", "0"),
    (300, "5*pi/3", "-sqrt(3)/2", "1/2"),
    (315, "7*pi/4", "-sqrt(2)/2", "sqrt(2)/2"),
    (330, "11*pi/6", "-1/2", "sqrt(3)/2"),
]


def deg_to_rad(rng: random.Random, skill_id: str) -> Problem:
    deg, rad, _sinv, _cosv = rng.choice(UNIT_CIRCLE[1:])
    if rng.choice([True, False]):
        prompt = f"Convert ${deg}^\\circ$ to radians. Enter a simplified multiple of pi, like 2*pi/3."
        ans, disp = rad, rad.replace("pi", "π").replace("*", "")
        steps = _steps(
            ("Goal", "Degrees and radians are two unit systems for the same angle. Calculus uses radians."),
            ("Conversion factor", f"{deg}° · (π/180) = {deg}π/180. The 180 in the denominator cancels degree units."),
            ("Reduce the fraction", f"{deg}/180 reduces to the coefficient in {rad}."),
            ("Check the size", f"{deg}° should sit in the same quadrant as {rad}. A half-turn is 180° = π."),
        )
        hint = "Multiply degrees by π/180, then reduce the fraction."
        miss = "Using 180/π, or forgetting to reduce (example: 150π/180 instead of 5π/6)."
    else:
        prompt = (
            f"Convert ${rad.replace('pi', r'\\pi').replace('*', '')}$ radians to degrees. "
            "Enter an integer."
        )
        ans, disp = str(deg), f"{deg}°"
        steps = _steps(
            ("Goal", "Going back to degrees is the inverse conversion. Many diagrams still label degrees."),
            ("Conversion factor", f"Multiply by 180/π: ({rad}) · (180/π) cancels π and leaves {deg}."),
            ("Arithmetic", f"The coefficient of π times 180 is {deg}. That is the degree measure."),
            ("Check the size", f"{rad} is a {deg}° angle. A half-turn is π = 180°."),
        )
        hint = "Multiply radians by 180/π. The π should cancel."
        miss = "Multiplying by π/180 (that's degrees to radians), or leaving π in the answer."
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=ans,
        answer_display=disp,
        hint=hint,
        common_mistakes=[miss],
        exam_tags=["ap_precalc_u3", "clep_precalc"],
        source="generated",
        cluster="trig",
        plot="unit_circle",
        plot_data={"deg": deg},
        steps=steps,
    )


def right_triangle(rng: random.Random, skill_id: str) -> Problem:
    # Pythagorean triples
    a, b, c = rng.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)])
    kind = rng.choice(["sin", "cos", "tan"])
    if kind == "sin":
        ans, disp = f"{a}/{c}", f"{a}/{c}"
        prompt = f"In a right triangle, opposite = {a} and hypotenuse = {c}. Find sin θ as a fraction."
        explain = "sine is opposite over hypotenuse (SOH)."
    elif kind == "cos":
        ans, disp = f"{b}/{c}", f"{b}/{c}"
        prompt = f"In a right triangle, adjacent = {b} and hypotenuse = {c}. Find cos θ as a fraction."
        explain = "cosine is adjacent over hypotenuse (CAH)."
    else:
        ans, disp = f"{a}/{b}", f"{a}/{b}"
        prompt = f"In a right triangle, opposite = {a} and adjacent = {b}. Find tan θ as a fraction."
        explain = "tangent is opposite over adjacent (TOA)."
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=ans,
        answer_display=disp,
        hint="SOH-CAH-TOA: sine = opp/hyp, cosine = adj/hyp, tangent = opp/adj.",
        common_mistakes=["Swapping opposite and adjacent, or putting the hypotenuse in the numerator."],
        exam_tags=["ap_precalc_u3", "clep_precalc"],
        source="generated",
        cluster="trig",
        plot="right_triangle",
        plot_data={"opp": a, "adj": b, "hyp": c},
        steps=_steps(
            ("Goal", "Right-triangle trig is a ratio of two sides. Name which two the function uses."),
            ("Which ratio", explain.capitalize() + " Do not use a calculator for these exact triples."),
            ("Plug in the sides", f"The matching ratio is {disp}."),
            ("Sanity", f"Every trig ratio of an acute angle is positive, and {disp} is between 0 and (for sine/cosine) 1."),
        ),
    )


def unit_circle(rng: random.Random, skill_id: str) -> Problem:
    deg, rad, sinv, cosv = rng.choice(UNIT_CIRCLE)
    fn = rng.choice(["sin", "cos"])
    val = sinv if fn == "sin" else cosv
    prompt = f"Find the exact value of $\\{fn}({rad.replace("pi", r"\pi").replace("*", "")})$."
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=val,
        answer_display=val.replace("sqrt", "√").replace("*", ""),
        hint="Use the reference angle and the quadrant sign. Sine is the y-coordinate; cosine is x.",
        common_mistakes=["Using the reference-angle value but with the wrong sign for that quadrant."],
        exam_tags=["ap_precalc_u3", "clep_precalc"],
        source="generated",
        cluster="trig",
        plot="unit_circle",
        plot_data={"deg": deg},
        steps=_steps(
            ("Goal", "Exact unit-circle values are coordinates of a point on the circle of radius 1, not calculator decimals."),
            ("Where is the angle", f"{deg}° is the same as {rad}. Sine is the y-coordinate and cosine is the x-coordinate of that point."),
            ("Reference and sign", f"The exact {fn} value at this standard angle is {val}. The sign comes from the quadrant (All Students Take Calculus)."),
            ("Write it", f"{fn}({rad}) = {val}. Leave square roots unsimplified as a single fraction if needed."),
        ),
    )


def other_trig(rng: random.Random, skill_id: str) -> Problem:
    # Avoid quadrantal angles so tan/sec/csc are defined.
    deg, rad, sinv, cosv = rng.choice(
        [p for p in UNIT_CIRCLE if p[2] not in ("0", "-0") and p[3] not in ("0", "-0")]
    )
    latex = rad.replace("pi", r"\pi").replace("*", "")
    fn = rng.choice(["tan", "cot", "sec", "csc"])
    if fn == "tan":
        prompt = f"Find the exact value of $\\tan({latex})$."
        ans = f"({sinv})/({cosv})"
        why = "tan θ = sin θ / cos θ = 1 / cot θ, wherever cosine is not 0."
        pieces = f"sin = {sinv} and cos = {cosv}."
    elif fn == "cot":
        prompt = f"Find the exact value of $\\cot({latex})$."
        ans = f"({cosv})/({sinv})"
        why = "cot θ = cos θ / sin θ = 1 / tan θ, wherever sine is not 0."
        pieces = f"cos = {cosv} and sin = {sinv}."
    elif fn == "sec":
        prompt = f"Find the exact value of $\\sec({latex})$."
        ans = f"1/({cosv})"
        why = "sec θ = 1 / cos θ, and the other way is cos θ = 1 / sec θ, wherever cosine is not 0."
        pieces = f"cos = {cosv}, so the reciprocal is 1/({cosv})."
    else:
        prompt = f"Find the exact value of $\\csc({latex})$."
        ans = f"1/({sinv})"
        why = "csc θ = 1 / sin θ, and the other way is sin θ = 1 / csc θ, wherever sine is not 0."
        pieces = f"sin = {sinv}, so the reciprocal is 1/({sinv})."
    disp = ans
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=ans,
        answer_display=disp,
        hint=(
            "Both directions: tan = sin/cos = 1/cot, cot = cos/sin = 1/tan, "
            "sec = 1/cos, cos = 1/sec, csc = 1/sin, sin = 1/csc. Use unit-circle sine and cosine."
        ),
        common_mistakes=["Inverting the ratio, or using cosine when the reciprocal of sine was required (csc, not sec)."],
        exam_tags=["ap_precalc_u3"],
        source="generated",
        cluster="trig",
        plot="unit_circle",
        plot_data={"deg": deg},
        steps=_steps(
            ("Goal", "The other four trig functions are defined from sine and cosine (or as reciprocals)."),
            ("Definition", why),
            ("Unit-circle pieces", pieces),
            ("Write the exact value", f"The exact value is {disp}. You may cancel a shared √2 or 2 if both parts share one."),
        ),
    )


def period_amp(rng: random.Random, skill_id: str) -> Problem:
    b = rng.choice([2, 3, 4, 5, 6])
    a = rng.choice([2, 3, 4, 5])
    kind = rng.choice(["period", "amp"])
    if kind == "period":
        prompt = f"What is the period of $y = \\sin({b}x)$? Enter a simplified expression like pi/2."
        ans = f"2*pi/{b}" if b != 2 else "pi"
        if b == 2:
            ans = "pi"
        elif b == 4:
            ans = "pi/2"
        elif b == 6:
            ans = "pi/3"
        else:
            ans = f"2*pi/{b}"
        return _prob(
            id=f"{skill_id}-{rng.randrange(10**9)}",
            skill_id=skill_id,
            prompt=prompt,
            answer=ans,
            answer_display=ans.replace("pi", "π").replace("*", ""),
            hint="Period of sin(bx) or cos(bx) is 2π/|b|.",
            common_mistakes=["Answering b, or 2π·b instead of 2π/|b|."],
            exam_tags=["ap_precalc_u3"],
            source="generated",
            cluster="trig",
            plot="sine",
            plot_data={"A": 1, "b": b, "kind": "sin", "title": rf"$y=\sin({b}x)$"},
            steps=_steps(
                ("Goal", "Period is how far x must move before the wave repeats one full cycle."),
                ("Parent period", "y = sin x has period 2π. Replacing x by bx compresses the graph by |b|."),
                ("Formula", f"Period = 2π/|{b}| = {ans}."),
                ("Check", f"When x increases by that amount, {b}x increases by 2π, a full sine cycle."),
            ),
        )
    prompt = f"What is the amplitude of $y = {a}\\cos(x)$?"
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(a),
        answer_display=str(a),
        hint="Amplitude is |A| in y = A sin(bx) or A cos(bx). It is never negative.",
        common_mistakes=["Reporting -A when A is written with a minus, but forgetting the absolute value."],
        exam_tags=["ap_precalc_u3"],
        source="generated",
        cluster="trig",
        plot="sine",
        plot_data={"A": a, "b": 1, "kind": "cos", "title": rf"$y={a}\cos x$"},
        steps=_steps(
            ("Goal", "Amplitude is the height from the midline to a peak, always a positive number."),
            ("Coefficient", f"Here A = {a}, so amplitude = |{a}| = {a}."),
            ("Picture", f"The graph oscillates between -{a} and {a} if it is not shifted vertically."),
            ("Not the period", "Amplitude is vertical. Period is horizontal. Do not mix the two numbers."),
        ),
    )


def tan_period(rng: random.Random, skill_id: str) -> Problem:
    b = rng.choice([1, 2, 3, 4])
    prompt = f"What is the period of $y = \\tan({b}x)$? Enter an expression like pi/2."
    if b == 1:
        ans = "pi"
    elif b == 2:
        ans = "pi/2"
    elif b == 4:
        ans = "pi/4"
    else:
        ans = f"pi/{b}"
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=ans,
        answer_display=ans.replace("pi", "π"),
        hint="Parent tangent and cotangent both have period π, not 2π. Period of tan(bx) or cot(bx) is π/|b|.",
        common_mistakes=["Using 2π/|b| as if tangent were sine."],
        exam_tags=["ap_precalc_u3"],
        source="generated",
        cluster="trig",
        plot="tan",
        plot_data={"b": b},
        steps=_steps(
            ("Goal", "Tangent repeats more often than sine because it comes from sin/cos and blows up at odd multiples of π/2. Cotangent has the same period π."),
            ("Parent period", "y = tan x and y = cot x both have period π (from one vertical asymptote to the next matching one)."),
            ("Compression", f"y = tan({b}x) has period π/|{b}| = {ans}. The same formula holds for cot({b}x)."),
            ("Asymptotes", "Those vertical lines are part of the graph's identity. Do not treat tan as a wave with amplitude."),
        ),
    )


def inverse_trig(rng: random.Random, skill_id: str) -> Problem:
    options = [
        ("sin", "1/2", "pi/6", "π/6"),
        ("sin", "sqrt(2)/2", "pi/4", "π/4"),
        ("sin", "sqrt(3)/2", "pi/3", "π/3"),
        ("sin", "1", "pi/2", "π/2"),
        ("sin", "0", "0", "0"),
        ("sin", "-1/2", "-pi/6", "−π/6"),
        ("cos", "1/2", "pi/3", "π/3"),
        ("cos", "0", "pi/2", "π/2"),
        ("cos", "1", "0", "0"),
        ("cos", "-1", "pi", "π"),
        ("tan", "1", "pi/4", "π/4"),
        ("tan", "0", "0", "0"),
        ("tan", "-1", "-pi/4", "−π/4"),
    ]
    meta = {
        "sin": {
            "inv": r"\sin^{-1}",
            "alt": r"\arcsin",
            "alt_en": "arcsin",
            "fwd": "sine",
            "fwd_tex": r"\sin",
            "domain": r"-1\le x\le 1",
            "domain_en": "−1 ≤ x ≤ 1",
            "rng": r"-\pi/2\le y\le\pi/2",
            "rng_en": "−π/2 ≤ y ≤ π/2",
        },
        "cos": {
            "inv": r"\cos^{-1}",
            "alt": r"\arccos",
            "alt_en": "arccos",
            "fwd": "cosine",
            "fwd_tex": r"\cos",
            "domain": r"-1\le x\le 1",
            "domain_en": "−1 ≤ x ≤ 1",
            "rng": r"0\le y\le\pi",
            "rng_en": "0 ≤ y ≤ π",
        },
        "tan": {
            "inv": r"\tan^{-1}",
            "alt": r"\arctan",
            "alt_en": "arctan",
            "fwd": "tangent",
            "fwd_tex": r"\tan",
            "domain": r"-\infty<x<\infty",
            "domain_en": "−∞ < x < ∞",
            "rng": r"-\pi/2<y<\pi/2",
            "rng_en": "−π/2 < y < π/2",
        },
    }
    arg_tex_map = {
        "1/2": r"1/2",
        "sqrt(2)/2": r"\sqrt{2}/2",
        "sqrt(3)/2": r"\sqrt{3}/2",
        "1": "1",
        "0": "0",
        "-1/2": r"-1/2",
        "-1": "-1",
    }
    fn, arg, ans, disp = rng.choice(options)
    info = meta[fn]
    arg_tex = arg_tex_map[arg]
    prompt = (
        f"Evaluate ${info['inv']}({arg_tex})$ in radians.\n\n"
        f"From Paul’s inverse trig table:\n\n"
        f"**Function:** $y = {info['inv']}(x)$\n\n"
        f"**Domain:** ${info['domain']}$\n\n"
        f"**Range:** ${info['rng']}$\n\n"
        f"**Definition:** $y = {info['inv']}(x)$ is equivalent to "
        f"$x = {info['fwd_tex']}(y)$.\n\n"
        f"**Inverse Properties:** "
        r"$\cos(\cos^{-1}(x))=x$, $\cos^{-1}(\cos(\theta))=\theta$, "
        r"$\sin(\sin^{-1}(x))=x$, $\sin^{-1}(\sin(\theta))=\theta$, "
        r"$\tan(\tan^{-1}(x))=x$, $\tan^{-1}(\tan(\theta))=\theta$."
        "\n\n"
        f"**Alternate notation:** ${info['inv']}(x) = {info['alt']}(x)$.\n\n"
        f"This is inverse {info['fwd']}, not {info['fwd']}. "
        f"Find the unique $y$ in the range such that "
        f"${info['fwd_tex']}(y) = {arg_tex}$."
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=ans,
        answer_display=disp,
        hint=(
            f"Paul: y = {fn}⁻¹(x) is equivalent to x = {info['fwd']}(y). "
            f"Domain {info['domain_en']}; Range {info['rng_en']}. "
            f"Alternate notation: {fn}⁻¹(x) = {info['alt_en']}(x)."
        ),
        common_mistakes=[
            f"Evaluating {info['fwd']}({arg}) instead of {fn}⁻¹({arg}). "
            f"For example, cos(0) = 1, but cos⁻¹(0) = π/2 because cos(π/2) = 0.",
            "Giving another angle with the same trig value that sits outside Paul’s range for that inverse.",
        ],
        exam_tags=["ap_precalc_u3"],
        source="generated",
        cluster="trig",
        plot="unit_circle",
        plot_data={},
        steps=_steps(
            (
                "Goal",
                f"Paul’s definition: y = {fn}⁻¹({arg}) is equivalent to {info['fwd']}(y) = {arg}, "
                f"with y in {info['rng_en']}. That is not {info['fwd']}({arg}), "
                f"and it is not 1/{info['fwd']}({arg}).",
            ),
            (
                "Domain and range",
                f"Function y = {fn}⁻¹(x). Domain {info['domain_en']}. Range {info['rng_en']}. "
                "Any other angle with the same trig value is a valid equation solution later, "
                "but it is not the value of the inverse.",
            ),
            (
                "Match a unit-circle angle",
                f"On the unit circle, cosine is the x-coordinate and sine is the y-coordinate. "
                f"The unique y in {info['rng_en']} whose {info['fwd']} is {arg} is {disp}.",
            ),
            (
                "Check",
                f"{info['fwd']}({disp}) = {arg}, and {disp} sits in {info['rng_en']}, "
                f"so {fn}⁻¹({arg}) = {info['alt_en']}({arg}) = {disp}.",
            ),
        ),
    )


def identity_simplify(rng: random.Random, skill_id: str) -> Problem:
    kind = rng.choice(["tan", "pythag", "recip"])
    if kind == "tan":
        prompt = r"Simplify $\dfrac{\sin x}{\cos x}$ to a single trig function. Enter tan(x)."
        ans, disp = "tan(x)", "tan(x)"
        steps = _steps(
            ("Goal", "Rewrite a quotient of basic trig functions as one named function."),
            ("Definition", "By definition, tan x = sin x / cos x wherever cos x ≠ 0."),
            ("Conclusion", "The simplified form is tan(x). That is a definition, not a coincidence."),
            ("Related identity", "cot x is the reciprocal, cos x / sin x. Do not swap them."),
        )
    elif kind == "pythag":
        prompt = r"Simplify $\sin^2 x + \cos^2 x$. Enter the integer it equals."
        ans, disp = "1", "1"
        steps = _steps(
            ("Goal", "The Pythagorean identity is the unit circle equation x^2 + y^2 = 1 with x = cos and y = sin."),
            ("Identity", "sin²x + cos²x = 1 for every x where sine and cosine are defined (all real x)."),
            ("Why", "A point (cos x, sin x) lies on the unit circle, so the sum of squares of coordinates is 1."),
            ("Answer", "The expression simplifies to the integer 1, not to another trig function."),
        )
    else:
        if rng.choice([True, False]):
            prompt = r"Simplify $\dfrac{1}{\sin x}$. Enter csc(x)."
            ans, disp = "csc(x)", "csc(x)"
            steps = _steps(
                ("Goal", "Reciprocal identities go both ways: csc x = 1/sin x and sin x = 1/csc x."),
                ("Definition", "csc x = 1/sin x, wherever sin x ≠ 0."),
                ("Conclusion", "The simplified form is csc(x)."),
                ("Not cosine", "The reciprocal of sine is cosecant, not cosine. Cosine is the cofunction, a different idea."),
            )
        else:
            prompt = r"Simplify $\dfrac{1}{\csc x}$. Enter sin(x)."
            ans, disp = "sin(x)", "sin(x)"
            steps = _steps(
                ("Goal", "The other reciprocal identity: sin x = 1/csc x, paired with csc x = 1/sin x."),
                ("Definition", "1/csc x is sine, wherever csc x is defined (sin x ≠ 0)."),
                ("Conclusion", "The simplified form is sin(x)."),
                ("Not secant", "Do not swap the pair. 1/sec x is cosine, and 1/cot x is tangent."),
            )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=ans,
        answer_display=disp,
        hint="Use a definition or the Pythagorean identity. Do not expand unless you must.",
        common_mistakes=["Writing cot when you meant tan, or thinking 1/sin x is cos x."],
        exam_tags=["ap_precalc_u3", "clep_precalc"],
        source="generated",
        cluster="trig",
        steps=steps,
    )


def sum_diff(rng: random.Random, skill_id: str) -> Problem:
    # cos(a-b) or sin(a+b) with 45 and 30 -> 75, exact
    prompt = r"Find the exact value of $\sin(75^\circ)$ using an angle-sum formula. Enter something like (sqrt(6)+sqrt(2))/4."
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer="(sqrt(6)+sqrt(2))/4",
        answer_display="(√6 + √2)/4",
        hint="75° = 45° + 30°. Use sin(a+b) = sin a cos b + cos a sin b.",
        common_mistakes=["Using 45+30 but subtracting the two products instead of adding (that's cosine of a sum)."],
        exam_tags=["ap_precalc_u3"],
        source="generated",
        cluster="trig",
        steps=_steps(
            ("Goal", "75° is not a 30-45-60 chart angle, but it is a sum of two chart angles."),
            ("Split the angle", "75° = 45° + 30°. The sum formula is sin(a+b) = sin a cos b + cos a sin b."),
            ("Plug in known values", "sin 45 = √2/2, cos 45 = √2/2, sin 30 = 1/2, cos 30 = √3/2. So (√2/2)(√3/2) + (√2/2)(1/2)."),
            ("Simplify", "(√6 + √2)/4. Keep the two square roots; they do not combine into one radical."),
        ),
    )


def double_angle(rng: random.Random, skill_id: str) -> Problem:
    prompt = r"If $\sin \theta = 3/5$ and $\theta$ is in quadrant I, find $\sin(2\theta)$ as a fraction."
    # cos = 4/5, sin 2θ = 2 sin cos = 24/25
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer="24/25",
        answer_display="24/25",
        hint="sin(2θ) = 2 sin θ cos θ. Find cos θ from a Pythagorean triple first.",
        common_mistakes=["Doubling 3/5 to get 6/5, which is not a valid sine and skips the formula."],
        exam_tags=["ap_precalc_u3"],
        source="generated",
        cluster="trig",
        steps=_steps(
            ("Goal", "Double-angle formulas need both sine and cosine of the original angle."),
            ("Find cosine", "sin² + cos² = 1 ⇒ cos² = 1 - 9/25 = 16/25. In quadrant I, cos θ = 4/5."),
            ("Apply the formula", "sin(2θ) = 2 sin θ cos θ = 2·(3/5)·(4/5) = 24/25."),
            ("Check size", "24/25 is less than 1, so it is a possible sine. 6/5 would have been impossible."),
        ),
    )


def product_sum(rng: random.Random, skill_id: str) -> Problem:
    prompt = (
        r"The product-to-sum identity starts $2\sin A \sin B = \cos(A-B) - \cos(A+B)$. "
        r"Using A = 45° and B = 15° is not required here: what is $2\sin x \sin x$ equal to, "
        r"as a single simplified expression in terms of cos(2x)? Enter 1-cos(2x) or equivalent."
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer="1-cos(2*x)",
        answer_display="1 - cos(2x)",
        hint="2 sin x sin x = 2 sin² x, and the double-angle/power-reduction identity is 2 sin² x = 1 - cos(2x).",
        common_mistakes=["Writing 2 sin(2x), or cos(2x) without the 1 minus."],
        exam_tags=["ap_precalc_u3"],
        source="generated",
        cluster="trig",
        steps=_steps(
            ("Goal", "Product-to-sum and power-reduction identities rewrite products as sums (or constants plus cosines)."),
            ("Same-angle product", "2 sin x sin x is 2 sin² x, a power rather than two different angles."),
            ("Power-reduction", "The identity 2 sin² x = 1 - cos(2x) is the product-to-sum formula with A = B = x."),
            ("Answer", "2 sin x sin x = 1 - cos(2x). This is the form calculus uses to integrate sin² x."),
        ),
    )


def solve_trig(rng: random.Random, skill_id: str) -> Problem:
    options = [
        (r"$\sin x = 1/2$", "2", "Two solutions: π/6 and 5π/6."),
        (r"$\cos x = 1/2$", "2", "Two solutions: π/3 and 5π/3."),
        (r"$\sin x = 0$", "2", "Two solutions in [0, 2π): 0 and π. (2π is the same angle as 0 and is excluded.)"),
        (r"$\cos x = -1$", "1", "Only x = π in [0, 2π)."),
        (r"$\sin x = 1$", "1", "Only x = π/2 in [0, 2π)."),
    ]
    expr, ans, detail = rng.choice(options)
    prompt = f"How many solutions does {expr} have in $[0, 2\\pi)$? Enter an integer."
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=ans,
        answer_display=ans,
        hint="Sketch one period of sine or cosine. Count intersections with the horizontal line, on a half-open full rotation.",
        common_mistakes=["Counting only the reference angle, or including 2π as an extra solution when it equals 0."],
        exam_tags=["ap_precalc_u3"],
        source="generated",
        cluster="trig",
        plot="sine",
        plot_data={"A": 1, "b": 1, "kind": "sin", "title": "Count intersections on one period"},
        steps=_steps(
            ("Goal", "On one full rotation there is usually more than one angle with a given sine or cosine."),
            ("Reference angle plus quadrants", "Sine is positive in QI and QII; cosine is positive in QI and QIV. Use that to list candidates."),
            ("Count on [0, 2π)", detail),
            ("Interval detail", "The interval is half-open at 2π, so do not count 0 and 2π as two different solutions."),
        ),
    )


def law_sines(rng: random.Random, skill_id: str) -> Problem:
    if rng.choice([True, False]):
        a_ang, b_ang = rng.choice([(40, 60), (30, 70), (45, 45), (20, 80)])
        c_ang = 180 - a_ang - b_ang
        prompt = (
            f"A triangle has angle A = {a_ang}° and angle B = {b_ang}°. "
            "Find angle C in degrees."
        )
        ans, disp = str(c_ang), str(c_ang)
        steps = _steps(
            ("Goal", "Before using Law of Sines, see whether the missing piece is an angle. If two angles are known, the third is determined."),
            ("Angle sum", f"A + B + C = 180°, so C = 180 - {a_ang} - {b_ang} = {c_ang}."),
            ("When you would use Law of Sines", "The full form is a/sin A = b/sin B = c/sin C. You need that after you have C, if the question asked for a side."),
            ("Ambiguous case later", "SSA can produce 0, 1, or 2 triangles. AAS/ASA like this one is unique."),
        )
        hint = "Angles in a triangle sum to 180°. Law of Sines needs a side only when you are finding a side."
        miss = "Adding A and B and calling that C, or using 90° as if every triangle were right."
    else:
        # 30-90-60: side opposite 30 is half the hypotenuse.
        a = rng.choice([3, 4, 5, 6, 7])
        hyp = 2 * a
        prompt = (
            f"Triangle ABC has A = 30°, B = 90°, and side a = {a} (opposite A). "
            "Use the Law of Sines to find side b (opposite B, the hypotenuse)."
        )
        ans, disp = str(hyp), str(hyp)
        steps = _steps(
            ("Goal", "Law of Sines: a/sin A = b/sin B = c/sin C. Here we know an angle-side pair and a second angle."),
            ("Write the proportion", f"{a}/sin 30° = b/sin 90°. sin 30° = 1/2 and sin 90° = 1."),
            ("Solve for b", f"b = {a} / (1/2) = {hyp}. The side opposite 90° is the hypotenuse, twice the side opposite 30°."),
            ("Check", f"A 30-60-90 triangle with short leg {a} has hypotenuse {hyp}. Law of Sines recovered the same fact."),
        )
        hint = "a/sin A = b/sin B = c/sin C. sin 30° = 1/2 and sin 90° = 1."
        miss = "Using sin 30° = √3/2, or swapping which side is opposite which angle."
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=ans,
        answer_display=disp,
        hint=hint,
        common_mistakes=[miss],
        exam_tags=["clep_precalc"],
        source="generated",
        cluster="trig",
        plot="oblique_triangle",
        plot_data={},
        steps=steps,
    )


def law_cosines(rng: random.Random, skill_id: str) -> Problem:
    if rng.choice([True, False]):
        prompt = (
            "A triangle has sides a = 3, b = 4, and included angle C = 90°. "
            "Find side c (the side opposite C)."
        )
        ans, disp = "5", "5"
        steps = _steps(
            ("Goal", "Law of Cosines handles SAS or SSS. A right angle is the special case that becomes Pythagoras."),
            ("Write the formula", "c² = a² + b² − 2ab cos C = 9 + 16 − 2·3·4·cos 90°. The cyclic companions are a² = b² + c² − 2bc cos A and b² = a² + c² − 2ac cos B."),
            ("Cosine of 90°", "cos 90° = 0, so c² = 25 and c = 5 (length is positive)."),
            ("Name it", "This is a 3-4-5 right triangle. Law of Cosines agrees with Pythagoras when C is right."),
        )
        hint = "Law of Cosines (all three cyclic forms): c² = a² + b² − 2ab cos C. If C = 90°, cos 90° = 0 and this is Pythagoras."
        miss = "Using a + b, or forgetting that the 2ab cos C term is 0 when C is right."
    else:
        side = rng.choice([4, 5, 6, 8])
        prompt = (
            f"A triangle has sides a = {side}, b = {side}, and included angle C = 60°. "
            "Find side c (opposite C)."
        )
        ans, disp = str(side), str(side)
        steps = _steps(
            ("Goal", "SAS with an included 60° and two equal sides is an equilateral triangle — Law of Cosines should say so."),
            ("Write the formula", f"c² = a² + b² − 2ab cos 60° = {side}² + {side}² − 2·{side}·{side}·(1/2)."),
            ("Simplify", f"cos 60° = 1/2, so the last term is {side}². Then c² = {side}² + {side}² − {side}² = {side}²."),
            ("Length", f"c = {side} (positive). Two sides and a 60° included angle force all three sides equal."),
        )
        hint = "Law of Cosines (cyclic): c² = a² + b² − 2ab cos C. cos 60° = 1/2."
        miss = "Using Law of Sines on SAS (you don't have a side opposite a known angle pair yet), or using cos 60° = √3/2."
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=ans,
        answer_display=disp,
        hint=hint,
        common_mistakes=[miss],
        exam_tags=["clep_precalc"],
        source="generated",
        cluster="trig",
        plot="oblique_triangle",
        plot_data={},
        steps=steps,
    )


def arc_length(rng: random.Random, skill_id: str) -> Problem:
    if rng.choice([True, False]):
        r, n, d = rng.choice([(6, 1, 3), (4, 1, 2), (10, 1, 5), (8, 1, 4), (12, 2, 3)])
        # s = r * (n π / d) = (r n / d) π
        coef_num, coef_den = r * n, d
        g = gcd(coef_num, coef_den)
        coef_num //= g
        coef_den //= g
        ans = "pi" if (coef_num, coef_den) == (1, 1) else (
            f"{coef_num}*pi" if coef_den == 1 else f"{coef_num}*pi/{coef_den}"
        )
        theta = "pi" if (n, d) == (1, 1) else (f"pi/{d}" if n == 1 else f"{n}*pi/{d}")
        theta_tex = theta.replace("pi", r"\pi").replace("*", "")
        prompt = (
            f"A circle has radius {r}. A central angle measures ${theta_tex}$ radians. "
            "Find the arc length. Enter a simplified multiple of pi, like 2*pi."
        )
        steps = _steps(
            ("Goal", "Arc length uses radians: s = rθ. Degrees would need a conversion first."),
            ("Plug in", f"s = {r} · ({theta}) = {ans}."),
            ("Why radians", "The formula s = rθ is the definition of radian measure: θ = s/r."),
            ("Units", "The answer is a length (same units as the radius), written as a multiple of π."),
        )
        hint = "s = rθ with θ in radians."
        miss = "Using the degree form of the angle in s = rθ, or forgetting to multiply by r."
    else:
        r = rng.choice([4, 6, 8, 10])
        # A = (1/2) r² (π/2) = r² π / 4
        ans = f"{(r * r) // 4}*pi"
        prompt = (
            f"A circle has radius {r}. A central angle measures $\\pi/2$ radians. "
            "Find the area of the sector. Enter a simplified multiple of pi, like 4*pi."
        )
        steps = _steps(
            ("Goal", "Sector area is A = (1/2) r² θ with θ in radians."),
            ("Plug in", f"A = (1/2)·{r}²·(π/2) = {ans}."),
            ("Picture", "π/2 is a quarter-turn, so this is one-fourth of the full disk area πr²."),
            ("Check", f"Full area is {r}²π. A quarter of that is {ans}, matching the formula."),
        )
        hint = "A = (1/2) r² θ with θ in radians. π/2 is a quarter circle."
        miss = "Using (1/2) r θ (that's missing an r), or reporting the arc length instead of the area."
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=ans,
        answer_display=ans.replace("pi", "π").replace("*", ""),
        hint=hint,
        common_mistakes=[miss],
        exam_tags=["ap_precalc_u3"],
        source="generated",
        cluster="trig",
        plot="sector",
        plot_data={"r": r, "frac": 0.25},
        steps=steps,
    )


def coterminal(rng: random.Random, skill_id: str) -> Problem:
    kind = rng.choice(["pos", "neg", "big"])
    if kind == "pos":
        extra = rng.choice([1, 2])
        core = rng.choice([20, 40, 75, 110, 200])
        given = core + 360 * extra
        ans = str(core)
        prompt = (
            f"Find the angle coterminal with {given}° that lies in $[0, 360)$. "
            "Enter an integer."
        )
        steps = _steps(
            ("Goal", "Coterminal angles share a terminal side. Subtract full turns of 360° until you land in [0, 360)."),
            ("Subtract", f"{given} minus {extra} full turn(s) of 360° is {given} - {360 * extra} = {core}."),
            ("Interval", f"{core} is in [0, 360), so it is the representative the question asked for."),
            ("Check", f"{core}° and {given}° differ by {extra} full rotation(s), so they point the same way."),
        )
    elif kind == "neg":
        core = rng.choice([30, 45, 90, 120, 200])
        given = core - 360
        ans = str(core)
        prompt = (
            f"Find the angle coterminal with {given}° that lies in $[0, 360)$. "
            "Enter an integer."
        )
        steps = _steps(
            ("Goal", "A negative angle is clockwise. Add 360° to land in the standard [0, 360) interval."),
            ("Add a turn", f"Add one full rotation: {given} + 360 = {core}. That lands on a positive angle."),
            ("Interval", f"{core} is in [0, 360). Do not stop at the negative angle the problem started with."),
            ("Check", f"{core}° is one full turn away from {given}°, so they are coterminal."),
        )
    else:
        given = rng.choice([750, 800, 900])
        core = given % 360
        ans = str(core)
        prompt = (
            f"Find the angle coterminal with {given}° that lies in $[0, 360)$. "
            "Enter an integer."
        )
        steps = _steps(
            ("Goal", "When the angle is larger than one turn, take the remainder after dividing by 360."),
            ("Reduce", f"{given} = {given // 360}·360 + {core}, so the remainder is {core}."),
            ("Interval", f"{core} is in [0, 360). That is the coterminal representative."),
            ("Check", f"Adding {given // 360} full turns to {core}° recovers {given}°."),
        )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=ans,
        answer_display=f"{ans}°",
        hint="Add or subtract 360° until the angle sits in [0, 360). That is the remainder modulo 360.",
        common_mistakes=["Leaving a negative angle, or subtracting 180° instead of 360°."],
        exam_tags=["ap_precalc_u3"],
        source="generated",
        cluster="trig",
        plot="unit_circle",
        plot_data={"deg": core},
        steps=steps,
    )


def angular_speed(rng: random.Random, skill_id: str) -> Problem:
    if rng.choice([True, False]):
        k = rng.choice([2, 3, 4, 5, 6])
        t = rng.choice([2, 4, 5])
        # θ = k π, ω = θ/t
        # Keep answers as multiples of pi when possible.
        num, den = k, t
        g = gcd(num, den)
        num //= g
        den //= g
        ans = "pi" if (num, den) == (1, 1) else (
            f"{num}*pi" if den == 1 else f"{num}*pi/{den}"
        )
        prompt = (
            f"A wheel turns through ${k}\\pi$ radians in {t} seconds. "
            "What is its angular speed in radians per second? Enter a simplified multiple of pi."
        )
        steps = _steps(
            ("Goal", "Angular speed is how fast the angle changes: ω = θ/t, with θ in radians."),
            ("Divide", f"ω = {k}π / {t} = {ans} rad/s."),
            ("Units", "Radians per second, not revolutions per second. (One revolution is 2π radians.)"),
            ("Check size", f"In {t} seconds the wheel covers {k} half-turns of π, which is consistent with {ans} each second."),
        )
        hint = "ω = θ/t with θ in radians."
        miss = "Dividing by 2π as if the question asked for revolutions per second."
    else:
        r = rng.choice([2, 3, 4, 5])
        w = rng.choice([2, 3, 4, 6])
        v = r * w
        prompt = (
            f"A rotating disk has radius {r} and angular speed {w} rad/s. "
            "Find the linear speed of a point on the rim. Enter an integer."
        )
        steps = _steps(
            ("Goal", "Linear (tangential) speed along the rim is v = rω."),
            ("Multiply", f"v = {r} · {w} = {v}."),
            ("Why", "In one second the angle is ω, so the arc is rω. Arc per second is linear speed."),
            ("Units", f"If r is in meters, v is {v} m/s. Do not add r and ω."),
        )
        hint = "v = rω. Radius times angular speed."
        miss = "Adding r and ω, or using v = r/ω."
        ans = str(v)
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=ans,
        answer_display=ans.replace("pi", "π").replace("*", "") if "pi" in ans else ans,
        hint=hint,
        common_mistakes=[miss],
        exam_tags=["ap_precalc_u3"],
        source="generated",
        cluster="trig",
        steps=steps,
    )


def elevation(rng: random.Random, skill_id: str) -> Problem:
    if rng.choice([True, False]):
        dist = rng.choice([8, 10, 12, 15, 20])
        prompt = (
            f"From {dist} feet away, the angle of elevation to the top of a pole is 45°. "
            "Find the height of the pole. Enter an integer."
        )
        ans = str(dist)
        steps = _steps(
            ("Goal", "Angle of elevation from the ground makes a right triangle. Height is the opposite side."),
            ("Which ratio", f"tan 45° = opposite/adjacent = height/{dist}."),
            ("Value", f"tan 45° = 1, so height = {dist}."),
            ("Picture", "A 45-45-90 triangle has equal legs. Distance and height match."),
        )
        hint = "tan(elevation) = height / distance. tan 45° = 1."
        miss = "Using sin 45° = height/distance, which would insert an extra √2."
        el_plot = {"dist": dist, "height": dist, "angle": r"$45^\circ$"}
    else:
        dist = rng.choice([10, 12, 16, 20])
        # 30°: height = dist * tan 30 = dist / √3, messy.
        # Use 30° with hypotenuse: a kite string of length dist at 30° to the ground.
        # height = dist * sin 30 = dist/2.
        prompt = (
            f"A guy wire of length {dist} m meets the ground at 30°. "
            "How high does it reach up the pole? Enter an integer."
        )
        ans = str(dist // 2)
        steps = _steps(
            ("Goal", "The wire is the hypotenuse. The height is opposite the 30° angle."),
            ("Which ratio", f"sin 30° = opposite/hypotenuse = height/{dist}."),
            ("Value", f"sin 30° = 1/2, so height = {dist}/2 = {ans}."),
            ("Check", "In a 30-60-90 triangle the side opposite 30° is half the hypotenuse."),
        )
        hint = "The wire is the hypotenuse. sin 30° = 1/2 = height / wire."
        miss = "Using tan 30° with the wire as adjacent, or using sin 30° = √3/2."
        el_plot = {"dist": dist, "height": dist // 2, "angle": r"$30^\circ$"}
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=ans,
        answer_display=ans,
        hint=hint,
        common_mistakes=[miss],
        exam_tags=["ap_precalc_u3"],
        source="generated",
        cluster="trig",
        plot="elevation",
        plot_data=el_plot,
        steps=steps,
    )


def cofunction(rng: random.Random, skill_id: str) -> Problem:
    kind = rng.choice(["sin", "cos", "tan"])
    if kind == "sin":
        prompt = r"Simplify $\sin(\pi/2 - x)$ to a single trig function of $x$. Enter cos(x)."
        ans, disp = "cos(x)", "cos(x)"
        ident = "sin(π/2 − x) = cos x. Complementary angles swap sine with cosine."
    elif kind == "cos":
        prompt = r"Simplify $\cos(\pi/2 - x)$ to a single trig function of $x$. Enter sin(x)."
        ans, disp = "sin(x)", "sin(x)"
        ident = "cos(π/2 − x) = sin x. The cofunction of cosine is sine."
    else:
        prompt = r"Simplify $\tan(\pi/2 - x)$ to a single trig function of $x$. Enter cot(x)."
        ans, disp = "cot(x)", "cot(x)"
        ident = "tan(π/2 − x) = cot x. Tangent and cotangent are cofunctions."
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=ans,
        answer_display=disp,
        hint="Cofunctions pair sine with cosine and tangent with cotangent. π/2 − x is the complement of x.",
        common_mistakes=["Writing the same function back (sin stays sin), or using a negative sign as if this were even/odd."],
        exam_tags=["ap_precalc_u3"],
        source="generated",
        cluster="trig",
        steps=_steps(
            ("Goal", "A cofunction identity rewrites a trig function of a complement as a different trig function of the original angle."),
            ("Identity", ident),
            ("Why", "On a right triangle, the two acute angles add to 90°. Opposite for one is adjacent for the other."),
            ("Answer", f"The simplified form is {disp}. Do not keep the π/2 in the answer."),
        ),
    )


def phase_shift(rng: random.Random, skill_id: str) -> Problem:
    if rng.choice([True, False]):
        # y = sin(x - h), shift right h
        h_tex, ans, disp, direction = rng.choice(
            [
                (r"\pi/2", "pi/2", "π/2", "right"),
                (r"\pi/3", "pi/3", "π/3", "right"),
                (r"\pi/4", "pi/4", "π/4", "right"),
                (r"\pi/6", "pi/6", "π/6", "right"),
            ]
        )
        prompt = (
            f"The graph of $y = \\sin(x - {h_tex})$ is the graph of $y = \\sin x$ shifted "
            f"how far to the {direction}? Enter a simplified multiple of pi, like pi/2."
        )
        steps = _steps(
            ("Goal", "Inside a sine, subtracting h from x shifts the graph right by h (horizontal shifts feel backwards)."),
            ("Form", f"y = sin(x − {disp}) is already factored. The number subtracted from x is the right shift."),
            ("Read it", f"The shift is {disp} to the right."),
            ("Check", "x has to be {disp} larger before the inside is 0, so the 'start' of the wave moves right."),
        )
        hint = "y = sin(x − h) is shifted h units to the right. The sign is the opposite of the one you see."
        miss = "Shifting left because of the minus sign, or reporting the phase as the coefficient of x."
        return _prob(
            id=f"{skill_id}-{rng.randrange(10**9)}",
            skill_id=skill_id,
            prompt=prompt,
            answer=ans,
            answer_display=disp,
            hint=hint,
            common_mistakes=[miss],
            exam_tags=["ap_precalc_u3"],
            source="generated",
            cluster="trig",
            plot="sine",
            plot_data={"A": 1, "b": 1, "shift": 1.0, "kind": "sin", "title": r"$y=\sin(x-h)$ shifts right"},
            steps=steps,
        )
    k = rng.choice([1, 2, 3, 4, 5])
    prompt = f"What is the midline of $y = 3\\sin(x) + {k}$? Enter the y-value of the midline (an integer)."
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(k),
        answer_display=str(k),
        hint="The midline is y = k in y = A sin(bx) + k. It is the horizontal axis the wave oscillates around.",
        common_mistakes=["Reporting the amplitude 3 instead of the vertical shift, or adding 3 + k."],
        exam_tags=["ap_precalc_u3"],
        source="generated",
        cluster="trig",
        plot="sine",
        plot_data={"A": 3, "b": 1, "k": k, "kind": "sin", "title": rf"midline $y={k}$"},
        steps=_steps(
            ("Goal", "The midline is the horizontal line the sinusoid oscillates around — the vertical shift."),
            ("Form", f"y = 3 sin(x) + {k} has k = {k}, so the midline is y = {k}."),
            ("Peaks", f"The graph goes {k}+3 down to {k}-3. The center of that band is {k}."),
            ("Not amplitude", "3 is the amplitude (vertical stretch). The midline is the shift, not the stretch."),
        ),
    )


def sinusoid_model(rng: random.Random, skill_id: str) -> Problem:
    kind = rng.choice(["period", "freq", "amp"])
    if kind == "period":
        # y = A cos(b π t), period = 2π / |b π| = 2/|b|
        b = rng.choice([1, 2, 4])
        period = {1: "2", 2: "1", 4: "1/2"}[b]
        prompt = (
            f"A displacement is $y = 5\\cos({b}\\pi t)$ with t in seconds. "
            "What is the period in seconds? Enter a number or a fraction like 1/2."
        )
        steps = _steps(
            ("Goal", "Period is the time for one full cycle. For y = A cos(ω t), T = 2π / |ω|."),
            ("Read ω", f"Here ω = {b}π, so T = 2π / ({b}π) = {period}."),
            ("Meaning", f"Every {period} second(s) the motion repeats. That is simple harmonic motion."),
            ("Not frequency yet", "Frequency is 1/T. The question asked for the period T."),
        )
        hint = "Period of cos(ω t) is T = 2π/|ω|."
        miss = "Reporting 2π/b (forgetting ω already includes π) or reporting the frequency 1/T."
        ans = period
    elif kind == "freq":
        # y = 3 sin(4 π t) → ω = 4π, f = ω/(2π) = 2
        n = rng.choice([2, 4, 6, 8])
        f = n // 2
        prompt = (
            f"An AC voltage is $v = 3\\sin({n}\\pi t)$ with t in seconds. "
            "What is the frequency in cycles per second? Enter an integer."
        )
        steps = _steps(
            ("Goal", "Frequency f is cycles per second. If the inside is ω t, then f = ω / (2π)."),
            ("Read ω", f"ω = {n}π, so f = {n}π / (2π) = {f}."),
            ("Check via period", f"T = 2π/ω = 2/{n} = {1}/{f} if f={f}, and f = 1/T = {f}."),
            ("Units", "Cycles per second (hertz). Amplitude 3 is volts, not frequency."),
        )
        hint = "f = ω/(2π) when the function is sin(ω t)."
        miss = "Reporting ω itself, or 2π/ω (that's the period, not the frequency)."
        ans = str(f)
    else:
        a = rng.choice([2, 3, 4, 5, 6])
        prompt = (
            f"A mass on a spring has displacement $y = -{a}\\cos(2t)$ in centimeters. "
            "What is the amplitude in centimeters? Enter an integer."
        )
        steps = _steps(
            ("Goal", "Amplitude is |A| in y = A cos(ω t). It is the maximum distance from the midline."),
            ("Absolute value", f"A = -{a}, so amplitude = |A| = {a}."),
            ("Picture", f"The mass travels {a} cm above and {a} cm below equilibrium."),
            ("Sign", "The leading minus is a reflection (or a phase of π), not a negative amplitude."),
        )
        hint = "Amplitude is |A|. A leading minus does not make the amplitude negative."
        miss = "Reporting -A because of the minus sign."
        ans = str(a)
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=ans,
        answer_display=ans,
        hint=hint,
        common_mistakes=[miss],
        exam_tags=["ap_precalc_u3"],
        source="generated",
        cluster="trig",
        plot="sine",
        plot_data={"A": 5, "b": 1, "kind": "cos", "title": "Sinusoidal model"},
        steps=steps,
    )


def half_angle(rng: random.Random, skill_id: str) -> Problem:
    # cos²(θ/2) = (1 + cos θ)/2 with a 3-4-5 or 5-12-13 cosine
    trip = rng.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17)])
    adj, opp, hyp = trip[0], trip[1], trip[2]
    # cos θ = adj/hyp, cos²(θ/2) = (1 + adj/hyp)/2 = (hyp + adj)/(2 hyp)
    num = hyp + adj
    den = 2 * hyp
    g = gcd(num, den)
    num //= g
    den //= g
    ans = str(num) if den == 1 else f"{num}/{den}"
    prompt = (
        f"If $\\cos \\theta = {adj}/{hyp}$ and $\\theta$ is in quadrant I, "
        r"find $\cos^2(\theta/2)$ as a simplified fraction."
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=ans,
        answer_display=ans,
        hint="The half-angle identity is cos²(θ/2) = (1 + cos θ)/2. The question asks for the square, so skip the square root.",
        common_mistakes=["Using (1 − cos θ)/2 (that's sin² of the half-angle), or taking a square root the question did not ask for."],
        exam_tags=["ap_precalc_u3"],
        source="generated",
        cluster="trig",
        plot="right_triangle",
        plot_data={"opp": opp, "adj": adj, "hyp": hyp},
        steps=_steps(
            ("Goal", "Half-angle formulas come from rearranging the double-angle formula for cosine."),
            ("Identity", "cos²(θ/2) = (1 + cos θ)/2. Asking for the square avoids a ± square-root choice."),
            ("Plug in", f"(1 + {adj}/{hyp})/2 = (({hyp} + {adj})/{hyp})/2 = {hyp + adj}/{2 * hyp} = {ans}."),
            ("Quadrant", "θ in QI makes θ/2 acute, so cosine of the half-angle is positive — consistent with a positive square."),
        ),
    )


def triangle_area(rng: random.Random, skill_id: str) -> Problem:
    if rng.choice([True, False]):
        a = rng.choice([6, 8, 10, 12])
        b = rng.choice([5, 7, 9])
        prompt = (
            f"A triangle has sides a = {a} and b = {b} with included angle C = 90°. "
            "Find the area. Enter an integer."
        )
        area = (a * b) // 2
        ans = str(area)
        steps = _steps(
            ("Goal", "Area = (1/2) ab sin C, using the included angle between those two sides. (Law of Tangents and Mollweide live on the same triangle sheet but are not needed for area.)"),
            ("Right angle", f"sin 90° = 1, so area = (1/2)·{a}·{b} = {area}. That is the usual (1/2) base × height."),
            ("Why included", "C is the angle between a and b, so those sides can act as base and height after the sine."),
            ("Check", f"A right triangle with legs {a} and {b} has area {area}."),
        )
        hint = "Area = (1/2) ab sin C. For C = 90°, sin 90° = 1."
        miss = "Forgetting the 1/2, or using sin 90° = 0."
    else:
        a = rng.choice([4, 6, 8, 10])
        # 60°: area = (1/2) a a sin 60 = (√3/4) a²
        area_ans = f"{(a * a) // 4}*sqrt(3)" if (a * a) % 4 == 0 else f"{a * a}*sqrt(3)/4"
        prompt = (
            f"An equilateral triangle has side {a}. Using Area = (1/2)ab sin C with C = 60°, "
            "find the area. Enter an expression like 9*sqrt(3)."
        )
        steps = _steps(
            ("Goal", "Every angle of an equilateral triangle is 60°. Two sides and the included 60° give the area."),
            ("Formula", f"Area = (1/2)·{a}·{a}·sin 60° = ({a * a}/2)·(√3/2) = {area_ans}."),
            ("sin 60°", "sin 60° = √3/2. Keep the radical; do not replace it with a decimal."),
            ("Check", f"The standard equilateral-area formula (√3/4)s² with s = {a} is the same {area_ans}."),
        )
        hint = "Area = (1/2) a² sin 60°, and sin 60° = √3/2."
        miss = "Using sin 60° = 1/2, or dropping the √3."
        ans = area_ans
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=ans,
        answer_display=ans.replace("sqrt", "√").replace("*", ""),
        hint=hint,
        common_mistakes=[miss],
        exam_tags=["clep_precalc"],
        source="generated",
        cluster="trig",
        plot="oblique_triangle",
        plot_data={},
        steps=steps,
    )


def ssa_ambiguous(rng: random.Random, skill_id: str) -> Problem:
    # A = 30°, b = 10, h = b sin A = 5.
    # a < 5 → 0; a = 5 → 1; 5 < a < 10 → 2; a ≥ 10 → 1
    a, expected, why = rng.choice(
        [
            (4, "0", "height h = b sin A = 10 · (1/2) = 5. Side a = 4 is shorter than the height, so the side cannot reach the other ray."),
            (5, "1", "height h = 5 and a = 5, so the side just meets the other ray at 90°. One right triangle."),
            (6, "2", "height h = 5 and a = 6 sits strictly between h and b, with A acute, so two triangles (the ambiguous case)."),
            (12, "1", "a = 12 is longer than b = 10, so the side swings past and meets the ray once. One triangle."),
        ]
    )
    prompt = (
        f"In triangle ABC, angle A = 30°, side a = {a} (opposite A), and side b = 10. "
        "How many triangles are possible? Enter 0, 1, or 2."
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=expected,
        answer_display=expected,
        hint="SSA: compute h = b sin A and compare a to h and to b. Acute A with h < a < b gives two triangles.",
        common_mistakes=["Assuming SSA always makes one triangle, the way ASA or SAS does."],
        exam_tags=["clep_precalc"],
        source="generated",
        cluster="trig",
        plot="oblique_triangle",
        plot_data={},
        steps=_steps(
            ("Goal", "SSA is the ambiguous case: 0, 1, or 2 triangles are possible. Compare a with the height h = b sin A."),
            ("Height", why),
            ("Rule of thumb", "If a < h: none. If a = h: one right triangle. If h < a < b (A acute): two. If a ≥ b: one."),
            ("Answer", f"The number of possible triangles is {expected}."),
        ),
    )


def polar_coords(rng: random.Random, skill_id: str) -> Problem:
    r = rng.choice([2, 3, 4, 5])
    deg, rad, sinv, cosv = rng.choice([(0, "0", "0", "1"), (90, "pi/2", "1", "0"), (180, "pi", "0", "-1"), (270, "3*pi/2", "-1", "0")])
    which = rng.choice(["x", "y"])
    if which == "x":
        # x = r cos
        if rad == "0":
            ans = str(r)
        elif rad == "pi":
            ans = str(-r)
        else:
            ans = "0"
        prompt = f"Polar point $(r,\\theta) = ({r}, {rad.replace("pi", r"\pi").replace("*", "")})$. Find the Cartesian x-coordinate."
    else:
        if rad == "pi/2":
            ans = str(r)
        elif rad == "3*pi/2":
            ans = str(-r)
        else:
            ans = "0"
        prompt = f"Polar point $(r,\\theta) = ({r}, {rad.replace("pi", r"\pi").replace("*", "")})$. Find the Cartesian y-coordinate."
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=ans,
        answer_display=ans,
        hint="x = r cos θ and y = r sin θ.",
        common_mistakes=["Swapping sine and cosine, or dropping the sign when θ is π or 3π/2."],
        exam_tags=["ap_precalc_u3"],
        source="generated",
        cluster="precalc",
        plot="polar_point",
        plot_data={"r": r, "deg": deg},
        steps=_steps(
            ("Goal", "Polar (r, θ) is distance from the origin plus an angle from the positive x-axis."),
            ("Conversion", "The Cartesian coordinates are x = r cos θ and y = r sin θ."),
            ("This angle", f"At θ corresponding to {deg}°, cosine and sine are 0, ±1 as on the axes."),
            ("Value", f"The requested coordinate is {ans}."),
        ),
    )


def polar_graphs(rng: random.Random, skill_id: str) -> Problem:
    a = rng.choice([2, 3, 4, 5])
    prompt = f"The polar graph $r = {a}$ is a circle. What is its radius?"
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(a),
        answer_display=str(a),
        hint="r = a (a constant) means every point is a units from the origin, a circle centered at the pole.",
        common_mistakes=["Calling it a line, or thinking the radius is 2a (that is r = 2a cos θ, a different circle)."],
        exam_tags=["ap_precalc_u3"],
        source="generated",
        cluster="precalc",
        plot="polar_circle",
        plot_data={"a": a},
        steps=_steps(
            ("Goal", "Recognize a basic polar graph from its equation."),
            ("Constant r", f"r = {a} says the distance from the origin never changes."),
            ("Geometry", "The set of points at a fixed distance from a point is a circle. The center is the pole (origin)."),
            ("Radius", f"The radius is {a}. (By contrast, r = {a} cos θ is a circle of diameter {a} through the origin.)"),
        ),
    )


def polar_complex(rng: random.Random, skill_id: str) -> Problem:
    a, b = rng.choice([(3, 4), (5, 12), (8, 15), (7, 24)])
    mag = int((a * a + b * b) ** 0.5)
    prompt = f"Find the modulus (magnitude) of the complex number ${a} + {b}i$."
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(mag),
        answer_display=str(mag),
        hint="|a+bi| = √(a² + b²). This is also r in the polar form r(cos θ + i sin θ).",
        common_mistakes=["Adding a+b, or leaving the answer as √(a²+b²) when it is a perfect square."],
        exam_tags=["ap_precalc_u3", "ap_precalc_u4"],
        source="generated",
        cluster="precalc",
        plot="complex",
        plot_data={"a": a, "b": b},
        steps=_steps(
            ("Goal", "The modulus is the distance from 0 in the complex plane, the r of polar form."),
            ("Formula", f"|a+bi| = √(a² + b²) = √({a}² + {b}²) = √({a*a + b*b})."),
            ("Simplify", f"√{a*a + b*b} = {mag} because this is a Pythagorean triple."),
            ("Polar form", f"The number is {mag}(cos θ + i sin θ) for θ = arctan({b}/{a}) in quadrant I."),
        ),
    )


def parametric(rng: random.Random, skill_id: str) -> Problem:
    t = rng.randint(1, 5)
    a, b = rng.randint(2, 5), rng.randint(-3, 4)
    x = a * t
    y = b * t if b else t
    prompt = f"If $x = {a}t$ and $y = {b if b else 1}t$, find $x$ when $t = {t}$."
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(x),
        answer_display=str(x),
        hint="Parametric equations are evaluated one coordinate at a time. Plug t into the x-formula.",
        common_mistakes=["Plugging t into y instead, or eliminating t when the question only asked for x at one t."],
        exam_tags=["ap_precalc_u4"],
        source="generated",
        cluster="precalc",
        steps=_steps(
            ("Goal", "A parameter t labels time (or another input). Each t gives one point (x(t), y(t))."),
            ("Use the x-equation", f"x = {a}t, so at t = {t} we have x = {a}·{t} = {x}."),
            ("The matching y", f"y would be {(b if b else 1)*t} at the same t, but the question asked only for x."),
            ("Picture", "As t changes, the point traces a line (or curve). Here one snapshot is enough."),
        ),
    )


def parametric_graph(rng: random.Random, skill_id: str) -> Problem:
    prompt = (
        r"The parametric equations $x = \cos t$, $y = \sin t$ trace a circle. "
        "What is the radius?"
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer="1",
        answer_display="1",
        hint="Eliminate t: x² + y² = cos² t + sin² t = 1.",
        common_mistakes=["Saying the radius is t, or 2π (that is a period, not a radius)."],
        exam_tags=["ap_precalc_u4"],
        source="generated",
        cluster="precalc",
        plot="unit_param",
        plot_data={},
        steps=_steps(
            ("Goal", "To recognize a parametric path, eliminate t or use a known identity."),
            ("Square and add", "x² + y² = cos² t + sin² t = 1, the unit circle."),
            ("Radius", "x² + y² = r² with r² = 1, so the radius is 1."),
            ("Direction", "As t increases from 0, the point starts at (1,0) and moves counterclockwise."),
        ),
    )


def vectors(rng: random.Random, skill_id: str) -> Problem:
    a, b = rng.choice([(3, 4), (5, 12), (6, 8), (9, 12), (8, 15)])
    mag = int((a * a + b * b) ** 0.5)
    prompt = f"Find the magnitude of $\\langle {a}, {b} \\rangle$."
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(mag),
        answer_display=str(mag),
        hint="Magnitude is √(a² + b²), the length of the arrow.",
        common_mistakes=["Adding the components, or giving a negative magnitude."],
        exam_tags=["ap_precalc_u4"],
        source="generated",
        cluster="precalc",
        plot="vector",
        plot_data={"a": a, "b": b},
        steps=_steps(
            ("Goal", "A vector's magnitude is its length, always ≥ 0."),
            ("Formula", f"|⟨{a},{b}⟩| = √({a}² + {b}²) = √({a*a + b*b})."),
            ("Simplify", f"That square root is {mag}."),
            ("Picture", "This is the hypotenuse of a right triangle with legs {a} and {b}."),
        ),
    )


def matrix_ops(rng: random.Random, skill_id: str) -> Problem:
    a11, a12, a21, a22 = [rng.randint(1, 6) for _ in range(4)]
    b11, b12, b21, b22 = [rng.randint(1, 6) for _ in range(4)]
    prompt = (
        f"Add the matrices. What is the (1,1) entry of "
        f"$\\begin{{bmatrix}} {a11} & {a12} \\\\ {a21} & {a22} \\end{{bmatrix}}"
        f"+ \\begin{{bmatrix}} {b11} & {b12} \\\\ {b21} & {b22} \\end{{bmatrix}}$?"
    )
    ans = a11 + b11
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(ans),
        answer_display=str(ans),
        hint="Add matching positions. The (1,1) entry is top-left plus top-left.",
        common_mistakes=["Multiplying the entries, or adding a11 to b22 (the diagonal of the other matrix)."],
        exam_tags=["ap_precalc_u4", "clep_algebra"],
        source="generated",
        cluster="precalc",
        steps=_steps(
            ("Goal", "Matrix addition is entrywise: only same-size matrices can be added."),
            ("Locate (1,1)", f"The top-left of the first matrix is {a11}. The top-left of the second is {b11}."),
            ("Add those two", f"{a11} + {b11} = {ans}. That is the (1,1) entry of the sum."),
            ("The rest", f"You would similarly add {a12}+{b12} in position (1,2), and so on. Multiplication is a different rule."),
        ),
    )


def gaussian(rng: random.Random, skill_id: str) -> Problem:
    xsol, ysol = rng.randint(1, 5), rng.randint(1, 5)
    prompt = (
        f"After Gaussian elimination, a system reduced to $x = {xsol}$, $y = {ysol}$. "
        "What is x? (This is the unique solution's first coordinate.)"
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(xsol),
        answer_display=str(xsol),
        hint="Row echelon form is meant to be read by back-substitution. Here x is already isolated.",
        common_mistakes=["Reporting y, or adding x and y."],
        exam_tags=["ap_precalc_u4"],
        source="generated",
        cluster="precalc",
        steps=_steps(
            ("Goal", "Gaussian elimination turns a system into an equivalent triangular system that is easy to read."),
            ("Reduced system", f"The last rows have already isolated the variables: x = {xsol} and y = {ysol}."),
            ("Read x", f"The first coordinate of the solution is {xsol}."),
            ("Why elimination works", "Each row operation (swap, scale, add a multiple) does not change the solution set."),
        ),
    )


def inverse_matrix(rng: random.Random, skill_id: str) -> Problem:
    a, b, c, d = rng.randint(1, 4), rng.randint(0, 3), rng.randint(0, 3), rng.randint(1, 4)
    det = a * d - b * c
    if det == 0:
        d += 1
        det = a * d - b * c
    prompt = (
        f"Find the determinant of $\\begin{{bmatrix}} {a} & {b} \\\\ {c} & {d} \\end{{bmatrix}}$. "
        "(A 2×2 matrix is invertible exactly when this is not 0.)"
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(det),
        answer_display=str(det),
        hint="For [[a,b],[c,d]], det = ad - bc.",
        common_mistakes=["Adding ad + bc, or multiplying all four entries."],
        exam_tags=["ap_precalc_u4"],
        source="generated",
        cluster="precalc",
        steps=_steps(
            ("Goal", "The determinant of a 2×2 matrix decides invertibility and appears in the inverse formula."),
            ("Formula", f"det = ad - bc = ({a})({d}) - ({b})({c}) = {a*d} - {b*c} = {det}."),
            ("Invertible?", f"Because det ≠ 0, an inverse exists. The inverse is (1/det) times [[d, -b], [-c, a]]."),
            ("If det were 0", "The matrix would be singular: the two rows would be parallel and no inverse would exist."),
        ),
    )


def cramer(rng: random.Random, skill_id: str) -> Problem:
    xsol, ysol = 2, 3
    prompt = (
        "Solve by Cramer's rule (or any method) for x:\n\n"
        "$x + y = 5$\n\n$x - y = -1$"
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer="2",
        answer_display="2",
        hint="Add the two equations to eliminate y, or use x = det A_x / det A.",
        common_mistakes=["Reporting y = 3 as if it were x."],
        exam_tags=["ap_precalc_u4"],
        source="generated",
        cluster="precalc",
        steps=_steps(
            ("Goal", "Cramer's rule expresses each variable as a ratio of determinants. For 2×2 it matches elimination."),
            ("Add to eliminate y", "(x+y) + (x-y) = 5 + (-1) ⇒ 2x = 4 ⇒ x = 2."),
            ("Optional Cramer check", "A = [[1,1],[1,-1]], det A = -2. Replace the x-column by [5,-1]: det A_x = -4. Then x = (-4)/(-2) = 2."),
            ("The pair", "Then y = 5 - x = 3, but the question asked only for x."),
        ),
    )


def ellipse(rng: random.Random, skill_id: str) -> Problem:
    a = rng.choice([3, 4, 5, 6])
    prompt = (
        f"The ellipse $\\dfrac{{x^2}}{{{a*a}}} + \\dfrac{{y^2}}{{4}} = 1$ has a horizontal semi-axis of what length?"
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(a),
        answer_display=str(a),
        hint="Standard form x²/a² + y²/b² = 1. The number under x² is a², so a is the horizontal semi-axis.",
        common_mistakes=["Reporting a² (the denominator) instead of a, or using 2 as if both axes were the same."],
        exam_tags=["clep_precalc"],
        source="generated",
        cluster="precalc",
        plot="ellipse",
        plot_data={"a": a, "b": 2},
        steps=_steps(
            ("Goal", "An ellipse in standard position is x²/a² + y²/b² = 1. Vertices sit at (±a, 0) and (0, ±b)."),
            ("Read the denominators", f"Under x² we have {a*a} = {a}², so the horizontal semi-axis is a = {a}."),
            ("The other axis", "Under y² we have 4 = 2², so the vertical semi-axis is 2."),
            ("Not a circle", f"Because {a} and 2 differ, the graph is stretched, not a circle."),
        ),
    )


def hyperbola(rng: random.Random, skill_id: str) -> Problem:
    prompt = (
        r"Does $\dfrac{x^2}{9} - \dfrac{y^2}{4} = 1$ open left-right or up-down? "
        "Enter left-right or up-down."
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer="left-right",
        answer_display="left-right",
        hint="The positive squared term tells you the axis it opens along. x² positive first means left-right.",
        common_mistakes=["Saying up-down because 9 > 4, mixing this with ellipse major-axis rules."],
        exam_tags=["clep_precalc"],
        source="generated",
        cluster="precalc",
        plot="hyperbola",
        plot_data={},
        steps=_steps(
            ("Goal", "A hyperbola has a minus between the two squared terms. The plus side is the direction it opens."),
            ("Form", "x²/a² - y²/b² = 1 opens left-right (vertices on the x-axis). y²/a² - x²/b² = 1 opens up-down."),
            ("This equation", "x² is the positive term, so the branches open left-right."),
            ("Vertices", "Vertices at (±3, 0) because a² = 9. That confirms a horizontal transverse axis."),
        ),
    )


def parabola_conic(rng: random.Random, skill_id: str) -> Problem:
    p = rng.choice([1, 2, 3, 4])
    prompt = f"The parabola $y = \\dfrac{{1}}{{{4*p}}} x^2$ has focus (0, p) with p equal to what number?"
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(p),
        answer_display=str(p),
        hint="Vertex form y = x²/(4p) has focus (0, p) when the vertex is at the origin.",
        common_mistakes=["Using 4p as the focus y-coordinate, which is four times too far."],
        exam_tags=["clep_precalc"],
        source="generated",
        cluster="precalc",
        plot="conic_parabola",
        plot_data={"p": p},
        steps=_steps(
            ("Goal", "A parabola as a conic is defined by equal distance to focus and directrix. The number p is that distance from the vertex."),
            ("Standard form", f"y = x²/(4p) matches the given coefficient 1/{4*p}, so 4p = {4*p}."),
            ("Solve for p", f"p = {p}. The focus is (0, {p})."),
            ("Directrix", f"The directrix is the line y = -{p}, the same distance on the other side of the vertex."),
        ),
    )


def rotation_axes(rng: random.Random, skill_id: str) -> Problem:
    prompt = (
        r"Does the conic $x^2 + xy + y^2 = 3$ require a rotation of axes to eliminate an $xy$ term? "
        "Enter yes or no."
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer="yes",
        answer_display="yes",
        hint="If there is an xy term, the axes are tilted. Rotation removes that B xy term.",
        common_mistakes=["Saying no because the equation still looks 'almost' like an ellipse aligned with the axes."],
        exam_tags=["clep_precalc"],
        source="generated",
        cluster="precalc",
        steps=_steps(
            ("Goal", "The general conic is Ax² + Bxy + Cy² + Dx + Ey + F = 0. A nonzero B means the axes are rotated."),
            ("Look for xy", "This equation contains xy with coefficient 1, so B = 1 ≠ 0."),
            ("Conclusion", "Yes, a rotation is required if you want an equation with no xy term."),
            ("How much", "The angle satisfies cot(2θ) = (A-C)/B. You do not need that value to answer yes/no."),
        ),
    )


def polar_conic(rng: random.Random, skill_id: str) -> Problem:
    e, name = rng.choice([(0.5, "ellipse"), (1, "parabola"), (1.5, "hyperbola")])
    prompt = (
        f"A polar conic has eccentricity e = {e}. "
        "What type of conic is it? Enter ellipse, parabola, or hyperbola."
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=name,
        answer_display=name,
        hint="e < 1 ellipse, e = 1 parabola, e > 1 hyperbola.",
        common_mistakes=["Reversing ellipse and hyperbola, or thinking e = 1 is a circle (a circle is e = 0)."],
        exam_tags=["ap_precalc_u3", "clep_precalc"],
        source="generated",
        cluster="precalc",
        steps=_steps(
            ("Goal", "Eccentricity classifies conics in one sentence, including polar form r = ed / (1 - e cos θ)."),
            ("The rule", "0 ≤ e < 1: ellipse (e = 0 is a circle). e = 1: parabola. e > 1: hyperbola."),
            ("This value", f"e = {e} is therefore a {name}."),
            ("Why polar form", "The focus-directrix definition that produces e is the same definition that produces polar conic equations."),
        ),
    )


def limit_numeric(rng: random.Random, skill_id: str) -> Problem:
    a = rng.choice([2, 3, 4, 5])
    prompt = (
        f"The function $f(x) = \\dfrac{{x^2 - {a*a}}}{{x - {a}}}$ is undefined at x = {a}. "
        f"What value does f(x) approach as x approaches {a}? Enter an integer."
    )
    ans = 2 * a
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(ans),
        answer_display=str(ans),
        hint="A table of values near x = a, or factoring, both show the same height of the hole.",
        common_mistakes=["Saying the limit does not exist because f(a) is undefined, or answering 0 because you see 0/0."],
        exam_tags=["clep_precalc"],
        source="generated",
        cluster="limits",
        plot="limit_hole",
        plot_data={"a": a},
        steps=_steps(
            ("Goal", "A limit is the y-value the graph approaches, not whether the function is defined at the point."),
            ("0/0 is not the answer", f"Plugging x = {a} gives 0/0, which means 'simplify', not 'the limit is 0'."),
            ("Cancel", f"x² - {a*a} = (x-{a})(x+{a}). For x ≠ {a}, f(x) = x+{a}."),
            ("Approach", f"As x → {a}, x+{a} → {ans}. Nearby table values like f({a}+0.001) sit next to {ans}."),
        ),
    )


def limit_algebra(rng: random.Random, skill_id: str) -> Problem:
    a = rng.choice([2, 3, 4, 5, 6])
    prompt = f"Evaluate $\\lim_{{x \\to {a}}} \\dfrac{{x^2 - {a*a}}}{{x - {a}}}$."
    ans = 2 * a
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(ans),
        answer_display=str(ans),
        hint="Factor the numerator as a difference of squares, cancel, then substitute.",
        common_mistakes=["Stopping at 0/0, or canceling x² with x to get x - a²/x."],
        exam_tags=["clep_precalc"],
        source="generated",
        cluster="limits",
        plot="limit_hole",
        plot_data={"a": a},
        steps=_steps(
            ("Goal", "Algebraic limits of rational functions start with substitution. If you get 0/0, factor or conjugate."),
            ("Factor", f"x² - {a*a} = (x-{a})(x+{a}). Cancel x-{a} for x ≠ {a}."),
            ("Simplified function", f"The limit equals lim (x+{a}) as x → {a}."),
            ("Substitute now", f"{a} + {a} = {ans}. The original graph has a hole at x = {a} of height {ans}."),
        ),
    )


def continuity(rng: random.Random, skill_id: str) -> Problem:
    prompt = (
        r"Is $f(x) = \dfrac{x^2-1}{x-1}$ continuous at $x = 1$? Enter yes or no."
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer="no",
        answer_display="no",
        hint="Continuity at a requires f(a) to exist, the limit to exist, and the two to be equal. Here f(1) is undefined.",
        common_mistakes=["Saying yes because the limit exists (a hole is still a discontinuity)."],
        exam_tags=["clep_precalc"],
        source="generated",
        cluster="limits",
        plot="limit_hole",
        plot_data={"a": 1},
        steps=_steps(
            ("Goal", "Continuous at a point means the graph has no hole, jump, or vertical asymptote there."),
            ("Does f(1) exist?", "The denominator is 0 at x = 1, so f(1) is undefined."),
            ("The limit still exists", "After canceling, the limit is 2. A hole of height 2 is a removable discontinuity."),
            ("Verdict", "No: without a defined value at x = 1, f is not continuous there. (You could redefine f(1)=2 to repair it.)"),
        ),
    )


MORE_GENERATORS = {
    "deg_to_rad": deg_to_rad,
    "right_triangle": right_triangle,
    "unit_circle": unit_circle,
    "other_trig": other_trig,
    "period_amp": period_amp,
    "tan_period": tan_period,
    "inverse_trig": inverse_trig,
    "identity_simplify": identity_simplify,
    "sum_diff": sum_diff,
    "double_angle": double_angle,
    "product_sum": product_sum,
    "solve_trig": solve_trig,
    "law_sines": law_sines,
    "law_cosines": law_cosines,
    "arc_length": arc_length,
    "coterminal": coterminal,
    "angular_speed": angular_speed,
    "elevation": elevation,
    "cofunction": cofunction,
    "phase_shift": phase_shift,
    "sinusoid_model": sinusoid_model,
    "half_angle": half_angle,
    "triangle_area": triangle_area,
    "ssa_ambiguous": ssa_ambiguous,
    "polar_coords": polar_coords,
    "polar_graphs": polar_graphs,
    "polar_complex": polar_complex,
    "parametric": parametric,
    "parametric_graph": parametric_graph,
    "vectors": vectors,
    "matrix_ops": matrix_ops,
    "gaussian": gaussian,
    "inverse_matrix": inverse_matrix,
    "cramer": cramer,
    "ellipse": ellipse,
    "hyperbola": hyperbola,
    "parabola_conic": parabola_conic,
    "rotation_axes": rotation_axes,
    "polar_conic": polar_conic,
    "limit_numeric": limit_numeric,
    "limit_algebra": limit_algebra,
    "continuity": continuity,
}
