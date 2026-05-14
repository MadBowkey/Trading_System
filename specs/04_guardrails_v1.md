# Guardrails v1

Status: DRAFT
Version: v1.0
Architecture: v1.6.1
Last updated: 2026-05-15
Owner: Trading System Project

## Zweck

Guardrails sind harte, binäre Python-Sperren.

Sie definieren, was unabhängig von LLM-Interpretation, Signalqualität oder Strategieabsicht verboten ist.

Das LLM darf Guardrails nicht interpretieren, relativieren oder überschreiben.

## Grundprinzip

Risk Metrics sind Warnsignale.

Guardrails sind harte Python-Entscheidungen.

Wenn eine Guardrail verletzt wird, entscheidet Python deterministisch über Blockade, Risikoreduktion, FORCE_CASH_ONLY oder SAFE_HOLD.

## Trennung SAFE_HOLD und CASH_ONLY

Technische Fehler führen zu SAFE_HOLD / NO_NEW_ACTIONS.

Echte Markt- oder Risikoverletzungen führen zu FORCE_CASH_ONLY, BLOCK_RISK_INCREASE oder kontrollierter Risikoreduktion.

Technische Fehler dürfen niemals CASH_ONLY auslösen.

## Data Validity Guardrails

### realtime_stale_timeout_seconds

Wert:
60 Sekunden

Gilt nur für Echtzeit-/Intraday-Modus.

### daily_eod_policy

Wert:
must_match_expected_trading_date

Für Tagesanalyse müssen die Daten zum erwarteten Handelstag passen.

### on_invalid_data

Reaktion:
BLOCK_ANALYSIS_AND_NEW_ACTIONS

Systemstatus:
SAFE_HOLD / NO_NEW_ACTIONS

Wichtig:
Ungültige Daten lösen keine Marktaktion aus.

## Portfolio Loss Limits

### max_intraday_drawdown_limit_pct

Wert:
3.0

Voraussetzung:
intraday_drawdown_available = true

Reaktion:
FORCE_CASH_ONLY

Bedeutung:
Ein echter Intraday-Drawdown-Breach ist ein Markt-/Risikoereignis und darf kontrollierten Risikoabbau auslösen.

## VaR Limits

### max_post_trade_var_99_1d_pct

Wert:
5.0

Reaktion:
BLOCK_RISK_INCREASE

Bedeutung:
Wenn der simulierte Post-Trade-VaR über 5.0 Prozent liegt, darf kein neues Risiko hinzugefügt werden.

## Leverage and Liquidity Limits

### max_effective_leverage_ratio_core

Wert:
1.0

Bedeutung:
Core v1 erlaubt keinen Hebel über die normale Baseline.

### min_cash_buffer_liquidity_pct

Wert:
20.0

Reaktion:
BLOCK_OR_DOWNSIZE_TRADE

Bedeutung:
Trades, die den Cash Buffer unter 20 Prozent drücken würden, werden blockiert oder verkleinert.

## Position and Concentration Limits

### max_single_asset_exposure_pct

Wert:
25.0

Bedeutung:
Kein einzelnes Asset darf nach Zielportfolio-Berechnung mehr als 25 Prozent des Portfolios ausmachen.

### hhi_soft_threshold

Wert:
0.25

Bedeutung:
Konzentrationswarnung. Kann den risk_multiplier_override begrenzen.

### hhi_no_worsening_threshold

Wert:
0.30

Bedeutung:
Ab diesem Wert dürfen Vorschläge die Konzentration nicht weiter verschlechtern.

### hhi_hard_threshold

Wert:
0.40

Bedeutung:
Harte Konzentrationszone. Neue Konzentration wird blockiert.

## Correlation Limits

### correlation_warning_threshold_20d

Wert:
0.75

Bedeutung:
Warnschwelle für hohe Korrelation.

### correlation_hard_threshold_20d

Wert:
0.80

Reaktion:
ALLOW_HIGHER_CONFIDENCE_ONLY

Bedeutung:
Wenn zwei hoch korrelierte Assets gleichzeitig INCREASE erhalten, darf nur das nach deterministischem Tie-Breaker stärkere Asset erhöht werden.

Tie-Breaker:

1. höherer confidence_score
2. höhere liquidity_score
3. niedriger volatility_risk_score
4. geringeres aktuelles Portfolio-Gewicht
5. sonst beide HOLD

## LLM Output Validation Limits

### min_asset_confidence_score

Wert:
0.60

Bedeutung:
Asset-Vorschläge mit niedriger Konfidenz dürfen kein neues Risiko erzeugen.

### min_global_decision_confidence

Wert:
0.65

Bedeutung:
Bei zu niedriger globaler LLM-Konfidenz darf kein neues Risiko erzeugt werden.

## Korrigierte Guardrail-Struktur

{
  "risk_policy_guardrails": {
    "policy_version": "risk_guardrails.v1",
    "data_validity": {
      "realtime_stale_timeout_seconds": 60,
      "daily_eod_policy": "must_match_expected_trading_date",
      "on_invalid_data": "BLOCK_ANALYSIS_AND_NEW_ACTIONS"
    },
    "portfolio_loss_limits": {
      "max_intraday_drawdown_limit_pct": 3.0,
      "requires_intraday_drawdown_available": true,
      "on_breach": "FORCE_CASH_ONLY"
    },
    "var_limits": {
      "max_post_trade_var_99_1d_pct": 5.0,
      "on_breach": "BLOCK_RISK_INCREASE"
    },
    "leverage_and_liquidity": {
      "max_effective_leverage_ratio_core": 1.0,
      "min_cash_buffer_liquidity_pct": 20.0,
      "on_cash_breach": "BLOCK_OR_DOWNSIZE_TRADE"
    },
    "position_and_concentration": {
      "max_single_asset_exposure_pct": 25.0,
      "hhi_soft_threshold": 0.25,
      "hhi_no_worsening_threshold": 0.30,
      "hhi_hard_threshold": 0.40
    },
    "correlation": {
      "correlation_warning_threshold_20d": 0.75,
      "correlation_hard_threshold_20d": 0.80,
      "on_pairwise_increase_conflict": "ALLOW_HIGHER_CONFIDENCE_ONLY"
    },
    "llm_output_validation": {
      "min_asset_confidence_score": 0.60,
      "min_global_decision_confidence": 0.65,
      "on_low_confidence": "IGNORE_OR_BLOCK_NEW_RISK"
    }
  }
}

## Nicht erlaubt

- Das LLM darf Guardrails nicht ändern.
- Das LLM darf Guardrails nicht überschreiben.
- Guardrail-Verletzungen dürfen nicht im Prompt weich interpretiert werden.
- Data Invalid darf niemals CASH_ONLY auslösen.
- SAFE_HOLD und CASH_ONLY dürfen nicht vermischt werden.
- Kein Hebel über 1.0 in Core v1.
- Keine automatische Liquidation durch technische Fehler.

## Codex-Hinweis

Codex darf diese Guardrails später als Konfigurationsdatei und Validator-Logik implementieren.

Warum:
Die Guardrails sind harte, regelbasierte Python-Prüfungen und gut testbar.

Wie:
Codex implementiert später risk_guardrails.yaml, GuardrailValidator, Testfälle und Audit-Events exakt nach dieser Spezifikation.

Codex darf keine Grenzwerte ändern und keine zusätzlichen Guardrails erfinden.
