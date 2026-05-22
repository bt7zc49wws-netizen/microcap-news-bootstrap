from __future__ import annotations


def evaluate_alpha(events: list[dict]) -> dict:
    pairs = []

    for e in events:
        decision = e["output"]["decision"]

        ctx = decision.get("decision_context", {})
        score = ctx.get("decision_score", 0.0)

        # synthetic return already computed in pipeline or fallback
        ret = 0.0
        if "label" in e:
            ret = e["label"]

        pairs.append((score, ret))

    if not pairs:
        return {"alpha": 0.0}

    n = len(pairs)

    avg_s = sum(p[0] for p in pairs) / n
    avg_r = sum(p[1] for p in pairs) / n

    cov = sum((s - avg_s) * (r - avg_r) for s, r in pairs) / n
    var_s = sum((s - avg_s) ** 2 for s, _ in pairs) / n

    alpha = cov / (var_s + 1e-9)

    return {
        "alpha": alpha,
        "samples": n
    }
