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

        if "label" in e:
            ret = e["label"]
        else:
            ret = e["output"].get("label", 0.0)

        b = bucket_score(score)
        buckets[b].append(ret)

    def avg(xs):
        return sum(xs) / len(xs) if xs else 0.0

    result = {}

    for name, values in buckets.items():
        result[name] = {
            "avg_return": avg(values),
            "samples": len(values),
        }

    result["monotonic"] = (
        result["HIGH"]["avg_return"]
        >= result["MID"]["avg_return"]
        >= result["LOW"]["avg_return"]
    )

    return result
