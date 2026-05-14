# Specification Index

Status: CURRENT
Architecture: v1.6.1
Last updated: 2026-05-15

## Zweck

Diese Datei ist die Inhaltskarte der lokalen Projektspezifikation.

Sie zeigt, welche Datei welche verbindliche Information enthält.

## Single Source of Truth

Die fachlich verbindlichen Spezifikationen liegen unter:

specs/

Die maschinenlesbaren Konfigurationen liegen unter:

config/

Die verbindlichen Testbeispiele liegen unter:

tests/golden_cases/

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

### Übergabe

- specs/99_handoff_snapshot_current.md  
  Enthält den aktuellen Übergabe-Snapshot für einen neuen Chat.

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

## Aktueller Arbeitsstand

Station 1 bis Station 5 sind lokal dokumentiert.

Station 5 ist für den aktuellen Core-v1-Scope ergänzt um:

- VAL_MRV_004A
- VAL_MRV_004B
- VAL_MRV_004C
- VAL_MRV_005
- VAL_MRV_006
- VAL_MRV_007

Nächster fachlicher Schritt:

Station 6 — Portfolio Engine spezifizieren.

## Arbeitsregel

Vor Weiterarbeit an einer Station zuerst die zugehörige Spec-Datei prüfen.

Neue Entscheidungen werden zuerst in specs/ dokumentiert, danach in config/ und tests/ abgebildet.
