# Pre-Handoff Gate 005 after Frozen State / Start Audit Protocol

Status: FAILED
Project: Trading System
Architecture: v1.6.1
Gate date: 2026-06-17
Scope: GitHub main, read-only check before planned new chat handoff

## Scope

Checked areas:

A) Mandatory handoff context
- specs/94_start_audit_protocol.md
- specs/95_operational_workflow_rules.md
- specs/96_frozen_project_state.md
- specs/97_new_chat_handoff_prompt_v1.md
- specs/98_spec_index.md
- specs/99_handoff_snapshot_current.md

B) Core affected specs
- specs/14_station_8_order_validator.md
- specs/15_audit_log_core_v1.md
- specs/16_execution_simulator_core_v1.md
- specs/17_pre_order_proposed_order_contract_core_v1.md
- specs/18_portfolio_state_ledger_core_v1.md

C) Golden Cases / Config
- tests/golden_cases/station_8_order_validator_cases.json
- tests/golden_cases/audit_log_core_v1_cases.json
- tests/golden_cases/execution_simulator_core_v1_cases.json
- tests/golden_cases/pre_order_contract_core_v1_cases.json
- tests/golden_cases/portfolio_state_ledger_core_v1_cases.json
- config/rule_registry.yaml

## Summary

KRITISCH: 0
MITTEL: 1
REDAKTIONELL: 0 blockierend
Handoff recommendation: NO

## Finding G005-MITTEL-001 — Simulator state boundary inconsistency

Severity: MITTEL
Status: OPEN

### Befund

The new audit protocol and Frozen State define a hard architecture invariant:

- Simulator results may influence risk logic but must never create Portfolio State.
- The simulator feedback channel must be a constraint channel, not a state channel.
- State changes are reserved for reconciliation of real broker/exchange fills.

Current existing specs still contain an older, weaker model:

- Spec 16 requires `post_execution_portfolio` as simulator output.
- Spec 16 describes serial hypothetical cash/position updates during simulation.
- Spec 18 allows `SIMULATED_POST_EXECUTION` as a portfolio_state_type.
- Spec 18 states that the Execution Simulator creates `SIMULATED_POST_EXECUTION`.
- Golden Cases still expect simulated post-execution portfolio artefacts and ledger storage of SIMULATED_POST_EXECUTION.

### Bewertung

This is not yet proven data corruption and therefore not KRITISCH.

It is a real architecture contract inconsistency and therefore MITTEL:

- Either the new hard invariant must be narrowed to mean no official / confirmed Portfolio State.
- Or Spec 16, Spec 18 and related Golden Cases must be adjusted so the Execution Simulator outputs only ExecutionConstraint / SimulationReport and never Portfolio State / Ledger State.

Until this is resolved, a new chat handoff would carry conflicting architecture instructions.

### Required resolution before handoff

One explicit architecture decision is required:

Option A — Constraint-only simulator
- Execution Simulator outputs ExecutionConstraint / SimulationReport only.
- Remove or reclassify `post_execution_portfolio` and `SIMULATED_POST_EXECUTION` as non-ledger, non-state scenario artefacts.
- Update Spec 16, Spec 18 and Golden Cases.

Option B — Simulated state allowed but not official state
- Keep `SIMULATED_POST_EXECUTION`, but define it as a strictly non-official, non-reconciliation, non-current ledger scenario state.
- Narrow the hard invariant in 94/96 from `no Portfolio State` to `no official/current/reconciliation State`.
- Add explicit wording preventing any transition to CURRENT_CONFIRMED without real reconciliation.

No automatic choice was made in this gate.

## PASS checks

A) Handoff context includes 94 and 96.

B) Frozen State is compact and not a replacement for specs.

C) `frozen` rule exists and includes deletion/replacement review.

D) Operational workflow correctly states GitHub main as canonical technical project state.

E) Station 8 remains FINAL and is not re-opened by this gate.

F) Audit Core remains FINAL and audit-compatible with Execution Simulator events.

G) ProposedOrder remains DRAFT and clearly before Station 8.

H) Portfolio Ledger still protects against automatic SIMULATED_POST_EXECUTION -> CURRENT_CONFIRMED conversion.

## Required file updates from this gate

Update required:

- specs/95_operational_workflow_rules.md
- specs/97_new_chat_handoff_prompt_v1.md
- specs/98_spec_index.md
- specs/99_handoff_snapshot_current.md

No update required:

- specs/94_start_audit_protocol.md
- specs/96_frozen_project_state.md

Reason: 94/96 express the current hard rule. The gate failure must be reflected in workflow/handoff/index/snapshot, not silently softened.

## Final gate result

Pre-Handoff Gate 005: FAILED

Handoff is blocked until G005-MITTEL-001 is resolved or explicitly reclassified by a new architecture decision.
