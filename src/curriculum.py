from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Skill:
    id: str
    title: str
    lesson: str
    openstax_url: str
    extra_note: str
    exam_tags: list[str]
    status: str  # ready | coming
    generator: str | None = None
    cluster: str = ""
    relevance: list[str] = field(default_factory=list)
    why_relevant: str = ""


@dataclass
class Unit:
    id: str
    title: str
    skills: list[Skill]


@dataclass
class Course:
    id: str
    title: str
    blurb: str
    units: list[Course] | list[Unit] = field(default_factory=list)


OS = "https://openstax.org/books/algebra-and-trigonometry-2e/pages"
PC = "https://openstax.org/books/precalculus-2e/pages"
SZ = "https://www.stitz-zeager.com/"
PHY_BOOK = "https://openstax.org/books/college-physics-2e/pages"


def _s(
    skill_id: str,
    title: str,
    lesson: str,
    slug: str,
    tags: list[str],
    status: str,
    generator: str | None,
    cluster: str,
    extra: str = "",
    book: str = "at",
) -> Skill:
    base = OS if book == "at" else PC
    return Skill(
        id=skill_id,
        title=title,
        lesson=lesson,
        openstax_url=f"{base}/{slug}",
        extra_note=extra
        or (
            "OpenStax odd-numbered section exercises have answers in the book answer key. "
            f"Stitz–Zeager (free PDF at {SZ}) includes answers to nearly all computational exercises."
        ),
        exam_tags=tags,
        status=status,
        generator=generator,
        cluster=cluster,
    )


def _alg_lesson(remember: str, method: str, pitfall: str) -> str:
    return (
        f"**Remember:** {remember}\n\n"
        f"**Method:** {method}\n\n"
        f"**Watch out:** {pitfall}\n\n"
        "If a line in a later solution looks like a magic trick, it is usually one of these "
        "moves. Slow down and write the line you are changing, then the same line after "
        "the rule. That habit is how rusty algebra comes back."
    )


def _phy_lesson(remember: str, method: str, pitfall: str) -> str:
    return (
        f"**Remember:** {remember}\n\n"
        f"**Method:** {method}\n\n"
        f"**Watch out:** {pitfall}\n\n"
        "AP Physics 1 and 2 are algebra-based: no calculus. Draw a labeled picture, list "
        "knowns with units, pick the matching equation, then check whether the size and "
        "the sign make physical sense. These problems use $g = 10\\,\\mathrm{m/s^2}$ when "
        "gravity appears, the same convenience many AP free-response questions allow."
    )


def _phy(
    skill_id: str,
    title: str,
    lesson: str,
    slug: str,
    tags: list[str],
    generator: str,
    cluster: str,
) -> Skill:
    return Skill(
        id=skill_id,
        title=title,
        lesson=lesson,
        openstax_url=f"{PHY_BOOK}/{slug}",
        extra_note=(
            "OpenStax College Physics 2e is algebra-based (CC BY 4.0) — the same level as "
            "AP Physics 1/2 and a one-year college intro physics sequence. Odd-numbered "
            "problems have answers in the student solution guide."
        ),
        exam_tags=tags,
        status="ready",
        generator=generator,
        cluster=cluster,
    )


CLEP_A = ["clep_algebra"]
CLEP_P = ["clep_precalc"]
AP1 = ["ap_precalc_u1", "clep_precalc"]
AP2 = ["ap_precalc_u2", "clep_precalc", "clep_algebra"]
AP3 = ["ap_precalc_u3", "clep_precalc"]
AP4 = ["ap_precalc_u4"]
AP_P1 = ["ap_physics1"]
AP_P2 = ["ap_physics2"]
AP_P12 = ["ap_physics1", "ap_physics2"]


