from __future__ import annotations

import random
from math import comb

from src.schema import Problem, Step, make_problem, steps


def _steps(*pairs: tuple[str, str]) -> list[Step]:
    return steps(*pairs)


def _prob(**kwargs) -> Problem:
    return make_problem(**kwargs)


def order_of_ops(rng: random.Random, skill_id: str) -> Problem:
    a, b, c, d = rng.randint(2, 6), rng.randint(2, 5), rng.randint(2, 8), rng.randint(2, 6)
    # a^2 * b - c * d   or with grouping
    value = a**2 * b - c * d
    prompt = f"Evaluate. Write the integer result.\n\n${a}^2 \\cdot {b} - {c} \\cdot {d}$"
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(value),
        answer_display=str(value),
        hint="Exponents before multiply, and multiply before subtract. The · is ordinary multiplication.",
        common_mistakes=[
            "Doing subtraction before multiplication, or computing (a^2 · b - c) · d.",
        ],
        exam_tags=["clep_algebra"],
        source="generated",
        cluster="foundations",
        steps=_steps(
            (
                "Goal",
                "Evaluate a numeric expression using the order of operations. We are not solving for a variable — there is a single number at the end.",
            ),
            (
                "Why this order",
                "If everyone picked a different order, 2 + 3 · 4 would be both 20 and 14. The agreed order is: grouping, exponents, multiply/divide left to right, add/subtract left to right.",
            ),
            (
                "Exponents first",
                f"${a}^2 = {a*a}$. Replace that power: ${a*a} \\cdot {b} - {c} \\cdot {d}$.",
            ),
            (
                "Multiplication next",
                f"${a*a} \\cdot {b} = {a*a*b}$ and ${c} \\cdot {d} = {c*d}$. Now the expression is ${a*a*b} - {c*d}$.",
            ),
            (
                "Subtract and check",
                f"${a*a*b} - {c*d} = {value}$. A quick check: the first product should be larger than the second here, so the result {value} being positive matches.",
            ),
        ),
    )


def exponents(rng: random.Random, skill_id: str) -> Problem:
    a = rng.randint(2, 5)
    m, n = rng.randint(2, 4), rng.randint(2, 4)
    kind = rng.choice(["product", "power", "neg"])
    if kind == "product":
        ans = a ** (m + n)
        prompt = f"Simplify to an integer.\n\n${a}^{{{m}}} \\cdot {a}^{{{n}}}$"
        steps = _steps(
            ("Goal", "Rewrite a product of powers that share a base as a single power, then evaluate."),
            (
                "Why the product rule",
                f"${a}^{{{m}}}$ is {m} factors of {a}, and ${a}^{{{n}}}$ is {n} more. Altogether that is {m+n} factors of {a}, which is ${a}^{{{m+n}}}$.",
            ),
            ("Add the exponents", f"${a}^{{{m}}} \\cdot {a}^{{{n}}} = {a}^{{{m}+{n}}} = {a}^{{{m+n}}}$."),
            ("Evaluate", f"${a}^{{{m+n}}} = {ans}$. That integer is the fully simplified form."),
        )
    elif kind == "power":
        ans = a ** (m * n)
        prompt = f"Simplify to an integer.\n\n$({a}^{{{m}}})^{{{n}}}$"
        steps = _steps(
            ("Goal", "A power of a power means 'raise that whole power to n'. Collapse to one exponent, then evaluate."),
            (
                "Why the power rule",
                f"$({a}^{{{m}}})^{{{n}}}$ means {n} copies of ${a}^{{{m}}}$ multiplied. That is {m*n} factors of {a}.",
            ),
            ("Multiply exponents", f"$({a}^{{{m}}})^{{{n}}} = {a}^{{{m}\\cdot{n}}} = {a}^{{{m*n}}}$."),
            ("Evaluate", f"${a}^{{{m*n}}} = {ans}$. That integer is the fully simplified form."),
        )
    else:
        ans = a ** (-n)
        prompt = f"Rewrite with a positive exponent and evaluate as a fraction.\n\n${a}^{{{-n}}}$"
        steps = _steps(
            ("Goal", "Negative exponents mean reciprocal, not 'the answer is negative'."),
            (
                "Definition",
                f"$a^{{-k}} = 1/a^{{k}}$ as long as $a \\neq 0$. So ${a}^{{{-n}}} = 1/{a}^{{{n}}}$.",
            ),
            ("Evaluate the positive power", f"${a}^{{{n}}} = {a**n}$. We still have to take the reciprocal next."),
            ("Write the reciprocal", f"The value is $1/{a**n}$."),
        )
        return _prob(
            id=f"{skill_id}-{rng.randrange(10**9)}",
            skill_id=skill_id,
            prompt=prompt,
            answer=f"1/{a**n}",
            answer_display=f"1/{a**n}",
            hint="a^{-n} = 1/a^n. The minus does not make the whole number negative.",
            common_mistakes=["Writing -1/a^n or -a^n instead of the reciprocal."],
            exam_tags=["clep_algebra"],
            source="generated",
            cluster="foundations",
            steps=steps,
        )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(ans),
        answer_display=str(ans),
        hint="Same base: add exponents for a product, multiply exponents for a power of a power.",
        common_mistakes=["Multiplying the bases, or adding exponents on a power of a power."],
        exam_tags=["clep_algebra"],
        source="generated",
        cluster="foundations",
        steps=steps,
    )


def radicals(rng: random.Random, skill_id: str) -> Problem:
    k = rng.choice([2, 3, 4, 5])
    m = rng.choice([2, 3, 5, 6, 7])
    inside = (k**2) * m
    prompt = f"Simplify the radical (pull out perfect squares).\n\n$\\sqrt{{{inside}}}$"
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=f"{k}*sqrt({m})",
        answer_display=f"{k}√{m}",
        hint="Factor the largest perfect square out of the radicand, then use √(ab) = √a · √b.",
        common_mistakes=["Taking √ of each addend if you rewrite, or reducing  √(k^2 m) to k m."],
        exam_tags=["clep_algebra"],
        source="generated",
        cluster="foundations",
        steps=_steps(
            ("Goal", "Rewrite the square root so the number inside has no perfect-square factor bigger than 1."),
            (
                "Why factor",
                f"√(a·b) = √a · √b when a, b ≥ 0. If a is a perfect square, √a becomes an integer sitting outside.",
            ),
            ("Factor the radicand", f"{inside} = {k**2} · {m}, and {k**2} = {k}^2 is a perfect square."),
            (
                "Split the radical",
                f"$\\sqrt{{{inside}}} = \\sqrt{{{k**2} \\cdot {m}}} = \\sqrt{{{k**2}}} \\cdot \\sqrt{{{m}}} = {k}\\sqrt{{{m}}}$.",
            ),
        ),
    )


