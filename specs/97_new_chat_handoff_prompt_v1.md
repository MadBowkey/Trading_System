# New Chat Handoff Prompt v1

Status: CURRENT
Prompt Version: handoff_prompt.v1
Architecture: v1.6.1
Last updated: 2026-05-15
Owner: Trading System Project

## Zweck

Diese Datei enthält den verbindlichen Übergabe-Prompt für einen neuen Chat, falls der aktuelle Chat endet oder die maximale Chatlänge erreicht wird.

Der neue Chat darf nicht aus Erinnerung oder aus dem alten Chat rekonstruieren, sondern muss nach Upload des Projekt-ZIP aus den lokalen Spezifikationsdateien arbeiten.

## Übergabe-Prompt

Wir setzen das Trading-System-Projekt fort.

Wichtig:
Ich lade gleich das aktuelle Projekt-ZIP hoch.
Der neue Chat kann lokale Windows-Pfade nicht selbst lesen.
Arbeite daher ausschließlich aus den hochgeladenen Dateien, nicht aus Erinnerung und nicht aus dem alten Chat.

Projekt:
Regime-adaptiver Portfolio-Allocator mit dynamischer Risikosteuerung, deduktiver Finanzlogik und LLM-Meta-Manager.

Gültiger Stand:
Architecture v1.6.1.
Station 1 bis Station 6 der Validierungs-Pipeline sind lokal dokumentiert.
Nächster fachlicher Schritt ist Station 7 — Post-Trade Risk Validator.

Lokaler Projektpfad beim Benutzer:
C:\Users\Daily\Documents\TradingSystem\trading_allocator_project

Nach dem ZIP-Upload bitte zuerst diese Dateien lesen und als verbindliche Projektgrundlage behandeln:

1. specs\98_spec_index.md
2. specs\99_handoff_snapshot_current.md
3. specs\00_project_overview_v1_6_1.md
4. specs\01_architecture_overview_v1_6_1.md
5. specs\02_llm_output_schema_v1.md
6. specs\03_risk_metrics_v1.md
7. specs\04_guardrails_v1.md
8. specs\05_deductive_rules_v1.md
9. specs\06_validator_pipeline_v1.md
10. specs\07_station_1_pre_llm_validator.md
11. specs\08_station_2_llm_meta_manager.md
12. specs\09_station_3_technical_schema_validator.md
13. specs\10_station_4_business_logic_validator.md
14. specs\11_station_5_market_risk_validator.md
15. specs\12_station_6_portfolio_engine.md
15. config\rule_registry.yaml
16. tests\golden_cases\station_3_tsv_cases.json
17. tests\golden_cases\station_4_blv_cases.json
18. tests\golden_cases\station_5_mrv_cases.json
19. tests\golden_cases\station_6_portfolio_engine_cases.json

Besonders wichtig:
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
Arbeitsregeln:
- Lokale Specs sind die Single Source of Truth.
- Nicht aus Erinnerung rekonstruieren.
- Vorschläge nicht automatisch übernehmen.
- Neue Vorschläge gegen Architecture v1.6.1 prüfen.
- SAFE_HOLD und CASH_ONLY strikt trennen.
- Technischer Fehler → SAFE_HOLD / NO_NEW_ACTIONS.
- Echtes Markt-/Risk-Event → FORCE_CASH_ONLY / BLOCK_RISK_INCREASE / kontrollierte Risikoreduktion.
- LLM bleibt Meta-Manager, nicht Trading-Bot.
- Python bleibt finale Validierungs-, Guardrail-, Portfolio- und Simulationsinstanz.
- Risk Metrics sind Warnsignale.
- Guardrails sind binäre Python-Sperren.
- Keine stille Änderung ohne Audit Log.
- Keine eigenmächtige Liquidation durch Validatoren.
- Keine automatische Universe-Erweiterung.
- Keine automatische Live-Parameteroptimierung.
- Codex erst einsetzen, wenn eine Spezifikation freigegeben ist.

Arbeitsstil:
Erst bestehenden Stand aus den Dateien zusammenfassen.
Dann sagen, ob der Stand konsistent ist.
Dann erst mit Station 7 — Post-Trade Risk Validator — beginnen.
Bei neuen Vorschlägen immer:
1. mit bestehender Spezifikation vergleichen,
2. bewerten,
3. ggf. korrigieren,
4. finale Fassung vorschlagen.

Beginne nach dem ZIP-Upload mit:
„Ich prüfe zuerst die hochgeladenen Spezifikationsdateien und bestätige den aktuellen Stand vor Station 6.“

## Änderungsprotokoll

### handoff_prompt.v1 — 2026-05-15

Initiale versionierte Fassung des Übergabe-Prompts.