COURSES: list[Course] = [
    Course(
        id="algebra",
        title="College Algebra",
        blurb="Foundations through functions, polynomials, exponentials, systems, and sequences.",
        units=[
            Unit(
                id="alg-ch1",
                title="1. Prerequisites (Algebra foundations)",
                skills=[
                    _s(
                        "alg-1-1",
                        "Real numbers and algebra essentials",
                        _alg_lesson(
                            "The real numbers include negatives, fractions, and irrationals. Absolute value |a| is distance from 0, so it is never negative.",
                            "Use the order of operations: grouping symbols, exponents, multiply/divide left to right, add/subtract left to right. Treat a fraction bar as a grouping symbol.",
                            "Doing addition before division, or dropping a negative sign when it sits in front of a fraction.",
                        ),
                        "1-1-real-numbers-algebra-essentials",
                        CLEP_A,
                        "ready",
                        "order_of_ops",
                        "foundations",
                    ),
                    _s(
                        "alg-1-2",
                        "Exponents and scientific notation",
                        _alg_lesson(
                            "a^m means a multiplied by itself m times. a^0 = 1 (a ≠ 0). a^{-n} = 1/a^n.",
                            "Product rule a^m a^n = a^{m+n}. Quotient a^m / a^n = a^{m-n}. Power (a^m)^n = a^{mn}.",
                            "Writing (2x)^3 as 2x^3. The exponent 3 applies only to x unless parentheses wrap 2x.",
                        ),
                        "1-2-exponents-and-scientific-notation",
                        CLEP_A,
                        "ready",
                        "exponents",
                        "foundations",
                    ),
                    _s(
                        "alg-1-3",
                        "Radicals and rational exponents",
                        _alg_lesson(
                            "√a is the principal (nonnegative) square root. a^{1/n} = ⁿ√a. a^{m/n} = (ⁿ√a)^m.",
                            "Simplify by factoring perfect squares/cubes out of the radical. Rationalize a denominator by multiplying by a conjugate when needed.",
                            "√(a+b) is not √a + √b. Also √(x^2) = |x|, not always x.",
                        ),
                        "1-3-radicals-and-rational-exponents",
                        CLEP_A,
                        "ready",
                        "radicals",
                        "foundations",
                    ),
                    _s(
                        "alg-1-4",
                        "Polynomials",
                        _alg_lesson(
                            "A polynomial is a sum of terms a_n x^n + ... + a_0. Degree is the highest power with a nonzero coefficient.",
                            "Add like terms. Multiply using distribution (FOIL for binomials). Keep track of signs.",
                            "Combining unlike terms (3x^2 + 5x is already simplified) or losing the middle term when squaring (x+2)^2 = x^2 + 4x + 4, not x^2 + 4.",
                        ),
                        "1-4-polynomials",
                        CLEP_A,
                        "ready",
                        "polynomials",
                        "foundations",
                    ),
                    _s(
                        "alg-1-5",
                        "Factoring polynomials",
                        _alg_lesson(
                            "Factoring undoes multiplying. Always try a greatest common factor first.",
                            "Trinomials x^2 + bx + c need two numbers that multiply to c and add to b. Difference of squares a^2 - b^2 = (a-b)(a+b).",
                            "Stopping after one factor when more factoring is possible, or sign errors on the constant term.",
                        ),
                        "1-5-factoring-polynomials",
                        CLEP_A,
                        "ready",
                        "factoring",
                        "foundations",
                    ),
                    _s(
                        "alg-1-6",
                        "Rational expressions",
                        _alg_lesson(
                            "A rational expression is a polynomial divided by a polynomial. It is undefined where the denominator is 0.",
                            "Simplify by factoring numerator and denominator, then cancel common factors (never cancel terms across a +).",
                            "Canceling the x in (x+2)/x to get 2. You can only cancel factors, not terms.",
                        ),
                        "1-6-rational-expressions",
                        CLEP_A,
                        "ready",
                        "rationals",
                        "foundations",
                    ),
                ],
            ),
            Unit(
                id="alg-ch2",
                title="2. Equations and inequalities",
                skills=[
                    _s(
                        "alg-2-1",
                        "Coordinate plane, distance, midpoint",
                        _alg_lesson(
                            "A point (x, y) is x units right/left and y units up/down from the origin.",
                            "Distance: √[(x2-x1)^2 + (y2-y1)^2]. Midpoint: average the x's and average the y's.",
                            "Forgetting to square both differences, or averaging incorrectly (midpoint is not a distance).",
                        ),
                        "2-1-the-rectangular-coordinate-systems-and-graphs",
                        CLEP_A + CLEP_P,
                        "ready",
                        "distance_midpoint",
                        "equations",
                    ),
                    _s(
                        "alg-2-2",
                        "Linear equations in one variable",
                        _alg_lesson(
                            "A linear equation can be written ax + b = 0 with a ≠ 0. Solutions make both sides equal.",
                            "Do the same operation to both sides. Undo addition/subtraction first, then multiplication/division. Distribute, then collect like terms.",
                            "Only moving one term when clearing parentheses, or dividing only one term by a coefficient.",
                        ),
                        "2-2-linear-equations-in-one-variable",
                        CLEP_A,
                        "ready",
                        "linear_eq",
                        "equations",
                    ),
                    _s(
                        "alg-2-3",
                        "Models and applications",
                        _alg_lesson(
                            "Word problems become equations after you name the unknown and translate English into algebra.",
                            "Define x clearly. Write an equation that matches the story (is, more than, per, total). Solve, then check units and whether the answer makes sense.",
                            "Solving a correct-looking equation that does not match the story, especially with consecutive integers or 'less than'.",
                        ),
                        "2-3-models-and-applications",
                        CLEP_A,
                        "ready",
                        "linear_model",
                        "equations",
                    ),
                    _s(
                        "alg-2-4",
                        "Complex numbers",
                        _alg_lesson(
                            "i is defined by i^2 = -1. A complex number is a + bi with a, b real.",
                            "Add real parts and imaginary parts separately. Multiply with distribution and replace i^2 with -1. Divide by multiplying by the conjugate.",
                            "Leaving i^2 in the answer, or treating i like a variable that can be canceled casually.",
                        ),
                        "2-4-complex-numbers",
                        CLEP_A + AP1,
                        "ready",
                        "complex",
                        "equations",
                    ),
                    _s(
                        "alg-2-5",
                        "Quadratic equations",
                        _alg_lesson(
                            "A quadratic has the form ax^2 + bx + c = 0, a ≠ 0. There can be 0, 1, or 2 real solutions (and always 2 complex solutions counting multiplicity).",
                            "Try factoring. If that fails, quadratic formula x = [-b ± √(b^2 - 4ac)] / (2a). Completing the square is the same idea in disguise.",
                            "Using the formula but forgetting 2a is the whole denominator. Sign errors on b.",
                        ),
                        "2-5-quadratic-equations",
                        CLEP_A + AP1,
                        "ready",
                        "quadratic",
                        "equations",
                    ),
                    _s(
                        "alg-2-6",
                        "Other equations (rational, radical, absolute value)",
                        _alg_lesson(
                            "Extra equation types still isolate the variable, then you must check because squaring or clearing a denominator can add fake solutions.",
                            "Absolute value: |u| = k becomes u = k or u = -k (if k ≥ 0). Radicals: isolate, square, then check. Rationals: multiply by the LCD, then check excluded values.",
                            "Keeping extraneous solutions that make a denominator 0 or a square root of a negative in the original.",
                        ),
                        "2-6-other-types-of-equations",
                        CLEP_A + CLEP_P,
                        "ready",
                        "other_eq",
                        "equations",
                    ),
                    _s(
                        "alg-2-7",
                        "Linear and absolute value inequalities",
                        _alg_lesson(
                            "Inequalities compare sizes. The solution is usually an interval of x-values, not a single number.",
                            "Solve like an equation, but reverse the inequality when you multiply or divide by a negative. For |u| < k, think -k < u < k.",
                            "Forgetting to flip the inequality when multiplying by a negative.",
                        ),
                        "2-7-linear-inequalities-and-absolute-value-inequalities",
                        CLEP_A,
                        "ready",
                        "inequality",
                        "equations",
                    ),
                ],
            ),
            Unit(
                id="alg-ch3",
                title="3. Functions",
                skills=[
                    _s(
                        "alg-3-1",
                        "Functions and function notation",
                        _alg_lesson(
                            "A function assigns each allowed input exactly one output. f(x) is the output when the input is x — it is not f times x.",
                            "To evaluate f(a), replace every x with a (use parentheses). To solve f(x) = k, set the formula equal to k.",
                            "Reading f(x+1) as f(x) + 1. Those are different unless f is a very special function.",
                        ),
                        "3-1-functions-and-function-notation",
                        AP1 + CLEP_A,
                        "ready",
                        "function_eval",
                        "functions",
                    ),
                    _s(
                        "alg-3-2",
                        "Domain and range",
                        _alg_lesson(
                            "Domain = allowed inputs. Range = possible outputs. Real-valued functions cannot divide by 0 or take an even root of a negative.",
                            "Find values that break the formula. Write the domain in interval notation. Range often needs a graph or completing the square.",
                            "Including x-values that make a denominator 0, or writing [0, ∞) for √(x-3) instead of [3, ∞).",
                        ),
                        "3-2-domain-and-range",
                        AP1 + CLEP_A,
                        "ready",
                        "domain",
                        "functions",
                    ),
                    _s(
                        "alg-3-3",
                        "Rates of change and graph behavior",
                        _alg_lesson(
                            "Average rate of change of f from a to b is [f(b)-f(a)] / (b-a) — the slope of the secant line.",
                            "Increasing means outputs grow as x grows. Turning points and intercepts describe the graph's shape.",
                            "Using (b-a) / (f(b)-f(a)) (that's the reciprocal of the rate you want).",
                        ),
                        "3-3-rates-of-change-and-behavior-of-graphs",
                        AP1,
                        "ready",
                        "rate_of_change",
                        "functions",
                    ),
                    _s(
                        "alg-3-4",
                        "Composition of functions",
                        _alg_lesson(
                            "(f ∘ g)(x) = f(g(x)): do g first, then feed that output into f.",
                            "Compute g(x), then substitute that entire expression into f. Domain of the composition is restricted by g and by f.",
                            "Composing in the wrong order. f ∘ g is usually not g ∘ f.",
                        ),
                        "3-4-composition-of-functions",
                        AP2 + CLEP_A,
                        "ready",
                        "composition",
                        "functions",
                    ),
                    _s(
                        "alg-3-5",
                        "Transformations of functions",
                        _alg_lesson(
                            "f(x) + k shifts up, f(x) - k down, f(x - h) right, f(x + h) left. a f(x) stretches vertically if |a| > 1.",
                            "Inside changes (on x) are horizontal and often feel backwards. Outside changes are vertical and behave as expected.",
                            "Thinking f(x-2) moves left because of the minus sign. It moves right.",
                        ),
                        "3-5-transformation-of-functions",
                        AP1,
                        "ready",
                        "transformations",
                        "functions",
                    ),
                    _s(
                        "alg-3-6",
                        "Absolute value functions",
                        _alg_lesson(
                            "y = |x| is a V-shape, vertex at the origin. y = a|x-h| + k moves and stretches that V.",
                            "The vertex is (h, k) for y = a|x-h| + k. The graph reflects over the x-axis if a is negative.",
                            "Graphing |x| + 2 as a V that opens from -2, or forgetting the vertex shift.",
                        ),
                        "3-6-absolute-value-functions",
                        CLEP_A + CLEP_P,
                        "ready",
                        "abs_function",
                        "functions",
                    ),
                    _s(
                        "alg-3-7",
                        "Inverse functions",
                        _alg_lesson(
                            "f^{-1} undoes f: (f^{-1} ∘ f)(x) = x. f^{-1} is not 1/f.",
                            "Replace f(x) with y, swap x and y, solve for y. That new y is f^{-1}(x). Domain and range swap.",
                            "Treating the -1 as an exponent. Also, not every function has an inverse unless it is one-to-one.",
                        ),
                        "3-7-inverse-functions",
                        AP2 + CLEP_A,
                        "ready",
                        "inverse",
                        "functions",
                    ),
                ],
            ),
            Unit(
                id="alg-ch4",
                title="4. Linear functions",
                skills=[
                    _s(
                        "alg-4-1",
                        "Linear functions",
                        _alg_lesson(
                            "A linear function has constant rate of change (slope) m. Slope-intercept form: y = mx + b.",
                            "m = (y2-y1)/(x2-x1). Point-slope: y - y1 = m(x - x1). Parallel lines share m; perpendicular lines have slopes that multiply to -1.",
                            "Inverting rise/run, or using the negative-reciprocal rule on a horizontal line (slope 0 has no perpendicular slope of the form -1/0).",
                        ),
                        "4-1-linear-functions",
                        AP1 + CLEP_A,
                        "ready",
                        "line",
                        "functions",
                    ),
                    _s(
                        "alg-4-2",
                        "Modeling with linear functions",
                        _alg_lesson(
                            "If a quantity changes by a constant amount per unit time, a line is a reasonable model.",
                            "Identify slope as the rate (with units) and intercept as the starting value. Write y = mx + b, then answer the question asked.",
                            "Mixing up which variable is independent, or using a point that is not actually on the model.",
                        ),
                        "4-2-modeling-with-linear-functions",
                        AP1 + CLEP_P,
                        "ready",
                        "linear_model",
                        "functions",
                    ),
                    _s(
                        "alg-4-3",
                        "Fitting linear models to data",
                        _alg_lesson(
                            "A line of best fit summarizes a trend; residuals are observed minus predicted.",
                            "For two exact points, the line through them is the model. For noisier data, you estimate slope from trend (graphing calculator / regression later).",
                            "Forcing a line through the origin when the intercept should not be 0.",
                        ),
                        "4-3-fitting-linear-models-to-data",
                        AP1,
                        "ready",
                        "line",
                        "functions",
                    ),
                ],
            ),
            Unit(
                id="alg-ch5",
                title="5. Polynomial and rational functions",
                skills=[
                    _s(
                        "alg-5-1",
                        "Quadratic functions",
                        _alg_lesson(
                            "A quadratic graph is a parabola. Vertex form a(x-h)^2 + k has vertex (h, k).",
                            "Vertex x-coordinate is x = -b/(2a) in standard form. Axis of symmetry is the vertical line through the vertex.",
                            "Using +b/(2a) instead of -b/(2a), or mixing up whether a > 0 opens up.",
                        ),
                        "5-1-quadratic-functions",
                        AP1,
                        "ready",
                        "parabola",
                        "poly",
                    ),
                    _s(
                        "alg-5-2",
                        "Power and polynomial functions",
                        _alg_lesson(
                            "Even-degree polynomials with positive leading coefficient go up on both ends. Odd degree with positive leading coefficient: down on the left, up on the right.",
                            "Leading term dominates end behavior. Degree n can have at most n real zeros.",
                            "Reading end behavior from the constant term instead of the leading term.",
                        ),
                        "5-2-power-functions-and-polynomial-functions",
                        AP1,
                        "ready",
                        "poly_end",
                        "poly",
                    ),
                    _s(
                        "alg-5-3",
                        "Graphs of polynomial functions",
                        _alg_lesson(
                            "Zeros are x-intercepts. Multiplicity odd: the graph crosses. Multiplicity even: it bounces.",
                            "Plot intercepts, use multiplicity, then sketch using end behavior.",
                            "Crossing the axis at a double root.",
                        ),
                        "5-3-graphs-of-polynomial-functions",
                        AP1,
                        "ready",
                        "poly_zeros",
                        "poly",
                    ),
                    _s(
                        "alg-5-4",
                        "Dividing polynomials",
                        _alg_lesson(
                            "Polynomial division is like integer long division. Remainder theorem: remainder when dividing by (x-c) is f(c).",
                            "Write missing powers with 0 coefficients. Synthetic division is a shortcut for divisors of the form x-c.",
                            "Dropping a 0 placeholder, which shifts every later coefficient.",
                        ),
                        "5-4-dividing-polynomials",
                        AP1 + CLEP_A,
                        "ready",
                        "poly_div",
                        "poly",
                    ),
                    _s(
                        "alg-5-5",
                        "Zeros of polynomial functions",
                        _alg_lesson(
                            "If f(c) = 0, then (x-c) is a factor. Complex zeros come in conjugate pairs for real coefficients.",
                            "Possible rational zeros are factors of constant over factors of leading coefficient. Test, factor, repeat.",
                            "Stopping after one rational zero when the leftover quadratic still factors.",
                        ),
                        "5-5-zeros-of-polynomial-functions",
                        AP1,
                        "ready",
                        "poly_zeros",
                        "poly",
                    ),
                    _s(
                        "alg-5-6",
                        "Rational functions",
                        _alg_lesson(
                            "Vertical asymptotes from zeros of the denominator (that do not cancel). Holes from factors that cancel. Horizontal asymptote from degrees of num/den.",
                            "Factor, cancel holes, set leftover denominator = 0 for vertical asymptotes. Compare degrees for HA: equal degrees → ratio of leading coefficients.",
                            "Calling a hole an asymptote, or using y = 0 as HA when degrees are equal but leading coefficients are not 1.",
                        ),
                        "5-6-rational-functions",
                        AP1,
                        "ready",
                        "rational_fn",
                        "poly",
                    ),
                    _s(
                        "alg-5-7",
                        "Inverses and radical functions",
                        _alg_lesson(
                            "√x is the inverse of x^2 only on [0, ∞). Cube root is defined for all real x.",
                            "To invert y = √(x-h) + k, swap and square carefully, then restore the domain.",
                            "Squaring and keeping extra solutions that do not land on the original range.",
                        ),
                        "5-7-inverses-and-radical-functions",
                        AP1,
                        "ready",
                        "inverse",
                        "poly",
                    ),
                    _s(
                        "alg-5-8",
                        "Variation",
                        _alg_lesson(
                            "Direct variation: y = kx. Inverse: y = k/x. Joint: y = kxz.",
                            "Use a given pair to find k, then evaluate at the new input.",
                            "Using inverse variation when the story says 'varies directly'.",
                        ),
                        "5-8-modeling-using-variation",
                        CLEP_A,
                        "ready",
                        "variation",
                        "poly",
                    ),
                ],
            ),
            Unit(
                id="alg-ch6",
                title="6. Exponential and logarithmic functions",
                skills=[
                    _s(
                        "alg-6-1",
                        "Exponential functions",
                        _alg_lesson(
                            "f(x) = a b^x (b > 0, b ≠ 1). Growth if b > 1, decay if 0 < b < 1.",
                            "b^{m+n} = b^m b^n. To solve b^x = b^k, set x = k when b is the same valid base.",
                            "Treating 2^x + 2^x as 2^{2x} instead of 2·2^x = 2^{x+1}.",
                        ),
                        "6-1-exponential-functions",
                        AP2,
                        "ready",
                        "exponential",
                        "explog",
                    ),
                    _s(
                        "alg-6-2",
                        "Graphs of exponential functions",
                        _alg_lesson(
                            "y = b^x always passes through (0, 1). Horizontal asymptote y = 0 unless shifted.",
                            "y = a b^{x-h} + k moves the asymptote to y = k and the intercept accordingly.",
                            "Giving y = b^x a y-intercept of b.",
                        ),
                        "6-2-graphs-of-exponential-functions",
                        AP2,
                        "ready",
                        "exponential",
                        "explog",
                    ),
                    _s(
                        "alg-6-3",
                        "Logarithmic functions",
                        _alg_lesson(
                            "log_b a = c means b^c = a. log and the matching exponential undo each other. ln is log_e; log often means log_10.",
                            "Rewrite logs as exponentials to evaluate. Domain of log_b(x) is x > 0.",
                            "Writing log(a+b) = log a + log b (false). Also log of a negative number is not real.",
                        ),
                        "6-3-logarithmic-functions",
                        AP2 + CLEP_A,
                        "ready",
                        "log_eval",
                        "explog",
                    ),
                    _s(
                        "alg-6-4",
                        "Graphs of logarithmic functions",
                        _alg_lesson(
                            "y = log_b x is the reflection of y = b^x across y = x. Vertical asymptote x = 0, passes through (1, 0).",
                            "Shifts: log_b(x-h) + k. Domain starts at the vertical asymptote.",
                            "Putting the asymptote on the x-axis (that is the exponential's asymptote).",
                        ),
                        "6-4-graphs-of-logarithmic-functions",
                        AP2,
                        "ready",
                        "log_eval",
                        "explog",
                    ),
                    _s(
                        "alg-6-5",
                        "Logarithmic properties",
                        _alg_lesson(
                            "log(uv) = log u + log v. log(u/v) = log u - log v. log(u^p) = p log u.",
                            "Expand products into sums; condense sums into a single log before exponentiating.",
                            "Applying the power rule to log(u) + log(v) incorrectly, or changing the base by accident.",
                        ),
                        "6-5-logarithmic-properties",
                        AP2 + CLEP_A,
                        "ready",
                        "log_props",
                        "explog",
                    ),
                    _s(
                        "alg-6-6",
                        "Exponential and logarithmic equations",
                        _alg_lesson(
                            "Same bases: set exponents equal. Different bases: take log of both sides. Logs on one side: rewrite as exponential.",
                            "Always check the domain: arguments of logs must stay positive.",
                            "Taking log of both sides but only of one term in a sum, e.g. log(2^x + 1).",
                        ),
                        "6-6-exponential-and-logarithmic-equations",
                        AP2 + CLEP_A,
                        "ready",
                        "explog_eq",
                        "explog",
                    ),
                    _s(
                        "alg-6-7",
                        "Exponential and logarithmic models",
                        _alg_lesson(
                            "Compound interest, population, cooling, and pH are classic exponential/log models.",
                            "Identify A0, rate, and time. For doubling, set A = 2 A0 and solve for t.",
                            "Using the wrong compounding formula, or mixing percent 5 with 5 instead of 0.05.",
                        ),
                        "6-7-exponential-and-logarithmic-models",
                        AP2 + CLEP_P,
                        "ready",
                        "explog_eq",
                        "explog",
                    ),
                    _s(
                        "alg-6-8",
                        "Fitting exponential models to data",
                        _alg_lesson(
                            "Exponential regression finds y = a b^x that best fits data. Semi-log plots can linearize exponential growth.",
                            "If equal x-steps multiply y by a constant, the data is exponential. That constant is the base.",
                            "Fitting a line to data that is clearly curving on a linear scale.",
                        ),
                        "6-8-fitting-exponential-models-to-data",
                        AP2,
                        "ready",
                        "exponential",
                        "explog",
                    ),
                ],
            ),
            Unit(
                id="alg-ch11",
                title="7. Systems of equations and inequalities",
                skills=[
                    _s(
                        "alg-11-1",
                        "Linear systems with two variables",
                        _alg_lesson(
                            "Two lines can meet at one point (unique solution), be parallel (none), or be the same line (infinitely many).",
                            "Substitution or elimination. Elimination: multiply so a pair of coefficients match, then add/subtract.",
                            "Adding equations that do not actually cancel a variable, or forgetting to substitute back to find both values.",
                        ),
                        "11-1-systems-of-linear-equations-two-variables",
                        CLEP_A + CLEP_P,
                        "ready",
                        "system2",
                        "systems",
                    ),
                    _s(
                        "alg-11-2",
                        "Linear systems with three variables",
                        _alg_lesson(
                            "Three planes can meet at a point, a line, or not at all.",
                            "Eliminate one variable at a time to get a 2×2 system, then back-substitute.",
                            "Inconsistent arithmetic on the third variable after finding x and y.",
                        ),
                        "11-2-systems-of-linear-equations-three-variables",
                        CLEP_A,
                        "ready",
                        "system2",
                        "systems",
                    ),
                    _s(
                        "alg-11-3",
                        "Nonlinear systems",
                        _alg_lesson(
                            "A line and a circle can meet 0, 1, or 2 times. Substitution is the usual path.",
                            "Solve the simpler equation for one variable, substitute, then check both coordinates in both originals.",
                            "Keeping an algebraic solution that does not lie on the circle because of a sign error.",
                        ),
                        "11-3-systems-of-nonlinear-equations-and-inequalities-two-variables",
                        CLEP_P,
                        "ready",
                        "system2",
                        "systems",
                    ),
                    _s(
                        "alg-11-4",
                        "Partial fractions",
                        _alg_lesson(
                            "Partial fractions undo adding rational expressions. Needed later in Calc 2, but the algebra is college algebra.",
                            "Factor the denominator. For distinct linear factors, write A/(x-r) + B/(x-s), clear denominators, solve for A, B.",
                            "Using a single A for a repeated factor (x-r)^2, which needs A/(x-r) + B/(x-r)^2.",
                        ),
                        "11-4-partial-fractions",
                        CLEP_P,
                        "ready",
                        "partial",
                        "systems",
                    ),
                ],
            ),
            Unit(
                id="alg-ch13",
                title="8. Sequences, series, counting, probability",
                skills=[
                    _s(
                        "alg-13-1",
                        "Sequences",
                        _alg_lesson(
                            "A sequence is a function whose domain is positive integers. a_n is the nth term.",
                            "To find a_n from a formula, plug in n. Recursive sequences need the previous term.",
                            "Off-by-one errors: a_1 is the first term, not a_0, unless the formula is written that way.",
                        ),
                        "13-1-sequences-and-their-notations",
                        CLEP_A,
                        "ready",
                        "sequence",
                        "sequences",
                    ),
                    _s(
                        "alg-13-2",
                        "Arithmetic sequences",
                        _alg_lesson(
                            "Constant difference d. a_n = a_1 + (n-1)d.",
                            "Find d from two terms, then write the formula or the requested term.",
                            "Using n d instead of (n-1)d.",
                        ),
                        "13-2-arithmetic-sequences",
                        AP2 + CLEP_A,
                        "ready",
                        "arithmetic_seq",
                        "sequences",
                    ),
                    _s(
                        "alg-13-3",
                        "Geometric sequences",
                        _alg_lesson(
                            "Constant ratio r. a_n = a_1 r^{n-1}.",
                            "Divide a later term by an earlier term to get r (raised to the right power).",
                            "Using r^n instead of r^{n-1}.",
                        ),
                        "13-3-geometric-sequences",
                        AP2 + CLEP_A,
                        "ready",
                        "geometric_seq",
                        "sequences",
                    ),
                    _s(
                        "alg-13-4",
                        "Series",
                        _alg_lesson(
                            "A series adds sequence terms. Arithmetic sum S_n = n(a_1 + a_n)/2. Geometric S_n = a_1 (1-r^n)/(1-r) for r ≠ 1.",
                            "Identify arithmetic vs geometric first, then pick the matching sum formula.",
                            "Summing with the sequence formula, or using infinite geometric sum when |r| ≥ 1.",
                        ),
                        "13-4-series-and-their-notations",
                        CLEP_A,
                        "ready",
                        "series",
                        "sequences",
                    ),
                    _s(
                        "alg-13-5",
                        "Counting principles",
                        _alg_lesson(
                            "nPr = n! / (n-r)! (order matters). nCr = n! / (r!(n-r)!) (order does not).",
                            "Ask: does rearranging the same items count as a new outcome? If yes, permutation.",
                            "Using combinations for PINs or lock combinations that actually care about order.",
                        ),
                        "13-5-counting-principles",
                        CLEP_A,
                        "ready",
                        "counting",
                        "sequences",
                    ),
                    _s(
                        "alg-13-6",
                        "Binomial theorem",
                        _alg_lesson(
                            "(a+b)^n = Σ C(n,k) a^{n-k} b^k. The kth term uses those powers.",
                            "The term with b^k has coefficient C(n,k) and a to the power n-k.",
                            "Forgetting the binomial coefficient, or swapping the exponents.",
                        ),
                        "13-6-binomial-theorem",
                        CLEP_A,
                        "ready",
                        "binomial",
                        "sequences",
                    ),
                    _s(
                        "alg-13-7",
                        "Probability",
                        _alg_lesson(
                            "P = (favorable outcomes) / (equally likely outcomes) for a uniform sample space.",
                            "Count carefully with combinations when order does not matter. Complement: P(not A) = 1 - P(A).",
                            "Adding probabilities of overlapping events without subtracting the overlap.",
                        ),
                        "13-7-probability",
                        CLEP_A,
                        "ready",
                        "probability",
                        "sequences",
                    ),
                ],
            ),
        ],
    ),
    Course(
        id="trig",
        title="Trigonometry",
        blurb="A complete trigonometry course: angles, the unit circle, graphs, identities, triangles, then polar, parametric, and vectors.",
        units=[
            Unit(
                id="trig-ch7",
                title="1. Angles, triangles, and the unit circle",
                skills=[
                    _s("trig-7-1", "Angles (degrees and radians)", _alg_lesson("π radians = 180°. Calculus uses radians.", "Degrees to radians: multiply by π/180 and reduce. Radians to degrees: multiply by 180/π.", "Using 180/π when converting to radians, or leaving an unreduced fraction like 150π/180."), "7-1-angles", AP3, "ready", "deg_to_rad", "trig"),
                    _s("trig-7-2", "Right triangle trigonometry", _alg_lesson("SOH-CAH-TOA names the three primary ratios.", "Sine = opp/hyp, cosine = adj/hyp, tangent = opp/adj.", "Swapping opposite and adjacent."), "7-2-right-triangle-trigonometry", AP3, "ready", "right_triangle", "trig"),
                    _s("trig-7-3", "The unit circle", _alg_lesson("On the unit circle, cosine is x and sine is y. Memorize the 0-30-45-60-90 family and quadrant signs.", "Find the reference angle, take the chart value, then attach the ASTC sign.", "A correct absolute value with the wrong quadrant sign."), "7-3-unit-circle", AP3, "ready", "unit_circle", "trig"),
                    _s("trig-7-4", "The other trigonometric functions", _alg_lesson("Both directions of each pair: tan = sin/cos = 1/cot, cot = cos/sin = 1/tan, sec = 1/cos and cos = 1/sec, csc = 1/sin and sin = 1/csc.", "Build them from unit-circle sine and cosine rather than a new chart. On the unit circle, tan = y/x, cot = x/y, sec = 1/x, csc = 1/y.", "Dividing in the wrong order, or using a reciprocal of the wrong function (csc is 1/sin, not 1/cos)."), "7-4-the-other-trigonometric-functions", AP3, "ready", "other_trig", "trig"),
                    _s("trig-7-5", "Arc length and area of a sector", _alg_lesson("θ must be in radians: arc length s = rθ and sector area A = (1/2) r² θ.", "Convert to radians first if the angle is in degrees, then multiply.", "Using the degree measure of θ in s = rθ, which is off by a factor of π/180."), "7-1-angles", AP3, "ready", "arc_length", "trig"),
                    _s("trig-7-6", "Coterminal angles", _alg_lesson("Coterminal angles share a terminal side. You get them by adding or subtracting full turns (360° or 2π).", "Add or subtract 360° (or 2π) until the angle sits in the requested interval, usually [0, 360) or [0, 2π).", "Stopping at a negative angle when the question asked for the coterminal angle in [0, 360)."), "7-1-angles", AP3, "ready", "coterminal", "trig"),
                    _s("trig-7-7", "Linear and angular speed", _alg_lesson("Angular speed ω is radians per unit time. Linear speed along the rim is v = rω.", "ω = θ/t with θ in radians. Then v = rω if you need distance per time along the circle.", "Mixing revolutions with radians, or using v = rθ instead of v = rω."), "7-1-angles", AP3, "ready", "angular_speed", "trig"),
                    _s("trig-7-8", "Applications of right triangles", _alg_lesson("Angle of elevation is up from horizontal; angle of depression is down from horizontal. They are equal if the lines are parallel.", "Draw the right triangle, label opposite/adjacent, then use tan (or sin/cos) of the given angle.", "Putting the height on the adjacent side, or using sine when the known pair is opposite and adjacent (that's tangent)."), "7-2-right-triangle-trigonometry", AP3, "ready", "elevation", "trig"),
                    _s("trig-7-9", "Cofunction identities", _alg_lesson("Complementary angles swap sine with cosine: sin(π/2 − x) = cos x, and tan(π/2 − x) = cot x.", "π/2 − x (or 90° − θ) is the complement. Replace the pair and drop the complement.", "Writing sin(π/2 − x) = sin x, which ignores that cofunctions are different functions."), "7-2-right-triangle-trigonometry", AP3, "ready", "cofunction", "trig"),
                ],
            ),
            Unit(
                id="trig-ch8",
                title="2. Periodic functions",
                skills=[
                    _s("trig-8-1", "Graphs of sine and cosine", _alg_lesson("Amplitude is |A|; period of sin(bx) is 2π/|b|.", "Read A and b from y = A sin(bx + φ) + k. Midline is y = k.", "Using 2π·b for the period, or treating amplitude as signed."), "8-1-graphs-of-the-sine-and-cosine-functions", AP3, "ready", "period_amp", "trig"),
                    _s("trig-8-2", "Graphs of the other trig functions", _alg_lesson("Tangent and cotangent both have period π: tan(θ + πn) = tan(θ) and cot(θ + πn) = cot(θ). Vertical asymptotes where the denominator is 0 (cos = 0 for tan, sin = 0 for cot).", "Period of tan(bx) or cot(bx) is π/|b|, not 2π/|b|. Sine, cosine, secant, and cosecant use 2π/|b|.", "Graphing tan as a sine wave with amplitude 1, or using the sine period 2π on cotangent."), "8-2-graphs-of-the-other-trigonometric-functions", AP3, "ready", "tan_period", "trig"),
                    _s("trig-8-3", "Inverse trigonometric functions", _alg_lesson("Paul’s Inverse Trig Functions, copied exactly. Definition: y = sin⁻¹(x) is equivalent to x = sin(y); y = cos⁻¹(x) is equivalent to x = cos(y); y = tan⁻¹(x) is equivalent to x = tan(y). Domain and Range — Function y = sin⁻¹(x), Domain −1 ≤ x ≤ 1, Range −π/2 ≤ y ≤ π/2; Function y = cos⁻¹(x), Domain −1 ≤ x ≤ 1, Range 0 ≤ y ≤ π; Function y = tan⁻¹(x), Domain −∞ < x < ∞, Range −π/2 < y < π/2. Inverse properties: cos(cos⁻¹(x)) = x, cos⁻¹(cos(θ)) = θ, sin(sin⁻¹(x)) = x, sin⁻¹(sin(θ)) = θ, tan(tan⁻¹(x)) = x, tan⁻¹(tan(θ)) = θ. Alternate notation: sin⁻¹(x) = arcsin(x), cos⁻¹(x) = arccos(x), tan⁻¹(x) = arctan(x).", "Ask which unique y in that function’s range has this sine, cosine, or tangent. Example: cos⁻¹(0) is π/2, not 0, because cos(π/2) = 0 while cos(0) = 1.", "Reading sin⁻¹(x) as 1/sin(x). Also picking 3π/2 for cos⁻¹(0) because cosine is 0 there too — 3π/2 is outside 0 ≤ y ≤ π, so cos⁻¹ will not choose it."), "8-3-inverse-trigonometric-functions", AP3, "ready", "inverse_trig", "trig"),
                    _s("trig-8-4", "Phase shift and midline", _alg_lesson("y = A sin(b(x − h)) + k is shifted right by h and up by k. The midline is y = k.", "Factor b out of the angle if needed so the shift is the number subtracted from x, not from bx.", "Calling the phase shift φ when the form is sin(bx − φ). The actual x-shift is φ/b."), "8-1-graphs-of-the-sine-and-cosine-functions", AP3, "ready", "phase_shift", "trig"),
                    _s("trig-8-5", "Modeling with sinusoids", _alg_lesson("A cosine or sine of time is simple harmonic motion and also an AC waveform: y = A cos(2π f t) + k.", "Period T = 2π/|ω| if the inside is ωt. Frequency f = 1/T (cycles per unit time).", "Using 2π/T as the period instead of T, or mixing frequency with angular frequency ω = 2πf."), "8-1-graphs-of-the-sine-and-cosine-functions", AP3, "ready", "sinusoid_model", "trig"),
                ],
            ),
            Unit(
                id="trig-ch9",
                title="3. Identities and equations",
                skills=[
                    _s("trig-9-1", "Verifying and simplifying identities", _alg_lesson("Start from definitions and Pythagorean identities, not from a calculator.", "Rewrite everything in sin and cos, then cancel or use sin²+cos²=1.", "Treating 1/sin as cos."), "9-1-solving-trigonometric-equations-with-identities", AP3, "ready", "identity_simplify", "trig"),
                    _s("trig-9-2", "Sum and difference identities", _alg_lesson("sin(a+b) = sin a cos b + cos a sin b, and cyclic companions.", "Split a non-chart angle into two chart angles (75 = 45+30).", "Using the cosine-sum minus sign on a sine sum."), "9-2-sum-and-difference-identities", AP3, "ready", "sum_diff", "trig"),
                    _s("trig-9-3", "Double-angle, half-angle, and reduction", _alg_lesson("sin(2θ)=2 sin θ cos θ. cos(2θ) has three useful forms.", "Find the missing of sin/cos from Pythagoras, then plug into the double-angle formula.", "Doubling the sine instead of using the formula."), "9-3-double-angle-half-angle-and-reduction-formulas", AP3, "ready", "double_angle", "trig"),
                    _s("trig-9-4", "Product-to-sum formulas", _alg_lesson("Products of sines and cosines become sums, which is how you integrate them later.", "2 sin A sin B = cos(A-B) - cos(A+B). Same-angle case is power-reduction.", "Leaving 2 sin² x instead of 1-cos(2x) when asked for a cosine form."), "9-4-sum-to-product-and-product-to-sum-formulas", AP3, "ready", "product_sum", "trig"),
                    _s("trig-9-5", "Solving trigonometric equations", _alg_lesson("Find the reference angle, then list every matching quadrant on one period.", "For sin x = k there are usually two solutions in [0, 2π).", "Reporting only the calculator's principal value."), "9-5-solving-trigonometric-equations", AP3, "ready", "solve_trig", "trig"),
                    _s("trig-9-6", "Half-angle formulas", _alg_lesson("cos²(θ/2) = (1 + cos θ)/2 and sin²(θ/2) = (1 − cos θ)/2. Square roots need a quadrant choice.", "First get cos θ (Pythagoras if needed), then plug into the half-angle identity. If the question asks for a square, skip the root.", "Taking the square root and dropping the ±, or using 1 − cos when you wanted 1 + cos."), "9-3-double-angle-half-angle-and-reduction-formulas", AP3, "ready", "half_angle", "trig"),
                ],
            ),
            Unit(
                id="trig-ch10",
                title="4. Further applications",
                skills=[
                    _s("trig-10-1", "Law of Sines", _alg_lesson("The full three-way form is sin(α)/a = sin(β)/b = sin(γ)/c, same as a/sin A = b/sin B = c/sin C. Two angles already determine the third.", "If you know two angles, use 180° first. Then Law of Sines for a missing side.", "SSA (the ambiguous case) can produce 0, 1, or 2 triangles."), "10-1-non-right-triangles-law-of-sines", AP3, "ready", "law_sines", "trig"),
                    _s("trig-10-2", "Law of Cosines", _alg_lesson("All three cyclic forms: a² = b² + c² − 2bc cos α, b² = a² + c² − 2ac cos β, c² = a² + b² − 2ab cos γ. Pythagoras is the right-angle special case (the cosine term vanishes).", "Use SAS or SSS. Pick the form whose left side is the side you want, opposite the known included angle.", "Using Law of Sines when you have two sides and the included angle (that's SAS, so use cosines)."), "10-2-non-right-triangles-law-of-cosines", AP3, "ready", "law_cosines", "trig"),
                    _s("trig-10-3", "Area of a triangle", _alg_lesson("Area = (1/2) ab sin C, using the included angle between sides a and b. The same cheat sheet also lists Law of Tangents, (a−b)/(a+b) = tan(½(α−β))/tan(½(α+β)) and the two cyclic companions on (b,c) and (a,c), plus Mollweide’s formula (a+b)/c = cos(½(α−β))/sin(½ γ).", "If C = 90°, area is the usual (1/2) base × height. Otherwise keep the sine of the included angle. Tangents and Mollweide are check identities after you solve a triangle.", "Using the non-included angle, or dropping the 1/2."), "10-1-non-right-triangles-law-of-sines", AP3, "ready", "triangle_area", "trig"),
                    _s("trig-10-4", "Ambiguous case (SSA)", _alg_lesson("SSA is the only triangle setup that can give 0, 1, or 2 triangles. Compare side a with height h = b sin A.", "If a < h: none. If a = h: one right triangle. If h < a < b and A is acute: two. If a ≥ b: one.", "Assuming SSA always makes a unique triangle the way ASA and SAS do."), "10-1-non-right-triangles-law-of-sines", AP3, "ready", "ssa_ambiguous", "trig"),
                ],
            ),
        ],
    ),
    Course(
        id="precalc",
        title="Precalculus extras",
        blurb="Topics that sit on top of functions and trig: polar, parametric, vectors, matrices, conics, and limits.",
        units=[
            Unit(
                id="pc-polar",
                title="1. Polar, parametric, and vectors",
                skills=[
                    _s("pc-10-3", "Polar coordinates", _alg_lesson("x = r cos θ, y = r sin θ. r is distance from the origin.", "Plug the given r and θ into those two formulas.", "Swapping sine and cosine, or losing the sign on π or 3π/2."), "10-3-polar-coordinates", AP3, "ready", "polar_coords", "precalc"),
                    _s("pc-10-4", "Polar graphs", _alg_lesson("r = a is a circle about the pole. r = a cos θ is a circle through the origin.", "Translate the equation into a sentence about distance or an x/y identity.", "Mixing r = a with r = 2a cos θ (different radii)."), "10-4-polar-coordinates-graphs", AP3, "ready", "polar_graphs", "precalc"),
                    _s("pc-10-5", "Polar form of complex numbers", _alg_lesson("|a+bi| = √(a²+b²) is the r in r(cos θ + i sin θ).", "Modulus first, then θ = atan2(b, a).", "Adding a+b instead of using Pythagoras."), "10-5-polar-form-of-complex-numbers", AP3 + AP4, "ready", "polar_complex", "precalc"),
                    _s("pc-10-6", "Parametric equations", _alg_lesson("x(t) and y(t) give a point for each t. Evaluate one coordinate at a time.", "To find x at a given t, use only the x-equation.", "Eliminating t when the question only asked for a snapshot."), "10-6-parametric-equations", AP4, "ready", "parametric", "precalc"),
                    _s("pc-10-7", "Parametric graphs", _alg_lesson("Eliminate t, or recognize x=cos t, y=sin t as the unit circle.", "Square and add when you see sine and cosine of the same t.", "Calling the period 2π the radius."), "10-7-parametric-equations-graphs", AP4, "ready", "parametric_graph", "precalc"),
                    _s("pc-10-8", "Vectors", _alg_lesson("Magnitude is length: √(a²+b²). Direction is a separate idea.", "Treat the components as legs of a right triangle.", "Reporting a negative magnitude, or adding the components."), "10-8-vectors", AP4, "ready", "vectors", "precalc"),
                ],
            ),
            Unit(
                id="pc-matrices",
                title="2. Matrices",
                skills=[
                    _s("pc-11-5", "Matrix operations", _alg_lesson("Addition is entrywise. (i,j) of A+B is a_ij + b_ij.", "Match positions: top-left with top-left.", "Multiplying entries when the question asked for a sum."), "11-5-matrices-and-matrix-operations", AP4 + CLEP_A, "ready", "matrix_ops", "precalc"),
                    _s("pc-11-6", "Gaussian elimination", _alg_lesson("Row operations produce an equivalent triangular system.", "Back-substitute from the last row up.", "Changing the solution by an arithmetic slip on one row."), "11-6-solving-systems-with-gaussian-elimination", AP4, "ready", "gaussian", "precalc"),
                    _s("pc-11-7", "Inverse matrices", _alg_lesson("A 2×2 matrix is invertible iff ad-bc ≠ 0.", "det = ad-bc. Inverse is (1/det) [[d,-b],[-c,a]].", "Using ad+bc for the determinant."), "11-7-solving-systems-with-inverses", AP4, "ready", "inverse_matrix", "precalc"),
                    _s("pc-11-8", "Cramer's rule", _alg_lesson("Each variable is a ratio of determinants: x = det A_x / det A.", "For 2×2, adding to eliminate is often faster and must match Cramer.", "Swapping which column you replace, which swaps x and y."), "11-8-solving-systems-with-cramers-rule", AP4, "ready", "cramer", "precalc"),
                ],
            ),
            Unit(
                id="pc-conics",
                title="3. Analytic geometry",
                skills=[
                    _s("pc-12-1", "The ellipse", _alg_lesson("x²/a² + y²/b² = 1. Vertices at (±a,0) and (0,±b).", "The denominator under x² is a²; take the square root for the semi-axis.", "Reporting a² as the axis length."), "12-1-the-ellipse", CLEP_P, "ready", "ellipse", "precalc"),
                    _s("pc-12-2", "The hyperbola", _alg_lesson("The squared term with the plus sign is the direction the hyperbola opens.", "x² - y² form opens left-right; y² - x² opens up-down.", "Using ellipse major-axis rules on a hyperbola."), "12-2-the-hyperbola", CLEP_P, "ready", "hyperbola", "precalc"),
                    _s("pc-12-3", "The parabola (conic)", _alg_lesson("y = x²/(4p) has vertex at the origin and focus (0,p).", "Read 4p from the coefficient, then p is the focus distance.", "Putting the focus at 4p instead of p."), "12-3-the-parabola", CLEP_P, "ready", "parabola_conic", "precalc"),
                    _s("pc-12-4", "Rotation of axes", _alg_lesson("A Bxy term means the conic is tilted relative to the coordinate axes.", "If B ≠ 0, a rotation is needed to eliminate xy.", "Ignoring xy because the rest looks like an aligned ellipse."), "12-4-rotation-of-axes", CLEP_P, "ready", "rotation_axes", "precalc"),
                    _s("pc-12-5", "Conics in polar coordinates", _alg_lesson("Eccentricity: e<1 ellipse, e=1 parabola, e>1 hyperbola.", "Read e from r = ed/(1-e cos θ) or from a stated value.", "Calling e=1 a circle. A circle is e=0."), "12-5-conic-sections-in-polar-coordinates", AP3 + CLEP_P, "ready", "polar_conic", "precalc"),
                ],
            ),
            Unit(
                id="pc-limits",
                title="4. Introduction to limits (Calc 1 on-ramp)",
                skills=[
                    _s(
                        "pc-limit-1",
                        "Limits numerically and graphically",
                        _alg_lesson("A limit is the height the graph approaches, even if there is a hole.", "Factor or use a table near the missing x-value. 0/0 is not the answer.", "Saying the limit DNE just because f(a) is undefined."),
                        "12-1-finding-limits-numerical-and-graphical-approaches",
                        CLEP_P,
                        "ready",
                        "limit_numeric",
                        "limits",
                        book="pc",
                    ),
                    _s(
                        "pc-limit-2",
                        "Limits algebraically",
                        _alg_lesson("Substitute first. If you get 0/0, factor, cancel, then substitute again.", "Difference of squares is the most common cancel in this course.", "Canceling terms instead of factors."),
                        "12-2-finding-limits-properties-of-limits",
                        CLEP_P,
                        "ready",
                        "limit_algebra",
                        "limits",
                        book="pc",
                    ),
                    _s(
                        "pc-limit-3",
                        "Continuity",
                        _alg_lesson("Continuous at a means f(a) exists, the limit exists, and they match.", "A hole is a discontinuity even when the limit exists.", "Calling a removable hole continuous because nearby points behave well."),
                        "12-3-continuity",
                        CLEP_P,
                        "ready",
                        "continuity",
                        "limits",
                        book="pc",
                    ),
                ],
            ),
        ],
    ),
    Course(
        id="physics",
        title="Physics 1 & 2",
        blurb=(
            "Algebra-based intro physics at AP Physics 1 and AP Physics 2 level "
            "(same depth as a one-year college sequence). Mechanics, waves, and DC circuits "
            "in Physics 1; fluids, thermo, E&M, optics, and photons in Physics 2."
        ),
        units=[
            Unit(
                id="phy-kin",
                title="P1. Kinematics",
                skills=[
                    _phy("phy-1-1", "Average velocity", _phy_lesson("Average velocity is displacement over time, Δx/Δt, including sign.", "Subtract initial position from final, then divide by the elapsed time.", "Using path length (distance) when the motion reversed."), "2-3-time-velocity-and-speed", AP_P1, "phy_avg_motion", "kinematics"),
                    _phy("phy-1-2", "Constant-acceleration equations", _phy_lesson("v = v₀ + at and Δx = v₀t + (1/2)at² only when a is constant.", "List v₀, a, t, Δx, v. Pick the equation that contains the unknown and the three knowns.", "Mixing in a Δx formula when Δx was never given."), "2-5-motion-equations-for-constant-acceleration-in-one-dimension", AP_P1, "phy_kinematics", "kinematics"),
                    _phy("phy-1-3", "Free fall", _phy_lesson("Dropped means v₀ = 0 and a = g. Thrown up means v₀ > 0 if up is positive.", "Use the same kinematics equations with a = ±g. These drills take g = 10 m/s².", "Using v = gt for a drop but forgetting the 1/2 in Δy = (1/2)gt²."), "2-7-falling-objects", AP_P1, "phy_freefall", "kinematics"),
                    _phy("phy-1-4", "Projectile motion", _phy_lesson("Split into x (a_x = 0) and y (a_y = −g). Time is shared.", "At 45° from level ground, range = v²/g. Otherwise use v_x = v cosθ and hang time from v_y.", "Treating the launch speed as only vertical, or using a_x = g."), "3-4-projectile-motion", AP_P1, "phy_projectile", "kinematics"),
                ],
            ),
            Unit(
                id="phy-force",
                title="P1. Newton's laws",
                skills=[
                    _phy("phy-2-1", "Newton's second law", _phy_lesson("ΣF = ma. a is caused by the net force, not by 'being in motion'.", "Draw a free-body diagram, add components, then a = F_net / m.", "Using a single force instead of the net force, or setting F = m v."), "4-3-newtons-second-law-of-motion-concept-of-a-system", AP_P1, "phy_n2", "forces"),
                    _phy("phy-2-2", "Kinetic friction", _phy_lesson("f_k = μ_k N. N is the normal force, which equals mg only on a horizontal surface with no other vertical forces.", "Read N from the free-body diagram, then multiply by μ_k. Direction opposes sliding.", "Using μ mg when N was already given, or using static friction on a sliding object."), "5-1-friction", AP_P1, "phy_friction", "forces"),
                    _phy("phy-2-3", "Weight and the normal force", _phy_lesson("Weight is mg, a force. Mass is kg. At rest on a table, n = mg because a = 0, not because they are a Newton-3 pair.", "ΣF_y = 0 at rest, so n = mg if those are the only vertical forces.", "Reporting mass as if it were a force, or saying n and mg are 'equal and opposite by Newton 3'."), "4-7-further-applications-of-newtons-laws-of-motion", AP_P1, "phy_weight", "forces"),
                ],
            ),
            Unit(
                id="phy-energy",
                title="P1. Energy",
                skills=[
                    _phy("phy-3-1", "Work by a constant force", _phy_lesson("W = Fd cosθ. Only the component along the displacement does work.", "θ = 0° means W = Fd. θ = 90° means W = 0.", "Putting mass into W = Fd, or using the force's magnitude times a perpendicular distance (that is torque)."), "7-1-work-the-scientific-definition", AP_P1, "phy_work", "energy"),
                    _phy("phy-3-2", "Kinetic energy", _phy_lesson("K = (1/2)mv². Twice the speed is four times the kinetic energy.", "Square v first, then multiply by m/2.", "Doing (1/2)(mv)² or dropping the 1/2."), "7-2-kinetic-energy-and-the-work-energy-theorem", AP_P1, "phy_ke_pe", "energy"),
                    _phy("phy-3-3", "Conservation of mechanical energy", _phy_lesson("If only gravity (or a spring) does work, K + U is constant. mgh at rest becomes (1/2)mv² at the bottom.", "Set E_top = E_bottom. Mass usually cancels. These drills use g = 10 m/s².", "Using kinematics with a missing time, or conserving energy when friction is doing work."), "7-6-conservation-of-energy", AP_P1, "phy_energy_cons", "energy"),
                ],
            ),
            Unit(
                id="phy-mom",
                title="P1. Momentum",
                skills=[
                    _phy("phy-4-1", "Impulse and Δp", _phy_lesson("Impulse J = F_net Δt = Δp. Units N·s = kg·m/s.", "For a constant net force, multiply F by the time it acts.", "Reporting F as the impulse, or dividing F by t."), "8-1-linear-momentum-and-force", AP_P1, "phy_impulse", "momentum"),
                    _phy("phy-4-2", "Inelastic collisions", _phy_lesson("Sticking together is perfectly inelastic: momentum conserved, K not conserved. m1 v1 = (m1+m2)v if the target starts at rest.", "Write p_before = p_after. Do not set kinetic energies equal.", "Averaging the two speeds, or using the elastic-collision shortcuts."), "8-5-inelastic-collisions-in-one-dimension", AP_P1, "phy_collision", "momentum"),
                ],
            ),
            Unit(
                id="phy-circle",
                title="P1. Circular motion, gravity, torque",
                skills=[
                    _phy("phy-5-1", "Centripetal acceleration", _phy_lesson("Uniform circular motion: speed constant, direction changing, a_c = v²/r toward the center.", "Square the speed, divide by the radius. The net force is m a_c inward.", "Calling this tangential acceleration (that would change the speed) or using a = v/r."), "6-2-centripetal-acceleration", AP_P1, "phy_centripetal", "circular"),
                    _phy("phy-5-2", "Surface gravity and Newton's law of gravity", _phy_lesson("g = GM/R². Same mass and twice the radius means g is four times smaller.", "Scale g by 1/(radius factor)² when M is unchanged.", "Scaling g by 1/R instead of 1/R²."), "6-5-newtons-universal-law-of-gravitation", AP_P1, "phy_gravity", "circular"),
                    _phy("phy-5-3", "Torque", _phy_lesson("τ = r F sinθ. Perpendicular force means τ = rF. Equilibrium needs Στ = 0 as well as ΣF = 0.", "Measure r from the pivot to the point of application. Use the perpendicular component of F.", "Adding r and F, or using a force along the lever arm (that torque is zero)."), "9-2-the-second-condition-for-equilibrium", AP_P1, "phy_torque", "circular"),
                ],
            ),
            Unit(
                id="phy-osc",
                title="P1. Oscillations, waves, and DC circuits",
                skills=[
                    _phy("phy-6-1", "Mass-spring period", _phy_lesson("T = 2π√(m/k). Amplitude does not appear. A stiffer spring (bigger k) oscillates faster.", "Form m/k, take the square root, multiply by 2π.", "Using √(k/m), or thinking a bigger pull-back makes a longer period."), "16-3-simple-harmonic-motion-a-special-periodic-motion", AP_P1, "phy_shm", "waves"),
                    _phy("phy-6-2", "Wave speed v = fλ", _phy_lesson("v = fλ for any periodic wave. v is set by the medium; f is set by the source.", "Multiply frequency in Hz by wavelength in meters to get m/s.", "Adding f and λ, or mixing this v with the SHM speed of a single particle."), "16-9-waves", AP_P1, "phy_wave", "waves"),
                    _phy("phy-7-1", "Ohm's law", _phy_lesson("I = V/R. Current through a resistor equals the voltage across it divided by R.", "In a single-resistor circuit the resistor sees the full battery voltage.", "Using I = VR, or confusing current with voltage."), "20-2-ohms-law-resistance-and-simple-circuits", AP_P12, "phy_ohm", "circuits"),
                ],
            ),
            Unit(
                id="phy-fluids",
                title="P2. Fluids and thermodynamics",
                skills=[
                    _phy("phy-8-1", "Pressure P = F/A", _phy_lesson("Pressure is force per area. 1 Pa = 1 N/m². Same force on a smaller area is more pressure.", "Divide the perpendicular force by the area.", "Using F·A, or jumping to ρgh when no depth was given."), "11-3-pressure", AP_P2, "phy_pressure", "fluids"),
                    _phy("phy-8-2", "Buoyancy", _phy_lesson("Archimedes: F_b = ρ_fluid V_displaced g. Fully submerged means V_displaced = V_object.", "Use the fluid's density, not the object's, unless you are comparing to weight.", "Dropping g so the answer has the wrong units, or using the object's density in F_b."), "11-7-archimedes-principle", AP_P2, "phy_buoyancy", "fluids"),
                    _phy("phy-8-3", "Continuity of flow", _phy_lesson("Incompressible: A1 v1 = A2 v2. Narrower pipe means faster flow.", "Solve v2 = A1 v1 / A2. Bernoulli then says faster means lower pressure.", "Thinking water slows down in a constriction."), "12-1-flow-rate-and-its-relation-to-velocity", AP_P2, "phy_continuity", "fluids"),
                    _phy("phy-9-1", "Ideal gas at constant volume", _phy_lesson("PV = nRT. At fixed V and n, P is proportional to Kelvin temperature.", "P2 = P1 (T2/T1) with T in kelvin. Doubling °C is not doubling T.", "Using Celsius in the ratio, or thinking pressure is independent of T at constant V."), "13-3-the-ideal-gas-law", AP_P2, "phy_ideal_gas", "thermo"),
                    _phy("phy-9-2", "First law of thermodynamics", _phy_lesson("With W = work by the gas, ΔU = Q − W. Heat in raises U; expansion work lowers U.", "Assign signs, then subtract. These drills use that OpenStax / AP sign convention.", "Adding Q and W, or flipping W without saying whether it is by or on the system."), "15-1-the-first-law-of-thermodynamics", AP_P2, "phy_first_law", "thermo"),
                ],
            ),
            Unit(
                id="phy-em",
                title="P2. Electricity and magnetism",
                skills=[
                    _phy("phy-10-1", "Coulomb's law", _phy_lesson("F = k |q1 q2| / r². Convert μC to C (×10⁻⁶) before substituting k = 9×10⁹.", "Square the charges' product, divide by r², multiply by k. Same signs repel.", "Leaving charges in μC, or using r instead of r²."), "18-3-coulombs-law", AP_P2, "phy_coulomb", "electro"),
                    _phy("phy-10-2", "Electric field and force", _phy_lesson("E is force per charge. F = qE once the field is known.", "Multiply q in coulombs by E in N/C. Direction follows E for a positive charge.", "Using Coulomb's law with no source distance given, or dividing E by q."), "18-4-electric-field-concept-of-a-field-revisited", AP_P2, "phy_efield", "electro"),
                    _phy("phy-11-1", "Series and parallel resistors", _phy_lesson("Series: R_eq = R1+R2 (bigger). Parallel: 1/R_eq = 1/R1+1/R2 (smaller than either).", "Identify the connection first. Parallel of 6 Ω and 3 Ω is 2 Ω.", "Adding parallel resistors as if they were in series."), "21-1-resistors-in-series-and-parallel", AP_P12, "phy_req", "circuits"),
                    _phy("phy-12-1", "Magnetic force on a moving charge", _phy_lesson("F = qvB sinθ. Perpendicular v and B means sin 90° = 1. Parallel means F = 0.", "Multiply q v B for the perpendicular case. Right-hand rule for direction.", "Using F = qE, or putting sin 0° when the problem said perpendicular."), "22-5-force-on-a-moving-charge-in-a-magnetic-field", AP_P2, "phy_magnetic", "magnetism"),
                ],
            ),
            Unit(
                id="phy-opt",
                title="P2. Optics and modern physics",
                skills=[
                    _phy("phy-13-1", "Snell's law", _phy_lesson("n1 sinθ1 = n2 sinθ2. Angles are from the normal. Bigger n means smaller θ.", "Solve for sinθ2 = n1 sinθ1 / n2. sin 30° = 1/2 is the usual AP value.", "Dropping the sines and setting n1 θ1 = n2 θ2."), "25-3-the-law-of-refraction", AP_P2, "phy_snell", "optics"),
                    _phy("phy-13-2", "Thin converging lens", _phy_lesson("1/f = 1/d_o + 1/d_i. Positive d_i is a real image on the far side of a converging lens.", "Compute 1/d_i = 1/f − 1/d_o, then invert. Keep all distances in the same unit.", "Adding f and d_o without taking reciprocals."), "25-6-image-formation-by-lenses", AP_P2, "phy_lens", "optics"),
                    _phy("phy-14-1", "Photon energy", _phy_lesson("A photon has E = hf = hc/λ. In eV with λ in nm, E = 1240/λ.", "Divide 1240 by the wavelength in nanometers. If E > work function, photoelectrons can leave.", "Multiplying 1240 by λ, or mixing meters with the 1240 eV·nm shortcut."), "29-2-the-photoelectric-effect", AP_P2, "phy_photon", "modern"),
                ],
            ),
        ],
    ),
]


