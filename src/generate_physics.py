from __future__ import annotations

import random

from src.schema import Problem, make_problem, steps


def _steps(*pairs: tuple[str, str]):
    return steps(*pairs)


def _p(
    rng: random.Random,
    skill_id: str,
    *,
    prompt: str,
    answer: str,
    display: str,
    hint: str,
    mistakes: list[str],
    step_pairs: list[tuple[str, str]],
    tags: list[str],
    cluster: str,
    plot: str | None = None,
    plot_data: dict | None = None,
) -> Problem:
    return make_problem(
        id=f"{skill_id}-{rng.randrange(10**9)}",
        skill_id=skill_id,
        prompt=prompt,
        answer=str(answer),
        answer_display=display,
        hint=hint,
        common_mistakes=mistakes,
        exam_tags=tags,
        source="generated",
        cluster=cluster,
        steps=_steps(*step_pairs),
        plot=plot,
        plot_data=plot_data or {},
    )


AP1 = ["ap_physics1"]
AP2 = ["ap_physics2"]
BOTH = ["ap_physics1", "ap_physics2"]
G = 10  # m/s^2 — stated in every prompt that uses it


def phy_avg_motion(rng: random.Random, skill_id: str) -> Problem:
    x0, x = rng.choice([0, 2, 4]), rng.choice([12, 16, 20, 24])
    t = rng.choice([2, 4, 5])
    v = (x - x0) / t
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A cart moves in a straight line from $x = {x0}\\,\\mathrm{{m}}$ to "
            f"$x = {x}\\,\\mathrm{{m}}$ in ${t}\\,\\mathrm{{s}}$. "
            "What is the average velocity in m/s? Sign matters: right is positive."
        ),
        answer=str(int(v) if v == int(v) else v),
        display=f"{v:g} m/s",
        hint="Average velocity is displacement over time, not the path length over time.",
        mistakes=["Using the speed formula with distance if the cart had turned around."],
        step_pairs=[
            ("Goal", "Average velocity is how fast the position coordinate changed, including direction."),
            ("Displacement, not distance", f"Δx = x_final − x_initial = {x} − {x0} = {x - x0} m. That is a signed change in position."),
            ("Divide by the time interval", f"v_avg = Δx / Δt = {x - x0}/{t} = {v:g} m/s."),
            ("Check the sign", "The cart ended farther in the positive direction, so the average velocity is positive. Units are m/s."),
        ],
        tags=AP1,
        cluster="kinematics",
        plot="motion_1d",
        plot_data={"x0": x0, "x": x},
    )


def phy_kinematics(rng: random.Random, skill_id: str) -> Problem:
    v0 = rng.choice([0, 2, 4, 6])
    a = rng.choice([2, 3, 4, 5])
    t = rng.choice([2, 3, 4])
    v = v0 + a * t
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A box starts at ${v0}\\,\\mathrm{{m/s}}$ and speeds up at a constant "
            f"${a}\\,\\mathrm{{m/s^2}}$ for ${t}\\,\\mathrm{{s}}$. "
            "What is the final speed in m/s?"
        ),
        answer=str(v),
        display=f"{v} m/s",
        hint="For constant acceleration, v = v₀ + a t. Do not square anything unless you need v² = v₀² + 2aΔx.",
        mistakes=["Using v = a t and dropping v₀, or mixing in Δx when it was not given."],
        step_pairs=[
            ("Goal", "Constant acceleration means velocity changes by the same amount each second."),
            ("Pick the matching equation", "We know v₀, a, and t, and we want v. That is v = v₀ + a t. (The Δx equations are for a different unknown.)"),
            ("Substitute", f"v = {v0} + ({a})({t}) = {v0} + {a * t} = {v} m/s."),
            ("Sense check", f"Each second adds {a} m/s, so after {t} s the extra speed is {a * t} m/s on top of {v0} m/s."),
        ],
        tags=AP1,
        cluster="kinematics",
        plot="vt",
        plot_data={"v0": v0, "a": a, "t": t},
    )


def phy_freefall(rng: random.Random, skill_id: str) -> Problem:
    # h = (1/2) g t^2 with g = 10, pick t so h is nice
    t = rng.choice([2, 3, 4])
    h = (G * t * t) // 2
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A stone is dropped from rest and hits the ground after ${t}\\,\\mathrm{{s}}$. "
            f"Take $g = {G}\\,\\mathrm{{m/s^2}}$ and ignore air. How far did it fall, in meters?"
        ),
        answer=str(h),
        display=f"{h} m",
        hint="Dropped means v₀ = 0. Then Δy = (1/2) g t² (downward taken as positive here).",
        mistakes=["Using Δy = g t (missing the 1/2), or putting g = 9.8 after the problem said to use 10."],
        step_pairs=[
            ("Goal", "Free fall with constant g is just 1-D kinematics with a = g and v₀ = 0 if it is dropped."),
            ("Choose downward as positive", f"Then a = +{G} m/s² and v₀ = 0, so Δy = v₀ t + (1/2) a t² = (1/2)({G})({t})²."),
            ("Compute t² first", f"t² = {t * t}. Then (1/2)({G})({t * t}) = {G // 2} · {t * t} = {h} m."),
            ("Check", f"In {t} s at g = {G}, a dropped object falls {h} m — on the order of a building story times a few, which is reasonable."),
        ],
        tags=AP1,
        cluster="kinematics",
        plot="freefall",
        plot_data={"h": h},
    )


