# Market Snapshot Contract v1

Status: DRAFT

Purpose:
Define the validated market snapshot input required by the quant signal builder.

Scope:
- Input contract only
- Provider-independent
- No paid API dependency
- No trading execution
- No broker integration
- No scoring
- No decision engine

Required fields:
- current_price
- open_price
- high_price
- low_price
- previous_close
- current_volume
- average_volume
- vwap_value
- atr_value
- breakout_level

Rules:
- All values must be numeric.
- Denominator-like values must be positive where required by formulas.
- Snapshot validation must happen before build_quant_signal.
- Provider-specific raw fields must not leak into quant signal output.
- Missing required fields must reject the snapshot before quant signal calculation.

Consumer:
- src/app/quant/signals.py
- build_quant_signal

Output contract:
- docs/contracts/quant-signal-contract-v1.md


Adapter:
- Function: adapt_market_snapshot
- Module: src/app/quant/adapters.py
- Input: already-normalized provider market payload
- Output: validated provider-independent market snapshot
- Smoke: scripts/quant/smoke_market_snapshot_adapter.py

Adapter rules:
- Required fields are selected from the payload.
- Provider-specific extra fields are ignored.
- Missing required fields reject the adapter call.
- Output must satisfy validate_market_snapshot.