def all_skills() -> list[Skill]:
    skills: list[Skill] = []
    for course in COURSES:
        for unit in course.units:
            skills.extend(unit.skills)
    return skills


def skill_by_id(skill_id: str) -> Skill | None:
    for skill in all_skills():
        if skill.id == skill_id:
            return skill
    return None


def course_for_skill(skill_id: str) -> Course | None:
    for course in COURSES:
        for unit in course.units:
            for skill in unit.skills:
                if skill.id == skill_id:
                    return course
    return None


@dataclass
class TrackUnit:
    id: str
    title: str
    skill_ids: list[str]


@dataclass
class Track:
    id: str
    title: str
    blurb: str
    units: list[TrackUnit]


def _unit_skill_ids(course_id: str) -> list[TrackUnit]:
    course = next(c for c in COURSES if c.id == course_id)
    return [TrackUnit(id=u.id, title=u.title, skill_ids=[s.id for s in u.skills]) for u in course.units]


TRACKS: list[Track] = [
    Track(
        id="algebra",
        title="College Algebra",
        blurb="Foundations through functions, polynomials, exponentials, systems, and sequences.",
        units=_unit_skill_ids("algebra"),
    ),
    Track(
        id="trig",
        title="Trigonometry",
        blurb=(
            "A complete trigonometry course: angles and the unit circle, graphs, "
            "identities and equations, oblique triangles, then polar, parametric, "
            "and vectors (OpenStax Chapter 10)."
        ),
        units=_unit_skill_ids("trig")
        + [
            TrackUnit(
                "trig-polar",
                "5. Polar, parametric, and vectors",
                [
                    "pc-10-3",
                    "pc-10-4",
                    "pc-10-5",
                    "pc-10-6",
                    "pc-10-7",
                    "pc-10-8",
                ],
            ),
        ],
    ),
    Track(
        id="precalc",
        title="Precalculus (full course)",
        blurb=(
            "A complete precalculus path: functions, polynomials, exp/log, trigonometry, "
            "polar/parametric, vectors, matrices, conics, sequences, and limits. "
            "This is the AP Precalculus + CLEP Precalculus map, not only the extras."
        ),
        units=[
            TrackUnit(
                "pc-fn",
                "1. Functions (the core of precalculus)",
                [
                    "alg-3-1",
                    "alg-3-2",
                    "alg-3-3",
                    "alg-3-4",
                    "alg-3-5",
                    "alg-3-6",
                    "alg-3-7",
                    "alg-4-1",
                    "alg-4-2",
                    "alg-2-6",
                    "alg-2-7",
                ],
            ),
            TrackUnit(
                "pc-poly",
                "2. Polynomial and rational functions (AP Precalc Unit 1)",
                [
                    "alg-5-1",
                    "alg-5-2",
                    "alg-5-3",
                    "alg-5-4",
                    "alg-5-5",
                    "alg-5-6",
                    "alg-5-7",
                    "alg-5-8",
                    "alg-2-4",
                    "alg-2-5",
                ],
            ),
            TrackUnit(
                "pc-explog",
                "3. Exponential and logarithmic functions (AP Precalc Unit 2)",
                [
                    "alg-6-1",
                    "alg-6-2",
                    "alg-6-3",
                    "alg-6-4",
                    "alg-6-5",
                    "alg-6-6",
                    "alg-6-7",
                    "alg-6-8",
                ],
            ),
            TrackUnit(
                "pc-trig",
                "4. Trigonometry (AP Precalc Unit 3)",
                [
                    "trig-7-1",
                    "trig-7-2",
                    "trig-7-3",
                    "trig-7-4",
                    "trig-7-5",
                    "trig-7-6",
                    "trig-7-7",
                    "trig-7-8",
                    "trig-7-9",
                    "trig-8-1",
                    "trig-8-2",
                    "trig-8-3",
                    "trig-8-4",
                    "trig-8-5",
                    "trig-9-1",
                    "trig-9-2",
                    "trig-9-3",
                    "trig-9-4",
                    "trig-9-5",
                    "trig-9-6",
                    "trig-10-1",
                    "trig-10-2",
                    "trig-10-3",
                    "trig-10-4",
                ],
            ),
            TrackUnit(
                "pc-polar",
                "5. Polar, parametric, and complex form",
                [
                    "pc-10-3",
                    "pc-10-4",
                    "pc-10-5",
                    "pc-10-6",
                    "pc-10-7",
                ],
            ),
            TrackUnit(
                "pc-vecmat",
                "6. Systems, vectors, and matrices (AP Precalc Unit 4)",
                [
                    "alg-11-1",
                    "alg-11-2",
                    "alg-11-3",
                    "alg-11-4",
                    "pc-10-8",
                    "pc-11-5",
                    "pc-11-6",
                    "pc-11-7",
                    "pc-11-8",
                ],
            ),
            TrackUnit(
                "pc-conics",
                "7. Analytic geometry (conics)",
                [
                    "alg-2-1",
                    "pc-12-1",
                    "pc-12-2",
                    "pc-12-3",
                    "pc-12-4",
                    "pc-12-5",
                ],
            ),
            TrackUnit(
                "pc-seq",
                "8. Sequences, series, and the binomial theorem",
                [
                    "alg-13-1",
                    "alg-13-2",
                    "alg-13-3",
                    "alg-13-4",
                    "alg-13-5",
                    "alg-13-6",
                ],
            ),
            TrackUnit(
                "pc-lim",
                "9. Limits and continuity (Calc 1 on-ramp)",
                [
                    "pc-limit-1",
                    "pc-limit-2",
                    "pc-limit-3",
                ],
            ),
        ],
    ),
    Track(
        id="physics",
        title="Physics 1 & 2",
        blurb=(
            "Algebra-based AP Physics 1 (mechanics, waves, DC circuits) and AP Physics 2 "
            "(fluids, thermo, E&M, optics, photons). Same level as a one-year college intro sequence."
        ),
        units=_unit_skill_ids("physics"),
    ),
]