def phy_projectile(rng: random.Random, skill_id: str) -> Problem:
    v = rng.choice([10, 20, 30])
    # 45° : range = v^2 / g
    r = v * v // G
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A ball is kicked from level ground at ${v}\\,\\mathrm{{m/s}}$ at $45^\\circ$. "
            f"Take $g = {G}\\,\\mathrm{{m/s^2}}$ and ignore air. What is the range in meters?"
        ),
        answer=str(r),
        display=f"{r} m",
        hint="At 45°, range = v²/g. Equivalently, v_x = v_y = v/√2, then time of flight 2 v_y / g.",
        mistakes=["Using v/g or (1/2) v t, or forgetting that 45° makes the sine of 2θ equal to 1."],
        step_pairs=[
            ("Goal", "Range is the horizontal distance until the ball returns to the same height."),
            ("Why 45° is special", r"The range formula is R = v² sin(2θ)/g. At 45°, 2θ = 90° and sin 90° = 1, so R = v²/g."),
            ("Substitute", f"R = ({v})² / {G} = {v * v}/{G} = {r} m."),
            ("Split-component check", f"v_x = v_y = {v}/√2. Hang time is 2 v_y / g, then R = v_x t, which simplifies to the same {r} m."),
        ],
        tags=AP1,
        cluster="kinematics",
        plot="projectile",
        plot_data={"v": v, "g": G},
    )


def phy_n2(rng: random.Random, skill_id: str) -> Problem:
    m = rng.choice([2, 4, 5, 8])
    a = rng.choice([2, 3, 4, 5])
    f = m * a
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A net force of ${f}\\,\\mathrm{{N}}$ acts on a ${m}\\,\\mathrm{{kg}}$ crate "
            "on a frictionless floor. What is the acceleration in m/s²?"
        ),
        answer=str(a),
        display=f"{a} m/s²",
        hint="Newton's second law is ΣF = m a, so a = F_net / m. Use the net force, not a single leftover force.",
        mistakes=["Multiplying F and m, or using weight mg instead of the given net force."],
        step_pairs=[
            ("Goal", "Acceleration is caused by the net force, not by being 'in motion'."),
            ("Write ΣF = m a", f"The problem already gives the net force {f} N and the mass {m} kg."),
            ("Solve for a", f"a = F_net / m = {f}/{m} = {a} m/s²."),
            ("Direction", "The acceleration is in the same direction as the net force. The number asked here is the magnitude."),
        ],
        tags=AP1,
        cluster="forces",
        plot="fbd",
        plot_data={"kind": "net"},
    )


def phy_friction(rng: random.Random, skill_id: str) -> Problem:
    n = rng.choice([20, 40, 50, 80])
    mu = rng.choice([0.2, 0.25, 0.4, 0.5])
    f = mu * n
    ans = int(f) if f == int(f) else f
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A crate is sliding. The normal force is ${n}\\,\\mathrm{{N}}$ and "
            f"$\\mu_k = {mu:g}$. What is the kinetic friction force in newtons?"
        ),
        answer=str(ans),
        display=f"{ans:g} N",
        hint="Kinetic friction is f_k = μ_k N. N is the normal force, which is not always equal to the weight.",
        mistakes=["Using μ mg when N was already given, or using static μ_s for a sliding crate."],
        step_pairs=[
            ("Goal", "Kinetic friction opposes sliding and has a simple magnitude once N and μ_k are known."),
            ("Formula", "f_k = μ_k N. Do not put a cosine here unless you are finding a component of a different force."),
            ("Multiply", f"Kinetic friction is μ_k times the normal: f_k = ({mu:g})({n}) = {ans:g} N."),
            ("What it does", f"That {ans:g} N pulls backward on the crate. Newton's second law would then use F_net = F_applied − f_k."),
        ],
        tags=AP1,
        cluster="forces",
        plot="fbd",
        plot_data={"kind": "friction"},
    )


def phy_weight(rng: random.Random, skill_id: str) -> Problem:
    m = rng.choice([2, 3, 5, 8, 10])
    w = m * G
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A {m} kg backpack sits at rest on a table. Take $g = {G}\\,\\mathrm{{m/s^2}}$. "
            "What is the normal force from the table, in newtons?"
        ),
        answer=str(w),
        display=f"{w} N",
        hint="At rest, ΣF_y = 0 so n = mg (no other vertical forces). Weight is mg, not m.",
        mistakes=["Reporting the mass in kilograms as if it were the force, or using n = m."],
        step_pairs=[
            ("Goal", "The table's normal force is whatever it takes to keep the backpack from accelerating vertically."),
            ("Free-body", f"Down: weight mg = {m}·{G} = {w} N. Up: normal n. At rest, a = 0 so n − mg = 0."),
            ("Solve", f"n = {w} N. That is equal in magnitude to the weight here, but they are not the same force."),
            ("Newton 3 reminder", "The backpack's weight is Earth pulling the pack. The normal is the table pushing the pack. Equal size here is from equilibrium, not from Newton's third law."),
        ],
        tags=AP1,
        cluster="forces",
        plot="fbd",
        plot_data={"kind": "weight"},
    )


