# Station 1 — Pre-LLM Validator

Status: DRAFT
Version: v1.0
Architecture: v1.6.1
Last updated: 2026-05-15
Owner: Trading System Project

## Kurzbeschreibung

Diese Prüfung stellt sicher, dass das System vor dem LLM-Aufruf technisch und funktional arbeitsfähig ist. Sie verhindert unnötige LLM-Kosten, fehlerhafte Analysen und Instabilität bei Datenabriss, unvollständigen Marktdaten oder unplausiblem Portfolio-/Universe-Zustand.

## Input

Marktdatenstatus, Portfolio Status, User Managed Universe, Data Quality Status, Trend Detection Output, Regime Output, Risk Metrics, System-/Analysekonfiguration.

## Output

Freigabe für den LLM-Aufruf, also Weiterleitung zu Station 2, oder sofortiger Stopp der Pipeline.

## Fehlerwirkung

SAFE_HOLD / NO_NEW_ACTIONS.

Die Pipeline stoppt vor dem LLM-Aufruf. Es wird keine Marktaktion ausgelöst.

## Wichtig

Ein Datenabriss, fehlende Preise, ein ungültiges Universe oder ein fehlerhafter Portfolio-Ist-Zustand sind reine technische Integritätsprobleme.

Sie werden strikt von Handelsentscheidungen getrennt und dürfen niemals als Marktrisiko interpretiert werden.

Daher ist CASH_ONLY, also eine aktive Marktaktion zum Abbau von Risiko, hier als Reaktion verboten.

## Aktueller Status

Diese Station ist fachlich abgenommen.

## Codex-Hinweis

Codex darf diese Station später implementieren.

Warum:
Die Prüfungen sind technisch, regelbasiert und klar testbar.

Wie:
Codex implementiert später den PreLLMValidator, ValidationResult, Audit-Events und Unit Tests exakt nach dieser Spezifikation.
