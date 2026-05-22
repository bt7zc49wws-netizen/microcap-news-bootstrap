"""Safe JSON serialization helpers."""

from __future__ import annotations

import json
from typing import Any


def loads_json_object(value: str) -> dict[str, Any]:
    try:
        data = json.loads(value)
    except Exception:
        return {}

    return data if isinstance(data, dict) else {}


def loads_json_list(value: str) -> list[str]:
    try:
        data = json.loads(value)
    except Exception:
        return []

    if not isinstance(data, list):
        return []

    return [str(item) for item in data]