def phy_work(rng: random.Random, skill_id: str) -> Problem:
    f = rng.choice([10, 15, 20, 25])
    d = rng.choice([2, 3, 4, 6])
    w = f * d
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A constant ${f}\\,\\mathrm{{N}}$ force pulls a crate {d} m in the same direction "
            "as the force. How much work does that force do, in joules?"
        ),
        answer=str(w),
        display=f"{w} J",
        hint="W = F d cosθ. Here θ = 0°, so cosθ = 1 and W = F d.",
        mistakes=["Using F/d, or putting mass into the formula when only F and d were given."],
        step_pairs=[
            ("Goal", "Work by a constant force is the force component along the displacement, times the distance."),
            ("Angle is zero", "The force is along the motion, so cos 0° = 1 and W = F d."),
            ("Multiply", f"Work is force times distance here: W = ({f} N)({d} m) = {w} J."),
            ("Meaning", f"{w} J is the energy transferred to the crate by this force. Other forces could still do negative work."),
        ],
        tags=AP1,
        cluster="energy",
        plot="fbd",
        plot_data={"kind": "net"},
    )


def phy_ke_pe(rng: random.Random, skill_id: str) -> Problem:
    m = rng.choice([2, 4, 5])
    v = rng.choice([4, 6, 8, 10])
    ke = m * v * v // 2
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A {m} kg cart moves at ${v}\\,\\mathrm{{m/s}}$. "
            "What is its kinetic energy in joules?"
        ),
        answer=str(ke),
        display=f"{ke} J",
        hint="K = (1/2) m v². Square the speed first; do not do (1/2)(m v)².",
        mistakes=["Forgetting the 1/2, or squaring m v instead of v."],
        step_pairs=[
            ("Goal", "Kinetic energy depends on mass and on speed squared — twice the speed is four times the K."),
            ("Write the formula", r"Kinetic energy is $K = \tfrac12 m v^2$ — mass times speed squared, then half."),
            ("Square, then multiply", f"v² = {v * v}. Then (1/2)({m})({v * v}) = {m / 2:g} · {v * v} = {ke} J."),
            ("Check", "Joules are N·m = kg·m²/s², which matches (kg)(m/s)²."),
        ],
        tags=AP1,
        cluster="energy",
        plot="carts",
        plot_data={"m1": m, "m2": ""},
    )


def phy_energy_cons(rng: random.Random, skill_id: str) -> Problem:
    m = rng.choice([2, 3, 4])
    h = rng.choice([5, 20])
    v = int((2 * G * h) ** 0.5)
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A {m} kg block slides down a frictionless ramp from rest, dropping {h} m "
            f"in height. Take $g = {G}\\,\\mathrm{{m/s^2}}$. "
            "How fast is it going at the bottom, in m/s?"
        ),
        answer=str(v),
        display=f"{v} m/s",
        hint="Mechanical energy is conserved. mgh at the top becomes (1/2)mv² at the bottom. Mass cancels.",
        mistakes=["Using v = g t with no time given, or forgetting the square root after 2gh."],
        step_pairs=[
            ("Goal", "No friction and no other nonconservative work means K + U is constant."),
            ("Top and bottom", f"Top: K = 0, U = mgh. Bottom: U = 0, K = (1/2) m v². So (1/2) m v² = m g h."),
            ("Cancel m and solve", f"v² = 2 g h = 2({G})({h}) = {2 * G * h}. Then v = √{2 * G * h} = {v} m/s."),
            ("Why mass vanished", "A heavier block has more potential energy and also more inertia. On a frictionless ramp they cancel, so the speed is the same as free fall from height h."),
        ],
        tags=AP1,
        cluster="energy",
        plot="ramp",
        plot_data={"h": h},
    )


def phy_impulse(rng: random.Random, skill_id: str) -> Problem:
    f = rng.choice([8, 10, 12, 20])
    t = rng.choice([2, 3, 5])
    j = f * t
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A {f} N net force acts on a cart for {t} s. "
            "What is the impulse on the cart, in N·s?"
        ),
        answer=str(j),
        display=f"{j} N·s",
        hint="Impulse J = F_net Δt, and it equals the change in momentum.",
        mistakes=["Dividing F by t, or reporting F as if it were already the impulse."],
        step_pairs=[
            ("Goal", "Impulse is the push delivered over a time interval. It equals Δp."),
            ("Constant force", "For a constant net force, J = F Δt."),
            ("Multiply", f"J = ({f})({t}) = {j} N·s (same as {j} kg·m/s)."),
            ("What it does", f"The cart's momentum changes by {j} kg·m/s in the direction of the force."),
        ],
        tags=AP1,
        cluster="momentum",
        plot="fbd",
        plot_data={"kind": "net"},
    )


