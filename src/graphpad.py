"""Coordinate grid the student draws a graph on."""

from __future__ import annotations

from pathlib import Path

import streamlit.components.v1 as components

_PAD = components.declare_component(
    "graphpad",
    path=str(Path(__file__).resolve().parents[1] / "components" / "graphpad"),
)


def graph_pad(*, key: str) -> dict | None:
    value = _PAD(key=key, default=None)
    if isinstance(value, dict) and value.get("points"):
        return value
    return None
