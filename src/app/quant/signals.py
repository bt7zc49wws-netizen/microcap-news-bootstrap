"""Build canonical quant signals from validated market snapshots.

This module must stay API-independent:
- no provider clients
- no network calls
- no database access
- no trading execution
"""

from __future__ import annotations
