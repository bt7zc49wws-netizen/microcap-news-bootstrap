from __future__ import annotations

from app.analytics.buckets import analyze_buckets
from app.analytics.expectancy import compute_expectancy
from app.replay.replay_engine import run_replay


def run_replay_with_metrics(events: list[dict]) -> dict:
    replayed = [run_replay(e) for e in events]

    metrics = compute_expectancy(replayed)
    bucket_metrics = analyze_buckets(replayed)

    quality_snapshot = {
        "expectancy": metrics.get("expectancy", 0.0),
        "high_bucket_avg_return": bucket_metrics["HIGH"]["avg_return"],
        "high_bucket_win_rate": bucket_metrics["HIGH"]["win_rate"],
        "high_bucket_stddev": bucket_metrics["HIGH"]["stddev"],
        "high_bucket_samples": bucket_metrics["HIGH"]["samples"],
        "monotonic": bucket_metrics["monotonic"],
    }

    expectancy_quality = (
        quality_snapshot["expectancy"]
        * quality_snapshot["high_bucket_win_rate"]
    ) / (1 + quality_snapshot["high_bucket_stddev"])

    return {
        "results": replayed,
        "metrics": metrics,
        "bucket_metrics": bucket_metrics,
        "quality_snapshot": quality_snapshot,
        "expectancy_quality": expectancy_quality,
    }
