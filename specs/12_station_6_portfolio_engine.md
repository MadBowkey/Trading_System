# Station 6 — Portfolio Engine

Status: DRAFT
Version: v1.0
Architecture: v1.6.1
Last updated: 2026-05-15
Owner: Trading System Project

## Kurzbeschreibung

Diese Station ist eine rein mathematische Berechnungsinstanz.

Sie nimmt die marktbereinigten strategischen Absichten und Risikovorgaben aus Station 5 entgegen und transformiert sie in konkrete, vorläufige Ziel- und Delta-Gewichte.

Sie trifft keine neuen Risikoentscheidungen, wendet keine Guardrails an und führt keine semantischen Reparaturen durch.

Entweder erzeugt sie einen konsistenten Portfolio-Vorschlag oder sie stoppt den aktuellen Lauf ohne Marktaktion.

## Input

Aus Station 5:

- marktbereinigte Asset-Absichten
- finaler risk_multiplier_override
- strategy_regime: BUILDUP, DEFENSIVE oder CASH_ONLY
- Systemstatus, falls vorhanden
- bereinigte HOLD / INCREASE / DECREASE / LIQUIDATE-Absichten

System- und Portfoliodaten:

- aktuelle Asset-Preise
- aktueller Portfolio-Ist-Zustand
- Ist-Gewichte
- Portfolio Value
- Cash-Bestand
- bestehende Positionen
- aktuelle Positionsgrößen
- User Managed Universe
- Allokationsparameter
- Positionslimits

Optional für spätere Erweiterung:

- Kovarianzmatrizen
- Volatilitätsdaten

Für Core v1 sind komplexe Optimierungsverfahren nicht zwingend. Die Portfolio Engine soll zunächst deterministisch und nachvollziehbar arbeiten.

## Output

Eine vorläufige Portfolio-Struktur für Station 7.

Der Output enthält:

- target_weights
- delta_weights
- cash_after_rebalance
- cash_quota_after_rebalance
- gross_exposure_after_rebalance
- net_exposure_after_rebalance
- position_change_plan
- preliminary_portfolio_projection

Die Zielstruktur muss rechnerisch geschlossen sein:

Summe aller Asset-Zielgewichte + Cash-Quote = 1.0

Erlaubte Toleranz:

±0.0001

## Fehlerwirkung

### Erfolgreiche Berechnung

Engine-Status:

PORTFOLIO_PROPOSAL_CREATED

Systemstatus:

NORMAL_CONTINUE

Pipeline:

CONTINUE

### Mathematisch nicht lösbar

Engine-Status:

PORTFOLIO_CONSTRUCTION_FAILED

Systemstatus:

NO_NEW_ACTIONS

Pipeline:

STOP_BEFORE_STATION_7

Marktaktion:

keine

### Technischer Fehler oder invalider Engine-Output

Engine-Status:

TECHNICAL_ERROR

Systemstatus:

SAFE_HOLD / NO_NEW_ACTIONS

Pipeline:

STOP

Marktaktion:

keine

## Wichtig

Die Portfolio Engine ist eine passive Rechenkomponente.

Sie darf nicht:

- INCREASE zu HOLD ändern
- HOLD zu INCREASE ändern
- Assets eigenmächtig entfernen
- LIQUIDATE erzwingen
- Zwangsverkäufe auslösen
- risk_multiplier_override ändern
- strategy_regime ändern
- Guardrails anwenden
- Post-Trade-Risiko final bewerten
- Orders erzeugen
- blockierte Assets reaktivieren

Station 6 berechnet.

Station 6 repariert nicht.

Station 6 entscheidet kein Risiko.

Station 6 erzeugt keine Orders.

## Regeln

### VAL_ENG_001 — Feasibility Check

Prüfung:

Kann unter den gegebenen Inputs eine zulässige Zielallokation berechnet werden?

Fehlerfall:

Keine zulässige Zielgewichtung berechenbar, z. B. weil die Cash-Restriktion nicht eingehalten werden kann.

Engine-Status:

PORTFOLIO_CONSTRUCTION_FAILED

Systemstatus:

NO_NEW_ACTIONS

Pipeline:

STOP_BEFORE_STATION_7

Marktaktion:

keine

### VAL_ENG_002 — Summen-Integrität

Prüfung:

Beträgt die Summe aller berechneten Asset-Zielgewichte inklusive Cash-Quote exakt 1.0 innerhalb der erlaubten Toleranz ±0.0001?

