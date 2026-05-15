# Station 7 — Post-Trade Risk Validator

Status: DRAFT
Version: v1.0
Architecture: v1.6.1
Last updated: 2026-05-15
Owner: Trading System Project

## Kurzbeschreibung

Diese Station ist die ex-ante Kontrollinstanz für das Gesamtportfolio.

Sie übernimmt die mandats-, regel- und risikobasierte Überprüfung der von der Portfolio Engine berechneten vorläufigen Portfolio-Struktur.

Sie stellt sicher, dass das hypothetische Zielportfolio keine harten Risiko-, Konzentrations-, Cash-/Liquiditäts-, Exposure-, Korrelations- oder Diversifikationsgrenzen verletzt, bevor konkrete Ordervorschläge abgeleitet werden.

## Input

Aus Station 6:

- Zielgewichtungen
- Delta-Gewichte
- Cash-Quote nach Rebalancing
- Exposure nach Rebalancing
- Positionsänderungsplan
- vorläufige Portfolio-Projektion

Zusätzlich:

- Guardrails
- Post-Trade-Risk-Metrics
- Mandatsgrenzen
- Konzentrationslimits
- HHI
- Portfolio-Korrelationslimits
- Cash-Buffer-Regeln
- Leverage-Limits
- Single-Asset-Exposure-Limits

## Output

Freigabe des unveränderten geprüften Zielportfolios für Station 8 oder vollständige Ablehnung des Zielportfolio-Vorschlags.

## Fehlerwirkung

### Erfolgreiche Prüfung

Validator-Status:

PORTFOLIO_VALIDATED

Systemstatus:

NORMAL_CONTINUE

Pipeline:

CONTINUE

### Verletzung harter Post-Trade-Limits

Validator-Status:

POST_TRADE_RISK_REJECTED

Systemstatus:

NO_NEW_ACTIONS

Pipeline:

STOP_BEFORE_STATION_8

Marktaktion:

keine

Orders:

keine

### Technischer Fehler oder Datenabriss

Validator-Status:

TECHNICAL_ERROR

Systemstatus:

SAFE_HOLD / NO_NEW_ACTIONS

Pipeline:

STOP

Marktaktion:

keine

Orders:

keine

## Wichtig

Der Post-Trade Risk Validator arbeitet rein binär auf Portfolio-Ebene.

Er darf nicht:

- Einzel-Assets manipulieren
- Aktionen downgraden
- Gewichte verschieben
- Zielstrukturen reparieren
- neu optimieren
- Orders erzeugen
- Zielportfolios teilweise freigeben

Entweder erfüllt das von Station 6 berechnete Gesamtportfolio alle Post-Trade-Risikolimits zeitgleich, oder der gesamte Vorschlag wird verworfen.

Station 7 prüft.

Station 7 repariert nicht.

Station 7 verändert nicht.

Station 7 erzeugt keine Orders.

## Regeln

### VAL_PTR_001 — Single Asset Exposure Limit Breach

Prüfung:

Überschreitet das berechnete Zielgewicht eines einzelnen Assets die konfigurierte Einzelwert- oder Mandatsgrenze?

Fehlerfall:

Ja.

Validator-Status:

POST_TRADE_RISK_REJECTED

Systemstatus:

NO_NEW_ACTIONS

Pipeline:

STOP_BEFORE_STATION_8

Marktaktion:

keine

Orders:

keine

Begründung:

Das von Station 6 berechnete Zielportfolio verletzt ein hartes Einzelwertlimit. Der PTRV darf das Gewicht nicht selbst reduzieren, sondern muss den gesamten Zielportfolio-Vorschlag verwerfen.

### VAL_PTR_002 — HHI Concentration Limit Breach

Prüfung:

Überschreitet der berechnete Herfindahl-Hirschman-Index des Zielportfolios die konfigurierte harte Konzentrationsgrenze?

Core-v1-Referenzwert:

HHI > 0.40 gilt als harte Konzentrationsverletzung.

Fehlerfall:

Ja.

Validator-Status:

POST_TRADE_RISK_REJECTED

Systemstatus:

NO_NEW_ACTIONS

Pipeline:

STOP_BEFORE_STATION_8

Marktaktion:

keine

Orders:

keine

Begründung:

Das Zielportfolio ist zu stark konzentriert. Der PTRV darf keine Gewichte verschieben oder neu optimieren, sondern verwirft den gesamten Vorschlag.

### VAL_PTR_003 — Missing or Invalid Risk Configuration

Prüfung:

Sind alle notwendigen Mandatsgrenzen, Guardrails, Post-Trade-Risk-Metrics und Konfigurationsdaten vollständig, aktuell und berechenbar?

