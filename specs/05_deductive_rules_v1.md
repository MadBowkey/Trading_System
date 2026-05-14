# Deductive Rules v1

Status: DRAFT
Version: v1.0
Architecture: v1.6.1
Last updated: 2026-05-15
Owner: Trading System Project

## Zweck

Deductive Rules sind ökonomisch-logische Leitplanken.

Sie bestimmen, welches globale Strategie-Regime das LLM wählen darf oder muss.

Sie sind keine Risk Metrics und keine Guardrails.

## Grundprinzip

Das System soll nicht rein datengetrieben handeln.

Datengetriebene Muster dürfen nur innerhalb deduktiver Finanzlogik genutzt werden.

Das LLM darf neue Muster interpretieren, aber nicht gegen feste ökonomische Leitplanken handeln.

## Strategy Regime

Core v1 erlaubt nur:

- BUILDUP
- DEFENSIVE
- CASH_ONLY

Nicht erlaubt:

- OFFENSIVE

Begründung:
OFFENSIVE ist für Core v1 zu aggressiv und zu unpräzise. Kontrollierter Positionsaufbau wird durch BUILDUP abgebildet.

## Risk Multiplier

risk_multiplier_override:

- BUILDUP / DEFENSIVE: 0.1 bis 1.0
- CASH_ONLY: exakt 0.0
- Werte über 1.0 sind verboten

Das LLM darf Risiko normal lassen oder reduzieren, aber nicht über die Core-v1-Baseline erhöhen.

## Deductive Rules

### DED_001 — Early Drawdown De-Risking

Logik:
Wenn intraday_drawdown_today_pct >= 2.5
oder max_drawdown_trailing_30d_pct >= 4.5,
dann darf strategy_regime nur DEFENSIVE oder CASH_ONLY sein.

Auswirkung:
- INCREASE ist nicht erlaubt.
- ADD_ON ist nicht erlaubt.
- Risikoerhöhung wird vor der harten Drawdown-Guardrail reduziert.

Ziel:
Proaktives De-Risking vor harter Python-Guardrail.

### DED_002 — Market Stress Defensive Mode

Logik:
Wenn systemic_volatility_z_score >= 2.0
oder expected_shortfall_99_1d_pct >= 4.0,
dann darf strategy_regime nur DEFENSIVE oder CASH_ONLY sein.

Auswirkung:
- BUILDUP ist nicht erlaubt.
- Neue offensive Risikoerhöhung ist nicht erlaubt.

Ziel:
Vermeidung aggressiver Marktphasen bei hohem systemischem Stress oder Tail-Risk.

### DED_003 — Bullish Trend With High Regime Shift Risk Blocks Increase

Logik:
Wenn ein Asset trend_status = BULLISH hat,
aber regime_shift_probability >= 40,
dann darf action nicht INCREASE sein.

Erlaubt:
- HOLD
- DECREASE

Nicht erlaubt:
- INCREASE

Ziel:
Verhindert Top-Buying in möglicherweise erschöpften Trends.

### DED_004 — High Correlation Pair No Double Increase

Logik:
Wenn peak_asset_correlation_20d >= 0.75
und beide Assets aus peak_correlation_pair INCREASE wollen,
darf nicht gleichzeitig bei beiden Assets Risiko erhöht werden.

Auswirkung:
Nur ein Asset darf erhöht werden.

Deterministischer Tie-Breaker durch Python:

1. höherer confidence_score
2. höhere liquidity_score
3. niedriger volatility_risk_score
4. geringeres aktuelles Portfolio-Gewicht
5. sonst beide HOLD

Ziel:
Verhindert Mehrfachkauf desselben Risikos.

### DED_005 — VaR Rising Proportional De-Risking

Logik:
Wenn var_99_1d_pct > 3.5
und var_99_1d_trend = RISING,
dann muss risk_multiplier_override unter 1.0 sinken.

Richtformel:

risk_multiplier_override =
1.0 - ((var_99_1d_pct - 3.5) / 1.5) * 0.5

Clamp:

- BUILDUP / DEFENSIVE: mindestens 0.1, maximal 1.0
- CASH_ONLY: exakt 0.0

Wichtig:
Das LLM darf diese Formel nicht frei verändern.

Ziel:
Proportionale Risikoreduktion bei steigendem statistischem Verlustrisiko.

### DED_006 — HHI Concentration Malus

Logik:
Wenn herfindahl_hirschman_index >= 0.25
und strategy_regime nicht CASH_ONLY ist,
dann darf risk_multiplier_override höchstens 0.80 sein.

Auswirkung:
Konzentrationsrisiko begrenzt die globale Risikofreigabe.

Ziel:
Automatische Zurückhaltung bei Klumpenrisiko.

## Verhältnis zu Risk Metrics

Risk Metrics liefern die Eingangswerte für deduktive Regeln.

Beispiele:
- Drawdown
- VaR
- Expected Shortfall
- HHI
- Korrelation
- regime_shift_probability

Risk Metrics selbst lösen keine Marktaktion aus.

## Verhältnis zu Guardrails

Deductive Rules steuern proaktiv vor harten Guardrails.

Guardrails erzwingen binär.

Beispiel:
DED_001 kann bereits bei 2.5 Prozent Drawdown DEFENSIVE erzwingen.
Die harte Python-Guardrail greift erst bei 3.0 Prozent Intraday Drawdown.

## Nicht erlaubt

- Das LLM darf Deductive Rules nicht ändern.
- Das LLM darf Deductive Rules nicht relativieren.
- Das LLM darf keine Strategie wählen, die deduktiven Regeln widerspricht.
- Datengetriebene Muster dürfen deduktive Regeln nicht überschreiben.
- Deductive Rules dürfen keine technischen Fehler als Marktrisiko interpretieren.

## Codex-Hinweis

Codex darf diese Regeln später als Konfiguration und Validator-Logik implementieren.

Warum:
Die Regeln sind deterministisch, klar benannt und testbar.

Wie:
Codex implementiert später deductive_rules.yaml, Rule Evaluation, Unit Tests und Audit-Events exakt nach dieser Spezifikation.

Codex darf keine deduktiven Regeln ändern, ergänzen oder abschwächen.
