# Quant Signal Contract v1

Status: ACTIVE_DRAFT

Purpose:
Define the canonical output names for the API-independent quant formula layer.

Scope:
- Pure calculated market signals only
- No provider-specific fields
- No paid API dependency
- No trading execution
- No broker integration

Canonical fields:
- price_change_pct
- gap_pct
- intraday_return_pct
- relative_volume
- dollar_volume
- range_pct
- close_location_value
- vwap
- vwap_distance_pct
- true_range
- atr
- atr_pct
- breakout_pct
- slope
- acceleration

Rules:
- Inputs must come from validated market data snapshots.
- Formula functions must remain pure.
- Formula functions must not perform network, database, broker, or filesystem operations.
- Missing or invalid denominator inputs must raise ValueError.
- Contract changes require tests and phase note update.

Current implementation:
- src/app/quant/formulas.py
- tests/quant/test_formulas.py
- scripts/quant/smoke_quant_formulas.py


Signal builder:
- Function: build_quant_signal
- Module: src/app/quant/signals.py
- Input: validated market snapshot values
- Output: canonical quant signal dict[str, float]
- Smoke: scripts/quant/smoke_quant_signal_builder.py

Builder output fields:
- price_change_pct
- gap_pct
- intraday_return_pct
- relative_volume
- dollar_volume
- range_pct
- close_location_value
- vwap_distance_pct
- atr_pct
- breakout_pct

Implementation guards:
- QUANT_SIGNAL_FIELDS is defined in src/app/quant/signals.py.
- build_quant_signal must raise ValueError if its output field set drifts from QUANT_SIGNAL_FIELDS.
- ENRICHED_MARKET_PAYLOAD_FIELDS is defined in src/app/quant/enrichment.py.
- enrich_stooq_market_payload must raise ValueError if its output field order drifts from ENRICHED_MARKET_PAYLOAD_FIELDS.
