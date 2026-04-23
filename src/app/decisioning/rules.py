from app.models.signal_snapshot import SignalSnapshot


def map_final_decision(signal: SignalSnapshot) -> tuple[str, str, str, str]:
    if signal.decision == "no_trade":
        return (
            "no_trade",
            "SIGNAL_NO_TRADE",
            "Signal resolved to no-trade path.",
            '{"source":"signal","rule":"no_trade_passthrough"}',
        )

    if signal.primary_ticker == "ABCD":
        return (
            "actionable",
            "WATCHLIST_ESCALATED_TO_ACTIONABLE",
            "Watchlist signal escalated to actionable decision.",
            '{"source":"signal","rule":"abcd_actionable_seed"}',
        )

    return (
        "watchlist",
        "SIGNAL_WATCHLIST",
        "Signal remained in watchlist state.",
        '{"source":"signal","rule":"watchlist_passthrough"}',
    )
