# Handoff Snapshot Current

Status: CURRENT
Project: Trading System
Architecture: v1.6.1
Snapshot date: 2026-06-17

## Pflichtkontext fuer neuen Chat

- specs/94_start_audit_protocol.md
- specs/95_operational_workflow_rules.md
- specs/96_frozen_project_state.md
- specs/97_new_chat_handoff_prompt_v1.md
- specs/98_spec_index.md
- _codex_reports/pre_handoff_gate_004_final_after_spt.md

Letztes bestandenes Pre-Handoff Gate:

- Finales Pre-Handoff Gate 004 wurde auf damaligem main-Stand bestanden.
- KRITISCH: 0
- MITTEL: 0
- Handoff-Empfehlung: JA
- Nach spaeteren Repo-Aenderungen ist vor einer neuen Uebergabe erneut ein aktuelles Pre-Handoff-Gate erforderlich.
- Seit Gate 004 wurden 94/95/96/97/98/99 aktualisiert; vor der geplanten neuen Chat-Uebergabe ist ein aktuelles Gate erforderlich.

## Aktueller Stand

A) Station 8 — Order Validator
Final abgeschlossen und konsolidiert um station_8_validation_ref sowie order_ref pro validierter Order.

B) Audit-Log Core v1.0
Final abgeschlossen und erweitert um audit-kompatible Execution-Simulator-Events nach Station 8.

C) Execution Simulator Core v1.0
Als konsistenter DRAFT abgeschlossen. Enthält Rolle, Input/Output, Output-/Report-Contract, Simulationsannahmen, Fill-/Preis-/Slippage-Regeln, Cash/Portfolio/Liquidität, Short-Regeln, Statuslogik, Audit-Log-Anbindung, Golden Cases und Codex-Hinweis.

D) Pre-Order / Proposed Order Contract Core v1.0
Als DRAFT angelegt. Definiert den Vertrag zwischen strategischer Entscheidung / Rebalancing-Logik und Station 8 Order Validator.

E) Portfolio State & Ledger Core v1.0
FINAL. Definiert Portfolio State und append-only Portfolio Ledger als Querschicht, nicht Station 9, inklusive portfolio_state_type, minimalen Pflichtfeldern, Schnittstellen, Core-v1-Grenzen, Golden Cases, Codex-Hinweis, Ledger-Index und Ledger Operation Outcomes.

F) Start Audit Protocol
CURRENT. Definiert den read-only Audit-Startmodus. Bestehende Artefakte gelten im Audit zunaechst als Hypothesen. Befunde werden mindestens als PASS, WARN, FAIL oder ALT klassifiziert und brauchen Beweis- oder Fehlbeweisbezug.

G) Frozen Project State
CURRENT. Friert uebergabekritische Chat-Entscheidungen kompakt ein. Enthalten sind unter anderem Audit-Maximen, Gegenentwurfs-Pflichten, State-Leak-Sicherungen, LLM-/Guardrail-Abgrenzung, Beweisbarkeitspflicht und `frozen`-Pflegeregel.

## Wichtige Dateien

- specs/94_start_audit_protocol.md
- specs/95_operational_workflow_rules.md
- specs/96_frozen_project_state.md
- specs/97_new_chat_handoff_prompt_v1.md
- specs/98_spec_index.md
- specs/14_station_8_order_validator.md
- specs/15_audit_log_core_v1.md
- specs/16_execution_simulator_core_v1.md
- specs/17_pre_order_proposed_order_contract_core_v1.md
- specs/18_portfolio_state_ledger_core_v1.md
- tests/golden_cases/station_8_order_validator_cases.json
- tests/golden_cases/audit_log_core_v1_cases.json
- tests/golden_cases/execution_simulator_core_v1_cases.json
- tests/golden_cases/pre_order_contract_core_v1_cases.json
- tests/golden_cases/portfolio_state_ledger_core_v1_cases.json
- _codex_reports/pre_handoff_gate_004_final_after_spt.md

## Wichtige Entscheidungen

