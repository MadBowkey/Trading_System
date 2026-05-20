# Specification Index

Status: CURRENT
Architecture: v1.6.1
Last updated: 2026-05-20

## Zweck

Diese Datei ist die Inhaltskarte der lokalen Projektspezifikation.

Sie zeigt, welche Datei welche verbindliche Information enthaelt.

## Single Source of Truth

GitHub `main` ist der kanonische technische Projektstand.

Die fachlich verbindlichen Spezifikationen liegen im Repo unter:

specs/

Die maschinenlesbaren Konfigurationen liegen im Repo unter:

config/

Die verbindlichen Testbeispiele liegen im Repo unter:

tests/golden_cases/

Lokale Ordner sind Arbeitskopien. Sie sind nur gueltig, wenn sie nachweislich mit GitHub `main` synchronisiert sind.

## Workflow / Handoff

- specs/95_operational_workflow_rules.md
  Enthält die verbindlichen Arbeitsregeln für ChatGPT, Codex, GitHub-Rueckkanal, lokale Ausfuehrung, PowerShell-Dateiaenderungen und neue Chat-Uebergaben.

- specs/97_new_chat_handoff_prompt_v1.md
  Enthält den versionierten Uebergabe-Prompt fuer einen neuen Chat.

- specs/99_handoff_snapshot_current.md
  Enthält den aktuellen Uebergabe-Snapshot fuer einen neuen Chat.

- _codex_reports/pre_handoff_gate_004_final_after_spt.md
  Enthält das letzte bestandene Pre-Handoff-Gate 004 nach der Source-of-Truth-Klaerung.

Aktueller Gate-Status:

- Finales Pre-Handoff Gate 004: bestanden auf damaligem main-Stand.
- KRITISCH: 0.
- MITTEL: 0.
- Handoff-Empfehlung: JA.
- Nach spaeteren Repo-Aenderungen ist vor einer neuen Uebergabe erneut ein aktuelles Pre-Handoff-Gate erforderlich.

## Spezifikationsdateien

### Projekt und Architektur

- specs/00_project_overview_v1_6_1.md
  Enthält Projektdefinition, Rollenverteilung, Kernprinzipien, SAFE_HOLD vs CASH_ONLY und Core-v1-Grenzen.

- specs/01_architecture_overview_v1_6_1.md
  Enthält die vollständige Architekturübersicht v1.6.1 und die Einordnung der Hauptkomponenten.

### LLM Output

- specs/02_llm_output_schema_v1.md
  Enthält die logische Struktur von LLMMetaManagerOutput, erlaubte Enums, risk_multiplier_override-Regeln und interne Konsistenzregeln.

### Risiko und Regeln

- specs/03_risk_metrics_v1.md
  Enthält alle aktuell definierten Risk Metrics, ihre Bedeutung und Beispielstruktur.

- specs/04_guardrails_v1.md
  Enthält alle aktuell definierten harten Python-Guardrails und Grenzwerte.

- specs/05_deductive_rules_v1.md
  Enthält die deduktiven Finanzregeln DED_001 bis DED_006.

### Validator Pipeline

- specs/06_validator_pipeline_v1.md
  Enthält die 8-stufige Validierungs-Pipeline.

- specs/07_station_1_pre_llm_validator.md
  Enthält die Spezifikation für Station 1.

- specs/08_station_2_llm_meta_manager.md
  Enthält die Spezifikation für Station 2.

- specs/09_station_3_technical_schema_validator.md
  Enthält die Spezifikation für Station 3 inklusive VAL_TSV_001 bis VAL_TSV_005.

- specs/10_station_4_business_logic_validator.md
  Enthält die Spezifikation für Station 4 inklusive VAL_BLV_001 bis VAL_BLV_007.

- specs/11_station_5_market_risk_validator.md
  Enthält die Spezifikation für Station 5 inklusive VAL_MRV_004A/B/C und VAL_MRV_005/006/007.

- specs/12_station_6_portfolio_engine.md
  Enthält die Spezifikation für Station 6 inklusive VAL_ENG_001 bis VAL_ENG_003.

- specs/13_station_7_post_trade_risk_validator.md
  Enthält die Spezifikation für Station 7 inklusive VAL_PTR_001 bis VAL_PTR_003.

- specs/14_station_8_order_validator.md
  Enthält die Spezifikation für Station 8 inklusive VAL_ORD_001 bis VAL_ORD_005.

### Core-Infrastruktur und nachgelagerte Module

