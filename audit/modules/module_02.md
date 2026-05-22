# Modul 02 – LLM Meta-Manager

## 1) Zweck und Verantwortung des Moduls
Der LLM Meta-Manager transformiert die von Station 1 freigegebenen Kontexte in eine **strukturierte strategische Absicht** (kein Order- und kein Portfolio-Engine-Modul).

Verantwortung im Systemkontext:
- Ableitung von `strategy_regime`, `risk_multiplier_override` und `target_allocation_adjustments` im LLMMetaManagerOutput-Format.
- Keine finalen Handelsentscheidungen, keine finalen Portfoliogewichte, keine Ordererzeugung.
- Bei API-/LLM-Fehlern: SAFE_HOLD / NO_NEW_ACTIONS und Pipeline-Stopp.

Evidenz:
- Station-2-Spezifikation mit Input-/Output- und Fehlerwirkung. `specs/08_station_2_llm_meta_manager.md`
- Pipeline-Rolle von Station 2 und Fehlerwirkung. `specs/06_validator_pipeline_v1.md`
- Output-Contract und Verbote im Output-Schema. `specs/02_llm_output_schema_v1.md`

## 2) Eingaben / Datenquellen
Erkennbare Eingaben laut Spezifikation:
- Freigegebene Kontexte aus Station 1: Marktdatenstatus, Portfolio-Status, User-Managed-Universe, Trend-Output, Regime-Output, Risk Metrics, System-/Analysekonfiguration.
- Zusatzinputs: System-Prompt, deduktive Regeln, Few-Shot-Beispiele, Structured-Output-Schema, API-Konfiguration.

Repo-Befund (ohne Annahmen):
- Die funktionale Datenstruktur ist in Specs beschrieben, aber keine lauffähige Station-2-Implementierung im Repo vorhanden.
- Golden Cases referenzieren Station-2-Output indirekt (z. B. `schema_version = llm_meta_manager_output.v1` in Station-3/4/5-Cases).

## 3) Ausgaben / Verträge / Abhängigkeiten
Vertraglicher Output:
- Ein Structured-Output-Objekt gemäß LLMMetaManagerOutput, Übergabe an Station 3.

Harte Vertragsgrenzen:
- Keine Orders, keine Stückzahlen, keine finalen Zielgewichte.
- Kein neues Regime außerhalb erlaubter Enums.
- Keine Guardrail- oder Universe-Änderung durch Station 2.

Abhängigkeiten:
- Upstream: Station 1 (nur freigegebene Daten dürfen verarbeitet werden).
- Downstream: Station 3 validiert technische Schema-Integrität; Station 4+ prüfen Logik/Risiko/Kontext.

## 4) Risiken / Konflikte / Inkonsistenzen
### Konflikt M02-C01 — Klassifikation: HIGH
- Typ: Umsetzungs-/Verifikationslücke.
- Befund: Station 2 ist fachlich spezifiziert, aber im aktuellen Repo ohne lauffähige Implementierung.
- Wirkung: Contract-Verhalten (Timeout/Retry/Error-Path, deterministische Übergabe an Station 3) nicht praktisch verifizierbar.
- Begründung HIGH: Kernmodul in der Pipeline, aber derzeit nur dokumentarisch abgedeckt.

### Konflikt M02-C02 — Klassifikation: MEDIUM
- Typ: Spezifikationskonsistenz.
- Befund: `specs/08_station_2_llm_meta_manager.md` markiert den Status als **DRAFT**, nennt jedoch gleichzeitig „fachlich abgenommen“.
- Wirkung: Unklare Reifegrad-Semantik (prozessual), potenziell widersprüchliche Erwartung für Implementierungsfreigaben.
- Begründung MEDIUM: Kein direkter Runtime-Blocker, aber Governance-/Freigaberisiko.

### Konflikt M02-C03 — Klassifikation: MEDIUM
- Typ: Testabdeckung/Traceability.
- Befund: Es existieren Golden Cases für Station 3/4/5 mit Station-2-Output-Referenzen, aber keine dedizierten Station-2-Golden-Cases im Repo.
- Wirkung: Station-2-spezifische Fehlerpfade (API-Ausfall, Timeout, leere Antwort) sind nicht als eigenständige Testfälle versioniert.
- Begründung MEDIUM: Mögliche Lücke in frühzeitiger Fehlerdetektion.

## 5) Architektur- und Sicherheitsbewertung
Architektur-Bewertung:
- Positiv: Station 2 ist klar als Intent-Erzeuger eingegrenzt; harte Trennung zu Schema-, Logik- und Risiko-Validatoren.
- Positiv: SAFE_HOLD-/NO_NEW_ACTIONS-Fehlerpfad bei LLM/API-Störungen ist klar vorgegeben.
- Risiko: Ohne Implementierungsartefakte sind Retry-, Timeout- und Failover-Mechaniken nicht prüfbar.

Sicherheits-/Robustheitsbewertung:
- Positiv: Spezifikation verhindert, dass Station 2 direkt Risiko erhöht via Order-/Gewichtserzeugung.
- Positiv: Nachgelagerte Validator-Kette reduziert Risiko fehlerhafter LLM-Ausgaben.
- Restrisiko: Operative Zuverlässigkeit (API-Handling, Logging-Detailtiefe, idempotente Übergabe) ist derzeit nicht empirisch abgesichert.

## 6) Empfehlung / Maßnahmen / offene Punkte
Empfehlungen (priorisiert):
1. **HIGH**: Minimalen Station-2-Implementierungsslice definieren (Client-Aufruf, Timeout/Retry, Fehlerpfad SAFE_HOLD, Übergabecontract an Station 3).
2. **MEDIUM**: Spezifikationsstatus harmonisieren (`DRAFT` vs. „fachlich abgenommen“) inkl. klarer Freigabedefinition.
3. **MEDIUM**: Dedizierte Golden Cases für Station 2 ergänzen (Timeout, API-Error, leere Antwort, korrektes Structured Output).

Offene Punkte:
- Welche verbindlichen Timeout-/Retry-Grenzen gelten für Station 2 im produktiven Betrieb?
- Welche minimalen Auditfelder sind bei Station-2-Fehlern zwingend zu loggen (zusätzlich zu Core-Audit-Standardfeldern)?
- Wird eine deterministische Prompt-/Ruleset-Versionierung pro Run verpflichtend gespeichert?