Fehlerfall:

Nein.

Validator-Status:

TECHNICAL_ERROR

Systemstatus:

SAFE_HOLD / NO_NEW_ACTIONS

Pipeline:

STOP

Marktaktion:

keine

Orders:

keine

Begründung:

Fehlende oder nicht ladbare Risiko- und Mandatsdaten führen zu technischem Blindflug. Das System friert den Lauf ein und erzeugt keine Orders.

## Audit-Log-Beispiele

### Fachliche Limit-Ablehnung

2026-05-15 02:55:00 | run_140_ptr | PostTradeRiskValidator | VAL_PTR_001 | POST_TRADE_RISK_REJECTED | Calculated target weight for 'SMH' (24.5%) exceeds configured single-asset exposure limit (20.0%) | System state: NO_NEW_ACTIONS | Pipeline: STOP_BEFORE_STATION_8 | Market action: none | Orders: none | Target portfolio rejected. No mutation allowed.

### HHI-Konzentrationsverletzung

2026-05-15 02:55:08 | run_141_ptr | PostTradeRiskValidator | VAL_PTR_002 | POST_TRADE_RISK_REJECTED | Calculated Herfindahl-Hirschman-Index (0.41) exceeds hard concentration limit of 0.40 | System state: NO_NEW_ACTIONS | Pipeline: STOP_BEFORE_STATION_8 | Market action: none | Orders: none | Target portfolio rejected. No mutation allowed.

### Technischer Infrastruktur-Fehler

2026-05-15 02:55:15 | run_142_ptr | PostTradeRiskValidator | VAL_PTR_003 | TECHNICAL_ERROR | Critical data missing: Failed to load mandate configuration limits from system database | System state: SAFE_HOLD | Pipeline: STOP | Market action: none | Orders: none | Execution aborted.

## Testfälle

### TC_PTR_001 — Fachliche Mandatsverletzung auf Portfolio-Ebene

Szenario:

Station 6 liefert eine mathematisch fehlerfreie Portfolio-Struktur. Der ETF SMH erhält darin ein berechnetes Zielgewicht von 24.5 Prozent. Die Konfiguration des Kontos begrenzt das maximale Gewicht pro Einzelwert dynamisch auf 20.0 Prozent. Die Datenfeeds sind voll intakt.

Erwartetes Ergebnis:

VAL_PTR_001 schlägt an.

Validator-Status:

POST_TRADE_RISK_REJECTED

Systemstatus:

NO_NEW_ACTIONS

Pipeline:

STOP_BEFORE_STATION_8

Marktaktion:

keine

Orders:

keine

Der Vorschlag wird vollständig verworfen.

### TC_PTR_002 — Fachliche Diversifikations-Verletzung

Szenario:

Die Portfolio Engine berechnet ein stark konzentriertes Zielportfolio. Der daraus resultierende HHI beträgt mathematisch 0.41. Die systemseitige Risikovorgabe erlaubt maximal einen HHI-Konzentrationswert von 0.40. Die Datenfeeds sind voll intakt.

Erwartetes Ergebnis:

VAL_PTR_002 schlägt an.

Validator-Status:

POST_TRADE_RISK_REJECTED

Systemstatus:

NO_NEW_ACTIONS

Pipeline:

STOP_BEFORE_STATION_8

Marktaktion:

keine

Orders:

keine

Der Lauf wird risikoseitig kontrolliert abgebrochen.

### TC_PTR_003 — Technischer Fehler durch Datenfeed-Abriss

Szenario:

Der Validator versucht, die Risikoprüfung zu starten, kann jedoch die aktuellen Mandatsgrenzen und HHI-Schwellenwerte nicht aus der System-Datenbank laden, da die Verbindung mitten im Lauf abbricht. Pflichtdaten fehlen.

Erwartetes Ergebnis:

VAL_PTR_003 schlägt an.

Validator-Status:

TECHNICAL_ERROR

Systemstatus:

SAFE_HOLD

Pipeline:

STOP

Marktaktion:

keine

Orders:

keine

Das System wird im sicheren Ruhezustand eingefroren.

## Aktueller Status

Diese Station ist fachlich abgenommen.

## Codex-Hinweis

Codex darf diese Station später implementieren.

Warum:

Der Post-Trade Risk Validator ist eine deterministische, binäre Prüfkomponente und gut testbar.

Wie:

Codex implementiert später PostTradeRiskValidator, PortfolioValidationResult, Regelprüfungen, Audit-Events und Unit Tests exakt nach dieser Spezifikation.

Codex darf keine Gewichte verändern, keine Aktionen downgraden, keine Zielstruktur reparieren und keine Orderlogik ergänzen.