def polynomials(rng: random.Random, skill_id: str) -> Problem:
    a, b, c, d = rng.randint(2, 5), rng.randint(1, 6), rng.randint(2, 5), rng.randint(1, 6)
    prompt = (
        f"Expand and simplify.\n\n$({a}x + {b})({c}x + {d})$"
    )
    A, B, C = a * c, a * d + b * c, b * d
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=f"{A}*x**2 + {B}*x + {C}",
        answer_display=f"{A}x^2 + {B}x + {C}",
        hint="Distribute every term in the first binomial through the second (FOIL), then combine like terms.",
        common_mistakes=["Forgetting the two middle products, so the x term is missing."],
        exam_tags=["clep_algebra"],
        source="generated",
        cluster="foundations",
        steps=_steps(
            ("Goal", "Turn a product of binomials into a single polynomial in standard form."),
            (
                "Why distribute",
                "Multiplication distributes over addition: (p+q)(r+s) = pr + ps + qr + qs. Nothing is 'optional'.",
            ),
            (
                "Four products",
                f"First: ${a}x \\cdot {c}x = {A}x^2$. Outer: ${a}x \\cdot {d} = {a*d}x$. "
                f"Inner: ${b} \\cdot {c}x = {b*c}x$. Last: ${b}\\cdot{d} = {C}$.",
            ),
            (
                "Combine the x terms",
                f"${a*d}x + {b*c}x = {B}x$. The simplified polynomial is ${A}x^2 + {B}x + {C}$.",
            ),
        ),
    )


def factoring(rng: random.Random, skill_id: str) -> Problem:
    r, s = rng.randint(2, 6), rng.randint(2, 6)
    if rng.random() < 0.5:
        s = -s
    b = r + s
    c = r * s
    b_disp = f"+ {b}" if b > 0 else f"- {abs(b)}"
    c_disp = f"+ {c}" if c > 0 else f"- {abs(c)}"
    r_disp = f"+ {r}" if r > 0 else f"- {abs(r)}"
    s_disp = f"+ {s}" if s > 0 else f"- {abs(s)}"
    prompt = f"Factor completely over the integers.\n\n$x^2 {b_disp}x {c_disp}$"
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=f"(x+{r})*(x+{s})",
        answer_display=f"(x {r_disp})(x {s_disp})",
        hint="Find two integers that multiply to the constant term and add to the middle coefficient.",
        common_mistakes=["Picking two numbers that multiply correctly but add with the wrong signs."],
        exam_tags=["clep_algebra"],
        source="generated",
        cluster="foundations",
        steps=_steps(
            ("Goal", "Rewrite the trinomial as a product of two binomials. Factoring undoes FOIL."),
            (
                "What to look for",
                f"We need integers m, n with m·n = {c} (the constant) and m+n = {b} (the x-coefficient).",
            ),
            (
                "Find the pair",
                f"{r} and {s} work: {r}·{s} = {c} and {r}+{s} = {b}.",
            ),
            (
                "Write the factors and check",
                f"$x^2 {b_disp}x {c_disp} = (x {r_disp})(x {s_disp})$. FOIL to confirm you get the original trinomial.",
            ),
        ),
    )


def rationals(rng: random.Random, skill_id: str) -> Problem:
    a, b = rng.randint(2, 5), rng.randint(2, 5)
    if a == b:
        b += 1
    prompt = f"Simplify the rational expression (cancel common factors).\n\n$\\dfrac{{{a}x}}{{{a}x^2 + {a*b}x}}$"
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=f"1/(x+{b})",
        answer_display=f"1/(x+{b})",
        hint="Factor the denominator completely, then cancel a common factor. State that x ≠ 0 and x ≠ -b.",
        common_mistakes=["Canceling the a x terms as if they were not part of a sum in the denominator."],
        exam_tags=["clep_algebra"],
        source="generated",
        cluster="foundations",
        steps=_steps(
            (
                "Goal",
                "Simplify a fraction of polynomials by canceling shared factors, not shared terms.",
            ),
            (
                "Factor first",
                f"Denominator: ${a}x^2 + {a*b}x = {a}x(x + {b})$. Numerator is already ${a}x$.",
            ),
            (
                "Cancel the common factor",
                f"$\\dfrac{{{a}x}}{{{a}x(x+{b})}} = \\dfrac{{1}}{{x+{b}}}$, provided ${a}x \\neq 0$.",
            ),
            (
                "Excluded values",
                f"Original denominator 0 when x = 0 or x = -{b}. The simplified form is $1/(x+{b})$ with those x-values still forbidden.",
            ),
        ),
    )


def distance_midpoint(rng: random.Random, skill_id: str) -> Problem:
    x1, y1 = rng.randint(-4, 4), rng.randint(-4, 4)
    x2, y2 = x1 + rng.choice([-6, -4, -3, 3, 4, 6]), y1 + rng.choice([-6, -4, 0, 4, 6])
    dx, dy = x2 - x1, y2 - y1
    dist2 = dx * dx + dy * dy
    prompt = (
        f"Find the distance between $({x1}, {y1})$ and $({x2}, {y2})$. "
        "Give an exact simplified radical (or integer)."
    )
    # simplify radical
    k, m = 1, dist2
    for p in range(int(dist2**0.5), 1, -1):
        if dist2 % (p * p) == 0:
            k, m = p, dist2 // (p * p)
            break
    if m == 1:
        ans, disp = str(k), str(k)
    else:
        ans, disp = f"{k}*sqrt({m})" if k != 1 else f"sqrt({m})", f"{k}√{m}" if k != 1 else f"√{m}"
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=ans,
        answer_display=disp,
        hint="Distance = √[(x2-x1)^2 + (y2-y1)^2]. Square both differences before adding.",
        common_mistakes=["Forgetting to square, or taking √ of each difference separately and adding."],
        exam_tags=["clep_algebra", "clep_precalc"],
        source="generated",
        cluster="equations",
        plot="two_points",
        plot_data={"x1": x1, "y1": y1, "x2": x2, "y2": y2},
        steps=_steps(
            ("Goal", "The distance between two points is the length of the hypotenuse of the right triangle they determine."),
            ("Horizontal and vertical change", f"Δx = {x2}-({x1}) = {dx},  Δy = {y2}-({y1}) = {dy}."),
            ("Pythagoras", f"Distance = $\\sqrt{{({dx})^2 + ({dy})^2}} = \\sqrt{{{dx*dx} + {dy*dy}}} = \\sqrt{{{dist2}}}$."),
            ("Simplify the radical", f"$\\sqrt{{{dist2}}}$ simplifies to {disp}."),
        ),
    )


def linear_eq(rng: random.Random, skill_id: str) -> Problem:
    a = rng.randint(2, 7)
    x_sol = rng.randint(-6, 8)
    b = rng.randint(-9, 9)
    c = a * x_sol + b
    b_disp = f"+ {b}" if b >= 0 else f"- {abs(b)}"
    prompt = f"Solve for $x$.\n\n${a}x {b_disp} = {c}$"
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(x_sol),
        answer_display=str(x_sol),
        hint="Undo addition/subtraction first so the x-term is alone, then divide by the coefficient of x.",
        common_mistakes=["Dividing only one term by a, or subtracting from only one side."],
        exam_tags=["clep_algebra"],
        source="generated",
        cluster="equations",
        steps=_steps(
            ("Goal", "Find the unique number x that makes both sides equal. A linear equation is a balanced scale."),
            (
                "Undo the constant",
                f"Subtract {b} from both sides (or add {abs(b)} if that constant was negative): "
                f"${a}x {b_disp} - ({b}) = {c} - ({b})$, so ${a}x = {c-b}$.",
            ),
            ("Undo the coefficient", f"Divide both sides by {a}: $x = {c-b}/{a} = {x_sol}$."),
            (
                "Check",
                f"Plug x = {x_sol} into the original: {a}({x_sol}) + ({b}) = {a*x_sol + b}, which equals {c}.",
            ),
        ),
    )


