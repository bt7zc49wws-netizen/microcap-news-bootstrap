from __future__ import annotations


def bucket_score(score: float) -> str:
    if score < 0.3:
        return "LOW"
    if score < 0.7:
        return "MID"
    return "HIGH"


def analyze_buckets(events: list[dict]) -> dict:
    buckets = {
        "LOW": [],
        "MID": [],
        "HIGH": [],
    }

    for e in events:
        score = e["output"]["decision"]["decision_context"]["decision_score"]
        ret = e["output"]["label"] if "label" in e["output"] else 0.0

        b = bucket_score(score)
        buckets[b].append(ret)

    def avg(xs):
        return sum(xs) / len(xs) if xs else 0.0

    return {
        "LOW": avg(buckets["LOW"]),
        "MID": avg(buckets["MID"]),
        "HIGH": avg(buckets["HIGH"]),
    }
