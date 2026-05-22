from app.replay.replay_engine import run_replay
from app.risk.gate import risk_gate
from app.execution.executor import execute_decision


def run_live(event: dict, state):
    result = run_replay(event)["output"]

    ctx = result.get("decision_context", {})
    confidence = ctx.get("confidence", 0.0)

    if not risk_gate(result, confidence):
        return {"status": "blocked"}

    return execute_decision(state, event["symbol"], result)
