from app.decision_engine import evaluate_decision_context


def run_replay(event: dict) -> dict:
    result = evaluate_decision_context(event)

    if "decision" not in result:
        result["decision"] = "no_trade"

    if "decision_context" not in result:
        result["decision_context"] = {
            "decision_score": 0.0,
            "confidence": 0.0,
            "risk_flags": []
        }

    return {
        "input": event,
        "output": {
            "decision": result
        }
    }
