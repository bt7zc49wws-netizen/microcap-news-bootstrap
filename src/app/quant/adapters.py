"""Adapt provider market data into provider-independent market snapshots.

This module prepares data for:
- validate_market_snapshot
- build_quant_signal_from_snapshot

Rules:
- no paid API dependency
- no trading execution
- no broker integration
- provider-specific fields must not leak into quant signal output
"""

from __future__ import annotations