def linear_model(rng: random.Random, skill_id: str) -> Problem:
    start = rng.choice([20, 30, 40, 50, 80])
    rate = rng.choice([2, 3, 4, 5, 6])
    hours = rng.randint(3, 9)
    total = start + rate * hours
    prompt = (
        f"A tank starts with {start} liters and is filled at {rate} liters per hour. "
        f"How many liters are in the tank after {hours} hours?"
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(total),
        answer_display=str(total),
        hint="This is a linear model: amount = start + (rate)(time).",
        common_mistakes=["Multiplying start by hours, or forgetting to add the starting amount."],
        exam_tags=["clep_algebra"],
        source="generated",
        cluster="equations",
        plot="variation",
        plot_data={"k": rate, "x1": 0, "y1": start, "x2": hours, "y2": total},
        steps=_steps(
            ("Goal", "Translate the story into a linear formula, then evaluate at the given time."),
            ("Define the pieces", f"Starting amount {start} L. Constant rate {rate} L/h. Time t = {hours} h."),
            ("Write the model", f"$A = {start} + {rate}t$. After {hours} hours, $A = {start} + {rate}({hours})$."),
            ("Compute", f"{start} + {rate*hours} = {total} liters. Units stay liters because (L/h)·h = L."),
        ),
    )


def complex_num(rng: random.Random, skill_id: str) -> Problem:
    a, b, c, d = rng.randint(1, 6), rng.randint(1, 6), rng.randint(1, 6), rng.randint(1, 6)
    real = a * c - b * d
    imag = a * d + b * c
    prompt = f"Multiply and write in $a+bi$ form.\n\n$({a}+{b}i)({c}+{d}i)$"
    disp = f"{real}+{imag}i" if imag >= 0 else f"{real}{imag}i"
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=f"{real}+{imag}*I",
        answer_display=disp,
        hint="FOIL, then replace i^2 with -1 and combine real and imaginary parts.",
        common_mistakes=["Leaving i^2 in the answer, or adding the i^2 term instead of subtracting because i^2 = -1."],
        exam_tags=["clep_algebra", "ap_precalc_u1"],
        source="generated",
        cluster="equations",
        steps=_steps(
            ("Goal", "The set of complex numbers is closed under multiplication. The answer should look like a + bi."),
            ("Definition of i", "i^2 = -1 by definition. Treat i like a variable until that replacement."),
            (
                "FOIL",
                f"({a})({c}) = {a*c}, ({a})({d}i) = {a*d}i, ({b}i)({c}) = {b*c}i, ({b}i)({d}i) = {b*d} i^2 = {b*d}(-1) = {-b*d}.",
            ),
            (
                "Combine",
                f"Real parts: {a*c} + ({-b*d}) = {real}. Imaginary parts: {a*d} + {b*c} = {imag}. Result: {disp}.",
            ),
        ),
    )


def quadratic(rng: random.Random, skill_id: str) -> Problem:
    r, s = rng.randint(-6, -1), rng.randint(1, 6)
    b = -(r + s)
    c = r * s
    b_disp = f"+ {b}" if b >= 0 else f"- {abs(b)}"
    c_disp = f"+ {c}" if c >= 0 else f"- {abs(c)}"
    prompt = f"Solve by factoring. List both solutions.\n\n$x^2 {b_disp}x {c_disp} = 0$"
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=f"{r}, {s}",
        answer_display=f"{r}, {s}",
        hint="Factor, then use the zero product property: a product is 0 only if a factor is 0.",
        common_mistakes=["Reporting the factors as the answers (x+3 instead of x=-3)."],
        exam_tags=["clep_algebra", "ap_precalc_u1"],
        source="generated",
        cluster="equations",
        plot="quadratic_abc",
        plot_data={"a": 1, "b": b, "c": c, "roots": [r, s]},
        steps=_steps(
            ("Goal", "A quadratic equation can have two real solutions. We want both x-values that make the polynomial 0."),
            (
                "Factor",
                f"Find numbers that multiply to {c} and add to {b}. The roots are {r} and {s}, so the factored form is (x - ({r}))(x - ({s})).",
            ),
            (
                "Zero product property",
                f"If A·B = 0, then A = 0 or B = 0. So x = {r} or x = {s}.",
            ),
            (
                "Check one root",
                f"For x = {r}: ({r})^2 + ({b})({r}) + ({c}) = {r*r + b*r + c}, which is 0. The other root checks the same way.",
            ),
        ),
    )


def other_eq(rng: random.Random, skill_id: str) -> Problem:
    k = rng.randint(3, 9)
    prompt = f"Solve.\n\n$|x| = {k}$"
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=f"{k}, {-k}",
        answer_display=f"{k}, {-k}",
        hint="|x| = k means x is k units from 0, so x = k or x = -k (when k ≥ 0).",
        common_mistakes=["Giving only the positive solution, or treating |x| = k like x = k only."],
        exam_tags=["clep_algebra", "clep_precalc"],
        source="generated",
        cluster="equations",
        steps=_steps(
            ("Goal", "Absolute value measures distance on the number line. Solve for every x at that distance from 0."),
            ("Translate", f"|x| = {k} means the distance from x to 0 is {k}."),
            ("Two points", f"The points {k} units from 0 are {k} and -{k}."),
            ("Check", f"|{k}| = {k} and |{-k}| = {k}. If the right-hand side were negative, there would be no solution."),
        ),
    )


def inequality(rng: random.Random, skill_id: str) -> Problem:
    a = -rng.randint(2, 5)
    x_edge = rng.randint(-4, 6)
    b = rng.randint(-6, 6)
    # a x + b < a*x_edge + b  with a negative, inequality flips when dividing
    rhs = a * x_edge + b
    b_disp = f"+ {b}" if b >= 0 else f"- {abs(b)}"
    prompt = (
        f"Solve the inequality. Give the edge value and the correct inequality direction "
        f"(write like x>3 or x<=-2).\n\n${a}x {b_disp} < {rhs}$"
    )
    # a is negative: dividing flips: x > x_edge
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=f"x>{x_edge}",
        answer_display=f"x > {x_edge}",
        hint="Isolate x like an equation, but reverse the inequality when you multiply or divide by a negative number.",
        common_mistakes=["Forgetting to flip the inequality when dividing by a negative coefficient."],
        exam_tags=["clep_algebra"],
        source="generated",
        cluster="equations",
        plot="number_line",
        plot_data={"edge": x_edge, "greater": True, "title": r"$x >$ the edge value"},
        steps=_steps(
            ("Goal", "Describe every x that makes the inequality true — usually an infinite interval, not one number."),
            ("Undo the constant", f"Subtract {b} from both sides: ${a}x < {rhs-b}$."),
            (
                "Divide by a negative",
                f"Divide by {a}. Because {a} is negative, reverse < to >: $x > {x_edge}$.",
            ),
            (
                "Sanity check",
                f"Pick a number larger than {x_edge}, plug in, and confirm the original inequality holds. A number smaller should fail.",
            ),
        ),
    )