def phy_collision(rng: random.Random, skill_id: str) -> Problem:
    m1 = rng.choice([2, 3])
    m2 = rng.choice([2, 4, 6])
    v1 = rng.choice([6, 8, 12])
    # perfectly inelastic, m2 at rest
    v = (m1 * v1) / (m1 + m2)
    ans = int(v) if v == int(v) else v
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A {m1} kg cart at ${v1}\\,\\mathrm{{m/s}}$ hits a {m2} kg cart at rest. "
            "They stick together. What is the speed after the collision, in m/s?"
        ),
        answer=str(ans),
        display=f"{ans:g} m/s",
        hint="Sticking is perfectly inelastic. Momentum is conserved; kinetic energy is not. m1 v1 = (m1+m2) v.",
        mistakes=["Averaging the speeds, or conserving kinetic energy as if it were elastic."],
        step_pairs=[
            ("Goal", "No external horizontal force (ideal track) means total momentum is the same before and after."),
            ("Before", f"p = m1 v1 + m2 · 0 = ({m1})({v1}) = {m1 * v1} kg·m/s."),
            ("After they stick", f"One object of mass {m1 + m2} kg moves at speed v, so ({m1 + m2}) v = {m1 * v1}."),
            ("Solve", f"v = {m1 * v1}/{m1 + m2} = {ans:g} m/s. Kinetic energy dropped; that missing energy went into deformation and heat."),
        ],
        tags=AP1,
        cluster="momentum",
        plot="carts",
        plot_data={"m1": m1, "m2": m2},
    )


def phy_centripetal(rng: random.Random, skill_id: str) -> Problem:
    v = rng.choice([4, 6, 8, 10])
    r = rng.choice([2, 4, 5])
    a = v * v / r
    ans = int(a) if a == int(a) else a
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A ball on a string moves in a horizontal circle of radius {r} m at "
            f"${v}\\,\\mathrm{{m/s}}$. What is the centripetal acceleration in m/s²?"
        ),
        answer=str(ans),
        display=f"{ans:g} m/s²",
        hint="a_c = v²/r, toward the center. Do not use a = v/t unless you are given a time.",
        mistakes=["Using v/r or v² r, or calling this a tangential acceleration (that would change the speed)."],
        step_pairs=[
            ("Goal", "Uniform circular motion has constant speed but changing direction, so there is a center-pointing acceleration."),
            ("Formula", r"The centripetal acceleration is $a_c = v^2 / r$, with v the speed and r the radius."),
            ("Substitute", f"a_c = ({v})² / {r} = {v * v}/{r} = {ans:g} m/s²."),
            ("Direction", f"The acceleration (and the net force m a_c) points toward the center. The speed stays {v} m/s."),
        ],
        tags=AP1,
        cluster="circular",
        plot="circle_motion",
        plot_data={"r": r},
    )


def phy_gravity(rng: random.Random, skill_id: str) -> Problem:
    factor = rng.choice([2, 3, 4])
    g_new = G / (factor * factor)
    ans = int(g_new) if g_new == int(g_new) else g_new
    return _p(
        rng,
        skill_id,
        prompt=(
            f"On a planet, g = {G} m/s² at the surface. A second planet has the same mass "
            f"but {factor} times the radius. What is g at that surface, in m/s²?"
        ),
        answer=str(ans),
        display=f"{ans:g} m/s²",
        hint="g = GM / R². Same M and a bigger R means g shrinks as 1/R².",
        mistakes=["Dividing g by the radius factor once (1/R instead of 1/R²)."],
        step_pairs=[
            ("Goal", "Surface gravity comes from Newton's law of gravity: mg = GMm / R², so g = GM/R²."),
            ("What changes", f"M is the same. R becomes {factor} R. Then g' = GM / ({factor} R)² = g / {factor * factor}."),
            ("Compute", f"g' = {G}/{factor * factor} = {ans:g} m/s²."),
            ("Picture", "A larger planet with the same mass is 'spread out' — you are farther from the center, so gravity at the surface is weaker."),
        ],
        tags=AP1,
        cluster="circular",
        plot="gravity",
        plot_data={"factor": factor},
    )


def phy_torque(rng: random.Random, skill_id: str) -> Problem:
    f = rng.choice([10, 20, 30, 40])
    d = rng.choice([2, 3, 4])
    tau = f * d
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A {f} N force is applied perpendicular to a wrench {d} m from a bolt. "
            "What is the torque about the bolt, in N·m?"
        ),
        answer=str(tau),
        display=f"{tau} N·m",
        hint="τ = r F sinθ. Perpendicular means θ = 90°, so τ = r F.",
        mistakes=["Using r + F, or forgetting that only the perpendicular component of F produces torque."],
        step_pairs=[
            ("Goal", "Torque measures how effectively a force twists an object about a pivot."),
            ("Right angle", "sin 90° = 1, so τ = r F. (If the force were along the wrench, τ would be 0.)"),
            ("Multiply", f"Torque is lever arm times force: τ = ({d} m)({f} N) = {tau} N·m."),
            ("Equilibrium note", f"To hold a bolt still, another torque of {tau} N·m the other way would be needed so Στ = 0."),
        ],
        tags=AP1,
        cluster="circular",
        plot="wrench",
        plot_data={"d": d},
    )


