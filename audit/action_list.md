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
| A-004 | Maßnahmenpaket zu Modul 02 (Betriebsreife Station-2-Laufzeitpfad) in Matrix priorisieren und Entscheidungsoption festlegen. | M02-C01 | Kritischer Übergangspfad ohne nachweisbare Runtime; Priorisierung nur über Matrix-Entscheid. | Architekturboard | in Matrix zu entscheiden |
| A-005 | Verbindlichen Hand-off-Contract 02->03 als Entscheidungsoption in Matrix aufnehmen (inkl. Fehlerpfad-Definition). | M02-C02 | Senkt Governance-/Schnittstellenrisiko ohne direkte Implementierungsfestlegung im Audit. | Tech Lead Core Pipeline | in Matrix zu entscheiden |
| A-006 | Nachweis-/Auditierbarkeitsoption für API-/Timeout-Fehlerpfade als Matrix-Option dokumentieren. | M02-C03 | Erhöht Traceability für Ausnahmefälle; aktuell nachrangig. | QA/Audit | in Matrix zu entscheiden |

## Akzeptiert
| ID | Risiko/Konflikt | Begründung der Akzeptanz | Freigabe durch | Datum |
|---|---|---|---|---|
