from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

MIN_STEPS = 4


class ProblemValidationError(ValueError):
    pass


@dataclass
class Step:
    title: str
    text: str

    def validate(self) -> None:
        if not self.title.strip():
            raise ProblemValidationError("Every step needs a title.")
        if len(self.text.strip()) < 20:
            raise ProblemValidationError(
                "Every step needs a real explanation (not a one-liner)."
            )


@dataclass
class Problem:
    id: str
    skill_id: str
    prompt: str
    answer: str
    answer_display: str
    steps: list[Step]
    hint: str
    common_mistakes: list[str]
    difficulty: str = "core"
    exam_tags: list[str] = field(default_factory=list)
    source: str = "original"
    cluster: str = ""
    stage: int | None = None
    plot: str | None = None
    plot_data: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.id.strip():
            raise ProblemValidationError("Problem id is required.")
        if not self.skill_id.strip():
            raise ProblemValidationError(f"{self.id}: skill_id is required.")
        if len(self.prompt.strip()) < 8:
            raise ProblemValidationError(f"{self.id}: prompt is too short.")
        if not str(self.answer).strip():
            raise ProblemValidationError(f"{self.id}: answer is required.")
        if not self.answer_display.strip():
            raise ProblemValidationError(f"{self.id}: answer_display is required.")
        if not self.hint.strip():
            raise ProblemValidationError(f"{self.id}: hint is required.")
        if len(self.steps) < MIN_STEPS:
            raise ProblemValidationError(
                f"{self.id}: need at least {MIN_STEPS} solution steps, got {len(self.steps)}."
            )
        for step in self.steps:
            step.validate()
        if not self.common_mistakes:
            raise ProblemValidationError(f"{self.id}: list at least one common mistake.")


def problem_from_dict(data: dict[str, Any]) -> Problem:
    steps = [Step(title=s["title"], text=s["text"]) for s in data["steps"]]
    problem = Problem(
        id=data["id"],
        skill_id=data["skill_id"],
        prompt=data["prompt"],
        answer=str(data["answer"]),
        answer_display=data["answer_display"],
        steps=steps,
        hint=data["hint"],
        common_mistakes=list(data.get("common_mistakes") or []),
        difficulty=data.get("difficulty", "core"),
        exam_tags=list(data.get("exam_tags") or []),
        source=data.get("source", "original"),
        cluster=data.get("cluster", ""),
        stage=data.get("stage"),
        plot=data.get("plot"),
        plot_data=dict(data.get("plot_data") or {}),
    )
    problem.validate()
    return problem


def steps(*pairs: tuple[str, str]) -> list[Step]:
    return [Step(title=t, text=x) for t, x in pairs]


def make_problem(**kwargs) -> Problem:
    problem = Problem(**kwargs)
    problem.validate()
    return problem
