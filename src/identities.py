from __future__ import annotations

import html
import json
import random
from dataclasses import dataclass

FIELD_ORDER = ("math", "physics", "ee", "me")
FIELD_LABEL = {
    "math": "Math",
    "physics": "Physics",
    "ee": "EE",
    "me": "ME",
}
FAMILY_ORDER = (
    "definitions",
    "reciprocal",
    "pythagorean",
    "even_odd",
    "cofunction",
    "sum_diff",
    "double_half",
    "product_sum",
    "inverse",
    "triangles",
    "complex",
)
FAMILY_LABEL = {
    "definitions": "Definitions",
    "reciprocal": "Reciprocal & quotient",
    "pythagorean": "Pythagorean",
    "even_odd": "Even, odd & period",
    "cofunction": "Cofunction",
    "sum_diff": "Sum & difference",
    "double_half": "Double & half angle",
    "product_sum": "Product & sum",
    "inverse": "Inverse trig",
    "triangles": "Triangle laws",
    "complex": "Complex & vectors",
}

_M = ("math",)
_MP = ("math", "physics")
_ME = ("math", "ee")
_MM = ("math", "me")
_MPE = ("math", "physics", "ee")
_MPM = ("math", "physics", "me")
_ALL = ("math", "physics", "ee", "me")
_PEM = ("physics", "ee", "me")


@dataclass(frozen=True)
class Identity:
    id: str
    family: str
    name: str
    lhs_html: str
    lhs_tex: str
    answer: str
    rhs_tex: str
    fields: tuple[str, ...]
    why: str

    @property
    def family_label(self) -> str:
        return FAMILY_LABEL[self.family]

    def field_labels(self) -> tuple[str, ...]:
        return tuple(FIELD_LABEL[f] for f in FIELD_ORDER if f in self.fields)


def _i(
    ident_id: str,
    family: str,
    name: str,
    lhs_html: str,
    lhs_tex: str,
    answer: str,
    rhs_tex: str,
    fields: tuple[str, ...],
    why: str,
) -> Identity:
    return Identity(
        ident_id,
        family,
        name,
        lhs_html,
        lhs_tex,
        answer,
        rhs_tex,
        fields,
        why,
    )


