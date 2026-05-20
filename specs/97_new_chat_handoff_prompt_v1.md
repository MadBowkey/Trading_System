# New Chat Handoff Prompt v1

Wir arbeiten im Projekt Trading System.

## Pflichtkontext

Vor jeder fachlichen Weiterarbeit muss der neue Chat lesen und beachten:

- `specs/95_operational_workflow_rules.md`
- `specs/98_spec_index.md`
- `specs/99_handoff_snapshot_current.md`
- `_codex_reports/pre_handoff_gate_004_final_after_spt.md`

Letztes bestandenes Pre-Handoff Gate:

- Finales Pre-Handoff Gate 004 wurde auf damaligem `main`-Stand bestanden.
- KRITISCH: 0
- MITTEL: 0
- Handoff-Empfehlung: JA
- Nach spaeteren Repo-Aenderungen ist vor einer neuen Uebergabe erneut ein aktuelles Pre-Handoff-Gate erforderlich.

## Harte Uebergaberegel

In der ersten Phase gilt:

- Projektstand nur read-only pruefen.
- Keine Dateien aendern.
- Keine Patches erzeugen.
- Keine ZIPs erzeugen.
- Keine PowerShell-Scripts schreiben.
- Keine Encoding-, BOM-, CRLF-, LF- oder Whitespace-Reparaturen vorschlagen.
- Keine abgeschlossenen Specs erneut konsolidieren.
- Keine bestehenden Specs redaktionell glaetten.
- Keine Implementierung beginnen.

Die erste Antwort soll nur enthalten:

A) Projektstand gelesen
B) relevante Dateien gefunden
C) aktueller Stand verstanden
D) projektweite Konsistenzpruefung
E) Befunde nach Schweregrad
F) Uebergabestand verwendbar: Ja/Nein
G) naechster fachlicher Vorschlag

## Arbeitsmodus

A) Projektweite Struktur, Konsistenz, Reports und Sync laufen soweit moeglich ueber Codex plus GitHub-Rueckkanal.
B) Codex-relevante Vorgaenge werden soweit moeglich automatisiert; das Team soll keine PR-Nummern, Reports oder Diffs manuell suchen oder kopieren muessen.
C) Fachliche Spezifikation von Modulen, Schnittstellen, Statuslogik und Architekturentscheidungen erfolgt durch Team plus ChatGPT.
D) Codex darf fachliche Logik nicht erfinden und ergaenzt Golden Cases nur auf Basis bereits beschlossener Specs.
E) GitHub `main` ist der kanonische technische Projektstand. Lokale Ordner sind Arbeitskopien, nicht Wahrheit.
F) Backend- oder chat-only-Aenderungen gelten nicht als erledigt, solange sie nicht im Repo nachvollziehbar geaendert, geprueft und bei Bedarf auf GitHub `main` gemerged sind.
G) Lokale PowerShell-Dateiaenderungen muessen als ein vollstaendiger ausfuehrbarer Block geliefert werden; bei Datei-Schreibvorgaengen mit explizitem StreamWriter Write/Close und try/finally.
H) Lange Reports, Logs und Diffs gehoeren nach GitHub; Chat-Antworten bleiben kurz: Fazit plus naechste Aktion.
I) `weiter` bedeutet den naechsten logischen Schritt ausfuehren, nicht mehrere Schritte buendeln.

## Aktueller Stand

A) Station 8 — Order Validator
Status: FINAL. An ProposedOrder angebunden. Jede validierte Order enthaelt order_ref und source_proposed_order_ref.

B) Audit-Log Core v1.0
Status: FINAL. Audit-kompatible Execution-Simulator-Events sind integriert.

C) Execution Simulator Core v1.0
Status: DRAFT. Integration abgeschlossen. Kein Bestandteil der Validierungs-Pipeline und keine Station 9.

D) Pre-Order / Proposed Order Contract Core v1.0
Status: DRAFT. Definiert den Vertrag zwischen strategischer Entscheidung / Rebalancing-Logik und Station 8.

E) Portfolio State & Ledger Core v1.0
Status: DRAFT. Definiert Portfolio State und append-only Portfolio Ledger als Querschicht, nicht Station 9, inklusive portfolio_state_type, minimalen Pflichtfeldern, Schnittstellen, Core-v1-Grenzen, Codex-Hinweis und Ledger-Index.

## Wichtige Dateien

- specs/95_operational_workflow_rules.md
- specs/14_station_8_order_validator.md
- specs/15_audit_log_core_v1.md
- specs/16_execution_simulator_core_v1.md
- specs/17_pre_order_proposed_order_contract_core_v1.md
- specs/18_portfolio_state_ledger_core_v1.md
- specs/98_spec_index.md
- specs/99_handoff_snapshot_current.md
- _codex_reports/pre_handoff_gate_004_final_after_spt.md
- tests/golden_cases/station_8_order_validator_cases.json
- tests/golden_cases/audit_log_core_v1_cases.json
- tests/golden_cases/execution_simulator_core_v1_cases.json
- tests/golden_cases/pre_order_contract_core_v1_cases.json

## Wichtige Regeln

A) Execution Simulator ist keine Station 9.
B) Keine Pipelinewirkung durch Simulator-FAILED.
C) Eigene Execution-Event-Typen bleiben erhalten: EXECUTION_SIMULATION_SUCCESS, EXECUTION_SIMULATION_PARTIAL, EXECUTION_SIMULATION_FAILED.
D) Keine Zuordnung auf RULE_PASS, RULE_REJECTED oder TECHNICAL_ERROR.
E) validator_status = PASS bleibt neutral; simulation_status wird separat gefuehrt.
F) ProposedOrder ist keine validierte oder ausfuehrbare Order.
G) Station 8 bleibt die fachliche Order-Validierung.
H) Rueckverfolgbarkeit: proposed_order_ref -> source_proposed_order_ref / order_ref -> source_order_ref.
I) Portfolio State & Ledger ist keine Station 9.
J) SIMULATED_POST_EXECUTION wird nie automatisch CURRENT_CONFIRMED.
K) Ledger ist append-only; Ledger-Index ist nur abgeleitete Navigationsstruktur.
L) Keine Uebergabe ohne bestandenes aktuelles Pre-Handoff-Gate.

## Projektweite Read-only-Pruefung

Bitte pruefe das gesamte Projekt read-only auf:

A) Projektstruktur
B) Spezifikationskonsistenz
C) Golden Cases
D) Handoff / Index
E) Redundanz / Struktur
F) offensichtliche Uebergabeluecken

Keine Dateien aendern. Keine Scripts. Keine Patches. Keine ZIPs.

## Naechster fachlicher Schritt

Spec 18 Golden Cases definieren und spaeter unter tests/golden_cases/ abbilden.
