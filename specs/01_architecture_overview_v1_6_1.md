# Architecture Overview v1.6.1

Status: DRAFT
Version: v1.0
Architecture: v1.6.1
Last updated: 2026-05-15
Owner: Trading System Project

## Zweck

Diese Datei beschreibt die übergeordnete Zielarchitektur des Trading Allocator Project.

Die Architektur ist Python-zentriert. Das LLM ist Meta-Manager, nicht Trading-Bot. Python bleibt die finale Rechen-, Validierungs-, Guardrail-, Portfolio- und Simulationsschicht.

## Architekturfluss

GUI / Manual Portfolio Input
↓
User Managed Universe max. 5 Instrumente
↓
IQFeed Data Layer
↓
Python Data Collector
↓
Parquet Data Lake
↓
Data Quality Engine
↓
Universe & Liquidity Check
↓
Dynamic Indicator Registry
↓
Feature Engine
↓
Trend Detection Core
↓
Regime Engine
↓
Dynamic Regime Matrix
↓
Alpha / Signal Engines
↓
Signal Confidence Normalizer
↓
Risk Metrics Engine
↓
Deductive Rule Layer
↓
LLM Meta-Manager
↓
Structured Output / Pydantic Validation
↓
Python Validator Pipeline
↓
Portfolio Engine
↓
Post-Trade Risk Validator
↓
Order Proposal Engine
↓
Order Validator
↓
Execution Simulator
↓
Portfolio Ledger
↓
Historical Report Store / Audit Log
↓
GUI Monitoring / Self-Analysis

## Zentrale Komponenten

### GUI / Manual Portfolio Input

Startpunkt der Tagesanalyse.

Der Benutzer gibt oder bestätigt:
- Portfolio Value
- Cash
- offene Positionen
- Einstandspreise
- Stop-Referenzen
- realized_pnl_today
- aktive Instrumente

### User Managed Universe

Core v1 arbeitet mit maximal 5 aktiven Instrumenten.

Das LLM darf das Universe nicht erweitern, löschen oder verändern.

### IQFeed Data Layer

Primäre Marktdatenquelle für historische und tägliche Marktdaten.

### Parquet Data Lake

Single Source of Truth für gespeicherte Daten, Features, Signale, Portfoliozustände, Reports und Audit Logs.

### Data Quality Engine

Prüft Datenvollständigkeit, Stale Data, fehlende Preise, falsche Handelstage und Feed-Probleme.

Data Invalid führt zu SAFE_HOLD / NO_NEW_ACTIONS, niemals zu CASH_ONLY.

### Feature Engine

Berechnet deterministisch alle benötigten Features.

Das LLM berechnet keine Indikatoren selbst.

### Trend Detection Core

Kritischstes technisches Subsystem.

Erkennt:
- trend_status
- trend_confidence
- momentum_status
- volatility_regime
- regime_shift_probability
- false_breakout_risk

### Regime Engine

Gatekeeper für die Marktumgebung.

Erkennt:
- TREND
- CHOP
- CRASH
- LOW_VOL
- HIGH_VOL
- TRANSITION

### Dynamic Regime Matrix

Deterministische Permission-Schicht.

Bestimmt, welche Strategieklassen, Aktionen und Engines im aktuellen Regime zulässig sind.

### Alpha / Signal Engines

Erzeugen Signale, keine Orders.

Kernbereiche:
- Trend / Momentum / Relative Strength
- Entry / Pullback / Mean Reversion light
- Defensive / Cash / Risk Reduction

### Risk Metrics Engine

Berechnet kontinuierliche Warnsignale wie Drawdown, VaR, Expected Shortfall, Cash Buffer, HHI, Korrelation und systemische Volatilität.

### Deductive Rule Layer

Ökonomisch-logische Leitplanken, die das strategische Spielfeld des LLM begrenzen.

### LLM Meta-Manager

Interpretiert den vorberechneten Kontext und erzeugt strukturierte strategische Absichten.

Das LLM erzeugt keine finalen Orders.

### Structured Output / Pydantic Validation

Erzwingt ein gültiges LLMMetaManagerOutput-Schema.

### Python Validator Pipeline

Prüft technische Struktur, interne Logik, Marktrisiko, Post-Trade-Risiko und finale Ordergültigkeit.

### Portfolio Engine

Wandelt validierte Absichten in ein mögliches Zielportfolio um.

Sie erzeugt noch keine Orders.

### Order Proposal Engine / Execution Simulator

Erzeugt simulierte Ordervorschläge und prüft Ausführungskosten, Slippage, Spread und Liquidität.

Core v1 bleibt Simulation.

## Core-v1-Grenzen

- maximal 5 aktive Instrumente
- kein OFFENSIVE-Regime
- kein Hebel über 1.0
- risk_multiplier_override maximal 1.0
- keine automatische Universe-Erweiterung
- keine automatische Live-Parameteroptimierung
- kein PyTorch/LSTM/Transformer im Kern
- kein vollautomatisches Live-Trading

## Codex-Einordnung

Codex ist kein Teil der Trading-Pipeline.

Codex ist ein Engineering-Werkzeug für:
- Projektstruktur
- Pydantic-Schemas
- Validatoren
- Tests
- Fixtures
- Audit Logging
- Parquet Reader/Writer
- GUI-Grundgerüst

Codex darf keine Architekturentscheidungen treffen, keine Guardrails ändern und keine Trading-Entscheidungen erzeugen.

## Nicht erlaubt

- LLM als direkter Trade-Entscheider.
- Python Guardrails durch Prompt relativieren.
- Technische Fehler als Marktrisiko interpretieren.
- Automatische Liquidation durch Validatoren ohne echten Markt-/Risk-Guardrail-Modus.
- Stille Änderungen ohne Audit Log.