def track_by_id(track_id: str) -> Track | None:
    for track in TRACKS:
        if track.id == track_id:
            return track
    return None


def track_skill_ids(track_id: str) -> set[str]:
    track = track_by_id(track_id)
    if track is None:
        return set()
    return {sid for unit in track.units for sid in unit.skill_ids}


def precalc_skill_ids() -> set[str]:
    return track_skill_ids("precalc")


def physics_skill_ids(*, exam: str | None = None) -> set[str]:
    """exam is 'ap_physics1', 'ap_physics2', or None for both."""
    skills = [s for s in all_skills() if s.id.startswith("phy-")]
    if exam:
        return {s.id for s in skills if exam in s.exam_tags}
    return {s.id for s in skills}


def locate_skill_on_track(
    skill_id: str, preferred_track: str | None = None
) -> tuple[str, str]:
    """Return (track_id, unit_id) for a skill. Prefers the skill's home course."""
    search_order: list[str] = []
    if preferred_track:
        search_order.append(preferred_track)
    if skill_id.startswith("alg-"):
        search_order.extend(["algebra", "precalc", "trig", "physics"])
    elif skill_id.startswith("trig-"):
        search_order.extend(["trig", "precalc", "algebra", "physics"])
    elif skill_id.startswith("phy-"):
        search_order.extend(["physics", "precalc", "algebra", "trig"])
    else:
        search_order.extend(["precalc", "algebra", "trig", "physics"])
    seen: set[str] = set()
    for tid in search_order:
        if tid in seen:
            continue
        seen.add(tid)
        track = track_by_id(tid)
        if track is None:
            continue
        for unit in track.units:
            if skill_id in unit.skill_ids:
                return tid, unit.id
    first = TRACKS[0]
    return first.id, first.units[0].id


