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

    def stddev(xs):
        if len(xs) < 2:
            return 0.0

        mean = avg(xs)
        variance = sum((x - mean) ** 2 for x in xs) / len(xs)

        return variance ** 0.5

    def win_rate(xs):
        if not xs:
            return 0.0

        wins = sum(1 for x in xs if x > 0)

        return wins / len(xs)

    result = {}

    for name, values in buckets.items():
        result[name] = {
            "avg_return": avg(values),
            "samples": len(values),
            "stddev": stddev(values),
            "win_rate": win_rate(values),
        }

    result["monotonic"] = (
        result["HIGH"]["avg_return"]
        >= result["MID"]["avg_return"]
        >= result["LOW"]["avg_return"]
    )

    return result