def function_eval(rng: random.Random, skill_id: str) -> Problem:
    a, b, c = rng.randint(1, 4), rng.randint(-5, 5), rng.randint(-4, 6)
    x0 = rng.randint(-3, 4)
    val = a * x0 * x0 + b * x0 + c
    b_disp = f"+ {b}x" if b >= 0 else f"- {abs(b)}x"
    c_disp = f"+ {c}" if c >= 0 else f"- {abs(c)}"
    prompt = f"If $f(x) = {a}x^2 {b_disp} {c_disp}$, find $f({x0})$."
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(val),
        answer_display=str(val),
        hint="Replace every x with the given input, using parentheses, then simplify.",
        common_mistakes=["Computing f(x) + x0, or forgetting to square the input."],
        exam_tags=["clep_algebra", "ap_precalc_u1"],
        source="generated",
        cluster="functions",
        plot="quadratic_abc",
        plot_data={"a": a, "b": b, "c": c, "x0": x0},
        steps=_steps(
            ("Goal", "f(x) is the output of the function f at input x. Evaluating is substitution, not multiplication by f."),
            ("Substitute with parentheses", f"$f({x0}) = {a}({x0})^2 + ({b})({x0}) + ({c})$."),
            ("Square first", f"({x0})^2 = {x0*x0}, so {a}({x0*x0}) = {a*x0*x0}."),
            ("Finish", f"{a*x0*x0} + ({b*x0}) + ({c}) = {val}. That number is f({x0})."),
        ),
    )


def domain(rng: random.Random, skill_id: str) -> Problem:
    h = rng.randint(2, 9)
    prompt = (
        f"Find the domain of $f(x) = \\sqrt{{x - {h}}}$. "
        f"Write the left endpoint of the domain (the smallest allowed x)."
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(h),
        answer_display=str(h),
        hint="For a square root of a real-valued function, the inside must be ≥ 0.",
        common_mistakes=["Using x > h and excluding the endpoint, where the square root is 0 and is allowed."],
        exam_tags=["clep_algebra", "ap_precalc_u1"],
        source="generated",
        cluster="functions",
        plot="sqrt_shift",
        plot_data={"h": h},
        steps=_steps(
            ("Goal", "Domain means 'which real inputs are allowed'. Square roots of negatives are not real."),
            ("Set up the inequality", f"We need $x - {h} \\ge 0$."),
            ("Solve", f"$x \\ge {h}$. In interval notation that is $[{h}, \\infty)$."),
            ("What to enter here", f"The left endpoint — the smallest allowed x — is {h}, and it is included."),
        ),
    )


def rate_of_change(rng: random.Random, skill_id: str) -> Problem:
    a, b = rng.randint(1, 4), rng.randint(-3, 5)
    x1, x2 = rng.randint(-2, 2), rng.randint(3, 6)
    f1 = a * x1 * x1 + b
    f2 = a * x2 * x2 + b
    roc = (f2 - f1) / (x2 - x1)
    prompt = (
        f"If $f(x) = {a}x^2 + {b}$, find the average rate of change from $x={x1}$ to $x={x2}$. "
        "A simplified fraction or integer is fine."
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(roc if roc != int(roc) else int(roc)),
        answer_display=str(roc if roc != int(roc) else int(roc)),
        hint="Average rate of change is [f(b)-f(a)] / (b-a), the slope of the secant.",
        common_mistakes=["Dividing in the wrong order, or using f(b-a)."],
        exam_tags=["ap_precalc_u1"],
        source="generated",
        cluster="functions",
        plot="secant",
        plot_data={"a": a, "b": b, "x1": x1, "x2": x2},
        steps=_steps(
            ("Goal", "Average rate of change is how much output changes per unit of input over an interval."),
            ("Evaluate the endpoints", f"f({x1}) = {a}({x1})^2 + {b} = {f1}. f({x2}) = {a}({x2})^2 + {b} = {f2}."),
            ("Form the slope", f"$\\dfrac{{f({x2})-f({x1})}}{{{x2}-{x1}}} = \\dfrac{{{f2}-{f1}}}{{{x2-x1}}} = \\dfrac{{{f2-f1}}}{{{x2-x1}}}$."),
            ("Simplify", f"The average rate of change is {roc if roc != int(roc) else int(roc)}."),
        ),
    )


def composition(rng: random.Random, skill_id: str) -> Problem:
    a, b, c, d = rng.randint(2, 5), rng.randint(-4, 4), rng.randint(2, 5), rng.randint(-3, 5)
    x0 = rng.randint(-3, 3)
    inner = c * x0 + d
    val = a * inner + b
    prompt = (
        f"If $f(x) = {a}x + {b}$ and $g(x) = {c}x + {d}$, find $(f \\circ g)({x0})$."
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(val),
        answer_display=str(val),
        hint="(f ∘ g)(x) = f(g(x)): evaluate g first, then plug that output into f.",
        common_mistakes=["Doing f first, or multiplying f(x) by g(x)."],
        exam_tags=["clep_algebra", "ap_precalc_u2"],
        source="generated",
        cluster="functions",
        steps=_steps(
            ("Goal", "Composition means 'function of a function'. The circle is not multiplication."),
            ("Inner function first", f"g({x0}) = {c}({x0}) + {d} = {inner}."),
            ("Outer function", f"f(g({x0})) = f({inner}) = {a}({inner}) + {b} = {val}."),
            ("Order check", "If you accidentally computed (g ∘ f), you would generally get a different number. Keep the right-to-left reading of ∘."),
        ),
    )


def transformations(rng: random.Random, skill_id: str) -> Problem:
    h = rng.randint(1, 5)
    prompt = (
        f"The graph of $y = \\sqrt{{x}}$ is shifted right {h} units. "
        f"What x-value is the new starting point of the graph (the left endpoint of the domain)?"
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(h),
        answer_display=str(h),
        hint="Replacing x by (x-h) moves the graph right h units. √x starts at 0, so √(x-h) starts at x = h.",
        common_mistakes=["Moving left because of the minus sign inside, or shifting vertically."],
        exam_tags=["ap_precalc_u1"],
        source="generated",
        cluster="functions",
        plot="sqrt_shift",
        plot_data={"h": h},
        steps=_steps(
            ("Goal", "Identify how a formula change moves a known graph."),
            ("Parent graph", "y = √x starts at (0, 0) and exists only for x ≥ 0."),
            (
                "Inside change",
                f"y = √(x-{h}) is the parent with x replaced by x-{h}. Horizontal replacements move the graph in the opposite direction of the sign: minus means right.",
            ),
            ("New start", f"The graph now starts when x-{h} = 0, i.e. x = {h}. That point is ({h}, 0)."),
        ),
    )