- specs/15_audit_log_core_v1.md
  Enthält die zentrale Audit-Log-Struktur Core v1.0 für Station 1 bis Station 8 inklusive Standardfeldern, Statuswerten, Event-Typen, Parquet-Schema, Partitionierung, Hash- und Verifikationslogik.

- specs/16_execution_simulator_core_v1.md
  Enthält den nachgelagerten What-If-Execution-Simulator nach Station 8 inklusive Input/Output, Output-/Report-Contract, Simulationsannahmen, Fill-Regeln, Cash-/Portfolio-Fortschreibung, Short-Regeln, Statuslogik und Audit-Log-Anbindung.

- specs/17_pre_order_proposed_order_contract_core_v1.md
  Enthält den Pre-Order / Proposed Order Contract vor Station 8 inklusive ProposedOrder-Feldern, Strukturstatus, Übergabe an Station 8, Abgrenzung und Codex-Hinweis.

- specs/18_portfolio_state_ledger_core_v1.md
  Enthält Portfolio State & Ledger Core v1.0 als Querschicht, nicht Station 9, inklusive portfolio_state_type, minimalen Pflichtfeldern, append-only Ledger-Regeln, Schnittstellen, Core-v1-Grenzen, Codex-Hinweis und Ledger-Index.

## Konfigurationsdateien

- config/rule_registry.yaml
  Maschinenlesbare Rule Registry für aktuell definierte Validator-Regeln.

- config/risk_guardrails.yaml
  Platzhalter für spätere maschinenlesbare Guardrail-Konfiguration.

- config/regime_matrix.yaml
  Platzhalter für spätere Regime-Matrix.

- config/indicator_registry.yaml
  Platzhalter für spätere Indicator Registry.

- config/universe.example.yaml
  Beispielstruktur für User Managed Universe.

## Golden Cases

- tests/golden_cases/station_3_tsv_cases.json
  Testfälle für Station 3.

- tests/golden_cases/station_4_blv_cases.json
  Testfälle für Station 4.

- tests/golden_cases/station_5_mrv_cases.json
  Testfälle für Station 5.

- tests/golden_cases/station_6_portfolio_engine_cases.json
  Testfälle für Station 6.

- tests/golden_cases/station_7_post_trade_risk_validator_cases.json
  Testfälle für Station 7.

- tests/golden_cases/station_8_order_validator_cases.json
  Testfälle für Station 8.

- tests/golden_cases/audit_log_core_v1_cases.json
  Enthält Golden Cases für Audit-Log Core v1.0 inklusive audit_schema_version, Pflichtfeldprüfung, nullable rule_id / asset_id, Non-Null-Prüfung, Reason-Limit und Hash-Verifikation.

- tests/golden_cases/execution_simulator_core_v1_cases.json
  Enthält Golden Cases für SUCCESS, PARTIAL, NO_FILL, FAILED, Cash-Grenzen, Short-Autorisierung, source_order_ref-Rückverfolgbarkeit, Audit-Hash und Portfolio-Konsistenz.

- tests/golden_cases/pre_order_contract_core_v1_cases.json
  Enthält Golden Cases für CONTRACT_READY, CONTRACT_INVALID, LIMIT/MARKET-Regeln, quantity-Format, Traceability, Short-Autorisierung und Abgrenzung zu Station 8.

Spec 18 Golden Cases sind noch nicht angelegt.

## Aktueller Arbeitsstand

Station 1 bis Station 8 sind dokumentiert.

Station 5 ist für den aktuellen Core-v1-Scope ergänzt um:

- VAL_MRV_004A
- VAL_MRV_004B
- VAL_MRV_004C
- VAL_MRV_005
- VAL_MRV_006
- VAL_MRV_007

Station 8 ist FINAL.

Audit Core v1.0 ist FINAL.

Execution Simulator Core v1.0 ist als konsistenter DRAFT abgeschlossen.

Pre-Order / Proposed Order Contract Core v1.0 ist als DRAFT angelegt.

Portfolio State & Ledger Core v1.0 ist als DRAFT angelegt.

Nächster fachlicher Schritt:

Spec 18 Golden Cases definieren und später unter tests/golden_cases/ abbilden.

## Arbeitsregel

Vor Weiterarbeit an einer Station oder Spec zuerst die zugehörige Spec-Datei prüfen.

Neue fachliche Entscheidungen werden zuerst durch Team plus ChatGPT in specs/ dokumentiert, danach in config/ und tests/ abgebildet.

Projektweite Struktur-, Konsistenz-, Report- und Sync-Aufgaben laufen soweit möglich über Codex plus GitHub-Rueckkanal.
