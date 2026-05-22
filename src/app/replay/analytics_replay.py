from __future__ import annotations

from app.analytics.buckets import analyze_buckets
from app.analytics.expectancy import compute_expectancy
from app.replay.replay_engine import run_replay


def run_replay_with_metrics(events: list[dict]) -> dict:
    replayed = [run_replay(e) for e in events]

    metrics = compute_expectancy(replayed)
    bucket_metrics = analyze_buckets(replayed)

    return {
        "results": replayed,
        "metrics": metrics,
        "bucket_metrics": bucket_metrics,
    }
