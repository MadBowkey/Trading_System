# Validator Pipeline v1

Status: DRAFT
Version: v1.0
Architecture: v1.6.1
Last updated: 2026-05-15
Owner: Trading System Project

## Zweck

Diese Spezifikation definiert die 8-stufige Validierungs-Pipeline vom Eingangszustand bis zur Order-Prüfung.

Die Pipeline trennt technische Integrität, strategische LLM-Absicht, Marktrisiko, Portfolio-Konstruktion und finale Ordervalidierung.

## Pipeline

1. Pre-LLM Validator
2. LLM Meta-Manager
3. Technical Schema Validator
4. Business Logic Validator
5. Market Risk Validator
6. Portfolio Engine
7. Post-Trade Risk Validator
8. Order Validator

## Grundprinzip

Technische Fehler führen zu SAFE_HOLD / NO_NEW_ACTIONS.

Echte Markt- oder Risikoprobleme führen zu FORCE_CASH_ONLY, BLOCK_RISK_INCREASE oder kontrollierter Risikoreduktion.

Das LLM erzeugt nur strategische Absichten. Python validiert, berechnet, blockiert und simuliert.

## Stationen

### 1. Pre-LLM Validator

Prüft, ob die Eingangsdaten belastbar genug sind, um das LLM überhaupt aufzurufen.

Fehlerwirkung:
SAFE_HOLD / NO_NEW_ACTIONS. Kein LLM-Aufruf. Keine Marktaktion.

### 2. LLM Meta-Manager

Erzeugt aus freigegebenen Markt-, Trend-, Risiko- und Portfolio-Kontexten eine strukturierte strategische Absicht.

Fehlerwirkung:
Bei API-Fehlern, Timeout, Nichterreichbarkeit oder leerer Antwort: SAFE_HOLD / NO_NEW_ACTIONS.

### 3. Technical Schema Validator

Prüft technische Gültigkeit des LLM-Outputs gegen das Pydantic-Schema.

Fehlerwirkung:
Bei Strukturfehlern: SAFE_HOLD / NO_NEW_ACTIONS.
Bei erlaubten Textkorrekturen: DOWNGRADED.

### 4. Business Logic Validator

Prüft interne logische Konsistenz des technisch gültigen LLM-Outputs.

Fehlerwirkung:
Nicht reparierbare Widersprüche: SAFE_HOLD / NO_NEW_ACTIONS.
Sicher reparierbare Widersprüche: DOWNGRADED.

### 5. Market Risk Validator

Gleicht die LLM-Absicht mit realen Markt-, Trend-, Risiko-, Universe- und Portfolio-Daten ab.

Fehlerwirkung:
Echtes Marktrisiko: FORCE_CASH_ONLY oder BLOCK_RISK_INCREASE.
Heilbares Asset-Risiko: DOWNGRADED.
Technische Inkonsistenz: SAFE_HOLD / NO_NEW_ACTIONS.

### 6. Portfolio Engine

Berechnet aus der validierten strategischen Absicht ein mögliches Zielportfolio.

Fehlerwirkung:
Wenn keine zulässige Zielstruktur berechnet werden kann, wird der Vorschlag blockiert oder zur Neuberechnung markiert.

### 7. Post-Trade Risk Validator

Prüft, ob das berechnete Zielportfolio nach der geplanten Anpassung innerhalb der harten Risikogrenzen bleibt.

Fehlerwirkung:
BLOCK_RISK_INCREASE, RECALCULATE_PORTFOLIO, DOWNSIZE_REQUIRED oder FORCE_CASH_ONLY.

### 8. Order Validator

Prüft finale simulierte Ordervorschläge vor Execution Simulation oder späterem Paper Trading.

Fehlerwirkung:
Ungültige Orders werden blockiert. Bei SAFE_HOLD gibt es grundsätzlich keine Orders.

## Wichtig

SAFE_HOLD und CASH_ONLY dürfen niemals vermischt werden.

Ein technischer Fehler ist kein Marktrisiko.

Eine echte Markt-Guardrail darf nur durch echte Markt- oder Risikodaten ausgelöst werden.

Keine Station darf Risiko eigenmächtig erhöhen.

Keine Station darf Änderungen ohne Audit Log durchführen.

## Codex-Hinweis

Codex darf diese Pipeline später implementieren, aber keine Station hinzufügen, entfernen oder fachlich verändern.

Codex-Aufgaben später:

- Validator-Klassen erstellen
- gemeinsames ValidationResult-Modell erstellen
- Rule Registry einbinden
- Unit Tests pro Station schreiben
- Golden Cases umsetzen
