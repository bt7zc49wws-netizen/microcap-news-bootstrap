# Execution Boundary Policy

Status: DRAFT

Purpose:
- Keep broker integration, IBKR dependency, order generation, and trading execution out of scope until the final phase.

Scope:
- broker boundary
- IBKR boundary
- order generation boundary
- trading execution boundary
- live readiness safety gate

Policy:
- No live readiness task may create orders.
- No live readiness task may send orders.
- No live readiness task may require IBKR.
- No live readiness task may require broker credentials.
- Any decision output before the final execution phase is analytical only.
- Actionable decisions before execution phase are not execution intents.
- Execution-related code paths must remain isolated from live provider readiness work.