def phy_shm(rng: random.Random, skill_id: str) -> Problem:
    # T = 2π √(m/k) = π when m/k = 1/4, e.g. m=1, k=4 or m=4, k=16
    m = rng.choice([1, 4])
    k = 4 * m
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A mass {m} kg is on a spring with k = {k} N/m. "
            r"What is the period of SHM in seconds? Use $\pi$ if it appears (enter pi)."
        ),
        answer="pi",
        display="π s",
        hint="T = 2π √(m/k) for a mass-spring. Amplitude does not appear.",
        mistakes=["Using T = 2π √(k/m) (upside down), or thinking a bigger amplitude makes a longer period."],
        step_pairs=[
            ("Goal", "The period of a mass on a spring depends only on m and k, not on how far you stretch it."),
            ("Formula", r"The mass-spring period is $T = 2\pi\sqrt{m/k}$. Amplitude does not appear."),
            ("Ratio", f"m/k = {m}/{k} = {m / k}. √(m/k) = √({m / k}) = { (m / k) ** 0.5:g}."),
            ("Finish", f"T = 2π · {(m / k) ** 0.5:g} = π seconds. Enter pi."),
        ],
        tags=AP1,
        cluster="waves",
        plot="spring",
        plot_data={},
    )


def phy_wave(rng: random.Random, skill_id: str) -> Problem:
    f = rng.choice([20, 40, 50, 100])
    lam = rng.choice([2, 4, 5, 8])
    v = f * lam
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A wave has frequency {f} Hz and wavelength {lam} m. "
            "What is the wave speed in m/s?"
        ),
        answer=str(v),
        display=f"{v} m/s",
        hint="v = f λ. Frequency in Hz is 1/s, so Hz·m = m/s.",
        mistakes=["Adding f and λ, or using v = f/λ."],
        step_pairs=[
            ("Goal", "Wave speed is how fast a crest travels through the medium, not how fast a particle of the medium oscillates."),
            ("The universal wave relation", "v = f λ holds for sound, light, and string waves (with different what determines v)."),
            ("Multiply", f"Wave speed is frequency times wavelength: v = ({f} Hz)({lam} m) = {v} m/s."),
            ("Picture", f"Each second, {f} crests pass. Each is {lam} m apart, so the lead crest advances {v} m."),
        ],
        tags=AP1,
        cluster="waves",
        plot="wave",
        plot_data={"lam": lam},
    )


def phy_ohm(rng: random.Random, skill_id: str) -> Problem:
    v = rng.choice([6, 9, 12, 24])
    r = rng.choice([2, 3, 4, 6])
    i = v // r
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A {v} V battery is connected across a {r} Ω resistor. "
            "What is the current in amperes?"
        ),
        answer=str(i),
        display=f"{i} A",
        hint="Ohm's law: I = V / R. Current is in amperes when V is in volts and R in ohms.",
        mistakes=["Using I = V R, or mixing up voltage drop with current."],
        step_pairs=[
            ("Goal", "Ohm's law relates the voltage across a resistor to the current through it."),
            ("Write I = V/R", f"The resistor sees the full battery voltage {v} V (single-resistor circuit)."),
            ("Divide", f"Current is voltage over resistance: I = {v}/{r} = {i} A."),
            ("Direction", "Conventional current leaves the positive terminal. The size is {i} A either way you draw it."),
        ],
        tags=BOTH,
        cluster="circuits",
        plot="circuit",
        plot_data={"kind": "ohm", "V": v, "R": r},
    )


def phy_pressure(rng: random.Random, skill_id: str) -> Problem:
    f = rng.choice([40, 50, 80, 100])
    a = rng.choice([0.2, 0.4, 0.5, 2])
    p = f / a
    ans = int(p) if p == int(p) else p
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A force of {f} N is spread evenly over {a:g} m². "
            "What is the pressure in pascals?"
        ),
        answer=str(ans),
        display=f"{ans:g} Pa",
        hint="P = F / A. One pascal is one newton per square meter.",
        mistakes=["Using F A, or mixing this with hydrostatic ρgh when no depth was given."],
        step_pairs=[
            ("Goal", "Pressure is force concentrated on an area — same force on a smaller area is more pressure."),
            ("Formula", "P = F/A, with F perpendicular to the surface."),
            ("Divide", f"Pressure is force over area: P = {f}/{a:g} = {ans:g} Pa."),
            ("Name", "Pascals are N/m². Atmospheric pressure is about 10⁵ Pa, so this number should be judged against that scale."),
        ],
        tags=AP2,
        cluster="fluids",
        plot="piston",
        plot_data={},
    )


def phy_buoyancy(rng: random.Random, skill_id: str) -> Problem:
    v = rng.choice([0.01, 0.02, 0.05])
    rho = 1000
    fb = rho * G * v
    ans = int(fb) if fb == int(fb) else fb
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A rock of volume {v:g} m³ is fully underwater. "
            f"Water has density 1000 kg/m³. Take $g = {G}\\,\\mathrm{{m/s^2}}$. "
            "What is the buoyant force in newtons?"
        ),
        answer=str(ans),
        display=f"{ans:g} N",
        hint="Archimedes: F_b = ρ_fluid V_displaced g. Fully submerged means V_displaced = V_object.",
        mistakes=["Using the rock's mass instead of the fluid density, or dropping g so the answer is in kg."],
        step_pairs=[
            ("Goal", "Buoyant force equals the weight of the fluid that used to sit in that volume."),
            ("Displaced volume", f"Fully under, V_disp = {v:g} m³."),
            ("Weight of that water", f"F_b = ρ V g = (1000)({v:g})({G}) = {ans:g} N."),
            ("Next step in a real problem", "Compare F_b to the rock's true weight to see if it sinks (it will, if the rock is denser than water)."),
        ],
        tags=AP2,
        cluster="fluids",
        plot="buoyancy",
        plot_data={},
    )


