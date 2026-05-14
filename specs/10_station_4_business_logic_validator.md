# Station 4 — Business Logic Validator

Status: DRAFT
Version: v1.0
Architecture: v1.6.1
Last updated: 2026-05-15
Owner: Trading System Project

## Kurzbeschreibung

Diese Station prüft die inhaltliche und logische Kohärenz des technisch validierten LLM-Outputs.

Sie stellt sicher, dass Regime, Multiplikatoren, Risikoflags und Asset-Aktionen keine widersprüchlichen Signale an die Portfolio Engine senden.

Heilbare Widersprüche werden nur dann korrigiert, wenn die Korrektur eindeutig risikoärmer oder risikoneutral ist.

## Input

Ein technisch fehlerfreies, typkonformes Pydantic-Objekt LLMMetaManagerOutput aus Station 3.

## Output

Ein intern konsistentes Datenobjekt für Station 5 oder ein kontrollierter Abbruch.

## Fehlerwirkung

Bei unheilbaren logischen Widersprüchen:

BLOCKED -> SAFE_HOLD / NO_NEW_ACTIONS.

Die Pipeline stoppt. Es erfolgt keine Marktaktion.

Bei heilbaren Widersprüchen:

DOWNGRADED.

Der Output wird restriktiv korrigiert, im Audit Log dokumentiert und weitergegeben.

## Wichtig

Ein Verbot überschreibt immer eine Erlaubnis.

Eine automatische Korrektur darf niemals Risiko erhöhen.

INCREASE darf zu HOLD werden, aber nie umgekehrt.

Der Business Logic Validator darf keine aktive Marktaktion erzwingen.

Insbesondere darf er keine eigenmächtige Liquidation auslösen.

## Regeln

### VAL_BLV_001 — Asset-Duplikate

Prüfung:
Ein Asset kommt mehrfach in target_allocation_adjustments vor.

Reaktion:

- identische Duplikate:
  DOWNGRADED. Ein Eintrag bleibt, Duplikat wird entfernt.

- INCREASE vs HOLD:
  DOWNGRADED. Ergebnis wird auf HOLD gesetzt.

- INCREASE vs DECREASE:
  BLOCKED -> SAFE_HOLD / NO_NEW_ACTIONS.

- INCREASE vs LIQUIDATE:
  BLOCKED -> SAFE_HOLD / NO_NEW_ACTIONS.

- HOLD vs LIQUIDATE:
  BLOCKED -> SAFE_HOLD / NO_NEW_ACTIONS.

Begründung:
Bei fundamentalen Widersprüchen darf der Validator keine aktive Marktaktion erzwingen. LIQUIDATE ist eine echte Handelsabsicht und darf nicht eigenmächtig gewählt werden.

### VAL_BLV_002 — CASH_ONLY braucht risk_multiplier_override = 0.0

Prüfung:
strategy_regime = CASH_ONLY, aber risk_multiplier_override ist nicht 0.0.

Reaktion:
DOWNGRADED.

risk_multiplier_override wird hart auf 0.0 gesetzt.

### VAL_BLV_003 — CASH_ONLY braucht alle Risiko-Flags false

Prüfung:
strategy_regime = CASH_ONLY, aber eines der folgenden Flags ist true:

- allow_new_positions
- allow_add_ons
- allow_risk_increase

Reaktion:
DOWNGRADED.

Alle drei Flags werden hart auf false gesetzt.

### VAL_BLV_004 — CASH_ONLY darf keine INCREASE-Aktion enthalten

Prüfung:
strategy_regime = CASH_ONLY und mindestens ein Asset hat action = INCREASE.

Reaktion:
DOWNGRADED.

Alle INCREASE-Aktionen werden zu HOLD.

### VAL_BLV_005 — DEFENSIVE darf keine Add-ons erlauben

Prüfung:
strategy_regime = DEFENSIVE, aber allow_add_ons = true.

Reaktion:
DOWNGRADED.

allow_add_ons wird hart auf false gesetzt.

### VAL_BLV_006 — BUILDUP/DEFENSIVE mit zu niedrigem risk_multiplier_override

Prüfung:
strategy_regime ist BUILDUP oder DEFENSIVE und risk_multiplier_override < 0.1.

Reaktion:
BLOCKED -> SAFE_HOLD / NO_NEW_ACTIONS.

Kein automatisches Anheben auf 0.1, weil das eine Risikoerhöhung gegenüber dem LLM-Output wäre.

### VAL_BLV_007 — allow_risk_increase=false verbietet INCREASE

Prüfung:
allow_risk_increase = false und mindestens ein Asset hat action = INCREASE.

Reaktion:
DOWNGRADED.

Alle INCREASE-Aktionen werden zu HOLD.

## Audit-Log-Beispiele

### Asset-Duplikat mit Konflikt INCREASE vs HOLD

2026-05-14 23:20:00 | run_112_blv | BusinessLogicValidator | VAL_BLV_001 | DOWNGRADED | NORMAL_CONTINUE | Duplicate asset 'QQQ' found with conflicting actions INCREASE vs HOLD | Resolved to safer action HOLD. Duplicate entry removed.

### Unheilbare Untergrenzen-Verletzung

2026-05-14 23:20:15 | run_113_blv | BusinessLogicValidator | VAL_BLV_006 | BLOCKED | SAFE_HOLD | risk_multiplier_override 0.05 is below 0.1 limit for BUILDUP regime. Auto-raise forbidden | Pipeline execution terminated. No market action.

## Testfälle

### TC_BLV_003 — Gefährliches Duplikat

Szenario:
Das LLM listet SMH zweimal auf. Eintrag 1 fordert INCREASE, Eintrag 2 fordert LIQUIDATE.

Erwartetes Ergebnis:
VAL_BLV_001 greift. Da die beiden Absichten fundamental widersprüchlich sind und LIQUIDATE eine aktive Marktaktion auslösen könnte, darf der BLV keine der beiden Absichten bevorzugen.

Status:
BLOCKED -> SAFE_HOLD / NO_NEW_ACTIONS.

### TC_BLV_004 — Multiplier-Konflikt nach unten

Szenario:
Das LLM wählt strategy_regime = BUILDUP, gibt jedoch risk_multiplier_override = 0.05 an.

Erwartetes Ergebnis:
VAL_BLV_006 schlägt an. Da ein Anheben auf 0.1 eine unzulässige Risikoerhöhung darstellt, bricht das System ab.

Status:
BLOCKED -> SAFE_HOLD / NO_NEW_ACTIONS.

## Aktueller Status

Diese Station ist fachlich abgenommen.

## Codex-Hinweis

Codex darf diese Station später implementieren.

Warum:
Die Regeln sind klar, deterministisch und testbar.

Wie:
Codex implementiert später den BusinessLogicValidator, die Downgrade-Logik, BLOCKED-Fälle, Audit-Events und Unit Tests.

Codex darf keine zusätzliche Reparaturlogik erfinden und keine aktive Marktaktion erzwingen.
