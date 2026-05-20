# Station 5 — Market Risk Validator

Status: DRAFT
Version: v1.0
Architecture: v1.6.1
Last updated: 2026-05-20
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


### VAL_MRV_005 — Asset Confidence Threshold

Prüfung:
Ein Asset hat confidence_score < 0.60 und action = INCREASE.

Reaktion:
DOWNGRADED.

Systemstatus:
NORMAL_CONTINUE.

Pipeline:
CONTINUE.

Aktion:
INCREASE wird zu HOLD.

Begründung:
Ein Asset mit zu niedriger LLM-Konfidenz darf kein neues Risiko erzeugen. Diese Regel gilt nur auf Asset-Ebene, da globale LLM-Confidence aktuell nicht Teil des Output-Schemas ist.

### VAL_MRV_006 — Regime Shift Risk Blocks Increase

Prüfung:
Ein Asset hat trend_status = BULLISH, regime_shift_probability >= 40.0 und action = INCREASE.

Reaktion:
DOWNGRADED.

Systemstatus:
NORMAL_CONTINUE.

Pipeline:
CONTINUE.

Aktion:
INCREASE wird zu HOLD.

Begründung:
Diese Regel widerspricht nicht dem bullischen Signal, sondern begrenzt es. Halten bleibt erlaubt, aber weiterer Risikoaufbau ist untersagt.

### VAL_MRV_007 — Correlated Pair No Double Increase

Prüfung:
peak_asset_correlation_20d >= 0.80 und beide Assets aus peak_correlation_pair haben action = INCREASE.

Reaktion:
DOWNGRADED.

Systemstatus:
NORMAL_CONTINUE.

Pipeline:
CONTINUE.

Aktion:
Nur das nach deterministischem Tie-Breaker stärkere Asset darf INCREASE behalten. Das unterlegene Asset wird auf HOLD gesetzt. Wenn kein eindeutiger Gewinner bestimmbar ist, werden beide Assets auf HOLD gesetzt.

Tie-Breaker:

1. höherer confidence_score
2. höhere liquidity_score
3. niedrigerer volatility_risk_score
4. geringeres aktuelles Portfolio-Gewicht
5. vollständiger Gleichstand oder fehlende Tie-Breaker-Daten: beide HOLD

Begründung:
Die Reihenfolge im LLM-Output darf niemals entscheiden. Die Auflösung erfolgt deterministisch und risikominimierend.

## Audit-Log-Beispiele

### Universe-Verletzung ohne Bestand

2026-05-14 23:42:00 | run_118_mrv | MarketRiskValidator | VAL_MRV_004A | DOWNGRADED | NORMAL_CONTINUE | Asset 'XYZ' is outside the active universe and has no current holdings | Removed 'XYZ' from target_allocation_adjustments.

### Universe-Verletzung mit Altbestand und INCREASE-Block

2026-05-14 23:42:15 | run_119_mrv | MarketRiskValidator | VAL_MRV_004B | DOWNGRADED | NORMAL_CONTINUE | Asset 'QQQ' is outside the active universe but position exists. Requested action: INCREASE | Action forced to HOLD to prevent unauthorized buying.

### Universe-Verletzung mit Altbestand und LIQUIDATE

2026-05-14 23:42:30 | run_120_mrv | MarketRiskValidator | VAL_MRV_004C | PASS_WITH_CONSTRAINTS | NORMAL_CONTINUE | Asset 'QQQ' is outside the active universe but position exists. Requested action: LIQUIDATE | Passed to Portfolio Engine as inventory management action.


### Zu geringe Asset Confidence

2026-05-15 01:21:00 | run_123_mrv | MarketRiskValidator | VAL_MRV_005 | DOWNGRADED | NORMAL_CONTINUE | CONTINUE | Asset 'QQQ' requested INCREASE with confidence_score 0.45 (< 0.60) | original_action=INCREASE | enforced_action=HOLD | Reason: Asset confidence below minimum threshold. New risk blocked.

### Hohe Trendbruchwahrscheinlichkeit

2026-05-15 01:24:00 | run_124_mrv | MarketRiskValidator | VAL_MRV_006 | DOWNGRADED | NORMAL_CONTINUE | CONTINUE | Asset 'SMH' is BULLISH but regime_shift_probability is 42% (>= 40%) | original_action=INCREASE | enforced_action=HOLD | Reason: High regime-shift risk blocks additional risk.

### Korrelations-Konflikt

2026-05-15 01:18:00 | run_125_mrv | MarketRiskValidator | VAL_MRV_007 | DOWNGRADED | NORMAL_CONTINUE | CONTINUE | High correlation 0.85 between QQQ and SMH. Both requested INCREASE. Tie-breaker: QQQ confidence_score 0.80 > SMH confidence_score 0.70 | winner=QQQ | downgraded_asset=SMH | original_action=INCREASE | enforced_action=HOLD | Reason: Correlated pair cannot both increase.

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
- HHI / Konzentration
- Risk Metrics nahe Guardrail

## Aktueller Status

Diese Station ist begonnen.

Fachlich beschlossen und implementierungsfähig sind:

- VAL_MRV_004A
- VAL_MRV_004B
- VAL_MRV_004C
- VAL_MRV_005
- VAL_MRV_006
- VAL_MRV_007

Weitere MRV-Erweiterungen bleiben offen und sind nicht implementierungsfähig, bis sie separat spezifiziert, geprüft und in Rule Registry sowie Golden Cases abgebildet sind.

## Codex-Hinweis

Codex darf die fachlich beschlossenen Regeln VAL_MRV_004A bis VAL_MRV_007 später implementieren.

Warum:
Die Regeln sind deterministisch, gut testbar und sicherheitskritisch.

Wie:
Codex implementiert später den MarketRiskValidator, Universe-/Altbestandslogik, Downgrade-Logik, Audit-Events und Unit Tests.

Codex darf keine zusätzlichen Marktrisiko-Regeln erfinden und keine aktive Liquidation eigenmächtig erzwingen.


