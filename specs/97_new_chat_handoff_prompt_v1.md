# New Chat Handoff Prompt v1

Wir arbeiten im Projekt Trading System.

Bitte nutze den hochgeladenen vollständigen Projektstand als Wahrheit. Keine Annahmen erfinden und keine nicht konsolidierten ZIP-/Patch-/Handoff-Stände als Wahrheit behandeln.

## Arbeitsmodus

A) Wir arbeiten primär auf Spezifikationsebene.
B) Fokus: Form, Struktur, Schnittstellen, Regeln, Statuslogik, Architekturgrenzen, Parameter und Golden Cases.
C) Code nur sparsam als Referenz/Pseudocode, wenn absolute Eindeutigkeit notwendig ist.
D) Implementierung bleibt später Codex überlassen.
E) Spezifikationen kompakt, menschenlesbar und ohne Redundanz formulieren.

## Aktueller Stand

A) Station 8 — Order Validator
Abgeschlossen und konsolidiert um station_8_validation_ref sowie validated_order_list[].order_ref.

B) Audit-Log Core v1.0
Abgeschlossen und erweitert um audit-kompatible Execution-Simulator-Events.

C) Execution Simulator Core v1.0
Status: DRAFT. Enthält Input/Output, Simulationsannahmen, Fill-Regeln, Cash/Portfolio/Liquidität, Short-Regeln, Statuslogik, Audit-Anbindung und Golden Cases.

## Wichtige Dateien

- specs/14_station_8_order_validator.md
- specs/15_audit_log_core_v1.md
- specs/16_execution_simulator_core_v1.md
- specs/98_spec_index.md
- specs/99_handoff_snapshot_current.md
- tests/golden_cases/station_8_order_validator_cases.json
- tests/golden_cases/audit_log_core_v1_cases.json
- tests/golden_cases/execution_simulator_core_v1_cases.json

## Wichtige Regeln

A) Execution Simulator ist keine Station 9.
B) Keine Pipelinewirkung durch Simulator-FAILED.
C) Eigene Execution-Event-Typen bleiben erhalten: EXECUTION_SIMULATION_SUCCESS, EXECUTION_SIMULATION_PARTIAL, EXECUTION_SIMULATION_FAILED.
D) Keine Zuordnung auf RULE_PASS, RULE_REJECTED oder TECHNICAL_ERROR.
E) validator_status = PASS bleibt neutral; simulation_status wird separat geführt.
F) Rückverfolgbarkeit: station_8_validation_ref → validated_order_list[].order_ref → simulated_fills[].source_order_ref.

## Nächster Schritt

Zuerst projektübergreifende Konsistenzprüfung durchführen. Erst danach Git aktualisieren und finales vollständiges Projekt-ZIP erstellen.
