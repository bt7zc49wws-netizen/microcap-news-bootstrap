# Scheduled Ingestion Runbook

Status: DRAFT

Purpose:
- Define the first operational runbook for scheduled live ingestion before paid APIs, broker integration, IBKR, order generation, or trading execution.

Scope:
- scheduled news ingestion
- scheduled market/fundamental ingestion
- run cadence ownership
- pre-run checks
- post-run validation
- failure visibility

Out of scope:
- paid APIs
- broker integration
- IBKR dependency
- order generation
- trading execution

Initial runbook:
- Confirm Docker services are healthy before scheduled ingestion.
- Confirm provider credentials/config are present only for explicitly enabled free/live providers.
- Run ingestion jobs with bounded timeout and retry policy.
- Validate freshness/staleness after ingestion completes.
- Quarantine malformed or partial records according to ingestion validation rules.
- Do not allow scheduled ingestion failure to silently produce actionable decisions.
- Record run status, provider status, freshness status, and failure reason when applicable.
