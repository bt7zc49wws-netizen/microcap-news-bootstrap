"""Batch replay + basic performance metrics."""

from __future__ import annotations

from app.replay.replay_engine import run_replay


def run_batch_replay(events: list[dict]) -> dict:
    results = [run_replay(e) for e in events]

    decisions = [r["output"]["decision"] for r in results]

    summary = {
        "total": len(results),
        "watchlist": decisions.count("watchlist"),
        "no_trade": decisions.count("no_trade"),
        "actionable": decisions.count("actionable"),
    }

    return {
        "results": results,
        "summary": summary,
    }
