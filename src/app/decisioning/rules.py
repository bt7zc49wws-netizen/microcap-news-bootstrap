from app.models.signal_snapshot import SignalSnapshot


def map_final_decision(signal: SignalSnapshot) -> dict:
    if signal.decision == "no_trade":
        return {
            "decision": "no_trade",
            "rule_id": "no_trade_passthrough",
            "reason_code": "SIGNAL_NO_TRADE",
            "reason_label": "Signal resolved to no-trade path.",
            "decision_summary": "Signal resolved to no-trade path.",
            "decision_context": '{"source":"signal","rule":"no_trade_passthrough"}',
        }

    if signal.primary_ticker == "ABCD":
        return {
            "decision": "actionable",
            "rule_id": "abcd_actionable_seed",
            "reason_code": "WATCHLIST_ESCALATED_TO_ACTIONABLE",
            "reason_label": "Watchlist signal escalated to actionable decision.",
            "decision_summary": "Watchlist signal escalated to actionable decision.",
            "decision_context": '{"source":"signal","rule":"abcd_actionable_seed"}',
        }

    return {
        "decision": "watchlist",
        "rule_id": "watchlist_passthrough",
        "reason_code": "SIGNAL_WATCHLIST",
        "reason_label": "Signal remained in watchlist state.",
        "decision_summary": "Signal remained in watchlist state.",
        "decision_context": '{"source":"signal","rule":"watchlist_passthrough"}',
    }