def abs_function(rng: random.Random, skill_id: str) -> Problem:
    h, k = rng.randint(1, 6), rng.randint(1, 6)
    prompt = f"What is the vertex of $y = |x - {h}| + {k}$? Enter as x,y with no parentheses (example: 2,3)."
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=f"{h},{k}",
        answer_display=f"({h}, {k})",
        hint="y = |x-h| + k has vertex (h, k). The V sits at that point.",
        common_mistakes=["Using (-h, k) because of the minus sign inside the absolute value."],
        exam_tags=["clep_algebra", "clep_precalc"],
        source="generated",
        cluster="functions",
        plot="abs_v",
        plot_data={"h": h, "k": k},
        steps=_steps(
            ("Goal", "The vertex is the corner of the V — the point where the expression inside the absolute value is 0."),
            ("Inside zero", f"|x-{h}| is 0 when x = {h}. That is the x-coordinate of the vertex."),
            ("Vertical shift", f"Adding {k} lifts the whole graph by {k}, so the y-coordinate of the vertex is {k}."),
            ("Vertex", f"({h}, {k}). Check: at x = {h}, y = |0| + {k} = {k}."),
        ),
    )


def inverse(rng: random.Random, skill_id: str) -> Problem:
    a = rng.randint(2, 6)
    b = rng.randint(-8, 8)
    prompt = (
        f"Find $f^{{-1}}(x)$ for $f(x) = {a}x + {b}$. "
        f"Enter the inverse as (x-({b}))/{a} or an equivalent simplified expression."
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=f"(x-({b}))/{a}",
        answer_display=f"(x - {b})/{a}",
        hint="Replace f(x) with y, swap x and y, solve for y. That y is the inverse function.",
        common_mistakes=["Writing 1/f(x), or swapping but forgetting to solve for y."],
        exam_tags=["clep_algebra", "ap_precalc_u2"],
        source="generated",
        cluster="functions",
        plot="inverse_line",
        plot_data={"a": a, "b": b},
        steps=_steps(
            ("Goal", "The inverse undoes f. f^{-1} is not an exponent of -1."),
            ("Set y = f(x)", f"Write $y = {a}x + {b}$. This y is just a name for the output so we can swap variables."),
            ("Swap x and y", f"$x = {a}y + {b}$. Solve: x - {b} = {a}y, so y = (x - {b})/{a}."),
            ("Name it", f"$f^{{-1}}(x) = (x - {b})/{a}$. Composition either way should return x."),
        ),
    )


def line(rng: random.Random, skill_id: str) -> Problem:
    x1, y1 = rng.randint(-4, 4), rng.randint(-4, 4)
    m = rng.choice([-3, -2, -1, 1, 2, 3, 4])
    x2 = x1 + rng.choice([1, 2, 3])
    y2 = y1 + m * (x2 - x1)
    prompt = f"Find the slope of the line through $({x1}, {y1})$ and $({x2}, {y2})$."
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(m),
        answer_display=str(m),
        hint="Slope m = (y2 - y1) / (x2 - x1).",
        common_mistakes=["Putting x's in the numerator, or reversing only one of the two differences."],
        exam_tags=["clep_algebra", "ap_precalc_u1"],
        source="generated",
        cluster="functions",
        plot="slope_line",
        plot_data={"x1": x1, "y1": y1, "x2": x2, "y2": y2},
        steps=_steps(
            ("Goal", "Slope is rise over run: how much y changes per 1 unit of x."),
            ("Write the formula", f"$m = \\dfrac{{{y2}-({y1})}}{{{x2}-({x1})}} = \\dfrac{{{y2-y1}}}{{{x2-x1}}}$."),
            ("Compute", f"m = {y2-y1}/{x2-x1} = {m}. Slope is a single number for the whole line."),
            ("Meaning", f"For every 1 unit you move right, y changes by {m}."),
        ),
    )


def parabola(rng: random.Random, skill_id: str) -> Problem:
    a = rng.choice([1, 2, -1, -2])
    h, k = rng.randint(-4, 4), rng.randint(-5, 5)
    # y = a(x-h)^2 + k  -> standard ax^2 + bx + c with vertex (h,k)
    b = -2 * a * h
    c = a * h * h + k
    prompt = (
        f"Find the x-coordinate of the vertex of $y = {a}x^2 + ({b})x + ({c})$."
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(h),
        answer_display=str(h),
        hint="For y = ax^2 + bx + c, the vertex x-coordinate is x = -b/(2a).",
        common_mistakes=["Using +b/(2a), or using -b/a."],
        exam_tags=["ap_precalc_u1"],
        source="generated",
        cluster="poly",
        plot="parabola",
        plot_data={"a": a, "h": h, "k": k},
        steps=_steps(
            ("Goal", "The vertex is the highest or lowest point of the parabola — the turning point."),
            ("Formula", f"x = -b/(2a). Here a = {a}, b = {b}."),
            ("Compute", f"x = -({b})/(2·{a}) = {-b}/{2*a} = {h}."),
            ("Open direction", f"Because a = {a} is {'positive (opens up, minimum)' if a > 0 else 'negative (opens down, maximum)'}."),
        ),
    )


def poly_end(rng: random.Random, skill_id: str) -> Problem:
    degree = rng.choice([3, 4, 5])
    lead = rng.choice([-3, -2, 2, 3, 4])
    prompt = (
        f"For $f(x) = {lead}x^{degree} + 5x - 1$, as $x \\to \\infty$, does $f(x)$ go to $\\infty$ or $-\\infty$? "
        "Enter inf or -inf."
    )
    to_pos = (lead > 0)
    ans = "inf" if to_pos else "-inf"
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=ans,
        answer_display="∞" if to_pos else "-∞",
        hint="End behavior is decided by the leading term a x^n only. For x → +∞, sign(a) wins.",
        common_mistakes=["Using the constant term, or thinking even/odd degree changes the right-hand end when a is given."],
        exam_tags=["ap_precalc_u1"],
        source="generated",
        cluster="poly",
        plot="polynomial",
        plot_data={"lead": lead, "degree": degree},
        steps=_steps(
            ("Goal", "Describe what happens to the graph far to the right. Lower-degree terms become negligible."),
            ("Leading term", f"The leading term is {lead}x^{degree}."),
            ("Large positive x", f"x^{degree} is positive for large positive x. Multiplying by {lead} makes the product {'positive' if to_pos else 'negative'}."),
            ("Conclusion", f"As x → ∞, f(x) → {ans}. (The left-hand end would also use even/odd degree.)"),
        ),
    )


def poly_zeros(rng: random.Random, skill_id: str) -> Problem:
    r, s, t = 1, rng.randint(2, 5), -rng.randint(2, 5)
    prompt = (
        f"List the real zeros of $f(x) = (x-{r})(x-{s})(x-{t})$. "
        "Enter three numbers separated by commas."
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=f"{r}, {s}, {t}",
        answer_display=f"{r}, {s}, {t}",
        hint="A product is zero when a factor is zero. Set each factor equal to 0.",
        common_mistakes=["Reporting the opposite signs (the numbers in the factors, not the actual zeros)."],
        exam_tags=["ap_precalc_u1"],
        source="generated",
        cluster="poly",
        plot="poly_zeros",
        plot_data={"roots": [r, s, t]},
        steps=_steps(
            ("Goal", "Zeros are inputs that make f(x) = 0. They are the x-intercepts of the graph."),
            ("Zero product", f"(x-{r})(x-{s})(x-{t}) = 0 when x-{r}=0 or x-{s}=0 or x-{t}=0."),
            ("Solve each", f"x = {r}, x = {s}, x = {t}."),
            ("Check a zero", f"f({r}) has a factor (x-{r}) that becomes 0, so the whole product is 0."),
        ),
    )


