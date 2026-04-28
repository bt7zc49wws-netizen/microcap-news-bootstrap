# News Decision Adapter Contract v1

Status: DRAFT

Purpose:
Define how news classification output is adapted into decision-context news input.

Scope:
- Offline-safe adaptation only
- No live provider calls
- No paid API dependency
- No broker integration
- No trading execution
- No scoring

Adapter:
- Function: adapt_news_for_decision
- Module: src/app/news_decision_adapter.py
- Smoke: scripts/quant/smoke_news_decision_adapter.py

Required classification inputs:
- event_type
- headline

Decision-context news output:
- event_type
- headline

Rules:
- event_type must not be empty
- headline must not be empty
- provider/classifier extra fields must not leak into decision-context news input
- adapter must remain pure validation/adaptation


End-to-end decision path:
- Smoke: scripts/quant/smoke_news_to_decision.py

Offline E2E chain:
- classification output
- adapt_news_for_decision
- build_decision_context
- evaluate_decision_context
- canonical decision result

E2E rules:
- The chain must remain offline-safe.
- The chain must not call live providers.
- The chain must not use paid APIs.
- The chain must not perform broker, order, or execution operations.