IDENTITIES: tuple[Identity, ...] = (
    _i("def-sin", "definitions", "Sine (right triangle)",
       "sin(θ)", r"\sin\theta",
       "opposite / hypotenuse", r"\dfrac{\text{opposite}}{\text{hypotenuse}}",
       _MPM, "SOHCAHTOA for related rates, force triangles, and any right-triangle height."),
    _i("def-cos", "definitions", "Cosine (right triangle)",
       "cos(θ)", r"\cos\theta",
       "adjacent / hypotenuse", r"\dfrac{\text{adjacent}}{\text{hypotenuse}}",
       _MPM, "Adjacent over hypotenuse is the adjacent-side component and the x-projection."),
    _i("def-tan", "definitions", "Tangent (right triangle)",
       "tan(θ)", r"\tan\theta",
       "opposite / adjacent", r"\dfrac{\text{opposite}}{\text{adjacent}}",
       _ALL, "Slope, rise/run, and the opposite/adjacent ratio on a phasor or friction triangle."),
    _i("def-csc", "definitions", "Cosecant (right triangle)",
       "csc(θ)", r"\csc\theta",
       "hypotenuse / opposite", r"\dfrac{\text{hypotenuse}}{\text{opposite}}",
       _M, "Reciprocal of sine; needed when a calculus integrand has 1/sin."),
    _i("def-sec", "definitions", "Secant (right triangle)",
       "sec(θ)", r"\sec\theta",
       "hypotenuse / adjacent", r"\dfrac{\text{hypotenuse}}{\text{adjacent}}",
       _ME, "Reciprocal of cosine; the derivative of tan is sec²."),
    _i("def-cot", "definitions", "Cotangent (right triangle)",
       "cot(θ)", r"\cot\theta",
       "adjacent / opposite", r"\dfrac{\text{adjacent}}{\text{opposite}}",
       _M, "Reciprocal of tangent; appears in some Calc 2 integrals."),
    _i("def-sin-uc", "definitions", "Sine (unit circle)",
       "sin(θ) on the unit circle", r"\sin\theta",
       "y", r"y",
       _MPE, "On the unit circle, sine is the y-coordinate of the point."),
    _i("def-cos-uc", "definitions", "Cosine (unit circle)",
       "cos(θ) on the unit circle", r"\cos\theta",
       "x", r"x",
       _MPE, "On the unit circle, cosine is the x-coordinate of the point."),
    _i("def-rad", "definitions", "Degrees to radians",
       "θ in radians if θ is in degrees", r"\theta_{\text{rad}}",
       "π θ / 180", r"\pi\theta/180",
       _ALL, "Calculus, ωt, and every rotation formula need radians, not degrees."),
    _i("rec-csc", "reciprocal", "Cosecant reciprocal",
       "csc(θ)", r"\csc\theta",
       "1 / sin(θ)", r"1/\sin\theta",
       _ME, "Rewrite 1/sin before differentiating or integrating."),
    _i("rec-sec", "reciprocal", "Secant reciprocal",
       "sec(θ)", r"\sec\theta",
       "1 / cos(θ)", r"1/\cos\theta",
       _ME, "sec is 1/cos; it shows up in tan′ = sec² and in some AC magnitudes."),
    _i("rec-cot", "reciprocal", "Cotangent reciprocal",
       "cot(θ)", r"\cot\theta",
       "1 / tan(θ)", r"1/\tan\theta",
       _M, "cot is 1/tan, equivalent to cos/sin."),
    _i("quo-tan", "reciprocal", "Tangent quotient",
       "tan(θ)", r"\tan\theta",
       "sin(θ) / cos(θ)", r"\sin\theta/\cos\theta",
       _ALL, "The slope identity: tan is sine over cosine on a triangle or a phasor."),
    _i("quo-cot", "reciprocal", "Cotangent quotient",
       "cot(θ)", r"\cot\theta",
       "cos(θ) / sin(θ)", r"\cos\theta/\sin\theta",
       _ME, "The other way up from tan; used when you clear a sine in the denominator."),
    _i("pyth-1", "pythagorean", "Main Pythagorean",
       "sin²(θ) + cos²(θ)", r"\sin^2\theta + \cos^2\theta",
       "1", r"1",
       _ALL, "The unit-circle equation. Rewrite before a derivative, and |phasor|² = 1."),
    _i("pyth-2", "pythagorean", "Tangent Pythagorean",
       "1 + tan²(θ)", r"1 + \tan^2\theta",
       "sec²(θ)", r"\sec^2\theta",
       _ME, "This is why d/dθ tan θ = sec² θ, and it is the trig sub for √(1+x²)."),
    _i("pyth-3", "pythagorean", "Cotangent Pythagorean",
       "1 + cot²(θ)", r"1 + \cot^2\theta",
       "csc²(θ)", r"\csc^2\theta",
       _M, "Companion of 1+tan²=sec²; used in some Calc 2 substitutions."),
    _i("pyth-sin", "pythagorean", "Solve for sin²",
       "sin²(θ)", r"\sin^2\theta",
       "1 − cos²(θ)", r"1 - \cos^2\theta",
       _MP, "Drop a cosine from a constraint, or replace sin² in an integrand."),
    _i("pyth-cos", "pythagorean", "Solve for cos²",
       "cos²(θ)", r"\cos^2\theta",
       "1 − sin²(θ)", r"1 - \sin^2\theta",
       _MP, "Same rewrite with sine as the leftover function."),
    _i("odd-sin", "even_odd", "Sine is odd",
       "sin(−θ)", r"\sin(-\theta)",
       "− sin(θ)", r"-\sin\theta",
       _MPE, "Odd functions: sine of a reversed time or reversed angle flips sign."),
    _i("even-cos", "even_odd", "Cosine is even",
       "cos(−θ)", r"\cos(-\theta)",
       "cos(θ)", r"\cos\theta",
       _MPE, "Even functions: cosine does not care about the sign of the angle."),
    _i("odd-tan", "even_odd", "Tangent is odd",
       "tan(−θ)", r"\tan(-\theta)",
       "− tan(θ)", r"-\tan\theta",
       _MPE, "Tangent is odd, like sine; a reversed slope is the negative slope."),
    _i("odd-csc", "even_odd", "Cosecant is odd",
       "csc(−θ)", r"\csc(-\theta)",
       "− csc(θ)", r"-\csc\theta",
       _M, "csc follows sine: it is an odd function."),
    _i("even-sec", "even_odd", "Secant is even",
       "sec(−θ)", r"\sec(-\theta)",
       "sec(θ)", r"\sec\theta",
       _M, "sec follows cosine: it is an even function."),
    _i("odd-cot", "even_odd", "Cotangent is odd",
       "cot(−θ)", r"\cot(-\theta)",
       "− cot(θ)", r"-\cot\theta",
       _M, "cot follows tangent: it is an odd function."),
    _i("per-sin", "even_odd", "Sine period 2π",
       "sin(θ + 2π n)", r"\sin(\theta + 2\pi n)",
       "sin(θ)", r"\sin\theta",
       _MPE, "Sine (and a full AC cycle) repeats every 2π radians."),
    _i("per-cos", "even_odd", "Cosine period 2π",
       "cos(θ + 2π n)", r"\cos(\theta + 2\pi n)",
       "cos(θ)", r"\cos\theta",
       _MPE, "Cosine also repeats every 2π; n is any integer."),
    _i("per-tan", "even_odd", "Tangent period π",
       "tan(θ + π n)", r"\tan(\theta + \pi n)",
       "tan(θ)", r"\tan\theta",
       _ME, "Tangent repeats every π, not 2π — vertical asymptotes every π."),
    _i("per-sin-w", "even_odd", "Period of sin(ωθ)",
       "period of sin(ω θ)", r"T\text{ for }\sin(\omega\theta)",
       "2π / ω", r"2\pi/\omega",
       _ALL, "T = 2π/ω is the period of AC voltage and of simple harmonic motion."),
    _i("per-tan-w", "even_odd", "Period of tan(ωθ)",
       "period of tan(ω θ)", r"T\text{ for }\tan(\omega\theta)",
       "π / ω", r"\pi/\omega",
       _ME, "Tangent’s natural period is π, so tan(ωθ) has period π/ω."),
    _i("co-sin", "cofunction", "Sine cofunction",
       "sin(π/2 − θ)", r"\sin(\pi/2 - \theta)",
       "cos(θ)", r"\cos\theta",
       _M, "A cofunction rewrite before differentiating sin(π/2 − x)."),
    _i("co-cos", "cofunction", "Cosine cofunction",
       "cos(π/2 − θ)", r"\cos(\pi/2 - \theta)",
       "sin(θ)", r"\sin\theta",
       _M, "Complementary angles swap sine and cosine."),
    _i("co-tan", "cofunction", "Tangent cofunction",
       "tan(π/2 − θ)", r"\tan(\pi/2 - \theta)",
       "cot(θ)", r"\cot\theta",
       _M, "The complement of tangent is cotangent."),
    _i("co-cot", "cofunction", "Cotangent cofunction",
       "cot(π/2 − θ)", r"\cot(\pi/2 - \theta)",
       "tan(θ)", r"\tan\theta",
       _M, "The complement of cotangent is tangent."),
    _i("co-sec", "cofunction", "Secant cofunction",
       "sec(π/2 − θ)", r"\sec(\pi/2 - \theta)",
       "csc(θ)", r"\csc\theta",
       _M, "The complement of secant is cosecant."),
    _i("co-csc", "cofunction", "Cosecant cofunction",
       "csc(π/2 − θ)", r"\csc(\pi/2 - \theta)",
       "sec(θ)", r"\sec\theta",
       _M, "The complement of cosecant is secant."),
    _i("sum-sinp", "sum_diff", "Sine of a sum",
       "sin(α + β)", r"\sin(\alpha + \beta)",
       "sin α cos β + cos α sin β", r"\sin\alpha\cos\beta + \cos\alpha\sin\beta",
       _MPE, "Phase shift: sin(ωt+φ) expands with this. Also beats and trig integrals."),
    _i("sum-sinm", "sum_diff", "Sine of a difference",
       "sin(α − β)", r"\sin(\alpha - \beta)",
       "sin α cos β − cos α sin β", r"\sin\alpha\cos\beta - \cos\alpha\sin\beta",
       _MPE, "Same expansion with the minus on the second term."),
    _i("sum-cosp", "sum_diff", "Cosine of a sum",
       "cos(α + β)", r"\cos(\alpha + \beta)",
       "cos α cos β − sin α sin β", r"\cos\alpha\cos\beta - \sin\alpha\sin\beta",
       _MPE, "The minus on the sine product is the usual trap. Used for phase and beats."),
    _i("sum-cosm", "sum_diff", "Cosine of a difference",
       "cos(α − β)", r"\cos(\alpha - \beta)",
       "cos α cos β + sin α sin β", r"\cos\alpha\cos\beta + \sin\alpha\sin\beta",
       _MPE, "Cosine of a difference adds the sine product. Dot-product angle formula."),
    _i("sum-tanp", "sum_diff", "Tangent of a sum",
       "tan(α + β)", r"\tan(\alpha + \beta)",
       "(tan α + tan β) / (1 − tan α tan β)", r"(\tan\alpha + \tan\beta)/(1 - \tan\alpha\tan\beta)",
       _ME, "Adding phases on a tangent; also the tangent-addition form of a double angle."),
    _i("sum-tanm", "sum_diff", "Tangent of a difference",
       "tan(α − β)", r"\tan(\alpha - \beta)",
       "(tan α − tan β) / (1 + tan α tan β)", r"(\tan\alpha - \tan\beta)/(1 + \tan\alpha\tan\beta)",
       _ME, "Difference of two angles’ tangents; signs flip from the sum formula."),
    _i("dbl-sin", "double_half", "Sine double angle",
       "sin(2θ)", r"\sin 2\theta",
       "2 sin(θ) cos(θ)", r"2\sin\theta\cos\theta",
       _MPE, "The 2 sin cos identity: integrals, power, and product waveforms."),
    _i("dbl-cos", "double_half", "Cosine double angle",
       "cos(2θ)", r"\cos 2\theta",
       "cos²(θ) − sin²(θ)", r"\cos^2\theta - \sin^2\theta",
       _MPE, "Primary double-angle cosine; the other two forms come from Pythagoras."),
    _i("dbl-cos-c", "double_half", "Cosine double angle (cos only)",
       "2 cos²(θ) − 1", r"2\cos^2\theta - 1",
       "cos(2θ)", r"\cos 2\theta",
       _MP, "Cosine double angle written only in cosine. Reverse of power-reduction."),
    _i("dbl-cos-s", "double_half", "Cosine double angle (sin only)",
       "1 − 2 sin²(θ)", r"1 - 2\sin^2\theta",
       "cos(2θ)", r"\cos 2\theta",
       _MP, "Cosine double angle written only in sine. Used for intensity ~ sin²."),
    _i("dbl-tan", "double_half", "Tangent double angle",
       "tan(2θ)", r"\tan 2\theta",
       "2 tan(θ) / (1 − tan²(θ))", r"2\tan\theta/(1 - \tan^2\theta)",
       _M, "Double-angle tangent; same pattern as tan(α+α)."),
    _i("half-sin", "double_half", "Sine half angle",
       "sin(θ/2)", r"\sin(\theta/2)",
       "± √((1 − cos θ) / 2)", r"\pm\sqrt{(1-\cos\theta)/2}",
       _M, "Half-angle sine. The sign is the quadrant of θ/2."),
    _i("half-cos", "double_half", "Cosine half angle",
       "cos(θ/2)", r"\cos(\theta/2)",
       "± √((1 + cos θ) / 2)", r"\pm\sqrt{(1+\cos\theta)/2}",
       _M, "Half-angle cosine. Plus cosine inside the root, unlike sine."),
    _i("half-tan", "double_half", "Tangent half angle",
       "tan(θ/2)", r"\tan(\theta/2)",
       "± √((1 − cos θ) / (1 + cos θ))", r"\pm\sqrt{(1-\cos\theta)/(1+\cos\theta)}",
       _M, "Half-angle tangent. The Weierstrass substitution in Calc 2 starts here."),
    _i("pow-sin", "double_half", "Power-reduce sin²",
       "sin²(θ)", r"\sin^2\theta",
       "(1 − cos(2θ)) / 2", r"(1-\cos 2\theta)/2",
       _MPE, "How you integrate sin², and how you average sin² over a cycle (RMS)."),
    _i("pow-cos", "double_half", "Power-reduce cos²",
       "cos²(θ)", r"\cos^2\theta",
       "(1 + cos(2θ)) / 2", r"(1+\cos 2\theta)/2",
       _MPE, "How you integrate cos², and the DC + double-frequency term in AC power."),
    _i("pow-tan", "double_half", "Power-reduce tan²",
       "tan²(θ)", r"\tan^2\theta",
       "(1 − cos(2θ)) / (1 + cos(2θ))", r"(1-\cos 2\theta)/(1+\cos 2\theta)",
       _M, "Power-reduction for tangent, from the sine and cosine versions."),
    _i("ps-ss", "product_sum", "Product sin sin",
       "sin(α) sin(β)", r"\sin\alpha\sin\beta",
       "½ [cos(α − β) − cos(α + β)]", r"\tfrac12[\cos(\alpha-\beta)-\cos(\alpha+\beta)]",
       _ME, "Product-to-sum: how you integrate a product of sines, and how mixers beat."),
    _i("ps-cc", "product_sum", "Product cos cos",
       "cos(α) cos(β)", r"\cos\alpha\cos\beta",
       "½ [cos(α − β) + cos(α + β)]", r"\tfrac12[\cos(\alpha-\beta)+\cos(\alpha+\beta)]",
       _ME, "Product of cosines becomes a sum of cosines at the difference and sum frequencies."),
    _i("ps-sc", "product_sum", "Product sin cos",
       "sin(α) cos(β)", r"\sin\alpha\cos\beta",
       "½ [sin(α + β) + sin(α − β)]", r"\tfrac12[\sin(\alpha+\beta)+\sin(\alpha-\beta)]",
       _ME, "sin·cos product-to-sum; the double-angle 2sin cos is the α=β case."),
    _i("ps-cs", "product_sum", "Product cos sin",
       "cos(α) sin(β)", r"\cos\alpha\sin\beta",
       "½ [sin(α + β) − sin(α − β)]", r"\tfrac12[\sin(\alpha+\beta)-\sin(\alpha-\beta)]",
       _ME, "cos·sin product-to-sum; watch the minus on the difference sine."),
    _i("sp-sins", "product_sum", "Sum of sines",
       "sin(α) + sin(β)", r"\sin\alpha + \sin\beta",
       "2 sin((α+β)/2) cos((α−β)/2)", r"2\sin\frac{\alpha+\beta}{2}\cos\frac{\alpha-\beta}{2}",
       _MPE, "Sum-to-product: two close frequencies become a beat envelope."),
    _i("sp-sind", "product_sum", "Difference of sines",
       "sin(α) − sin(β)", r"\sin\alpha - \sin\beta",
       "2 cos((α+β)/2) sin((α−β)/2)", r"2\cos\frac{\alpha+\beta}{2}\sin\frac{\alpha-\beta}{2}",
       _MPE, "Difference of sines; used in interference and in some trig integrals."),
    _i("sp-coss", "product_sum", "Sum of cosines",
       "cos(α) + cos(β)", r"\cos\alpha + \cos\beta",
       "2 cos((α+β)/2) cos((α−β)/2)", r"2\cos\frac{\alpha+\beta}{2}\cos\frac{\alpha-\beta}{2}",
       _MPE, "Two cosines in phase add as a cosine of the average angle."),
    _i("sp-cosd", "product_sum", "Difference of cosines",
       "cos(α) − cos(β)", r"\cos\alpha - \cos\beta",
       "−2 sin((α+β)/2) sin((α−β)/2)", r"-2\sin\frac{\alpha+\beta}{2}\sin\frac{\alpha-\beta}{2}",
       _MPE, "Cosine difference has an overall minus. Easy to drop."),
    _i("inv-sin-rng", "inverse", "Range of arcsin",
       "range of arcsin(x)", r"\text{range of }\arcsin x",
       "[−π/2, π/2]", r"[-\pi/2,\ \pi/2]",
       _ALL, "Principal sine inverse: the angle a calculator returns, and the Calc 1 range."),
    _i("inv-cos-rng", "inverse", "Range of arccos",
       "range of arccos(x)", r"\text{range of }\arccos x",
       "[0, π]", r"[0,\ \pi]",
       _MPE, "Principal cosine inverse lives in [0, π], not ±π/2."),
    _i("inv-tan-rng", "inverse", "Range of arctan",
       "range of arctan(x)", r"\text{range of }\arctan x",
       "(−π/2, π/2)", r"(-\pi/2,\ \pi/2)",
       _ALL, "arctan of a slope or of Im/Re for a phasor in the open interval (−π/2, π/2)."),
    _i("inv-sin", "inverse", "Sine cancels arcsin",
       "sin(arcsin(x))", r"\sin(\arcsin x)",
       "x", r"x",
       _M, "True for x in [−1, 1]. The inner inverse already picked the principal angle."),
    _i("inv-cos", "inverse", "Cosine cancels arccos",
       "cos(arccos(x))", r"\cos(\arccos x)",
       "x", r"x",
       _M, "True for x in [−1, 1]. Going the other way, arccos(cos θ) needs the range."),
    _i("inv-tan", "inverse", "Tangent cancels arctan",
       "tan(arctan(x))", r"\tan(\arctan x)",
       "x", r"x",
       _M, "True for all real x. arctan(tan θ) is only θ if θ is in (−π/2, π/2)."),
    _i("tri-sines", "triangles", "Law of Sines",
       "sin(α) / a", r"\dfrac{\sin\alpha}{a}",
       "sin(β) / b = sin(γ) / c", r"\dfrac{\sin\beta}{b} = \dfrac{\sin\gamma}{c}",
       _MPM, "Non-right triangles in statics: one side-angle pair determines the others."),
    _i("tri-cos", "triangles", "Law of Cosines",
       "a²", r"a^2",
       "b² + c² − 2bc cos(α)", r"b^2 + c^2 - 2bc\cos\alpha",
       _MPM, "Magnitude of a resultant of two vectors that are not perpendicular."),
    _i("tri-tan", "triangles", "Law of Tangents",
       "(a − b) / (a + b)", r"\dfrac{a-b}{a+b}",
       "tan(½(α−β)) / tan(½(α+β))", r"\dfrac{\tan\frac12(\alpha-\beta)}{\tan\frac12(\alpha+\beta)}",
       _MM, "A companion to the Law of Sines when two sides and their opposite angles are known."),
    _i("tri-area", "triangles", "Triangle area",
       "area of a triangle", r"\text{Area}",
       "(1/2) ab sin(C)", r"\tfrac12 ab\sin C",
       _MPM, "Area from two sides and the included angle: panels, force triangles, flux."),
    _i("eul", "complex", "Euler’s formula",
       "e^{iθ}", r"e^{i\theta}",
       "cos(θ) + i sin(θ)", r"\cos\theta + i\sin\theta",
       _MPE, "The EE identity: a phasor, a rotation, and the definition of cis θ."),
    _i("vec-x", "complex", "x-component",
       "Aₓ if A is at angle θ from the x-axis", r"A_x",
       "A cos(θ)", r"A\cos\theta",
       _PEM, "Resolving a force, a velocity, or a phasor onto the x-axis."),
    _i("vec-y", "complex", "y-component",
       "Aᵧ if A is at angle θ from the x-axis", r"A_y",
       "A sin(θ)", r"A\sin\theta",
       _PEM, "Resolving onto the y-axis. Sine is the opposite / y piece."),
)

