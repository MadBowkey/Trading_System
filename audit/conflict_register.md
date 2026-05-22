# Konfliktregister

Zentrale Sammlung aller identifizierten Konflikte aus den Modulen 1–10.

## Klassifikation (verbindlich)
- CRITICAL
- HIGH
- MEDIUM
- LOW

## Einträge
| ID | Modul | Konfliktbeschreibung | Klasse | Betroffene Schnittstellenmodule | Status (vor Matrix) | Notizen |
|---|---|---|---|---|---|---|
| M01-C01 | Modul 01 | Spezifikations-/Golden-Case-Basis vorhanden, aber keine nachweisbare produktive Datenpipeline-Implementierung im aktuellen Repo-Stand. | HIGH | 02, 03, 05, 06, 07, 08 | offen | Verifiziert über Repo-Struktur (Specs/Configs/Tests ohne Runtime-Code). |
| M01-C02 | Modul 01 | `indicator_registry.yaml` und `regime_matrix.yaml` enthalten leere Kernlisten (`indicators`, `regimes`). | MEDIUM | 02, 05, 06 | offen | Placeholder vs. produktiv unklar; Risiko inkonsistenter Folgeentscheidungen. |
| M01-C03 | Modul 01 | Universe-Konfiguration nur als `universe.example.yaml` explizit sichtbar; produktives Pendant nicht eindeutig festgelegt. | LOW | 01, 05 | offen | Risiko von Fehlkonfiguration bei Übergang in Betrieb. |
| M02-C01 | Modul 02 | Spezifikation für Station 2 vorhanden, aber keine nachweisbare produktive Laufzeitimplementierung (LLM-Client/Structured-Output/Fehlerpfade) im aktuellen Repo-Stand. | HIGH | 03, 04, 05, 06, 07, 08, 09, 10 | offen | Verstärkt Problemcluster aus M01-C01 (fehlende ausführbare Pipelinebasis). |
| M02-C02 | Modul 02 | Übergabevertrag Modul 02 -> Modul 03 ist fachlich beschrieben, aber nicht als verbindlicher ausführbarer Contract im Laufzeitpfad nachweisbar. | MEDIUM | 03, 04 | offen | Risiko uneinheitlicher Fehlerbehandlung (rohes JSON vs. Objektübergabe). |
| M02-C03 | Modul 02 | Spezifizierte SAFE_HOLD-/NO_NEW_ACTIONS-Fehlerwirkung bei API-/Timeout-Fehlern ohne produktive Artefakte derzeit nicht empirisch verifizierbar. | LOW | 03, 09, 10 | offen | Traceability-/Nachweislücke, kein direkter Fachwiderspruch. |
