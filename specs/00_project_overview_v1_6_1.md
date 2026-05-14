# Project Overview v1.6.1

Status: DRAFT
Version: v1.0
Architecture: v1.6.1
Last updated: 2026-05-15
Owner: Trading System Project

## Zweck

Dieses Projekt ist ein regime-adaptiver Portfolio-Allocator mit dynamischer Risikosteuerung, deduktiver Finanzlogik und LLM-Meta-Manager.

Das System soll auf Tagesbasis Markt-, Trend-, Risiko- und Portfolioinformationen auswerten und daraus kontrollierte Portfolio-Anpassungen ableiten.

## Rollenverteilung

- Python ist das Master-System für Berechnung, Validierung, Guardrails, Portfolio Engine, Order Simulation, Logging und Audit.
- Das LLM ist Meta-Manager und erzeugt strukturierte strategische Absichten.
- Das LLM erzeugt keine finalen Orders.
- Codex ist Engineering-Werkzeug und implementiert nur freigegebene Spezifikationen.

## Kernprinzipien

- Risk Metrics sind kontinuierliche Warnsignale.
- Guardrails sind binäre Python-Sperren.
- Deductive Rules begrenzen, was das LLM strategisch wählen darf.
- SAFE_HOLD und CASH_ONLY sind strikt getrennt.
- Jede Python-Korrektur wird im Audit Log gespeichert.
- Keine stille Änderung ohne Audit Log.

## Systemstatus

### SAFE_HOLD / NO_NEW_ACTIONS

Auslöser:

- LLM_OUTPUT_INVALID
- DATA_INVALID
- SCHEMA_ERROR
- Pydantic ValidationError
- stale data
- technischer Pipeline-Fehler

Wirkung:

- keine Marktaktion
- Portfolio bleibt unverändert
- bestehende Broker-Stops laufen weiter
- kein CASH_ONLY

### CASH_ONLY / FORCE_CASH_ONLY

Auslöser:

- echte Drawdown-Guardrail
- VaR-/Risk-Hard-Breach
- Crash-Regime
- Extreme Volatility
- echtes Markt-/Risikoproblem

Wirkung:

- Risikoabbau erlaubt
- keine neuen Risiko-Positionen
- Portfolio Engine plant kontrollierte Reduktion
- Order Validator prüft spätere Ausführung

## Core-v1-Grenzen

- maximal 5 aktive Instrumente
- kein OFFENSIVE-Regime
- kein Hebel über 1.0
- risk_multiplier_override maximal 1.0
- keine automatische Universe-Erweiterung
- keine automatische Live-Parameteroptimierung
- kein PyTorch/LSTM/Transformer im Kern
- kein vollautomatisches Live-Trading

## Nicht erlaubt

- Das LLM darf keine finalen Orders erzeugen.
- Das LLM darf Guardrails nicht ändern.
- Das LLM darf das Universe nicht verändern.
- Validatoren dürfen keine eigenmächtige Liquidation erzwingen.
- Technische Fehler dürfen niemals CASH_ONLY auslösen.