def phy_continuity(rng: random.Random, skill_id: str) -> Problem:
    a1 = rng.choice([0.02, 0.04])
    v1 = rng.choice([2, 3, 4])
    a2 = a1 / 2
    v2 = v1 * 2
    ans = int(v2) if v2 == int(v2) else v2
    return _p(
        rng,
        skill_id,
        prompt=(
            f"Water flows at ${v1:g}\\,\\mathrm{{m/s}}$ in a pipe of area {a1:g} m². "
            f"The pipe narrows to {a2:g} m². What is the speed in the narrow part, in m/s?"
        ),
        answer=str(ans),
        display=f"{ans:g} m/s",
        hint="Continuity: A1 v1 = A2 v2 for incompressible flow. Narrower means faster.",
        mistakes=["Setting A1 v1 = A2 / v2, or thinking the water slows down in a constriction."],
        step_pairs=[
            ("Goal", "The same volume of incompressible water has to pass every cross-section each second."),
            ("Continuity", "Incompressible flow keeps A v constant, so A1 v1 = A2 v2."),
            ("Solve", f"v2 = A1 v1 / A2 = ({a1:g})({v1:g})/{a2:g} = {ans:g} m/s."),
            ("Bernoulli hint", "Faster in the narrow part also means lower pressure there — that is the next AP Physics 2 idea."),
        ],
        tags=AP2,
        cluster="fluids",
        plot="pipe",
        plot_data={},
    )


def phy_ideal_gas(rng: random.Random, skill_id: str) -> Problem:
    p1 = rng.choice([100, 150, 200])
    factor = rng.choice([2, 3])
    p2 = p1 * factor
    return _p(
        rng,
        skill_id,
        prompt=(
            f"An ideal gas is trapped at constant volume. The Kelvin temperature is multiplied by {factor}. "
            f"If the original pressure was {p1} kPa, what is the new pressure in kPa?"
        ),
        answer=str(p2),
        display=f"{p2} kPa",
        hint="At constant V and n, P/T is constant (Gay-Lussac). Use Kelvin, which the problem already did.",
        mistakes=["Using Celsius, or thinking pressure stays the same at constant volume."],
        step_pairs=[
            ("Goal", "For a fixed amount of ideal gas, PV = nRT. If V and n are fixed, P is proportional to T."),
            ("Ratio form", "P1 / T1 = P2 / T2, so P2 = P1 (T2 / T1)."),
            ("Temperature factor", f"T2 / T1 = {factor}, so P2 = {p1} · {factor} = {p2} kPa."),
            ("Why Kelvin", "Doubling 20°C is not 40°C in the gas law. The problem already stated Kelvin, so the factor is honest."),
        ],
        tags=AP2,
        cluster="thermo",
        plot="piston",
        plot_data={},
    )


def phy_first_law(rng: random.Random, skill_id: str) -> Problem:
    q = rng.choice([40, 60, 80, 100])
    w = rng.choice([10, 20, 30])
    du = q - w
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A gas absorbs {q} J of heat and does {w} J of work on the surroundings. "
            r"Using $\Delta U = Q - W$ (W = work by the gas), what is $\Delta U$ in joules?"
        ),
        answer=str(du),
        display=f"{du} J",
        hint="First law: ΔU = Q − W when W is work done by the system. Heat in is positive Q.",
        mistakes=["Adding Q and W, or using W as work on the gas without flipping the sign."],
        step_pairs=[
            ("Goal", "The first law is energy accounting for a thermodynamic system."),
            ("Sign convention here", "Q > 0 means heat enters the gas. W > 0 means the gas does work (expands). Then ΔU = Q − W."),
            ("Subtract", f"Internal energy change is heat in minus work out: ΔU = {q} − {w} = {du} J."),
            ("Meaning", f"The internal energy rose by {du} J — some of the incoming heat was spent doing work, the rest stayed in the gas."),
        ],
        tags=AP2,
        cluster="thermo",
        plot="energy_bars",
        plot_data={"q": q, "w": w, "du": du},
    )


def phy_coulomb(rng: random.Random, skill_id: str) -> Problem:
    # F = k q1 q2 / r^2 with k=9e9, q=1e-6, r=0.1 -> 0.9 N
    r = rng.choice([0.1, 0.2])
    q = 1e-6
    f = 9e9 * q * q / (r * r)
    ans = int(f) if abs(f - round(f)) < 1e-9 else round(f, 3)
    return _p(
        rng,
        skill_id,
        prompt=(
            f"Two +1.0 μC charges are {r:g} m apart in empty space. "
            r"Use $k = 9.0\times 10^9\,\mathrm{N\cdot m^2/C^2}$. "
            "What is the repulsive force in newtons?"
        ),
        answer=str(ans),
        display=f"{ans:g} N",
        hint="F = k |q1 q2| / r². Convert μC to C: 1 μC = 10^{-6} C.",
        mistakes=["Forgetting to convert μC, or using r instead of r² in the denominator."],
        step_pairs=[
            ("Goal", "Coulomb's law is the electrostatic analog of Newton's gravity law."),
            ("Put charges in coulombs", r"$1.0\,\mu\mathrm{C} = 1.0\times 10^{-6}\,\mathrm{C}$."),
            (
                "Substitute",
                f"F = (9.0×10⁹)(1.0×10^{{-6}})² / ({r:g})² = (9.0×10⁹)(1.0×10^{{-12}}) / {r * r:g} = {ans:g} N.",
            ),
            ("Sign", "Same-sign charges repel. The number asked is the magnitude of that repulsive force."),
        ],
        tags=AP2,
        cluster="electro",
        plot="charges",
        plot_data={"r": r},
    )