def poly_div(rng: random.Random, skill_id: str) -> Problem:
    # divide (x^2 + (a+b)x + ab) by (x+a)  leftover (x+b) remainder 0
    a = rng.randint(2, 5)
    b = rng.randint(2, 6)
    s = a + b
    p = a * b
    prompt = (
        f"Divide $x^2 + {s}x + {p}$ by $x + {a}$. "
        f"What is the quotient? Enter as x+k (remainder is 0)."
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=f"x+{b}",
        answer_display=f"x+{b}",
        hint="If remainder is 0, the divisor is a factor. You can also use synthetic division with root -a.",
        common_mistakes=["Using synthetic division with +a instead of the root x = -a."],
        exam_tags=["clep_algebra", "ap_precalc_u1"],
        source="generated",
        cluster="poly",
        steps=_steps(
            ("Goal", "Polynomial division asks: what times (x+a) gives the original quadratic?"),
            ("Because it factors", f"x^2 + {s}x + {p} = (x+{a})(x+{b}). You can FOIL to verify: middle term {a}+{b}={s}, constant {a}·{b}={p}."),
            ("Quotient", f"Dividing by (x+{a}) leaves the other factor, x+{b}, with remainder 0."),
            ("Remainder theorem reminder", f"The remainder when dividing by x+{a} = x-(-{a}) equals f(-{a}), which is 0 here, confirming exact division."),
        ),
    )


def rational_fn(rng: random.Random, skill_id: str) -> Problem:
    p, q = rng.randint(2, 6), rng.randint(2, 6)
    if p == q:
        q += 1
    prompt = (
        f"Find the vertical asymptote of $f(x) = \\dfrac{{x+{p}}}{{x-{q}}}$. "
        "Enter the x-value of the asymptote."
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(q),
        answer_display=f"x = {q}",
        hint="Vertical asymptotes come from zeros of the denominator that do not cancel with the numerator.",
        common_mistakes=["Using the numerator's zero, or reporting y = q."],
        exam_tags=["ap_precalc_u1"],
        source="generated",
        cluster="poly",
        plot="rational",
        plot_data={"p": p, "q": q},
        steps=_steps(
            ("Goal", "A vertical asymptote is a vertical line the graph approaches but does not cross (for a simplified rational function)."),
            ("Denominator zero", f"x - {q} = 0 when x = {q}."),
            ("Check cancellation", f"The numerator at x = {q} is {q}+{p} = {q+p} ≠ 0, so the factor does not cancel. This is a VA, not a hole."),
            ("Write the line", f"The vertical asymptote is the line x = {q}."),
        ),
    )


def variation(rng: random.Random, skill_id: str) -> Problem:
    k = rng.choice([6, 8, 12, 24, 30])
    x1, y1 = rng.choice([2, 3, 4, 5]), None
    y1 = k * x1
    x2 = rng.choice([6, 8, 10])
    y2 = k * x2
    prompt = (
        f"y varies directly with x. If y = {y1} when x = {x1}, what is y when x = {x2}?"
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(y2),
        answer_display=str(y2),
        hint="Direct variation means y = kx. Find k from the first pair, then evaluate.",
        common_mistakes=["Using inverse variation y = k/x on a 'varies directly' problem."],
        exam_tags=["clep_algebra"],
        source="generated",
        cluster="poly",
        plot="variation",
        plot_data={"k": k, "x1": x1, "y1": y1, "x2": x2, "y2": y2},
        steps=_steps(
            ("Goal", "Direct variation: outputs scale by the same factor as inputs."),
            ("Find k", f"y = kx ⇒ {y1} = k·{x1} ⇒ k = {y1}/{x1} = {k}."),
            ("Evaluate at the new x", f"Now y = {k} · {x2} = {y2}. That is the predicted output at the new input."),
            ("Proportion check", f"y1/x1 = y2/x2: {y1}/{x1} = {y2}/{x2} = {k}."),
        ),
    )


def exponential(rng: random.Random, skill_id: str) -> Problem:
    base = rng.choice([2, 3])
    n = rng.randint(3, 6)
    prompt = f"Evaluate $ {base}^{{{n}}} $."
    ans = base**n
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(ans),
        answer_display=str(ans),
        hint="An exponential with a positive integer exponent is repeated multiplication of the base.",
        common_mistakes=["Computing base*n instead of repeated multiplication."],
        exam_tags=["ap_precalc_u2"],
        source="generated",
        cluster="explog",
        plot="exponential",
        plot_data={"base": base, "n": n},
        steps=_steps(
            ("Goal", "Evaluate a power. The exponent counts how many times the base is a factor."),
            ("Write the product", f"{base}^{n} means {n} factors of {base}."),
            ("Multiply stepwise", f"Keep a running product until you have used {n} factors. The result is {ans}."),
            ("Not multiplication by the exponent", f"{base}·{n} = {base*n}, which is a different (wrong) number."),
        ),
    )


def log_eval(rng: random.Random, skill_id: str) -> Problem:
    b = rng.choice([2, 3, 5, 10])
    e = rng.randint(2, 4)
    arg = b**e
    prompt = f"Evaluate $\\log_{{{b}}} {arg}$."
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(e),
        answer_display=str(e),
        hint="log_b a = c means b^c = a. Ask: 'b to what power is a?'",
        common_mistakes=["Swapping the base and the argument, or answering with b^e."],
        exam_tags=["clep_algebra", "ap_precalc_u2"],
        source="generated",
        cluster="explog",
        plot="log",
        plot_data={"base": b, "arg": arg},
        steps=_steps(
            ("Goal", "A logarithm is an exponent. The value of the log is the missing exponent."),
            ("Rewrite", f"$\\log_{{{b}}} {arg} = c$ means ${b}^c = {arg}$."),
            ("Find the power", f"{b}^{e} = {arg}, so the logarithm (the missing exponent) is {e}."),
            ("Domain reminder", "Logs of nonpositive numbers are not real. The argument here is positive, so we are fine."),
        ),
    )


def log_props(rng: random.Random, skill_id: str) -> Problem:
    a, b = rng.choice([2, 3, 5]), rng.choice([2, 3, 4])
    prompt = (
        f"Use log properties to write as a single number (an integer): "
        f"$\\log_{{{a}}} {a**b} + \\log_{{{a}}} {a}$."
    )
    ans = b + 1
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(ans),
        answer_display=str(ans),
        hint="log u + log v = log(uv), and log_b (b^k) = k.",
        common_mistakes=["Multiplying the two logs, or writing log(u+v)."],
        exam_tags=["clep_algebra", "ap_precalc_u2"],
        source="generated",
        cluster="explog",
        steps=_steps(
            ("Goal", "Combine logs, then evaluate using the definition."),
            ("Sum rule", f"$\\log_{{{a}}} {a**b} + \\log_{{{a}}} {a} = \\log_{{{a}}}(({a**b})·{a}) = \\log_{{{a}}}({a**(b+1)})$."),
            ("Definition", f"$\\log_{{{a}}}({a}^{{{ans}}}) = {ans}$, because the log returns the exponent."),
            ("Another path", f"Each log is already an exponent: {b} + 1 = {ans}."),
        ),
    )


