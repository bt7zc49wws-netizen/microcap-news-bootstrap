from app.replay.replay_engine import run_replay
from app.analytics.alpha import evaluate_alpha


def run_alpha_replay(events: list[dict]) -> dict:
    replayed = [run_replay(e) for e in events]

    return {
        "results": replayed,
        "alpha_metrics": evaluate_alpha(replayed),
    }
