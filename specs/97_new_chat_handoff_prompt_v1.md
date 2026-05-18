# New Chat Handoff Prompt v1

Wir arbeiten im Projekt Trading System.

Bitte nutze den hochgeladenen vollständigen Projektstand ausschließlich als Read-only-Lesestand.

## Harte Übergaberegel

In der ersten Phase gilt:

- Keine Dateien ändern.
- Keine Patches erzeugen.
- Keine ZIPs erzeugen.
- Keine PowerShell-Scripts schreiben.
- Keine Encoding-, BOM-, CRLF-, LF- oder Whitespace-Reparaturen vorschlagen.
- Keine abgeschlossenen Specs erneut konsolidieren.
- Keine bestehenden Specs redaktionell glätten.
- Keine Implementierung beginnen.

Die erste Antwort soll nur enthalten:

A) ZIP gelesen
B) relevante Dateien gefunden
C) aktueller Stand verstanden
D) projektweite Konsistenzprüfung
E) Befunde nach Schweregrad
F) Übergabestand verwendbar: Ja/Nein
G) nächster fachlicher Vorschlag

## Arbeitsmodus

A) Wir arbeiten primär auf Spezifikationsebene.
B) Fokus: Form, Struktur, Schnittstellen, Regeln, Statuslogik, Architekturgrenzen, Parameter und Golden Cases.
C) Code nur sparsam als Referenz/Pseudocode, wenn absolute Eindeutigkeit notwendig ist.
D) Implementierung bleibt später Codex überlassen.
E) Spezifikationen kompakt, menschenlesbar und ohne Redundanz formulieren.

## Aktueller Stand

A) Station 8 — Order Validator
Status: FINAL. An ProposedOrder angebunden. Jede validierte Order enthält order_ref und source_proposed_order_ref.

B) Audit-Log Core v1.0
Status: FINAL. Audit-kompatible Execution-Simulator-Events sind integriert.

C) Execution Simulator Core v1.0
Status: DRAFT. Integration abgeschlossen. Kein Bestandteil der Validierungs-Pipeline und keine Station 9.

D) Pre-Order / Proposed Order Contract Core v1.0
Status: DRAFT. Definiert den Vertrag zwischen strategischer Entscheidung / Rebalancing-Logik und Station 8.

## Wichtige Dateien

- specs/14_station_8_order_validator.md
- specs/15_audit_log_core_v1.md
- specs/16_execution_simulator_core_v1.md
- specs/17_pre_order_proposed_order_contract_core_v1.md
- specs/98_spec_index.md
- specs/99_handoff_snapshot_current.md
- tests/golden_cases/station_8_order_validator_cases.json
- tests/golden_cases/audit_log_core_v1_cases.json
- tests/golden_cases/execution_simulator_core_v1_cases.json
- tests/golden_cases/pre_order_contract_core_v1_cases.json

## Wichtige Regeln

A) Execution Simulator ist keine Station 9.
B) Keine Pipelinewirkung durch Simulator-FAILED.
C) Eigene Execution-Event-Typen bleiben erhalten: EXECUTION_SIMULATION_SUCCESS, EXECUTION_SIMULATION_PARTIAL, EXECUTION_SIMULATION_FAILED.
D) Keine Zuordnung auf RULE_PASS, RULE_REJECTED oder TECHNICAL_ERROR.
E) validator_status = PASS bleibt neutral; simulation_status wird separat geführt.
F) ProposedOrder ist keine validierte oder ausführbare Order.
G) Station 8 bleibt die fachliche Order-Validierung.
H) Rückverfolgbarkeit: proposed_order_ref → source_proposed_order_ref / order_ref → source_order_ref.

## Projektweite Read-only-Prüfung

Bitte prüfe das gesamte hochgeladene Projekt-ZIP read-only auf:

A) Projektstruktur
B) Spezifikationskonsistenz
C) Golden Cases
D) Handoff / Index
E) Redundanz / Struktur
F) offensichtliche Übergabelücken

Keine Dateien ändern. Keine Scripts. Keine Patches. Keine ZIPs.

## Nächster fachlicher Kandidat

Spec 18 — Portfolio State / Portfolio Ledger Core v1.0.

Bitte nur fachlich vorschlagen, wie Spec 18 aufgebaut werden sollte. Noch keine lokale Dateiänderung.