def explog_eq(rng: random.Random, skill_id: str) -> Problem:
    b = rng.choice([2, 3])
    xsol = rng.randint(2, 5)
    prompt = f"Solve for $x$.\n\n${b}^{{x}} = {b**xsol}$"
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(xsol),
        answer_display=str(xsol),
        hint="If the bases are the same (and valid), the exponents are equal.",
        common_mistakes=["Taking x equal to the right-hand side instead of the matching exponent."],
        exam_tags=["clep_algebra", "ap_precalc_u2"],
        source="generated",
        cluster="explog",
        plot="exponential",
        plot_data={"base": b, "n": xsol},
        steps=_steps(
            ("Goal", "Solve an exponential equation. Same bases let you equate exponents."),
            ("Rewrite the right side", f"The number {b**xsol} is itself a power of {b}: {b**xsol} = {b}^{xsol}."),
            ("Equal bases", f"{b}^x = {b}^{xsol} implies x = {xsol}, because the exponential function base {b} is one-to-one."),
            ("Check", f"{b}^{xsol} = {b**xsol}, which matches the right-hand side."),
        ),
    )


def system2(rng: random.Random, skill_id: str) -> Problem:
    xsol, ysol = rng.randint(1, 6), rng.randint(1, 6)
    a1, b1 = rng.randint(1, 3), rng.randint(1, 3)
    a2, b2 = rng.randint(1, 3), rng.randint(1, 3)
    if a1 * b2 == a2 * b1:
        b2 += 1
    c1 = a1 * xsol + b1 * ysol
    c2 = a2 * xsol + b2 * ysol
    prompt = (
        f"Solve the system. Enter x,y.\n\n"
        f"${a1}x + {b1}y = {c1}$\n\n${a2}x + {b2}y = {c2}$"
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=f"{xsol},{ysol}",
        answer_display=f"({xsol}, {ysol})",
        hint="Use elimination or substitution. Find one variable, then plug back to get the other.",
        common_mistakes=["Stopping after finding x, or adding equations that do not cancel a variable."],
        exam_tags=["clep_algebra", "clep_precalc"],
        source="generated",
        cluster="systems",
        plot="system",
        plot_data={"a1": a1, "b1": b1, "c1": c1, "a2": a2, "b2": b2, "c2": c2, "x": xsol, "y": ysol},
        steps=_steps(
            ("Goal", "A solution of a 2×2 linear system is an ordered pair (x, y) that satisfies both equations at once."),
            (
                "Elimination idea",
                "Multiply one or both equations so the y-coefficients (or x) match, then subtract to cancel that variable.",
            ),
            ("The solution pair", f"The unique intersection is x = {xsol}, y = {ysol}."),
            (
                "Check both lines",
                f"{a1}({xsol})+{b1}({ysol}) = {c1} and {a2}({xsol})+{b2}({ysol}) = {c2}. Both originals are satisfied.",
            ),
        ),
    )


def partial(rng: random.Random, skill_id: str) -> Problem:
    r, s = 1, rng.randint(2, 5)
    # 1/((x-r)(x-s)) = A/(x-r)+B/(x-s)
    # A = 1/(r-s)? Wait 1/((x-1)(x-s))
    # A(x-s)+B(x-r)=1. x=r: A(r-s)=1, A=1/(r-s)
    prompt = (
        f"Decompose $\\dfrac{{1}}{{(x-{r})(x-{s})}}$ into partial fractions. "
        f"What is the numerator A on the term for $(x-{r})$? "
        f"(The form is $A/(x-{r}) + B/(x-{s})$.)"
    )
    A = 1 / (r - s)
    # keep as fraction
    # r-s = 1-s negative
    den = r - s
    from math import gcd

    g = gcd(1, den)
    num, den2 = 1 // g, den // g
    ans = f"{num}/{den2}" if den2 != 1 else str(num)
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=ans,
        answer_display=ans,
        hint="Write A/(x-r)+B/(x-s), clear denominators, then plug in x=r to isolate A.",
        common_mistakes=["Using A = 1, or swapping A and B."],
        exam_tags=["clep_precalc"],
        source="generated",
        cluster="systems",
        steps=_steps(
            ("Goal", "Partial fractions rewrites a rational expression as a sum of simpler pieces."),
            ("Setup", f"Assume $1/((x-{r})(x-{s})) = A/(x-{r}) + B/(x-{s})$."),
            ("Clear denominators", f"A(x-{s}) + B(x-{r}) = 1. Set x = {r}: A({r}-{s}) = 1, so A = 1/({r}-{s}) = {ans}."),
            ("Meaning", "You would similarly find B by setting x to the other root. This skill is algebra you will reuse in Calc 2 integrals."),
        ),
    )


def sequence(rng: random.Random, skill_id: str) -> Problem:
    a1, d, n = rng.randint(2, 9), rng.randint(2, 5), rng.randint(5, 9)
    an = a1 + (n - 1) * d
    prompt = f"The sequence is arithmetic: a1 = {a1}, common difference d = {d}. Find a_{{{n}}}."
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(an),
        answer_display=str(an),
        hint="a_n = a1 + (n-1)d. You add the difference once for each step after the first term.",
        common_mistakes=["Using n d instead of (n-1)d."],
        exam_tags=["clep_algebra", "ap_precalc_u2"],
        source="generated",
        cluster="sequences",
        plot="seq",
        plot_data={"kind": "arith", "a1": a1, "d": d, "n": n},
        steps=_steps(
            ("Goal", "Find one term of an arithmetic sequence from the explicit formula."),
            ("Formula", f"a_n = a_1 + (n-1)d = {a1} + (n-1)({d})."),
            ("Plug in n", f"a_{n} = {a1} + ({n}-1)({d}) = {a1} + {n-1}·{d} = {a1} + {(n-1)*d} = {an}."),
            ("Count the jumps", f"From term 1 to term {n} there are {n-1} jumps of {d}."),
        ),
    )


def arithmetic_seq(rng: random.Random, skill_id: str) -> Problem:
    return sequence(rng, skill_id)


def geometric_seq(rng: random.Random, skill_id: str) -> Problem:
    a1, r, n = rng.choice([2, 3, 5]), rng.choice([2, 3]), rng.randint(4, 6)
    an = a1 * (r ** (n - 1))
    prompt = f"Geometric sequence: a1 = {a1}, ratio r = {r}. Find a_{{{n}}}."
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(an),
        answer_display=str(an),
        hint="a_n = a1 r^{n-1}. The first term is already 'r to the 0'.",
        common_mistakes=["Using r^n instead of r^{n-1}."],
        exam_tags=["clep_algebra", "ap_precalc_u2"],
        source="generated",
        cluster="sequences",
        plot="seq",
        plot_data={"kind": "geo", "a1": a1, "r": r, "n": n},
        steps=_steps(
            ("Goal", "A geometric sequence multiplies by r at every step."),
            ("Formula", f"The explicit formula is a_n = {a1} · {r}^{{n-1}}. The first term already uses exponent 0."),
            ("Evaluate", f"a_{n} = {a1} · {r}^{n-1} = {a1} · {r**(n-1)} = {an}."),
            ("Count the multiplications", f"You multiply by r exactly {n-1} times to get from a1 to a_{n}."),
        ),
    )