TAG_LABELS = {"calc": "Calc 1", "ee": "EE", "me": "ME"}

# High-leverage only. Untagged skills still matter as prerequisites; they are
# just not the ones that show up constantly in Calc 1 or first-year EE/ME.
RELEVANCE: dict[str, tuple[tuple[str, ...], str]] = {
    "alg-1-2": (
        ("calc", "ee", "me"),
        "Power rules and scientific notation show up in every derivative and every unit conversion.",
    ),
    "alg-1-3": (
        ("calc",),
        "Fractional powers and roots appear as soon as you differentiate √x or simplify a radical inside a limit.",
    ),
    "alg-1-5": (
        ("calc",),
        "Calc 1 spends more time factoring so you can cancel than it spends on new formulas.",
    ),
    "alg-1-6": (
        ("calc",),
        "Simplifying rational expressions is how you evaluate most 0/0 limits.",
    ),
    "alg-2-1": (
        ("me",),
        "Coordinates, distance, and midpoint are the 2-D language of displacements and force diagrams.",
    ),
    "alg-2-4": (
        ("ee",),
        "AC circuits treat voltages and currents as complex numbers (impedance and phasors).",
    ),
    "alg-2-5": (
        ("calc", "ee", "me"),
        "Quadratics show up in projectile motion, optimization, and characteristic equations.",
    ),
    "alg-2-7": (
        ("calc",),
        "Sign charts for inequalities become the increasing/decreasing tests in Calc 1.",
    ),
    "alg-3-1": (
        ("calc", "ee", "me"),
        "Every derivative and every circuit or motion model is a function. f(x) is not f times x.",
    ),
    "alg-3-2": (
        ("calc",),
        "You cannot take a limit or plug a physical value into a formula whose domain you ignored.",
    ),
    "alg-3-3": (
        ("calc", "me"),
        "Average rate of change is the derivative without the limit. In mechanics it is average velocity.",
    ),
    "alg-3-4": (
        ("calc", "ee", "me"),
        "The chain rule is composition. Nested functions are how most engineering formulas are built.",
    ),
    "alg-3-5": (
        ("calc", "ee", "me"),
        "Shifts and stretches are how you read graphs of position, voltage, and trig waves.",
    ),
    "alg-3-6": (
        ("calc",),
        "Absolute value is the first piecewise function you will differentiate.",
    ),
    "alg-3-7": (
        ("calc", "ee"),
        "ln undoes e^x. Inverse functions are how you solve exponential decay and some integrals.",
    ),
    "alg-4-1": (
        ("calc", "ee", "me"),
        "The tangent line is a linear function. Ohm's law and Hooke's law are linear models.",
    ),
    "alg-4-2": (
        ("ee", "me"),
        "Constant-rate models are the starting point for steady current and for constant-velocity motion.",
    ),
    "alg-5-1": (
        ("calc", "me"),
        "Parabolas are the position graph of constant acceleration and the first optimization curves.",
    ),
    "alg-5-2": (
        ("calc",),
        "End behavior of polynomials is the same idea as limits at infinity.",
    ),
    "alg-5-3": (
        ("calc",),
        "Intercepts and multiplicity are how you sketch a graph before you have a derivative.",
    ),
    "alg-5-4": (
        ("calc",),
        "Polynomial division is the algebra behind the remainder theorem and later partial fractions.",
    ),
    "alg-5-5": (
        ("calc",),
        "Finding zeros is how you find intercepts, equilibrium points, and critical-value candidates.",
    ),
    "alg-5-6": (
        ("calc",),
        "Vertical asymptotes and end behavior are limit problems in disguise.",
    ),
    "alg-5-7": (
        ("calc",),
        "Restricted domains and root inverses return in related rates and inverse-function derivatives.",
    ),
    "alg-5-8": (
        ("ee", "me"),
        "Direct and inverse variation are how many force, gravity, and circuit relations are first written.",
    ),
    "alg-6-1": (
        ("calc", "ee", "me"),
        "Exponential growth and decay is RC/RL charging, damping, and the derivative of e^x.",
    ),
    "alg-6-2": (
        ("calc", "ee", "me"),
        "Reading a growth/decay graph is how you check a time-constant sketch.",
    ),
    "alg-6-3": (
        ("calc", "ee"),
        "Logs convert multiply-into-add; they are also how you solve for time in exponential models.",
    ),
    "alg-6-4": (
        ("ee",),
        "Log graphs are the shape of Bode plots and of log-scale lab data.",
    ),
    "alg-6-5": (
        ("calc", "ee"),
        "Log properties are required to differentiate ln and to expand decibel calculations.",
    ),
    "alg-6-6": (
        ("calc", "ee", "me"),
        "Solving b^x = k or ln x = k is how you find time constants and half-lives.",
    ),
    "alg-6-7": (
        ("ee", "me"),
        "Exponential models are cooling, damping, and capacitor discharge.",
    ),
    "alg-6-8": (
        ("ee", "me"),
        "Fitting y = a b^x is how decay or charging lab data becomes a formula.",
    ),
    "alg-11-1": (
        ("ee", "me"),
        "Two-equation systems are two-loop circuits and two-force equilibrium.",
    ),
    "alg-11-2": (
        ("ee", "me"),
        "Three-variable systems are mesh analysis and 3-D force balance.",
    ),
    "alg-11-4": (
        ("calc",),
        "Partial fractions are the algebra of integrating rational functions in Calc 2.",
    ),
    "alg-13-4": (
        ("calc",),
        "Infinite series start here so the geometric series in Calc 2 is not a surprise.",
    ),
    "alg-13-6": (
        ("calc",),
        "Binomial expansions anticipate the (1+x)^n work that calculus continues.",
    ),
    "trig-7-1": (
        ("calc", "ee", "me"),
        "Calculus and all AC or rotation formulas use radians, not degrees.",
    ),
    "trig-7-2": (
        ("calc", "ee", "me"),
        "Related rates, phasor triangles, and resolving forces all start with opposite/adjacent/hypotenuse.",
    ),
    "trig-7-3": (
        ("calc", "ee", "me"),
        "Sine and cosine of standard angles are the values you use constantly in Calc 1 and in waveforms.",
    ),
    "trig-7-4": (
        ("calc", "ee"),
        "tan and sec show up in derivatives; tan is also the ratio on a phasor or impedance triangle. The other reciprocal direction is sin = 1/csc, cos = 1/sec, tan = 1/cot.",
    ),
    "trig-7-5": (
        ("calc", "ee", "me"),
        "Arc length s = rθ (θ in radians) is polar calculus, rotor angle, and any circular motion.",
    ),
    "trig-7-6": (
        ("calc", "ee"),
        "Reducing an angle into [0, 2π) is how you wrap a calculus angle and how you wrap a phase in AC.",
    ),
    "trig-7-7": (
        ("calc", "ee", "me"),
        "Angular speed ω and rim speed v = rω are circular related rates, motors, gears, and rotating shafts.",
    ),
    "trig-7-8": (
        ("calc", "me"),
        "Angle of elevation is the first related-rates picture and the first statics height-from-a-distance picture.",
    ),
    "trig-7-9": (
        ("calc",),
        "Cofunction identities are how you rewrite sin(π/2 − x) before differentiating or integrating.",
    ),
    "trig-8-1": (
        ("calc", "ee", "me"),
        "AC voltages and simple harmonic motion are A sin(ωt + φ). Amplitude and period are physical.",
    ),
    "trig-8-2": (
        ("calc",),
        "Tangent and cotangent both have period π. Their asymptotes are the first trig graphs with discontinuities, which calculus will ask about.",
    ),
    "trig-8-3": (
        ("calc", "ee", "me"),
        "Paul: y = sin⁻¹(x) is equivalent to x = sin(y); alternate notation sin⁻¹(x) = arcsin(x), not 1/sin. arctan shows up in integrals and as the angle of a resultant or of a complex number.",
    ),
    "trig-8-4": (
        ("calc", "ee", "me"),
        "Phase shift is the φ in A sin(ωt + φ): delayed voltage, delayed displacement, shifted graph.",
    ),
    "trig-8-5": (
        ("calc", "ee", "me"),
        "A sinusoid in time is AC voltage and simple harmonic motion. Period and frequency are physical.",
    ),
    "trig-9-1": (
        ("calc", "ee"),
        "Pythagorean identities rewrite trig before a derivative, and they are the identity behind sin² + cos² = 1 on a phasor.",
    ),
    "trig-9-2": (
        ("calc", "ee"),
        "Sum and difference identities appear in phase shifts, beats, and trig integrals.",
    ),
    "trig-9-3": (
        ("calc", "ee"),
        "Double-angle and 2 sin cos are how you integrate sin² and how you handle product waveforms in AC.",
    ),
    "trig-9-4": (
        ("calc",),
        "Product-to-sum is how you integrate products of sines and cosines.",
    ),
    "trig-9-5": (
        ("calc", "ee", "me"),
        "Solving sin θ = k is how you find times in a cycle and angles in a mechanism.",
    ),
    "trig-9-6": (
        ("calc",),
        "Half-angle formulas are the power-reduction identities you use to integrate sin² and cos².",
    ),
    "trig-10-1": (
        ("me",),
        "Law of Sines is statics: finding a force or a length in a non-right triangle.",
    ),
    "trig-10-2": (
        ("me",),
        "Law of Cosines (all three cyclic forms) is the magnitude of a resultant of two vectors that are not perpendicular.",
    ),
    "trig-10-3": (
        ("me",),
        "Area = (1/2)ab sin C is how you find the area of a force triangle or a structural panel that is not a right triangle.",
    ),
    "trig-10-4": (
        ("me",),
        "SSA is the ambiguous case: two different force/geometry diagrams can share the same two sides and a non-included angle.",
    ),
    "pc-10-3": (
        ("calc", "ee", "me"),
        "Polar form describes rotation, AC phasors, and later polar calculus.",
    ),
    "pc-10-4": (
        ("calc", "ee"),
        "Polar graphs are Calc 2 polar curves and also the polar plots used for radiation and frequency response.",
    ),
    "pc-10-5": (
        ("ee",),
        "A phasor is a complex number in polar form — this is core electrical engineering.",
    ),
    "pc-10-6": (
        ("calc", "ee", "me"),
        "Position as x(t), y(t) is parametric motion, a time-domain signal pair, and the start of vector calculus.",
    ),
    "pc-10-7": (
        ("calc", "me"),
        "Eliminating the parameter is how you see the path a particle actually traces.",
    ),
    "pc-10-8": (
        ("calc", "ee", "me"),
        "Forces, velocity, and field quantities are vectors. Magnitude is not the sum of components.",
    ),
    "pc-11-5": (
        ("ee",),
        "Circuit networks are written with matrices; this is the linear algebra underneath mesh analysis.",
    ),
    "pc-11-6": (
        ("ee", "me"),
        "Gaussian elimination is how you actually solve those network and equilibrium systems.",
    ),
    "pc-11-7": (
        ("ee",),
        "Matrix inverses solve Ax = b in one shot — mesh analysis and other linear models.",
    ),
    "pc-limit-1": (
        ("calc",),
        "This is the first week of Calc 1. A hole in the graph can still have a limit.",
    ),
    "pc-limit-2": (
        ("calc",),
        "Factor, cancel, substitute: the main Calc 1 algebraic limit technique.",
    ),
    "pc-limit-3": (
        ("calc",),
        "Continuity is which functions you are allowed to differentiate.",
    ),
    "phy-2-1": (
        ("me",),
        "ΣF = ma is the starting equation of every statics and dynamics course.",
    ),
    "phy-3-3": (
        ("me",),
        "Mechanical energy conservation is how you size a drop, a spring, or a flywheel without tracking time.",
    ),
    "phy-4-2": (
        ("me",),
        "Collisions and impulse are crash analysis and any impact in a mechanism.",
    ),
    "phy-5-1": (
        ("me",),
        "Centripetal acceleration is rotation, banked curves, and any part that travels in a circle.",
    ),
    "phy-7-1": (
        ("ee",),
        "Ohm's law is the first equation of circuit analysis.",
    ),
    "phy-11-1": (
        ("ee",),
        "Series and parallel equivalents are how you reduce a resistor network before Kirchhoff.",
    ),
    "phy-10-1": (
        ("ee",),
        "Coulomb's law is the force law behind every electrostatics and capacitor problem.",
    ),
    "phy-12-1": (
        ("ee",),
        "F = qvB is the force on charges in motors, Hall sensors, and cyclotrons.",
    ),
    "phy-8-2": (
        ("me",),
        "Buoyancy and displaced volume show up in naval architecture and any submerged part.",
    ),
    "phy-9-2": (
        ("me",),
        "The first law is energy accounting for engines, refrigerators, and control volumes.",
    ),
}


def _apply_relevance() -> None:
    known = {s.id for s in all_skills()}
    missing = [sid for sid in RELEVANCE if sid not in known]
    if missing:
        raise RuntimeError(f"Relevance tags point at unknown skills: {missing}")
    for skill in all_skills():
        packed = RELEVANCE.get(skill.id)
        if packed is None:
            continue
        tags, why = packed
        skill.relevance = list(tags)
        skill.why_relevant = why


_apply_relevance()


def format_skill_title(skill: Skill) -> str:
    if not skill.relevance:
        return skill.title
    marks = " · ".join(TAG_LABELS[t] for t in skill.relevance if t in TAG_LABELS)
    return f"{skill.title}  · {marks}"


def relevance_line(skill: Skill) -> str:
    if not skill.relevance:
        return ""
    marks = " · ".join(f"**{TAG_LABELS[t]}**" for t in skill.relevance if t in TAG_LABELS)
    if skill.why_relevant:
        return f"{marks} — {skill.why_relevant}"
    return marks


def skills_with_tag(tag: str) -> list[Skill]:
    return [s for s in all_skills() if tag in s.relevance]
