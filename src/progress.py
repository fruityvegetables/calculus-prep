from __future__ import annotations

import json
from datetime import datetime, timezone


def empty_progress() -> dict:
    return {
        "started": datetime.now(timezone.utc).isoformat(),
        "diagnostic": None,
        "diagnostic_history": [],
        "attempts": [],
        "correct_by_skill": {},
        "wrong_by_skill": {},
    }


def record_attempt(progress: dict, skill_id: str, correct: bool, problem_id: str) -> None:
    progress["attempts"].append(
        {
            "skill_id": skill_id,
            "correct": correct,
            "problem_id": problem_id,
            "at": datetime.now(timezone.utc).isoformat(),
        }
    )
    key = "correct_by_skill" if correct else "wrong_by_skill"
    progress[key][skill_id] = progress[key].get(skill_id, 0) + 1


def record_diagnostic(progress: dict, rec: dict) -> None:
    stamped = {**rec, "at": rec.get("at") or datetime.now(timezone.utc).isoformat()}
    progress["diagnostic"] = stamped
    history = progress.setdefault("diagnostic_history", [])
    history.append(stamped)


def to_json(progress: dict) -> str:
    return json.dumps(progress, indent=2)
