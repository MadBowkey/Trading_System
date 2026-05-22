# Maßnahmenliste

Priorisierte Maßnahmen aus Audit und Entscheidungsmatrix.

## Jetzt
| ID | Maßnahme | Bezug (Modul/Konflikt) | Begründung | Owner | Zieltermin |
|---|---|---|---|---|---|
| A-001 | Minimalen implementierbaren Datenebenen-Slice spezifizieren (Ingest, Validierung, Gate-Outcome) inkl. Akzeptanztests aus Golden Cases. | M01-C01 | Ohne ausführbaren Slice bleibt Modul-1-Prüfung rein dokumentarisch. | Tech Lead Data Pipeline | kurzfristig |

## Später
| ID | Maßnahme | Bezug (Modul/Konflikt) | Begründung | Owner | Zielversion/Zeitfenster |
|---|---|---|---|---|---|
| A-002 | `indicator_registry` und `regime_matrix` fachlich befüllen oder explizites Empty-Policy-Verhalten definieren. | M01-C02 | Reduziert Folgeinkonsistenzen in Risiko-/Portfolio-Modulen. | Quant + Risk | nächste Version |
| A-003 | Konventionsdokument für Konfigurationsdateien (`*.example.yaml` vs. produktiv) erstellen. | M01-C03 | Verhindert Betriebsverwechslungen und reduziert Onboarding-Fehler. | DevOps/Platform | nächste Version |

## Akzeptiert
| ID | Risiko/Konflikt | Begründung der Akzeptanz | Freigabe durch | Datum |
|---|---|---|---|---|