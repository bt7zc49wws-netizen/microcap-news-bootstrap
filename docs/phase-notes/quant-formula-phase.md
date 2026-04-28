# Quant Formula Phase

Status: DONE

Scope completed:
- API-independent pure formula layer
- price_change_pct
- gap_pct
- intraday_return_pct
- relative_volume
- dollar_volume
- range_pct
- close_location_value
- VWAP
- VWAP distance %
- true range
- ATR
- ATR %
- breakout %
- slope
- acceleration
- smoke script

Rules preserved:
- no paid API
- no trading execution
- no IBKR
- pure functions only
- tests green before commit
- current architecture preserved

Latest validation:
- quant formula smoke ok
- 125 passed


Contract:
- docs/contracts/quant-signal-contract-v1.md
