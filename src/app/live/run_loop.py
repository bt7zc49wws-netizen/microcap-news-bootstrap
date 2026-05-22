from app.replay.replay_engine import run_replay
from app.execution.executor import execute_decision
from app.portfolio.state import PortfolioState


def run_once(*args):
    """
    Supports BOTH:
    - run_once(event)
    - run_once(state, event)
    """

    # case 1: run_once(event)
    if len(args) == 1:
        event = args[0]
        state = PortfolioState()

    # case 2: run_once(state, event)
    elif len(args) == 2:
        state, event = args

    else:
        raise ValueError("invalid arguments")

    # safety guard (CRITICAL)
    if not isinstance(event, dict):
        event = {
            "symbol": getattr(event, "symbol", "UNK"),
            "quant_signal": {},
            "news": {},
        }

    decision = run_replay(event)["output"]

    return execute_decision(state, event["symbol"], decision)
