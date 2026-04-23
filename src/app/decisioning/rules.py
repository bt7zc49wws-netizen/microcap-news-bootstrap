from app.models.signal_snapshot import SignalSnapshot


NO_TRADE_PASSTHROUGH_RULE = {
    "rule_id": "no_trade_passthrough",
    "decision": "no_trade",
    "reason_code": "SIGNAL_NO_TRADE",
    "reason_label": "Signal resolved to no-trade path.",
    "decision_summary": "Signal resolved to no-trade path.",
    "decision_context": '{"source":"signal","rule":"no_trade_passthrough"}',
}

ABCD_ACTIONABLE_SEED_RULE = {
    "rule_id": "abcd_actionable_seed",
    "decision": "actionable",
    "reason_code": "WATCHLIST_ESCALATED_TO_ACTIONABLE",
    "reason_label": "Watchlist signal escalated to actionable decision.",
    "decision_summary": "Watchlist signal escalated to actionable decision.",
    "decision_context": '{"source":"signal","rule":"abcd_actionable_seed"}',
}

WATCHLIST_PASSTHROUGH_RULE = {
    "rule_id": "watchlist_passthrough",
    "decision": "watchlist",
    "reason_code": "SIGNAL_WATCHLIST",
    "reason_label": "Signal remained in watchlist state.",
    "decision_summary": "Signal remained in watchlist state.",
    "decision_context": '{"source":"signal","rule":"watchlist_passthrough"}',
}


DECISION_RULES_REGISTRY = {
    "no_trade_passthrough": NO_TRADE_PASSTHROUGH_RULE,
    "abcd_actionable_seed": ABCD_ACTIONABLE_SEED_RULE,
    "watchlist_passthrough": WATCHLIST_PASSTHROUGH_RULE,
}


def map_final_decision(signal: SignalSnapshot) -> dict:
    if signal.decision == "no_trade":
        return DECISION_RULES_REGISTRY["no_trade_passthrough"]

    if signal.primary_ticker == "ABCD":
        return DECISION_RULES_REGISTRY["abcd_actionable_seed"]

    return DECISION_RULES_REGISTRY["watchlist_passthrough"]
