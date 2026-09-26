"""
# Algebra · Trig · Precalculus study app

A local Streamlit app for returning students. Every in-app problem has a
checkable answer and a step-by-step solution written for people who have
not done math in a long time.

## Run locally

```powershell
cd C:\Users\gertt\calc1-prep
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
pytest
```

Open the URL Streamlit prints (usually http://localhost:8501).

## How the diagnostic works

The placement test is **not** a grade. It finds the earliest chapter you
should actually study so you do not redo algebra you still have, and so
you do not jump into trig with shaky factoring.

1. **Four stages, eight questions each**, one at a time.
2. **Stage 1 — Algebra foundations:** order of operations, exponents,
   radicals, factoring, rational expressions, linear and quadratic
   equations, inequalities.
3. **Stage 2 — College algebra / functions:** function notation, domain,
   composition, transformations, inverses, vertex of a parabola, logs
   and exponentials.
4. **Stage 3 — Trigonometry:** radians, unit circle, right triangles,
   period, inverse sine, a basic identity, counting solutions, triangle
   angle sum.
5. **Stage 4 — Precalculus extras:** systems, conics, polar, sequences,
   binomial theorem, a limit, vectors, a matrix entry.

You need about **70% on a stage to continue**. If a stage is below that,
the app **stops** and places you at the first missed skill in that stage.
That is on purpose: later stages would just measure guessing.

You still get a list of every missed skill, even on stages you passed, so
a single rusty topic does not vanish.

After the test, study in the app and use **Extra practice** for more
volume. In **Study**, pick **Precalculus (full course)** for the complete
AP/CLEP path (functions through limits). Extra practice **Precalculus**
uses that same full pool, not only polar/matrices/conics.

## Where extra practice (with answers) comes from

College Board AP/CLEP exams are copyrighted, so this app does **not**
copy those tests. Extra drills come from open (Creative Commons) books:

- **OpenStax Algebra and Trigonometry 2e** (CC BY 4.0). Odd-numbered
  section exercises, Try It problems, and practice tests have answers in
  the book answer key.
  https://openstax.org/books/algebra-and-trigonometry-2e/
- **OpenStax Precalculus 2e** (CC BY 4.0) for limits and extra precalc.
  https://openstax.org/books/precalculus-2e/
- **Stitz–Zeager Precalculus** (free PDF). Answers to nearly all
  computational exercises are in the text.
  http://www.stitz-zeager.com/

Each skill in the app links to the matching OpenStax section. In-app
problems are original (generated or authored) so every one can ship with
a full walkthrough, not just a final number.

## Credit exams this catalog maps to

There is no AP Algebra or AP Trigonometry exam. The credit exams are:

- CLEP College Algebra
- CLEP Precalculus
- AP Precalculus (Units 1–3 on the exam; Unit 4 is in the catalog anyway)

## Deploy later (public URL)

1. Push this folder to a GitHub repository.
2. Go to https://share.streamlit.io and deploy `app.py`.
3. Keep `requirements.txt` as-is. Do not add secrets.

Progress is stored in the browser session (download JSON from the
Progress page if you want a backup). No login in this version.

## Project layout

- `app.py` — Streamlit UI
- `src/curriculum.py` — full algebra / trig / precalc skill tree
- `src/generate.py` — algebra problem generators with filled-in steps
- `src/diagnostic_bank.py` — 32 authored diagnostic items
- `src/check.py` — sympy answer checking
- `tests/` — quality gate (no problem without a real solution)
"""
# calculus-prep