A) Execution Simulator ist keine Station 9.
B) Execution Simulator verändert keine Pipeline- oder Systemstatus.
C) Execution-Simulator-Events behalten eigene event_type-Werte: EXECUTION_SIMULATION_SUCCESS, EXECUTION_SIMULATION_PARTIAL, EXECUTION_SIMULATION_FAILED.
D) Execution-Simulator-Events werden nicht auf RULE_PASS, RULE_REJECTED oder TECHNICAL_ERROR gemappt.
E) validator_status bleibt PASS; simulation_status wird separat geführt.
F) Simulator-FAILED bedeutet: Simulation nicht belastbar, nicht Station 8 ungültig, kein Pipeline-Stopp.
G) Rückverfolgbarkeit: proposed_order_ref -> source_proposed_order_ref / order_ref -> source_order_ref.
H) Keine erneute Konsolidierung von Specs 14/15/16 ohne konkreten Fehlerbefund.
I) ProposedOrder ist ein Vorschlag vor Station 8, keine validierte oder ausführbare Order.
J) Station 8 ist an ProposedOrder angebunden; jede validierte Order erhält source_proposed_order_ref und order_ref.
K) Portfolio State & Ledger ist keine Station 9, sondern eine Querschicht.
L) SIMULATED_POST_EXECUTION wird nie automatisch zu CURRENT_CONFIRMED.
M) Ledger ist append-only; Ledger-Index ist nur abgeleitete Navigationsstruktur.
N) Ledger Operation Outcomes erzeugen keine Pipeline-, System- oder Audit-Core-Statuswerte.
O) Projektweite Struktur-, Konsistenz-, Report- und Sync-Aufgaben laufen soweit möglich über Codex plus GitHub-Rueckkanal.
P) Fachliche Spezifikation von Modulen und Schnittstellen erfolgt durch Team plus ChatGPT; Codex erfindet keine neue fachliche Logik.
Q) Codex-relevante Vorgaenge werden soweit möglich automatisiert; manuelles Kopieren von PR-Nummern, Reports oder Diffs ist Ausnahme.
R) Lokale PowerShell-Dateiaenderungen erfordern einen vollständigen ausführbaren Block und bei Schreibvorgaengen explizites StreamWriter-Handling mit Write, Close und try/finally.
S) GitHub main ist der kanonische technische Projektstand; lokale Ordner sind Arbeitskopien.
T) Chat-beschlossene, uebergabekritische Regeln werden in Frozen State gefuehrt, wenn sie nicht sinnvoll vollstaendig in 95/97/98/99 oder eine Fachspec gehoeren.
U) `frozen` bedeutet: Frozen State kuratiert pruefen und aktualisieren; alte Eintraege muessen auf Loeschung, Ersetzung oder Ueberfuehrung in Fachspecs geprueft werden.
V) Bestehende Artefakte gelten im Architektur-Audit zunaechst als Hypothesen, nicht als Autoritaet.
W) Audit mutiert nicht und repariert nicht.
X) Simulator-Ergebnisse duerfen Risikologik beeinflussen, aber niemals Portfolio-State erzeugen.
Y) Nur echte Broker-/Exchange-Fills duerfen ueber Reconciliation offiziellen Portfolio-State aktualisieren.
Z) Das LLM darf Strategie interpretieren und vorschlagen; harte Risiko-, Guardrail- und Validatorentscheidungen muessen deterministisch ausserhalb reiner Prompt-Logik pruefbar sein.
AA) Groessere Architekturentscheidungen muessen gegen starke Gegenentwuerfe oder schlankere Alternativen geprueft werden.
AB) Architekturgrenzen muessen durch Datei, Contract, Golden Case, Enum, Zustandsuebergang oder deterministischen Test beweisbar sein.

## Nächster Schritt

Vor der geplanten neuen Chat-Uebergabe ein aktuelles Pre-Handoff-Gate auf GitHub `main` durchfuehren, das `specs/94_start_audit_protocol.md` und `specs/96_frozen_project_state.md` einschliesst. Uebergabe nur starten, wenn KRITISCH 0 und MITTEL 0 bestaetigt sind.