def series(rng: random.Random, skill_id: str) -> Problem:
    a1, d, n = rng.randint(2, 5), rng.randint(2, 4), rng.choice([5, 6, 8, 10])
    an = a1 + (n - 1) * d
    s = n * (a1 + an) // 2
    prompt = f"Sum the first {n} terms of the arithmetic sequence with a1 = {a1} and d = {d}."
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(s),
        answer_display=str(s),
        hint="S_n = n(a1 + a_n)/2. First find a_n, then average the first and last and multiply by n.",
        common_mistakes=["Adding a1 + n d without using the pairing formula."],
        exam_tags=["clep_algebra"],
        source="generated",
        cluster="sequences",
        steps=_steps(
            ("Goal", "A series is a sum of sequence terms. Arithmetic sums have a pairing shortcut."),
            ("Last term", f"a_{n} = {a1} + ({n}-1)({d}) = {an}."),
            ("Sum formula", f"S_{n} = {n}({a1}+{an})/2 = {n}({a1+an})/2 = {s}."),
            ("Why it works", "Pair first with last, second with second-last, … Each pair has the same sum, and there are n/2 such pairs (or n times the average)."),
        ),
    )


def counting(rng: random.Random, skill_id: str) -> Problem:
    n = rng.randint(6, 10)
    r = rng.randint(2, 4)
    val = comb(n, r)
    prompt = f"Compute $C({n},{r}) = \\binom{{{n}}}{{{r}}}$ (combinations, order does not matter)."
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(val),
        answer_display=str(val),
        hint="C(n,r) = n! / (r! (n-r)!). You can also cancel the r factors in the numerator n(n-1)...(n-r+1).",
        common_mistakes=["Computing a permutation P(n,r) instead, which is larger because order is counted."],
        exam_tags=["clep_algebra"],
        source="generated",
        cluster="sequences",
        steps=_steps(
            ("Goal", "Count unordered selections of r items from n."),
            ("Formula", f"C({n},{r}) = {n}! / ({r}! · {n-r}!)."),
            ("Compute", f"C({n},{r}) = {val}. That is how many unordered {r}-groups exist from {n} items."),
            ("Why smaller than P", f"P({n},{r}) would count ordered lists. Each unordered group corresponds to {r}! ordered lists, so we divide by r!."),
        ),
    )


def binomial(rng: random.Random, skill_id: str) -> Problem:
    n = rng.choice([4, 5, 6])
    k = rng.randint(1, n - 1)
    coef = comb(n, k)
    prompt = (
        f"In the expansion of $(x+y)^{n}$, what is the coefficient of $x^{{{n-k}}} y^{{{k}}}$?"
    )
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(coef),
        answer_display=str(coef),
        hint="The coefficient of x^{n-k} y^k in (x+y)^n is C(n,k).",
        common_mistakes=["Using C(n, n-k) and then multiplying by extra powers, or using n instead of C(n,k)."],
        exam_tags=["clep_algebra"],
        source="generated",
        cluster="sequences",
        steps=_steps(
            ("Goal", "The binomial theorem lists every term of (x+y)^n with a combination coefficient."),
            ("General term", f"The term with y^{k} is C({n},{k}) x^{n-k} y^{k}."),
            ("Coefficient only", f"C({n},{k}) = {coef}. That integer sits in front of x^{n-k} y^{k}."),
            ("Check a tiny case", "For (x+y)^2 the y^1 term has coefficient C(2,1)=2, matching x^2 + 2xy + y^2."),
        ),
    )


def probability(rng: random.Random, skill_id: str) -> Problem:
    red, blue = rng.randint(3, 7), rng.randint(2, 6)
    total = red + blue
    prompt = (
        f"A bag has {red} red marbles and {blue} blue marbles. "
        "One marble is drawn at random. What is P(red)? Enter a simplified fraction a/b."
    )
    from math import gcd

    g = gcd(red, total)
    ans = f"{red // g}/{total // g}"
    return _prob(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=ans,
        answer_display=ans,
        hint="P = favorable / total, when each marble is equally likely.",
        common_mistakes=["Using red/blue instead of red/total."],
        exam_tags=["clep_algebra"],
        source="generated",
        cluster="sequences",
        steps=_steps(
            ("Goal", "A uniform probability is a count of equally likely outcomes."),
            ("Favorable and total", f"Favorable: {red} red. Total marbles: {red}+{blue} = {total}."),
            ("Form the ratio", f"P(red) = {red}/{total} = {ans} in lowest terms."),
            ("Check", f"The probability is between 0 and 1, and P(blue) = {blue}/{total} would complete the complement to 1."),
        ),
    )


GENERATORS = {
    "order_of_ops": order_of_ops,
    "exponents": exponents,
    "radicals": radicals,
    "polynomials": polynomials,
    "factoring": factoring,
    "rationals": rationals,
    "distance_midpoint": distance_midpoint,
    "linear_eq": linear_eq,
    "linear_model": linear_model,
    "complex": complex_num,
    "quadratic": quadratic,
    "other_eq": other_eq,
    "inequality": inequality,
    "function_eval": function_eval,
    "domain": domain,
    "rate_of_change": rate_of_change,
    "composition": composition,
    "transformations": transformations,
    "abs_function": abs_function,
    "inverse": inverse,
    "line": line,
    "parabola": parabola,
    "poly_end": poly_end,
    "poly_zeros": poly_zeros,
    "poly_div": poly_div,
    "rational_fn": rational_fn,
    "variation": variation,
    "exponential": exponential,
    "log_eval": log_eval,
    "log_props": log_props,
    "explog_eq": explog_eq,
    "system2": system2,
    "partial": partial,
    "sequence": sequence,
    "arithmetic_seq": arithmetic_seq,
    "geometric_seq": geometric_seq,
    "series": series,
    "counting": counting,
    "binomial": binomial,
    "probability": probability,
}


def generate_problem(generator_name: str, skill_id: str, seed: int | None = None) -> Problem:
    fn = lookup_generator(generator_name)
    last_err: Exception | None = None
    for extra in range(8):
        try:
            return fn(random.Random((seed or 0) + extra * 9973), skill_id)
        except Exception as exc:  # pragma: no cover - defensive
            last_err = exc
    raise RuntimeError(f"Could not generate {generator_name} for {skill_id}: {last_err}")


def lookup_generator(name: str):
    if name in GENERATORS:
        return GENERATORS[name]
    from src.generate_more import MORE_GENERATORS
    from src.generate_physics import PHYSICS_GENERATORS

    GENERATORS.update(MORE_GENERATORS)
    GENERATORS.update(PHYSICS_GENERATORS)
    if name not in GENERATORS:
        known = ", ".join(sorted(GENERATORS))
        raise KeyError(f"No generator named {name!r}. Known: {known}")
    return GENERATORS[name]


def ensure_all_generators() -> dict:
    from src.generate_more import MORE_GENERATORS
    from src.generate_physics import PHYSICS_GENERATORS

    GENERATORS.update(MORE_GENERATORS)
    GENERATORS.update(PHYSICS_GENERATORS)
    return GENERATORS