def phy_efield(rng: random.Random, skill_id: str) -> Problem:
    q = rng.choice([0.02, 0.04, 0.05])
    e = rng.choice([20, 40, 50, 80])
    f = q * e
    ans = int(f) if f == int(f) else f
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A {q:g} C charge sits in a uniform electric field of {e:g} N/C. "
            "What is the electric force on the charge, in newtons?"
        ),
        answer=str(ans),
        display=f"{ans:g} N",
        hint="F = q E. The field's units N/C already mean 'newtons of force per coulomb of charge'.",
        mistakes=["Dividing E by q, or using F = k q / r² when no distance was given."],
        step_pairs=[
            ("Goal", "An electric field is a force-per-charge map. Once E is known, F is just qE."),
            ("Formula", "F = q E (magnitude). Direction: with E for a positive charge."),
            ("Multiply", f"F = ({q:g})({e:g}) = {ans:g} N."),
            ("Check units", "C · (N/C) = N. The field already included Coulomb's k and the source charges that made it."),
        ],
        tags=AP2,
        cluster="electro",
        plot="efield",
        plot_data={},
    )


def phy_req(rng: random.Random, skill_id: str) -> Problem:
    if rng.random() < 0.5:
        r1, r2 = rng.choice([2, 3, 4]), rng.choice([4, 5, 6])
        req = r1 + r2
        kind = "series"
        prompt = (
            f"Two resistors {r1} Ω and {r2} Ω are in series. "
            "What is the equivalent resistance in ohms?"
        )
        explain = f"Series: same current, resistances add. R_eq = {r1} + {r2} = {req} Ω."
    else:
        r1, r2 = 6, 3
        req = 2
        kind = "parallel"
        prompt = (
            f"Two resistors {r1} Ω and {r2} Ω are in parallel. "
            "What is the equivalent resistance in ohms?"
        )
        explain = (
            f"Parallel: 1/R_eq = 1/{r1} + 1/{r2} = {1/r1:g} + {1/r2:g} = {1/r1 + 1/r2:g}, "
            f"so R_eq = {req} Ω. (Always less than the smaller resistor.)"
        )
    return _p(
        rng,
        skill_id,
        prompt=prompt,
        answer=str(req),
        display=f"{req} Ω",
        hint="Series: add. Parallel: add inverses, then invert. Parallel R_eq is smaller than either branch.",
        mistakes=["Adding parallel resistors as if they were in series, or taking the average."],
        step_pairs=[
            ("Goal", "Replace a resistor network by one resistor that draws the same current from the battery."),
            ("Identify the connection", f"This problem is {kind}."),
            ("Compute", explain),
            ("Check", "Series R_eq is bigger than each piece. Parallel R_eq is smaller than each piece."),
        ],
        tags=BOTH,
        cluster="circuits",
        plot="circuit",
        plot_data={"kind": kind, "R1": r1, "R2": r2},
    )


def phy_magnetic(rng: random.Random, skill_id: str) -> Problem:
    q = rng.choice([0.02, 0.04])
    v = rng.choice([10, 20, 25])
    b = rng.choice([0.2, 0.4, 0.5])
    f = q * v * b  # sin 90 = 1
    ans = int(f) if abs(f - round(f)) < 1e-12 else round(f, 3)
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A {q:g} C charge moves at {v:g} m/s perpendicular to a {b:g} T magnetic field. "
            "What is the magnetic force in newtons?"
        ),
        answer=str(ans),
        display=f"{ans:g} N",
        hint="F = q v B sinθ. Perpendicular means sin 90° = 1.",
        mistakes=["Using F = q E, or putting sin 0° (parallel motion gives zero magnetic force)."],
        step_pairs=[
            ("Goal", "A magnetic field pushes a moving charge perpendicular to both v and B."),
            ("Angle", "θ = 90° between v and B, so sinθ = 1 and F = q v B."),
            ("Multiply", f"F = ({q:g})({v:g})({b:g}) = {ans:g} N."),
            ("Direction", "Right-hand rule for a positive charge: v fingers, curl toward B, thumb is F. The number asked is the magnitude."),
        ],
        tags=AP2,
        cluster="magnetism",
        plot="magnetic",
        plot_data={},
    )


