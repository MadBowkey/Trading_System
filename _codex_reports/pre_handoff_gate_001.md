# Pre-Handoff-Gate 001 — Cross-Reference-Prüfung

Datum: 2026-05-19  
Repo: /workspace/Trading_System  
HEAD: 0e11990 Separate station 7 validator status from event type  
Branch: work

## Scope
Read-only-Analyse der bestehenden Projektdateien in:
- `specs/*.md`
- `config/*.yaml`
- `tests/golden_cases/*.json`

Einzige Änderung in diesem Task: diese Report-Datei.

## Methode
- Cross-Reference-Scan über Status-/Enum-Felder, Referenzketten und Contract-Grenzen.
- Fokusdateien gemäß Aufgabenstellung inklusive:
  - `specs/01_architecture_overview_v1_6_1.md`
  - `specs/06_validator_pipeline_v1.md`
  - `specs/17_pre_order_proposed_order_contract_core_v1.md`
  - `specs/14_station_8_order_validator.md`
  - `specs/97_new_chat_handoff_prompt_v1.md`
  - `specs/98_spec_index.md`
  - `specs/99_handoff_snapshot_current.md`

## Befundmatrix

| Schwere | Bereich | Datei(en) | Befund | Begründung | Empfehlung | Aktion nötig |
| ------- | ------- | --------- | ------ | ---------- | ---------- | ------------ |
| MITTEL | A) Status-/Enum-Konsistenz | `config/rule_registry.yaml`, `specs/15_audit_log_core_v1.md` | In `rule_registry` werden pseudo-Enums mit `_OR_` verwendet (`DOWNGRADED_OR_REJECTED`, `NORMAL_CONTINUE_OR_NO_NEW_ACTIONS`, `CONTINUE_OR_STOP_BEFORE_EXECUTION_SIMULATION`, `APPROVED_OR_REJECTED`). | Diese Werte sind keine erlaubten atomaren Statuswerte aus Audit-Core-Allowlist; dadurch entsteht Mapping-Mehrdeutigkeit zwischen Regelkatalog und Audit/Golden-Cases. | Regelkatalog-Status auf echte Einzelwerte oder explizites Entscheidungsmodell (z. B. bedingte Branches) umstellen; keine kombinierten Platzhalterwerte als finale Status ausgeben. | Ja |
| MITTEL | C) Contract-Kompatibilität | `specs/17_pre_order_proposed_order_contract_core_v1.md`, `tests/golden_cases/station_8_order_validator_cases.json` | Station-8-Golden-Cases modellieren Proposed-Order-Eingaben, aber ohne expliziten `contract_status=CONTRACT_READY`-Gate im Payload/Precondition. | Spec 17 fordert strukturelle Vorprüfung und Übergabe bei `CONTRACT_READY`; die Gate-Bedingung ist in Station-8-Cases nur implizit, nicht explizit prüfbar. | Station-8-Case-Kontrakt um explizite Precondition-Referenz auf `CONTRACT_READY` ergänzen (inhaltlich, nicht implementativ). | Ja |
| GERING | B) Referenzketten | `specs/17_pre_order_proposed_order_contract_core_v1.md`, `tests/golden_cases/station_8_order_validator_cases.json`, `tests/golden_cases/execution_simulator_core_v1_cases.json` | Referenzkette `proposed_order_ref → source_proposed_order_ref → order_ref → source_order_ref` ist konsistent dokumentiert; in Execution-Cases teils als Regeltext/Erwartung statt überall als vollständige konkrete Payload-Beispiele. | Kein Widerspruch, aber unterschiedliche Schärfegrade zwischen „muss vorhanden sein“ und „konkret geliefert“. | Für kritische Integrationspfade weiterhin explizite Beispiel-Payloads je Casefamilie priorisieren. | Nein |
| REDAKTIONELL | D) Architekturtexte | `specs/01_architecture_overview_v1_6_1.md`, `specs/06_validator_pipeline_v1.md` | Architektur-/Pipelinetexte enthalten Stellen mit älterer/unscharfer Terminologie gegenüber den neueren Specs 14/15/16/17 (v. a. ProposedOrder-Abgrenzung und Simulator-Rolle). | Keine direkte Regelkollision gefunden, aber Leserisiko bei Handoff durch unterschiedliche Detailtiefe. | Präzisierende Querverweise auf Specs 14/15/16/17 an Schlüsselstellen ergänzen (ohne Rekonsolidierung). | Nein |
| KEINE AKTION | E) Golden-Case-Klassifizierung | `tests/golden_cases/station_8_order_validator_cases.json`, `tests/golden_cases/execution_simulator_core_v1_cases.json`, `tests/golden_cases/pre_order_contract_core_v1_cases.json`, weitere Station-Cases | Dreiteilung möglich: (1) ausführbare Payload-Fixtures: v. a. Stationsfälle mit `input_payload`; (2) Szenario-/Contract-Cases: v. a. viele Execution-/Contract-Erwartungsfälle; (3) unklar/implementierungsgefährlich: nur dort, wo „OR“-Erwartungen bewusst mehrere zulässige Resultate codieren. | Insgesamt ausreichend für Spezifikationsabgleich; Ambiguität ist punktuell und bekannt. | Keine Sofortmaßnahme; Ambiguität bei zukünftiger Testhärtung gezielt reduzieren. | Nein |
| KEINE AKTION | F) Handoff/Index/Metadaten | `specs/97_new_chat_handoff_prompt_v1.md`, `specs/98_spec_index.md`, `specs/99_handoff_snapshot_current.md`, `README.md` | HEAD-Bezug, Projektstatus und „Spec 18 nur Kandidat“ sind konsistent. „Keine Station 9“ wird in Handoff/Snapshot klar festgehalten. | Kein Widerspruch zur geforderten Übergabelogik festgestellt. | Keine Aktion. | Nein |

## Klassifizierung Golden Cases

### 1) Ausführbare Payload-Fixtures
- Station-spezifische Cases mit konkreten `input_payload` und erwarteten Statusfeldern.
- Beispiele: Station 4/5/6/7/8, Audit-Core-Grundfälle.

### 2) Szenario-/Contract-Cases
- Cases mit starken Regel- und Erwartungsassertionen, teils ohne vollständig ausmodellierte End-to-End-Payload.
- Besonders im Execution-Simulator-Kontext verbreitet (traceability-/policy-orientiert).

### 3) Unklar / implementierungsgefährlich
- Fälle mit absichtlichen Mehrfachausgängen (`*_OR_*`, `FULL_OR_PARTIAL`, `PARTIAL_OR_NO_FILL`) sind als Spezifikationsspielraum nützlich, aber für deterministische Regressionstests potenziell mehrdeutig.

## Gate-Entscheidungsnotiz
Es bestehen offene Befunde mit Schweregrad **MITTEL**.  
Daher **keine Übergabeempfehlung** im Sinne eines vollständig geschlossenen Pre-Handoff-Gates.

## Abschlussdaten
1. Repo-Root: `/workspace/Trading_System`  
2. HEAD: `0e11990 Separate station 7 validator status from event type`  
3. Branch: `work`  
4. Geänderte Dateien: `_codex_reports/pre_handoff_gate_001.md`
