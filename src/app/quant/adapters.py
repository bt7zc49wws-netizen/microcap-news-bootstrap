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

from app.quant.snapshot import REQUIRED_MARKET_SNAPSHOT_FIELDS, validate_market_snapshot


def adapt_market_snapshot(payload: dict[str, float]) -> dict[str, float]:
    """Adapt already-normalized market payload into validated market snapshot."""
    snapshot = {
        field: payload[field]
        for field in REQUIRED_MARKET_SNAPSHOT_FIELDS
    }
    return validate_market_snapshot(snapshot)

def adapt_mapped_market_snapshot(
    payload: dict[str, float],
    field_map: dict[str, str],
) -> dict[str, float]:
    """Adapt provider payload using a provider-to-canonical field map.

    field_map format:
    {
        "canonical_field": "provider_field"
    }
    """
    mapped_payload = {
        canonical_field: payload[provider_field]
        for canonical_field, provider_field in field_map.items()
    }
    return adapt_market_snapshot(mapped_payload)

