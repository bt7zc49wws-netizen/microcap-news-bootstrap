from __future__ import annotations

from app.replay.replay_engine import run_replay
from app.analytics.expectancy import compute_expectancy

def run_replay_with_metrics(events: list[dict]) -> dict:
    replayed = [run_replay(e) for e in events]

    metrics = compute_expectancy(replayed)

    return {
        "results": replayed,
        "metrics": metrics,
    }
