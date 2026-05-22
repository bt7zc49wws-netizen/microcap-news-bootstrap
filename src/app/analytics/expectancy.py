from __future__ import annotations

from app.analytics.labels import label_event


def compute_expectancy(events: list[dict]) -> dict:
    scored = []

    for e in events:
        decision = e["output"]["decision"]
        ctx = decision.get("decision_context", {})

        score = ctx.get("decision_score", 0.0)
        future_return = label_event(e)

        scored.append((score, future_return))

    if not scored:
        return {"expectancy": 0.0, "score_edge": 0.0}

    n = len(scored)

    avg_r = sum(x[1] for x in scored) / n
    avg_s = sum(x[0] for x in scored) / n

    cov = sum((s - avg_s) * (r - avg_r) for s, r in scored) / n
    var = sum((s - avg_s) ** 2 for s, _ in scored) / n

    return {
        "expectancy": avg_r,
        "score_edge": cov / (var + 1e-9),
        "samples": n,
    }
