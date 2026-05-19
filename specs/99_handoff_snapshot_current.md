# Handoff Snapshot Current

Status: CURRENT
Project: Trading System
Architecture: v1.6.1
Snapshot date: 2026-05-19

## Aktueller Stand

A) Station 8 — Order Validator
Final abgeschlossen und konsolidiert um station_8_validation_ref sowie order_ref pro validierter Order.

B) Audit-Log Core v1.0
Final abgeschlossen und erweitert um audit-kompatible Execution-Simulator-Events nach Station 8.

C) Execution Simulator Core v1.0
Als konsistenter DRAFT abgeschlossen. Enthält Rolle, Input/Output, Output-/Report-Contract, Simulationsannahmen, Fill-/Preis-/Slippage-Regeln, Cash/Portfolio/Liquidität, Short-Regeln, Statuslogik, Audit-Log-Anbindung, Golden Cases und Codex-Hinweis.

D) Pre-Order / Proposed Order Contract Core v1.0
Als DRAFT angelegt. Definiert den Vertrag zwischen strategischer Entscheidung / Rebalancing-Logik und Station 8 Order Validator.

## Wichtige Dateien

- specs/14_station_8_order_validator.md
- specs/15_audit_log_core_v1.md
- specs/16_execution_simulator_core_v1.md
- specs/17_pre_order_proposed_order_contract_core_v1.md
- tests/golden_cases/station_8_order_validator_cases.json
- tests/golden_cases/audit_log_core_v1_cases.json
- tests/golden_cases/execution_simulator_core_v1_cases.json
- tests/golden_cases/pre_order_contract_core_v1_cases.json
- specs/98_spec_index.md
- specs/97_new_chat_handoff_prompt_v1.md

## Wichtige Entscheidungen

A) Execution Simulator ist keine Station 9.
B) Execution Simulator verändert keine Pipeline- oder Systemstatus.
C) Execution-Simulator-Events behalten eigene event_type-Werte: EXECUTION_SIMULATION_SUCCESS, EXECUTION_SIMULATION_PARTIAL, EXECUTION_SIMULATION_FAILED.
D) Execution-Simulator-Events werden nicht auf RULE_PASS, RULE_REJECTED oder TECHNICAL_ERROR gemappt.
E) validator_status bleibt PASS; simulation_status wird separat geführt.
F) Simulator-FAILED bedeutet: Simulation nicht belastbar, nicht Station 8 ungültig, kein Pipeline-Stopp.
G) Rückverfolgbarkeit: proposed_order_ref → source_proposed_order_ref / order_ref → source_order_ref.
H) Keine erneute Konsolidierung von Specs 14/15/16 ohne konkreten Fehlerbefund.
I) ProposedOrder ist ein Vorschlag vor Station 8, keine validierte oder ausführbare Order.
J) Station 8 ist an ProposedOrder angebunden; jede validierte Order erhält source_proposed_order_ref und order_ref.

## Nächster Schritt

Nächster fachlicher Kandidat: Spec 18 — Portfolio State / Portfolio Ledger Core v1.0.
