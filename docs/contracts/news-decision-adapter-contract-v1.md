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
