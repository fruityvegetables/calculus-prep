"""On-device handwriting pad. The browser reads the ink; Python only receives the text."""

from __future__ import annotations

from pathlib import Path

import streamlit.components.v1 as components

_PAD = components.declare_component(
    "handwriting",
    path=str(Path(__file__).resolve().parents[1] / "components" / "handwriting"),
)


def handwriting_pad(*, key: str) -> dict | None:
    value = _PAD(key=key, default=None)
    if isinstance(value, dict) and value.get("expression"):
        return value
    return None
