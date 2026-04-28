"""Derive provider-independent market snapshot inputs from normalized OHLCV series.

Rules:
- no paid API dependency
- no trading execution
- no broker integration
- no provider client calls
- pure transformation only
"""

from __future__ import annotations