_EXTRA_DISTRACTORS: dict[str, tuple[str, ...]] = {
    "definitions": ("x / y", "y / x", "1", "θ"),
    "reciprocal": ("cos(θ) / sin(θ)", "sin(θ) / cos(θ)", "1 / tan(θ)", "1 / sin(θ)"),
    "pythagorean": ("0", "−1", "tan²(θ)", "sin(θ) cos(θ)", "2"),
    "even_odd": ("2π", "π", "2π / ω", "π / ω", "θ", "−θ"),
    "cofunction": ("sin(θ)", "cos(θ)", "tan(θ)", "cot(θ)", "sec(θ)", "csc(θ)"),
    "sum_diff": (
        "sin α cos β − cos α sin β",
        "cos α cos β + sin α sin β",
        "sin α sin β + cos α cos β",
    ),
    "double_half": (
        "2 sin(θ) cos(θ)",
        "cos(2θ)",
        "sin(2θ)",
        "(1 + cos(2θ)) / 2",
        "(1 − cos(2θ)) / 2",
    ),
    "product_sum": (
        "½ [cos(α − β) + cos(α + β)]",
        "½ [cos(α − β) − cos(α + β)]",
        "2 sin((α+β)/2) cos((α−β)/2)",
        "−2 sin((α+β)/2) sin((α−β)/2)",
    ),
    "inverse": ("[0, 2π]", "all real numbers", "[−π, π]", "x", "θ"),
    "triangles": (
        "b² + c² + 2bc cos(α)",
        "b² + c² − 2bc sin(α)",
        "(1/2) ab cos(C)",
        "sin(β) / b = sin(γ) / c",
    ),
    "complex": (
        "cos(θ) − i sin(θ)",
        "sin(θ) + i cos(θ)",
        "A sin(θ)",
        "A cos(θ)",
        "A tan(θ)",
    ),
}


