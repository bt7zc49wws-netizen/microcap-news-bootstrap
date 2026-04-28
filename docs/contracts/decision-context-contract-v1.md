# Decision Context Contract v1

Status: DRAFT

Purpose:
Define the offline-safe context object that combines already-computed news and quant inputs before decision logic.

Scope:
- Context composition only
- No scoring
- No decision classification
- No live provider calls
- No paid API dependency
- No broker integration
- No trading execution

Builder:
- Function: build_decision_context
- Module: src/app/decision_context.py
- Smoke: scripts/quant/smoke_decision_context_builder.py

Required inputs:
- symbol
- news
- quant_signal

Output fields:
- symbol
- news
- quant_signal

Rules:
- symbol must not be empty
- news must not be empty
- quant_signal must not be empty
- symbol is normalized to uppercase
- news and quant_signal are already-computed inputs
- builder must remain pure composition