def phy_snell(rng: random.Random, skill_id: str) -> Problem:
    n2 = rng.choice([1.5, 2.0])
    # n1=1, θ1=30, sin30=1/2, sinθ2 = 0.5/n2
    s2 = 0.5 / n2
    ans = s2
    # keep as fraction string
    if n2 == 1.5:
        answer, display = "1/3", "1/3"
    else:
        answer, display = "0.25", "0.25"
    return _p(
        rng,
        skill_id,
        prompt=(
            f"Light in air (n = 1.00) hits a material with n = {n2:g} at an incidence angle of 30°. "
            r"What is $\sin\theta_2$ in the material? Enter a decimal or a fraction."
        ),
        answer=answer,
        display=display,
        hint="Snell's law: n1 sinθ1 = n2 sinθ2. sin 30° = 1/2.",
        mistakes=["Setting n1 θ1 = n2 θ2 without the sines, or swapping θ1 and θ2."],
        step_pairs=[
            ("Goal", "Refraction bends the ray because the wave speed changes. Snell's law tracks the sines."),
            ("Write Snell", r"Snell's law is $n_1\sin\theta_1 = n_2\sin\theta_2$, with angles from the normal."),
            ("Plug in", f"(1) sin 30° = ({n2:g}) sinθ2. sin 30° = 1/2, so sinθ2 = (1/2)/{n2:g} = {display}."),
            ("Bigger n, smaller θ", "The ray bends toward the normal in the slower (larger n) material, so θ2 < 30° and sinθ2 < 1/2."),
        ],
        tags=AP2,
        cluster="optics",
        plot="snell",
        plot_data={"n2": n2},
    )


def phy_lens(rng: random.Random, skill_id: str) -> Problem:
    # 1/f = 1/do + 1/di with f=10, do=30 -> di=15
    f = 10
    do = rng.choice([15, 30])
    di = 1 / (1 / f - 1 / do)
    ans = int(di) if abs(di - round(di)) < 1e-9 else di
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A thin converging lens has focal length {f} cm. An object sits {do} cm away. "
            "How far from the lens is the image, in cm?"
        ),
        answer=str(ans),
        display=f"{ans:g} cm",
        hint="Thin-lens: 1/f = 1/d_o + 1/d_i. Solve for d_i. Distances are in cm here, keep them in cm.",
        mistakes=["Adding f and d_o, or using 1/f = d_o + d_i without the reciprocals."],
        step_pairs=[
            ("Goal", "The thin-lens equation locates the image for a given object distance and focal length."),
            ("Write reciprocals", rf"$1/f = 1/d_o + 1/d_i \Rightarrow 1/d_i = 1/{f} - 1/{do}$."),
            ("Compute", f"1/d_i = {1 / f:g} − {1 / do:g} = {1 / f - 1 / do:g}, so d_i = {ans:g} cm."),
            ("Sign meaning", "Positive d_i (this answer) is a real image on the far side of a converging lens."),
        ],
        tags=AP2,
        cluster="optics",
        plot="lens",
        plot_data={},
    )


def phy_photon(rng: random.Random, skill_id: str) -> Problem:
    lam = rng.choice([200, 400, 620])
    # E(eV) = 1240 / λ(nm)
    energy = 1240 / lam
    ans = int(energy) if abs(energy - round(energy)) < 1e-9 else round(energy, 2)
    return _p(
        rng,
        skill_id,
        prompt=(
            f"A photon has wavelength {lam} nm. Using $E(\\mathrm{{eV}}) = 1240 / \\lambda(\\mathrm{{nm}})$, "
            "what is the photon energy in eV?"
        ),
        answer=str(ans),
        display=f"{ans:g} eV",
        hint="This is E = hc/λ with hc packaged as 1240 eV·nm. Do not convert to meters unless you use 6.63×10^{-34}.",
        mistakes=["Multiplying 1240 by λ, or leaving λ in meters while using 1240."],
        step_pairs=[
            ("Goal", "A photon's energy is set by its frequency (or wavelength). This is the quantum idea behind the photoelectric effect."),
            ("The shortcut constant", r"$E = hc/\lambda$. With λ in nm and E in eV, hc ≈ 1240 eV·nm."),
            ("Divide", f"Photon energy in eV is 1240 over wavelength in nm: E = 1240/{lam} = {ans:g} eV."),
            ("Photoelectric link", "If this photon hits a metal with work function φ, leftover KE_max = E − φ (if E > φ)."),
        ],
        tags=AP2,
        cluster="modern",
        plot="wave",
        plot_data={"lam": max(lam / 100, 2)},
    )


PHYSICS_GENERATORS = {
    "phy_avg_motion": phy_avg_motion,
    "phy_kinematics": phy_kinematics,
    "phy_freefall": phy_freefall,
    "phy_projectile": phy_projectile,
    "phy_n2": phy_n2,
    "phy_friction": phy_friction,
    "phy_weight": phy_weight,
    "phy_work": phy_work,
    "phy_ke_pe": phy_ke_pe,
    "phy_energy_cons": phy_energy_cons,
    "phy_impulse": phy_impulse,
    "phy_collision": phy_collision,
    "phy_centripetal": phy_centripetal,
    "phy_gravity": phy_gravity,
    "phy_torque": phy_torque,
    "phy_shm": phy_shm,
    "phy_wave": phy_wave,
    "phy_ohm": phy_ohm,
    "phy_pressure": phy_pressure,
    "phy_buoyancy": phy_buoyancy,
    "phy_continuity": phy_continuity,
    "phy_ideal_gas": phy_ideal_gas,
    "phy_first_law": phy_first_law,
    "phy_coulomb": phy_coulomb,
    "phy_efield": phy_efield,
    "phy_req": phy_req,
    "phy_magnetic": phy_magnetic,
    "phy_snell": phy_snell,
    "phy_lens": phy_lens,
    "phy_photon": phy_photon,
}
