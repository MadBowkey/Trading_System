# New Prompt

Status: CURRENT
Project: Trading System
Last updated: 2026-06-18

## Purpose

This file is the long-form startup instruction for a new chat.

The short copy-paste prompt from the old chat points to this file. The new chat reads and executes this file.

## Repository

Repository: `MadBowkey/Trading_System`
Branch: `main`

GitHub `main` is the canonical technical project state.

## Required context

Read first:

- README.md
- specs/93_new_chat_transition_protocol.md
- specs/94_start_audit_protocol.md
- specs/95_operational_workflow_rules.md
- specs/96_frozen_project_state.md
- specs/97_new_chat_handoff_prompt_v1.md
- specs/98_spec_index.md
- specs/99_handoff_snapshot_current.md

Then read the current gate report named in `specs/99_handoff_snapshot_current.md`.

Also read the specs, golden cases and config files that are relevant to the current gate status or next work item.

## First phase

Begin read-only.

Check structure, handoff consistency, current gate status and open findings before proposing work.

## First response

Report briefly:

A) project state read
B) required files found
C) current gate status from 99
D) consistency result by severity
E) handoff usable yes/no
F) next suggested work item

The next suggested work item must come from `specs/99_handoff_snapshot_current.md`.

If `99` does not name a concrete next work item, report handoff usable: no. Do not infer a broad audit or substitute another work item.

## Short commands

`weiter` = next logical work step only.

`frozen` = curated Frozen State check and update if needed.

`uebergabe` / `übergabe` = run the New Chat Transition Protocol.

## Current project core

- Station 8: FINAL
- Audit Core v1.0: FINAL
- Execution Simulator Core v1.0: DRAFT
- Pre-Order Contract Core v1.0: DRAFT
- Portfolio State & Ledger Core v1.0: FINAL
- New Chat Transition Protocol: CURRENT
- Start Audit Protocol: CURRENT
- Frozen Project State: CURRENT

## Key boundary

SIMULATED_POST_EXECUTION may be stored or reported, but it is not confirmed and never becomes CURRENT_CONFIRMED automatically.

Simulation results may inform risk logic, but official confirmed portfolio state is updated only through reconciliation of real broker or exchange fills.

## Next step

Use `specs/99_handoff_snapshot_current.md` to identify the current next work item after the read-only check.