def identities_for(*, field: str = "all", family: str = "all") -> tuple[Identity, ...]:
    rows = IDENTITIES
    if field != "all":
        rows = tuple(item for item in rows if field in item.fields)
    if family != "all":
        rows = tuple(item for item in rows if item.family == family)
    return rows


def family_ids_present(rows: tuple[Identity, ...]) -> tuple[str, ...]:
    seen: list[str] = []
    for item in rows:
        if item.family not in seen:
            seen.append(item.family)
    return tuple(fid for fid in FAMILY_ORDER if fid in seen)


def _pool(family: str) -> list[str]:
    values: list[str] = []
    for item in IDENTITIES:
        if item.family == family and item.answer not in values:
            values.append(item.answer)
    for extra in _EXTRA_DISTRACTORS.get(family, ()):
        if extra not in values:
            values.append(extra)
    return values


def _select_html(item: Identity) -> str:
    options = list(_pool(item.family))
    random.Random(item.id).shuffle(options)
    bits = ['<option value="">Choose…</option>']
    for value in options:
        bits.append(
            f'<option value="{html.escape(value, quote=True)}">{html.escape(value)}</option>'
        )
    return (
        f'<select data-id="{html.escape(item.id)}" '
        f'aria-label="{html.escape(item.name)}">{"".join(bits)}</select>'
    )


