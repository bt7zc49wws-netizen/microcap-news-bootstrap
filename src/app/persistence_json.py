"""Persistence JSON helpers."""

from __future__ import annotations

import json
from typing import Any


def dumps_json_object(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True)


def dumps_json_list(value: list[str]) -> str:
    return json.dumps(sorted(set(str(item) for item in value)))