Fehlerfall:

Nein.

Engine-Status:

TECHNICAL_ERROR

Systemstatus:

SAFE_HOLD / NO_NEW_ACTIONS

Pipeline:

STOP

Begründung:

Ein nicht geschlossenes Zielportfolio ist kein fachlicher Optimierungsfehler, sondern ein invalider Engine-Output. Die Portfolio Engine darf kein rechnerisch inkonsistentes Portfolio an Station 7 übergeben.

### VAL_ENG_003 — Input- und Datenintegrität

Prüfung:

Sind alle für die Berechnung notwendigen technischen Inputdaten vollständig, aktuell und mathematisch plausibel?

Fehlerbeispiele:

- Preis fehlt
- Preis <= 0
- Portfolio Value <= 0
- Cash-Bestand fehlt
- Positionsdaten widersprechen Portfolio Value
- Portfolio Value ist veraltet oder nicht mit Positionsdaten vereinbar
- Division durch Null
- numerischer Pflichtwert fehlt

Engine-Status:

TECHNICAL_ERROR

Systemstatus:

SAFE_HOLD / NO_NEW_ACTIONS

Pipeline:

STOP

Marktaktion:

keine

## Audit-Log-Beispiele

### Feasibility-Fehler

2026-05-15 02:41:15 | run_131_eng | PortfolioEngine | VAL_ENG_001 | PORTFOLIO_CONSTRUCTION_FAILED | Insufficient cash to construct requested target allocation | System state: NO_NEW_ACTIONS | Pipeline: STOP_BEFORE_STATION_7 | Market action: none | Portfolio construction halted.

### Invalider Engine-Output

2026-05-15 02:41:22 | run_132_eng | PortfolioEngine | VAL_ENG_002 | TECHNICAL_ERROR | Target allocation sum equals 0.985, expected 1.0 ± 0.0001 | System state: SAFE_HOLD | Pipeline: STOP | Market action: none | System frozen due to invalid engine output.

## Testfälle

### TC_ENG_001 — Feasibility-Fehler durch Cash-Mangel

Szenario:

Station 5 übergibt eine erlaubte INCREASE-Absicht für SMH. Die Portfolio-Daten sind technisch gültig. Die Engine stellt bei der Zielgewichtberechnung jedoch fest, dass unter Einhaltung der Cash-Restriktion keine zulässige Zielallokation berechnet werden kann, ohne den Cash-Bestand negativ werden zu lassen.

Erwartetes Ergebnis:

VAL_ENG_001 schlägt an.

Die Engine meldet:

PORTFOLIO_CONSTRUCTION_FAILED

Systemstatus:

NO_NEW_ACTIONS

Pipeline:

STOP_BEFORE_STATION_7

Marktaktion:

keine

### TC_ENG_001B — Technischer Fehler durch veralteten Portfolio Value

Szenario:

Die Engine erkennt, dass der Portfolio Value veraltet, widersprüchlich oder nicht mit den mathematischen Positionsdaten vereinbar ist.

Erwartetes Ergebnis:

VAL_ENG_003 schlägt an.

Die Engine meldet:

TECHNICAL_ERROR

Systemstatus:

SAFE_HOLD

Pipeline:

STOP

Marktaktion:

keine

### TC_ENG_002 — Invalider Engine-Output bei Summen-Prüfung

Szenario:

Der Berechnungsalgorithmus schließt die Berechnung ab, bricht jedoch eine Schleife zu früh ab. Das ausgegebene Zielportfolio addiert sich inklusive Cash-Quote nur auf 0.985.

Erwartetes Ergebnis:

VAL_ENG_002 schlägt an.

Da der Output mathematisch korrupt ist, meldet die Engine:

TECHNICAL_ERROR

Systemstatus:

SAFE_HOLD

Pipeline:

STOP

Marktaktion:

keine

## Aktueller Status

Diese Station ist fachlich abgenommen.

## Codex-Hinweis

Codex darf diese Station später implementieren.

Warum:

Die Portfolio Engine ist eine deterministische mathematische Berechnungsinstanz und gut testbar.

Wie:

Codex implementiert später PortfolioEngine, PortfolioProposal, Zielgewichtberechnung, Summenprüfung, Feasibility-Prüfung, Audit-Events und Unit Tests exakt nach dieser Spezifikation.

Codex darf keine semantischen Downgrades, keine Guardrail-Entscheidungen und keine Orderlogik ergänzen.
