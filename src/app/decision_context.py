"""Build decision context from offline-safe news and quant inputs.

Rules:
- no live provider calls
- no paid API dependency
- no broker integration
- no trading execution
- pure composition only
"""

from __future__ import annotations
