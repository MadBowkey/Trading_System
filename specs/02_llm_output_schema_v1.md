# LLM Output Schema v1

Status: DRAFT
Version: v1.0
Architecture: v1.6.1
Last updated: 2026-05-15
Owner: Trading System Project

## Zweck

Diese Spezifikation beschreibt die logische Struktur des Pydantic-Output-Schemas für den LLM Meta-Manager.

Das LLM erzeugt keine Orders, sondern ausschließlich eine strukturierte strategische Absicht.

## Hauptobjekt

LLMMetaManagerOutput

## Struktur

LLMMetaManagerOutput enthält:

- schema_version
- run_id
- strategy_regime
- risk_multiplier_override
- allow_new_positions
- allow_add_ons
- allow_risk_increase
- target_allocation_adjustments
- reasoning_short

## strategy_regime

Erlaubte Werte:

- BUILDUP
- DEFENSIVE
- CASH_ONLY

Nicht erlaubt:

- OFFENSIVE

## risk_multiplier_override

Erlaubter Wertebereich:

- 0.0 bis 1.0

Regeln:

- BUILDUP / DEFENSIVE: 0.1 bis 1.0
- CASH_ONLY: exakt 0.0
- Werte > 1.0 sind verboten
- kein Hebeln über die Core-v1-Baseline

## target_allocation_adjustments

Liste von AllocationAdjustment-Objekten.

Regeln:

- maximal 5 Einträge
- jedes Asset darf nur einmal vorkommen
- alle Assets müssen aus dem User Managed Universe oder aus bestehenden Portfolio-Altbeständen stammen

## AllocationAdjustment

Ein AllocationAdjustment enthält:

- asset_id
- action
- strategy_class
- confidence_score
- asset_risk_multiplier_override
- reason_codes
- reasoning_short

## action

Erlaubte Werte:

- HOLD
- INCREASE
- DECREASE
- LIQUIDATE

Bedeutung:

- HOLD: keine Veränderung der Position
- INCREASE: strategische Absicht zur Erhöhung
- DECREASE: strategische Absicht zur Reduktion
- LIQUIDATE: strategische Absicht zur vollständigen Schließung

Wichtig:

Diese Aktionen sind keine finalen Orders.

## strategy_class

Erlaubte Werte:

- TREND_FOLLOWING
- TREND_PULLBACK
- TREND_MONITORING
- RISK_CONTROL
- DEFENSIVE_CASH
- NO_ACTION

## confidence_score

Erlaubter Wertebereich:

- 0.0 bis 1.0

Bedeutung:

Der confidence_score beschreibt die LLM-Konfidenz für diese konkrete Asset-Absicht.

## asset_risk_multiplier_override

Optionaler asset-spezifischer Risikomultiplikator.

Erlaubter Wertebereich:

- null
- 0.0 bis 1.0

Wenn null, gilt der globale risk_multiplier_override.

## reason_codes

Liste standardisierter Begründungscodes.

Zweck:

- spätere Auswertung
- Audit
- Reporting
- Self-Analysis
- Testbarkeit

## reasoning_short

Kurze Begründung.

Regel:

- maximal 150 Zeichen

Wenn reasoning_short länger als 150 Zeichen ist, darf Station 3 den String hart auf exakt 150 Zeichen kürzen.

## Interne Konsistenzregeln

- Keine unbekannten Felder.
- Keine unbekannten Enum-Werte.
- Kein Asset doppelt in target_allocation_adjustments.
- CASH_ONLY braucht risk_multiplier_override = 0.0.
- CASH_ONLY braucht allow_new_positions = false.
- CASH_ONLY braucht allow_add_ons = false.
- CASH_ONLY braucht allow_risk_increase = false.
- CASH_ONLY darf keine INCREASE-Aktionen enthalten.
- DEFENSIVE darf keine Add-ons erlauben.
- BUILDUP / DEFENSIVE brauchen risk_multiplier_override >= 0.1.
- allow_risk_increase = false verbietet INCREASE-Aktionen.

## Nicht erlaubt

- Das LLM darf keine BUY- oder SELL-Orders erzeugen.
- Das LLM darf keine Stückzahlen erzeugen.
- Das LLM darf keine finalen Zielgewichte festlegen.
- Das LLM darf kein neues StrategyRegime erfinden.
- Das LLM darf keine Guardrails ändern.
- Das LLM darf das User Managed Universe nicht verändern.

## Codex-Hinweis

Codex darf dieses Schema später als Pydantic-Modell implementieren.

Warum:
Die Struktur ist klar typisiert, regelbasiert und testbar.

Wie:
Codex implementiert später Enums, BaseModel-Klassen, Field-Grenzen, interne Validatoren und JSON-Schema-Export.

Codex darf keine zusätzlichen Felder, Enums oder Reparaturlogiken ergänzen.
