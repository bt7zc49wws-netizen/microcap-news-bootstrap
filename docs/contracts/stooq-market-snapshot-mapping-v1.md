# Stooq Market Snapshot Mapping v1

Status: DRAFT

Purpose:
Define how normalized Stooq market/fundamental data will map into the provider-independent market snapshot contract.

Scope:
- Mapping contract only
- No paid API dependency
- No trading execution
- No broker integration
- No decision engine
- No direct provider client changes in this step

Target output:
- docs/contracts/market-snapshot-contract-v1.md

Required canonical fields:
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

Notes:
- Stooq may not provide every required derived field directly.
- Missing derived fields must be computed upstream or rejected before quant signal calculation.
- Provider raw fields must not leak past the adapter boundary.
