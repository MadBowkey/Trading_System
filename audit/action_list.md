# Maßnahmenliste

Priorisierte Maßnahmen aus Audit und Entscheidungsmatrix.

## Jetzt
| ID | Maßnahme | Bezug (Modul/Konflikt) | Begründung | Owner | Zieltermin |
|---|---|---|---|---|---|
| A-001 | Minimalen implementierbaren Datenebenen-Slice spezifizieren (Ingest, Validierung, Gate-Outcome) inkl. Akzeptanztests aus Golden Cases. | M01-C01 | Ohne ausführbaren Slice bleibt Modul-1-Prüfung rein dokumentarisch. | Tech Lead Data Pipeline | kurzfristig |

## Später
| ID | Maßnahme | Bezug (Modul/Konflikt) | Begründung | Owner | Zielversion/Zeitfenster |
|---|---|---|---|---|---|
| A-004 | Minimalen Station-2-Implementierungsslice spezifizieren (Client-Aufruf, Timeout/Retry, SAFE_HOLD-Fehlerpfad, Übergabe an Station 3). | M02-C01 | Schließt zentrale Verifikationslücke des Intent-Moduls. | Tech Lead Integration | kurzfristig |
| A-005 | Statusharmonisierung für Station 2 (`DRAFT` vs. fachlich abgenommen) mit klarer Freigabedefinition dokumentieren. | M02-C02 | Vermeidet Governance-Widersprüche in Umsetzung und Abnahme. | Architektur/Governance | nächste Version |
| A-006 | Dedizierte Station-2-Golden-Cases ergänzen (Timeout/API-Error/leere Antwort/valides Structured Output). | M02-C03 | Verbessert Testbarkeit und Fehlerpfad-Absicherung. | QA + Platform | nächste Version |
| A-002 | `indicator_registry` und `regime_matrix` fachlich befüllen oder explizites Empty-Policy-Verhalten definieren. | M01-C02 | Reduziert Folgeinkonsistenzen in Risiko-/Portfolio-Modulen. | Quant + Risk | nächste Version |
| A-003 | Konventionsdokument für Konfigurationsdateien (`*.example.yaml` vs. produktiv) erstellen. | M01-C03 | Verhindert Betriebsverwechslungen und reduziert Onboarding-Fehler. | DevOps/Platform | nächste Version |

## Akzeptiert
| ID | Risiko/Konflikt | Begründung der Akzeptanz | Freigabe durch | Datum |
|---|---|---|---|---|
