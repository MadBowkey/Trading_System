# Station 5 — Market Risk Validator

Status: DRAFT
Version: v1.0
Architecture: v1.6.1
Last updated: 2026-05-15
Owner: Trading System Project

## Kurzbeschreibung

Diese Station gleicht die intern konsistenten strategischen Absichten des LLM mit echten Markt-, Trend-, Risiko- und Systemdaten ab.

Während Station 4 nur die innere Logik des LLM-Outputs prüft, stellt Station 5 sicher, dass die Absichten mit der realen Marktlage, dem erlaubten Universe und den aktuellen Risikometriken vereinbar sind.

## Input

Ein intern konsistentes Pydantic-Objekt aus Station 4.

Zusätzlich:

- Trend Detection Output
- Regime Output
- Risk Metrics
- Portfolio Status
- User Managed Universe
- Blacklist
- Korrelationen
- HHI
- Liquiditätsdaten
- System-/Analysekonfiguration

## Output

Ein marktbereinigtes Absichts-Objekt für Station 6.

Einzelne Asset-Aktionen können blockiert, entfernt oder auf risikoärmere Aktionen herabgestuft worden sein.

Globale Risikozustände können BLOCK_RISK_INCREASE oder FORCE_CASH_ONLY auslösen.

## Fehlerwirkung

Bei echten Markt-/Risikoverletzungen:

FORCE_CASH_ONLY, BLOCK_RISK_INCREASE oder assetbezogene Herabstufung.

Bei nicht behebbaren technischen Inkonsistenzen, die in dieser Station unerwartet sichtbar werden:

SAFE_HOLD / NO_NEW_ACTIONS.

## Wichtig

Diese Station darf fachliche Entscheidungen verändern, aber nur risikosenkend oder risikoneutral.

Sie darf INCREASE zu HOLD herabstufen, ein riskantes Asset entfernen oder Risikoerhöhung blockieren.

Sie darf niemals Risiko erhöhen.

Sie darf niemals eine aktive Liquidation eigenmächtig erzwingen, außer ein echter Markt-/Risk-Guardrail-Modus erlaubt kontrollierten Risikoabbau über die nachfolgenden Stationen.

Technischer Fehler führt zu SAFE_HOLD.

Echtes Marktrisiko führt zu FORCE_CASH_ONLY oder BLOCK_RISK_INCREASE.

Heilbares Asset-Risiko führt zu DOWNGRADED.

## Regeln bisher

### VAL_MRV_004A — Asset außerhalb Universe ohne Bestand

Prüfung:
Ein Asset ist nicht im User Managed Universe enthalten und es existiert keine bestehende Position im Portfolio Status.

Reaktion:
DOWNGRADED.

Das Asset wird aus target_allocation_adjustments entfernt.

Begründung:
Es gibt keinen legitimen Verwaltungsbedarf für ein unbekanntes oder nicht erlaubtes Asset ohne Bestand. Kein Neuaufbau außerhalb des User Managed Universe.

### VAL_MRV_004B — Asset außerhalb Universe mit Altbestand und INCREASE

Prüfung:
Ein Asset ist nicht im User Managed Universe enthalten, es existiert aber eine bestehende Position, und das LLM fordert INCREASE.

Reaktion:
DOWNGRADED.

INCREASE wird zu HOLD.

Begründung:
Altbestände dürfen verwaltet werden, aber ein Neuaufbau außerhalb des aktiven Universe ist verboten.

### VAL_MRV_004C — Asset außerhalb Universe mit Altbestand und Verwaltungsaktion

Prüfung:
Ein Asset ist nicht im User Managed Universe enthalten, es existiert aber eine bestehende Position, und die Aktion ist HOLD, DECREASE oder LIQUIDATE.

Reaktion:
PASS_WITH_CONSTRAINTS.

Die Absicht wird als Bestandsverwaltung an Station 6 weitergegeben.

Begründung:
Altpositionen dürfen nicht still gelöscht oder ignoriert werden. Sie müssen gehalten, reduziert oder zur Glattstellung vorgeschlagen werden können.

## Audit-Log-Beispiele

### Universe-Verletzung ohne Bestand

2026-05-14 23:42:00 | run_118_mrv | MarketRiskValidator | VAL_MRV_004A | DOWNGRADED | NORMAL_CONTINUE | Asset 'XYZ' is outside the active universe and has no current holdings | Removed 'XYZ' from target_allocation_adjustments.

### Universe-Verletzung mit Altbestand und INCREASE-Block

2026-05-14 23:42:15 | run_119_mrv | MarketRiskValidator | VAL_MRV_004B | DOWNGRADED | NORMAL_CONTINUE | Asset 'QQQ' is outside the active universe but position exists. Requested action: INCREASE | Action forced to HOLD to prevent unauthorized buying.

### Universe-Verletzung mit Altbestand und LIQUIDATE

2026-05-14 23:42:30 | run_120_mrv | MarketRiskValidator | VAL_MRV_004C | PASS_WITH_CONSTRAINTS | NORMAL_CONTINUE | Asset 'QQQ' is outside the active universe but position exists. Requested action: LIQUIDATE | Passed to Portfolio Engine as inventory management action.

## Testfälle

### TC_MRV_005 — Universums-Ausschluss bei Neubestand

Szenario:
Das LLM fordert ein INCREASE für ein unbekanntes Asset XYZ. Der Abgleich mit User Managed Universe und Portfolio Status zeigt: Das Asset existiert weder in der Konfiguration noch im aktuellen Depot.

Erwartetes Ergebnis:
VAL_MRV_004A schlägt an.

Status:
DOWNGRADED.

Aktion:
Das Asset wird komplett aus target_allocation_adjustments entfernt.

### TC_MRV_006 — Abbaubarkeit von Altbeständen außerhalb des Universe

Szenario:
Das LLM fordert LIQUIDATE für QQQ. QQQ wurde aus dem User Managed Universe entfernt. Im Portfolio Status existiert jedoch noch eine QQQ-Position.

Erwartetes Ergebnis:
VAL_MRV_004C greift.

Status:
PASS_WITH_CONSTRAINTS.

Aktion:
Die Absicht bleibt erhalten und wird an die Portfolio Engine übergeben, damit diese die Glattstellung mathematisch einplanen kann.

### TC_MRV_007 — Neuaufbau eines Altbestands außerhalb des Universe

Szenario:
Das LLM fordert INCREASE für QQQ. QQQ wurde aus dem User Managed Universe entfernt. Im Portfolio Status existiert jedoch noch eine QQQ-Position.

Erwartetes Ergebnis:
VAL_MRV_004B greift.

Status:
DOWNGRADED.

Aktion:
INCREASE wird zu HOLD.

## Offene Regeln

Noch zu spezifizieren:

- Blacklist
- Makro-/Stress-Regeln
- Trend-Konformität
- Korrelation
- HHI / Konzentration
- Confidence-Schwellen
- Risk Metrics nahe Guardrail

## Aktueller Status

Diese Station ist begonnen.

VAL_MRV_004A, VAL_MRV_004B und VAL_MRV_004C sind fachlich abgenommen.

Die übrigen MRV-Regeln sind noch offen.

## Codex-Hinweis

Codex darf diese Station später implementieren, sobald alle MRV-Regeln finalisiert sind.

Warum:
Die Regeln sind deterministisch, gut testbar und sicherheitskritisch.

Wie:
Codex implementiert später den MarketRiskValidator, Universe-/Altbestandslogik, Downgrade-Logik, Audit-Events und Unit Tests.

Codex darf keine zusätzlichen Marktrisiko-Regeln erfinden und keine aktive Liquidation eigenmächtig erzwingen.
