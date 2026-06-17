# Pre-Handoff Gate 010 Next Work Item Spec 16

Status: PASSED
Project: Trading System
Architecture: v1.6.1
Gate date: 2026-06-18
Scope: GitHub main, handoff correction after missing next work item

## Cause check

The previous new chat did not propose `Spec 16 ergaenzen` because the handoff snapshot did not name a concrete next work item.

The New Prompt instructed the new chat to use the handoff snapshot for the next step. Since the snapshot only contained the start prompt, the new chat inferred a broad audit instead of the targeted Spec 16 change.

## Corrections

A) specs/97_new_chat_handoff_prompt_v1.md now states that the next work item must come from specs/99_handoff_snapshot_current.md when explicitly set there.

B) specs/99_handoff_snapshot_current.md now contains the concrete next work item: targeted Spec 16 addition.

C) specs/93_new_chat_transition_protocol.md now requires the handoff snapshot to contain either a concrete next work item or an explicit statement that no next work item is set.

## Summary

KRITISCH: 0
MITTEL: 0
REDAKTIONELL: 0 blockierend
Handoff recommendation: YES

## Next work item for new chat

Spec 16 gezielt ergaenzen.

Section: Simulation Feedback / Execution Constraint Boundary.

Goal: The Execution Simulator provides an ExecutionConstraintReport / SimulationReport. This feedback channel may influence replanning, order reduction, blocking, Pre-Execution Risk Gate or a new isolated planning pass. It must never create or replace official Portfolio State, CURRENT_CONFIRMED, Ledger Current State, Reconciliation, real fills, real positions or official risk state.

Before editing, read-only check Spec 16, Spec 18, 94/96 and relevant golden cases. Then propose the minimal required change to Spec 16.

## Final gate result

Pre-Handoff Gate 010: PASSED

Handoff is allowed.
