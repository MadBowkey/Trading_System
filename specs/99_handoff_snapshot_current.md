# Handoff Snapshot — Trading Allocator Project

Status: CURRENT HANDOFF
Architecture: v1.6.1
Last updated: 2026-05-15

## Projektstand

Das Projekt ist ein regime-adaptiver Portfolio-Allocator mit dynamischer Risikosteuerung, deduktiver Finanzlogik und LLM-Meta-Manager.

Rollen:
- Python = Master-System für Berechnung, Validierung, Guardrails, Portfolio Engine, Simulation, Logging und Audit.
- LLM = Meta-Manager, erzeugt nur strategische Absichten.
- Codex = Engineering-Werkzeug, implementiert nur freigegebene Specs.

## Kernregeln

- SAFE_HOLD ist strikt von CASH_ONLY getrennt.
- Technische Fehler führen zu SAFE_HOLD / NO_NEW_ACTIONS.
- Echte Markt-/Risikoverletzungen führen zu FORCE_CASH_ONLY, BLOCK_RISK_INCREASE oder kontrollierter Risikoreduktion.
- Risk Metrics sind Warnsignale.
- Guardrails sind binäre Python-Sperren.
- LLM erzeugt keine Orders.
- Python entscheidet final.
- Keine stille Änderung ohne Audit Log.
- Keine eigenmächtige Liquidation durch Validatoren.
- Core v1: maximal 5 aktive Instrumente.
- Kein OFFENSIVE-Regime.
- risk_multiplier_override maximal 1.0.
- Keine automatische Universe-Erweiterung.
- Keine automatische Live-Parameteroptimierung.

## Validierungs-Pipeline

1. Pre-LLM Validator
2. LLM Meta-Manager
3. Technical Schema Validator
4. Business Logic Validator
5. Market Risk Validator
6. Portfolio Engine
7. Post-Trade Risk Validator
8. Order Validator

## Aktueller Arbeitsstand

Station 1 bis Station 8 sind für den aktuellen Core-v1-Scope lokal dokumentiert.

Station 5 enthält aktuell folgende finalisierte Regeln:
- VAL_MRV_004A — Asset außerhalb Universe ohne Bestand
- VAL_MRV_004B — Asset außerhalb Universe mit Altbestand und INCREASE
- VAL_MRV_004C — Asset außerhalb Universe mit Altbestand und HOLD / DECREASE / LIQUIDATE
- VAL_MRV_005 — Asset Confidence Threshold
- VAL_MRV_006 — Regime Shift Risk Blocks Increase
- VAL_MRV_007 — Correlated Pair No Double Increase


Station 6 enthält aktuell folgende finalisierte Regeln:
- VAL_ENG_001 — Feasibility Check
- VAL_ENG_002 — Summen-Integrität
- VAL_ENG_003 — Input- und Datenintegrität


Station 7 enthält aktuell folgende finalisierte Regeln:
- VAL_PTR_001 — Single Asset Exposure Limit Breach
- VAL_PTR_002 — HHI Concentration Limit Breach
- VAL_PTR_003 — Missing or Invalid Risk Configuration


Station 8 enthält aktuell folgende finalisierte Regeln:
- VAL_ORD_001 — Technische Order-Integrität
- VAL_ORD_002 — Liquiditäts-Check
- VAL_ORD_003 — Broker-/Tick-Size-/Lot-Normalisierung
- VAL_ORD_004 — Kosten / Slippage
- VAL_ORD_005 — Normalisierte Orderliste verletzt Zielplan / Post-Trade-Konformität

Nächster fachlicher Schritt:
Station 6 — Portfolio Engine spezifizieren.

## Lokale Single Source of Truth

Die verbindlichen Spezifikationen liegen in:

- specs/00_project_overview_v1_6_1.md
- specs/01_architecture_overview_v1_6_1.md
- specs/02_llm_output_schema_v1.md
- specs/03_risk_metrics_v1.md
- specs/04_guardrails_v1.md
- specs/05_deductive_rules_v1.md
- specs/06_validator_pipeline_v1.md
- specs/07_station_1_pre_llm_validator.md
- specs/08_station_2_llm_meta_manager.md
- specs/09_station_3_technical_schema_validator.md
- specs/10_station_4_business_logic_validator.md
- specs/11_station_5_market_risk_validator.md

Regeln:
- config/rule_registry.yaml

Golden Cases:
- tests/golden_cases/station_3_tsv_cases.json
- tests/golden_cases/station_4_blv_cases.json
- tests/golden_cases/station_5_mrv_cases.json

## Startprompt für neuen Chat

Wir setzen das Trading-System-Projekt fort.

Nutze diesen Handoff Snapshot als Orientierung.
Die lokalen Specs sind die Single Source of Truth.
Nicht aus dem Chat rekonstruieren, sondern anhand der Specs weiterarbeiten.

Gültiger Stand:
Architecture v1.6.1.
Station 1 bis Station 8 sind lokal dokumentiert.
Station 5 enthält VAL_MRV_004A/B/C sowie VAL_MRV_005/006/007.
Nächster Schritt ist Station 6 Portfolio Engine.

Arbeitsregeln:
Vorschläge nicht automatisch übernehmen.
Auf Konsistenz mit v1.6.1 prüfen.
SAFE_HOLD und CASH_ONLY strikt trennen.
LLM bleibt Meta-Manager.
Python bleibt finale Validierungs- und Guardrail-Instanz.
Keine stille Änderung ohne Audit Log.
Codex erst einsetzen, wenn die Spezifikation freigegeben ist.

## Audit-Log Core v1.0

Die Audit-Log-Struktur Core v1.0 ist lokal dokumentiert.

Relevante Dateien:

- specs/15_audit_log_core_v1.md
- tests/golden_cases/audit_log_core_v1_cases.json

Status:

- Core v1.0 umfasst nur Station 1 bis Station 8.
- Keine ML-Felder in Core v1.0.
- audit_schema_version ist Pflichtfeld.
- audit_hash ist ein Einzel-Event-Integritäts-Hash.
- Keine Hash-Chain.
- Kein Merkle-Baum.
- Kein HMAC.
- Parquet ist das primäre Speicherformat.
- JSON ist nur Export-, Debugging- und Prüfungsformat.

Nächster fachlicher Schritt:

Audit-Log Core v1.0 final prüfen und anschließend entscheiden, ob die Core-v1-Spezifikation abgeschlossen ist oder ob zuerst die Execution-Simulation spezifiziert wird.
