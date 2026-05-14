# Station 3 — Technical Schema Validator

Status: DRAFT
Version: v1.0
Architecture: v1.6.1
Last updated: 2026-05-15
Owner: Trading System Project

## Kurzbeschreibung

Diese Station übernimmt die strikte technische Prüfung des vom LLM gelieferten Antwortobjekts.

Sie validiert den Output gegen das Pydantic-Schema LLMMetaManagerOutput.

Hier wird entschieden, ob das JSON-Dokument syntaktisch, strukturell und typtechnisch einwandfrei ist, sodass es von den Folge-Validatoren verarbeitet werden darf.

## Input

Das von Station 2 generierte Structured-Output-Objekt, entweder als roher JSON-String oder als noch unvalidiertes Objekt.

## Output

Ein syntaktisch und typtechnisch valides Pydantic-Objekt, das an Station 4 übergeben wird, oder ein Abbruch der Pipeline.

## Fehlerwirkung

Bei unheilbaren Strukturfehlern:

SAFE_HOLD / NO_NEW_ACTIONS.

Die Pipeline stoppt. Es erfolgt keine Marktaktion.

Bei klar begrenzten, nicht-semantischen Formatverletzungen:

DOWNGRADED.

Der Wert wird restriktiv korrigiert, vollständig im Audit Log dokumentiert, und die Pipeline darf weiterlaufen.

## Wichtig

Diese Station darf keine fachliche Entscheidung verändern.

Sie darf niemals aus INCREASE ein HOLD machen, keinen risk_multiplier_override ändern, kein strategy_regime korrigieren und keine fehlenden Pflichtfelder erraten.

Erlaubt ist nur technische Reparatur von nicht-handlungsrelevanten Textfeldern.

## Regeln

### VAL_TSV_001 — JSON nicht parsebar

Prüfung:
Das Objekt ist kein valides, fehlerfrei parsebares JSON.

Reaktion:
BLOCKED -> SAFE_HOLD / NO_NEW_ACTIONS.

Die Pipeline stoppt sofort.

### VAL_TSV_002 — Pflichtfeld fehlt

Prüfung:
Ein im Pydantic-Schema definiertes Pflichtfeld fehlt.

Reaktion:
BLOCKED -> SAFE_HOLD / NO_NEW_ACTIONS.

Es werden keine Feldwerte geraten oder ergänzt.

### VAL_TSV_003 — Datentyp, Enum oder Wertebereich ungültig

Prüfung:
Ein Feld entspricht nicht dem definierten Datentyp, einem erlaubten Enum-Wert oder dem erlaubten Wertebereich.

Beispiele:
- strategy_regime = OFFENSIVE
- action = BUY
- risk_multiplier_override > 1.0
- confidence_score außerhalb 0.0 bis 1.0

Reaktion:
BLOCKED -> SAFE_HOLD / NO_NEW_ACTIONS.

Keine automatische Typ-, Enum- oder Wertebereichskorrektur.

### VAL_TSV_004 — Zu viele Asset-Adjustments

Prüfung:
target_allocation_adjustments enthält mehr als 5 Einträge.

Reaktion:
BLOCKED -> SAFE_HOLD / NO_NEW_ACTIONS.

Station 3 darf nicht entscheiden, welche Assets entfernt werden.

### VAL_TSV_005 — Textfeld überschreitet Längenlimit

Prüfung:
Ein reasoning_short-Feld überschreitet 150 Zeichen.

Erlaubte Felder:
- LLMMetaManagerOutput.reasoning_short
- AllocationAdjustment.reasoning_short

Reaktion:
DOWNGRADED.

Der String wird hart auf exakt 150 Zeichen abgeschnitten.

Die Pipeline läuft weiter.

Ein Audit-Log-Eintrag ist Pflicht.

Nicht erlaubt:
Diese Reparatur gilt nicht für asset_id, strategy_regime, action, strategy_class, reason_codes, confidence_score oder risk_multiplier_override.

## Audit-Log-Beispiele

### Fehlendes Pflichtfeld

2026-05-14 23:12:00 | run_108_tsv | TechnicalSchemaValidator | VAL_TSV_002 | BLOCKED | SAFE_HOLD | Field 'strategy_regime' is missing in LLM output | Execution stopped. No handoff to Station 4. No market action.

### Erlaubte Textkorrektur

2026-05-14 23:12:15 | run_109_tsv | TechnicalSchemaValidator | VAL_TSV_005 | DOWNGRADED | NORMAL_CONTINUE | asset reasoning_short for 'QQQ' length 162 > 150 | Truncated to exactly 150 characters. Object repaired and passed to Station 4.

## Testfälle

### TC_TSV_003 — Fehlendes Pflichtfeld

Szenario:
Das LLM vergisst das globale Feld strategy_regime. Die restliche Struktur inklusive aller Asset-Absichten ist perfekt lesbar.

Erwartetes Ergebnis:
VAL_TSV_002 schlägt an. Das System rät nicht, sondern bricht die Kette sofort ab.

Status:
BLOCKED -> SAFE_HOLD / NO_NEW_ACTIONS.

### TC_TSV_004 — Zu viele Assets

Szenario:
Das LLM liefert eine Liste mit 6 statt der maximal erlaubten 5 Assets in target_allocation_adjustments.

Erwartetes Ergebnis:
VAL_TSV_004 schlägt an. Station 3 darf nicht eigenmächtig entscheiden, welches Asset gestrichen wird.

Status:
BLOCKED -> SAFE_HOLD / NO_NEW_ACTIONS.

## Aktueller Status

Diese Station ist fachlich abgenommen.

## Codex-Hinweis

Codex darf diese Station später implementieren.

Warum:
Die Prüfung ist stark regelbasiert, deterministisch und gut testbar.

Wie:
Codex implementiert später den TechnicalSchemaValidator, die Pydantic-Validierung, die erlaubte reasoning_short-Kürzung, Audit-Events und Unit Tests.

Codex darf keine fachliche Reparaturlogik ergänzen.