def _tags_html(item: Identity) -> str:
    return "".join(
        f'<span class="tag {field}">{html.escape(FIELD_LABEL[field])}</span>'
        for field in FIELD_ORDER
        if field in item.fields
    )


def identities_practice_html(*, field: str = "all", family: str = "all") -> str:
    rows = identities_for(field=field, family=family)
    if not rows:
        return (
            '<div id="id-drill"><p class="hint">No identities in this filter. '
            "Pick All fields or another family.</p></div>"
        )
    cards = []
    jump = []
    key = []
    for index, item in enumerate(rows):
        active = " active" if index == 0 else ""
        cards.append(
            f'<article class="id-card{active}" data-id="{html.escape(item.id)}">'
            f'<div class="meta"><span class="fam">{html.escape(item.family_label)}</span>'
            f"{_tags_html(item)}</div>"
            f'<h3>{html.escape(item.name)}</h3>'
            f'<div class="eq"><span class="lhs">{item.lhs_html}</span>'
            f'<span class="eqs">=</span>{_select_html(item)}</div>'
            f'<p class="why">{html.escape(item.why)}</p>'
            "</article>"
        )
        jump.append(
            f'<option value="{html.escape(item.id)}">{html.escape(item.name)}</option>'
        )
        key.append({"id": item.id, "answer": item.answer})
    key_json = json.dumps(key, ensure_ascii=False)
    return f"""
<div id="id-drill">
<style>
  html, body {{ margin: 0; background: #0e1117; color: #e8eef8; }}
  #id-drill {{ color: #e8eef8; font-family: inherit; max-width: 100%; }}
  #id-drill * {{ box-sizing: border-box; }}
  #id-drill .hint {{ font-size: 0.95rem; color: #9aa8bc; margin: 0 0 0.6rem; }}
  #id-drill .bar, #id-drill .editor-nav {{
    display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap; margin: 0 0 0.7rem;
  }}
  #id-drill button {{
    background: #1f2a3d; color: #e8eef8; border: 1px solid #3d4b61; border-radius: 10px;
    padding: 0.65rem 0.9rem; min-height: 44px; font-size: 1rem; cursor: pointer;
    touch-action: manipulation; flex: 1 1 auto;
  }}
  #id-drill button.primary {{ background: #e11d48; border-color: #e11d48; font-weight: 600; }}
  #id-drill #score {{ min-height: 1.3em; font-size: 0.95rem; color: #cbd5e1; flex: 1 1 100%; }}
  #id-drill .jump {{
    display: flex; flex-direction: column; gap: 0.25rem; margin: 0 0 0.7rem; font-size: 0.95rem;
  }}
  #id-drill select, #id-drill label {{ font-size: 16px; min-height: 44px; }}
  #id-drill select {{
    width: 100%; padding: 0.55rem 0.5rem; border-radius: 8px; border: 1px solid #3d4b61;
    background: #111827; color: #f8fafc; color-scheme: dark;
  }}
  #id-drill .list {{ display: flex; flex-direction: column; gap: 0.75rem; }}
  #id-drill .id-card {{
    display: none; padding: 0.9rem; border: 1px solid #3d4b61; border-radius: 12px;
    background: #111827;
  }}
  #id-drill .id-card.active {{ display: block; }}
  #id-drill .id-card.ok {{ border-color: #3dd68c; }}
  #id-drill .id-card.bad {{ border-color: #f87171; }}
  #id-drill .meta {{
    display: flex; flex-wrap: wrap; gap: 0.35rem; align-items: center; margin: 0 0 0.45rem;
  }}
  #id-drill .fam {{ color: #9aa8bc; font-size: 0.8rem; margin-right: 0.25rem; }}
  #id-drill .tag {{
    font-size: 0.72rem; border-radius: 999px; padding: 0.12rem 0.5rem; font-weight: 600;
  }}
  #id-drill .tag.math {{ background: #1e3a5f; color: #bfdbfe; }}
  #id-drill .tag.physics {{ background: #4a1d4a; color: #f5d0fe; }}
  #id-drill .tag.ee {{ background: #134e4a; color: #99f6e4; }}
  #id-drill .tag.me {{ background: #4a3412; color: #fdba74; }}
  #id-drill h3 {{ margin: 0 0 0.55rem; font-size: 1.02rem; font-weight: 650; }}
  #id-drill .eq {{
    display: grid; grid-template-columns: 1fr auto 1fr; gap: 0.45rem; align-items: center;
  }}
  @media (max-width: 520px) {{
    #id-drill .eq {{ grid-template-columns: 1fr; }}
    #id-drill .eqs {{ display: none; }}
  }}
  #id-drill .lhs {{
    font-size: 1.05rem; color: #dbe7f6; text-align: right; overflow-wrap: anywhere;
  }}
  @media (max-width: 520px) {{ #id-drill .lhs {{ text-align: left; }} }}
  #id-drill .eqs {{ color: #9aa8bc; font-weight: 700; }}
  #id-drill .why {{ margin: 0.55rem 0 0; color: #9aa8bc; font-size: 0.9rem; }}
  #id-drill select.mismatch {{ border-color: #f87171; background: #3f0d12; }}
  #id-drill .ok select {{ border-color: #3dd68c; background: #052e16; }}
  @media (min-width: 540px) {{
    #id-drill .id-card {{ display: block; }}
    #id-drill .jump, #id-drill .editor-nav {{ display: none; }}
    #id-drill #score {{ flex: 1 1 auto; }}
    #id-drill button {{ flex: 0 0 auto; }}
    #id-drill .eq {{ grid-template-columns: minmax(8rem, 1.1fr) auto minmax(10rem, 1.3fr); }}
  }}
</style>
<p class="hint">Pick the matching right-hand side from the menu. Tags mark <b>Math</b> (calculus/precalc),
<b>Physics</b>, <b>EE</b>, and <b>ME</b>. On a phone, one identity at a time — use Previous / Next.
Check grades every blank in this filter.</p>
<div class="bar">
  <button type="button" class="primary" id="id-check">Check</button>
  <button type="button" id="id-reveal">Reveal</button>
  <button type="button" id="id-clear">Clear</button>
  <span id="score"></span>
</div>
<label class="jump">Identity
  <select id="jump">{"".join(jump)}</select>
</label>
<div class="list">
  {"".join(cards)}
</div>
<div class="editor-nav">
  <button type="button" id="id-prev">Previous</button>
  <button type="button" id="id-next">Next</button>
</div>
<script>
(function () {{
  const root = document.getElementById("id-drill");
  if (!root) return;
  const KEY = {key_json};
  const IDS = KEY.map((row) => row.id);
  let selected = IDS[0];
  function show(id) {{
    selected = id;
    root.querySelectorAll(".id-card").forEach((el) => {{
      el.classList.toggle("active", el.dataset.id === id);
    }});
    const jump = root.querySelector("#jump");
    if (jump) jump.value = id;
  }}
  const jump = root.querySelector("#jump");
  if (jump) jump.addEventListener("change", () => show(jump.value));
  const prev = root.querySelector("#id-prev");
  const next = root.querySelector("#id-next");
  if (prev) prev.addEventListener("click", () => {{
    const i = IDS.indexOf(selected);
    show(IDS[(i - 1 + IDS.length) % IDS.length]);
  }});
  if (next) next.addEventListener("click", () => {{
    const i = IDS.indexOf(selected);
    show(IDS[(i + 1) % IDS.length]);
  }});
  function selectFor(id) {{
    return root.querySelector('select[data-id="' + id + '"]');
  }}
  root.querySelector("#id-check").addEventListener("click", () => {{
    let need = 0, good = 0;
    KEY.forEach((k) => {{
      const card = root.querySelector('.id-card[data-id="' + k.id + '"]');
      const sel = selectFor(k.id);
      if (!sel || !card) return;
      need += 1;
      sel.classList.remove("mismatch");
      card.classList.remove("ok", "bad");
      if (sel.value === k.answer) {{
        good += 1;
        card.classList.add("ok");
      }} else {{
        card.classList.add("bad");
        sel.classList.add("mismatch");
      }}
    }});
    root.querySelector("#score").textContent = need ? (good + " / " + need + " identities correct") : "";
  }});
  root.querySelector("#id-reveal").addEventListener("click", () => {{
    KEY.forEach((k) => {{
      const card = root.querySelector('.id-card[data-id="' + k.id + '"]');
      const sel = selectFor(k.id);
      if (sel) {{
        sel.value = k.answer;
        sel.classList.remove("mismatch");
      }}
      if (card) {{
        card.classList.remove("bad");
        card.classList.add("ok");
      }}
    }});
    root.querySelector("#score").textContent = "Revealed. Clear and try again without looking.";
  }});
  root.querySelector("#id-clear").addEventListener("click", () => {{
    root.querySelectorAll("select[data-id]").forEach((sel) => {{
      sel.value = "";
      sel.classList.remove("mismatch");
    }});
    root.querySelectorAll(".id-card").forEach((el) => el.classList.remove("ok", "bad"));
    root.querySelector("#score").textContent = "";
  }});
  show(selected);
}})();
</script>
</div>
"""


def grouped_identities(field: str = "all") -> list[tuple[str, tuple[Identity, ...]]]:
    rows = identities_for(field=field)
    groups: list[tuple[str, tuple[Identity, ...]]] = []
    for family in FAMILY_ORDER:
        chunk = tuple(item for item in rows if item.family == family)
        if chunk:
            groups.append((FAMILY_LABEL[family], chunk))
    return groups
