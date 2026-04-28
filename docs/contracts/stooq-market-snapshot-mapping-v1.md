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

Initial normalized Stooq field map:

| Canonical field | Stooq normalized field | Status |
|---|---|---|
| current_price | close | DIRECT |
| open_price | open | DIRECT |
| high_price | high | DIRECT |
| low_price | low | DIRECT |
| previous_close | previous_close | REQUIRED_DERIVED_OR_UPSTREAM |
| current_volume | volume | DIRECT |
| average_volume | average_volume | REQUIRED_DERIVED_OR_UPSTREAM |
| vwap_value | vwap | REQUIRED_DERIVED_OR_UPSTREAM |
| atr_value | atr | REQUIRED_DERIVED_OR_UPSTREAM |
| breakout_level | breakout_level | REQUIRED_DERIVED_OR_UPSTREAM |

Rules:
- DIRECT fields may map from normalized Stooq OHLCV data.
- REQUIRED_DERIVED_OR_UPSTREAM fields must be supplied by an upstream normalization/enrichment step before adapter use.
- Adapter must reject snapshots where required derived fields are missing.
- This contract does not require Stooq client changes yet.


Implementation:
- Field map constant: STOOQ_MARKET_SNAPSHOT_FIELD_MAP
- Adapter function: adapt_stooq_market_snapshot
- Module: src/app/quant/adapters.py
- Smoke: scripts/quant/smoke_stooq_market_snapshot_adapter.py

Implementation rules:
- Adapter expects normalized Stooq-like payload keys.
- Derived/upstream-required fields must exist before adapter call.
- Adapter output must satisfy Market Snapshot Contract v1.
- Provider-specific extra fields must not leak into the snapshot.


Enrichment helpers:
- derive_previous_close
- derive_average_volume
- derive_vwap
- derive_atr
- derive_breakout_level
- Module: src/app/quant/enrichment.py
- Smoke: scripts/quant/smoke_stooq_enrichment_helpers.py

Enrichment rules:
- Helpers operate on normalized OHLCV rows.
- Helpers must not call provider clients.
- Helpers must not perform network, database, broker, or filesystem operations.
- Current row is excluded from completed-row lookback calculations where applicable.
- Derived values are intended to satisfy Market Snapshot Contract v1 before Stooq adapter use.


Payload enrichment:
- Function: enrich_stooq_market_payload
- Module: src/app/quant/enrichment.py
- Input: normalized OHLCV rows
- Output: normalized Stooq-like payload containing direct and derived fields
- Smoke: scripts/quant/smoke_stooq_market_payload_enrichment.py

Payload enrichment output fields:
- close
- open
- high
- low
- volume
- previous_close
- average_volume
- vwap
- atr
- breakout_level

Payload enrichment rules:
- Current row provides close/open/high/low/volume.
- Completed rows provide previous_close, average_volume, vwap, atr, and breakout_level.
- Provider client calls are forbidden.
- Network, database, broker, and filesystem operations are forbidden.
