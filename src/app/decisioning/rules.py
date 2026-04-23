from app.models.signal_snapshot import SignalSnapshot


def _matches_no_trade_passthrough(signal: SignalSnapshot) -> bool:
    return signal.decision == "no_trade"


def _matches_abcd_actionable_seed(signal: SignalSnapshot) -> bool:
    return (
        signal.decision == "watchlist"
        and signal.primary_ticker == "ABCD"
        and signal.reason_code == "FINANCING_KEYWORD_MATCH"
    )


def _matches_watchlist_passthrough(signal: SignalSnapshot) -> bool:
    return signal.decision == "watchlist"


DECISION_RULES = [
    {
        "rule_id": "no_trade_passthrough",
        "evaluation_order": 10,
        "decision": "no_trade",
        "reason_code": "SIGNAL_NO_TRADE",
        "reason_label": "Signal resolved to no-trade path.",
        "decision_summary": "Signal resolved to no-trade path.",
        "eligibility_summary": "signal.decision == no_trade",
        "decision_context": '{"source":"signal","rule":"no_trade_passthrough"}',
        "matches": _matches_no_trade_passthrough,
    },
    {
        "rule_id": "abcd_actionable_seed",
        "evaluation_order": 20,
        "decision": "actionable",
        "reason_code": "WATCHLIST_ESCALATED_TO_ACTIONABLE",
        "reason_label": "Watchlist signal escalated to actionable decision.",
        "decision_summary": "Watchlist signal escalated to actionable decision.",
        "eligibility_summary": "signal.decision == watchlist AND primary_ticker == ABCD AND reason_code == FINANCING_KEYWORD_MATCH",
        "decision_context": '{"source":"signal","rule":"abcd_actionable_seed"}',
        "matches": _matches_abcd_actionable_seed,
    },
    {
        "rule_id": "watchlist_passthrough",
        "evaluation_order": 999,
        "decision": "watchlist",
        "reason_code": "SIGNAL_WATCHLIST",
        "reason_label": "Signal remained in watchlist state.",
        "decision_summary": "Signal remained in watchlist state.",
        "eligibility_summary": "signal.decision == watchlist",
        "decision_context": '{"source":"signal","rule":"watchlist_passthrough"}',
        "matches": _matches_watchlist_passthrough,
    },
]

DECISION_RULES_REGISTRY = {
    rule["rule_id"]: {
        "rule_id": rule["rule_id"],
        "evaluation_order": rule["evaluation_order"],
        "decision": rule["decision"],
        "reason_code": rule["reason_code"],
        "reason_label": rule["reason_label"],
        "decision_summary": rule["decision_summary"],
        "eligibility_summary": rule["eligibility_summary"],
    }
    for rule in DECISION_RULES
}


def map_final_decision(signal: SignalSnapshot) -> dict:
    for rule in sorted(DECISION_RULES, key=lambda r: r["evaluation_order"]):
        if rule["matches"](signal):
            return {
                "rule_id": rule["rule_id"],
                "decision": rule["decision"],
                "reason_code": rule["reason_code"],
                "reason_label": rule["reason_label"],
                "decision_summary": rule["decision_summary"],
                "decision_context": rule["decision_context"],
            }

    raise RuntimeError("no decision rule matched signal")
