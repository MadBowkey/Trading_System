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
| M02-C01 | Modul 02 | Station 2 ist fachlich spezifiziert, aber ohne lauffähige Implementierung im aktuellen Repo; Contract-Verhalten nicht praktisch verifizierbar. | HIGH | 01, 03, 04 | offen | Risiko liegt in nicht validierten Timeout/Retry/Error-Paths. |
| M02-C02 | Modul 02 | Spezifikationsstatuskonflikt: `DRAFT` und zugleich „fachlich abgenommen“ in Station-2-Spezifikation. | MEDIUM | Governance, 03, 04 | offen | Reifegrad-/Freigabelogik unklar. |
| M02-C03 | Modul 02 | Keine dedizierten Station-2-Golden-Cases für API-Fehlerpfade im Repo. | MEDIUM | 03, Audit | offen | Testlücke für Timeout/leer/API-Error-Handling. |
