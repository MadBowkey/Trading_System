# Risk Metrics v1

Status: DRAFT
Version: v1.0
Architecture: v1.6.1
Last updated: 2026-05-15
Owner: Trading System Project

## Zweck

Risk Metrics beschreiben den aktuellen Risikozustand des Portfolios und des Marktes.

Sie sind kontinuierliche Warnsignale für den LLM Meta-Manager.

Risk Metrics sind keine harten Sperren. Harte Sperren werden durch Python Guardrails erzwungen.

## Grundprinzip

Risk Metrics zeigen, wie nah das System an kritischen Risikozonen ist.

Das LLM nutzt diese Werte, um defensiver zu werden, bevor harte Guardrails greifen.

Beispiel:

VaR steigt, ist aber noch unter dem harten Limit.
Das LLM soll Risiko reduzieren.
Python blockiert erst, wenn die harte Guardrail verletzt ist.

## Portfolio Risk Metrics

### intraday_drawdown_today_pct

Aktueller prozentualer Verlust des Portfolios vom Höchststand des heutigen Handelstages.

Wertebereich:
0.0 bis 100.0

Nur hart nutzbar, wenn intraday_drawdown_available = true.

### intraday_drawdown_available

Boolean.

Gibt an, ob ein verlässlicher Intraday-Portfolio-Equity-Verlauf vorhanden ist.

### max_drawdown_trailing_30d_pct

Maximaler kumulierter Verlust der letzten 30 Tage.

Wertebereich:
0.0 bis 100.0

### var_99_1d_pct

Value-at-Risk auf 1-Tages-Haltedauer bei 99 Prozent Konfidenz.

Wertebereich:
0.0 bis 100.0

### var_99_1d_trend

Trend des VaR.

Erlaubte Werte:

- RISING
- FALLING
- STABLE

### var_99_1d_change_5d_pct_points

Veränderung des VaR über 5 Handelstage in Prozentpunkten.

### expected_shortfall_99_1d_pct

Expected Shortfall / Conditional VaR bei 99 Prozent Konfidenz und 1-Tages-Haltedauer.

Zeigt den erwarteten Verlust im Tail-Risk-Fall.

### var_method

Methode der VaR-Berechnung.

Core v1:
parametric_normal

### var_lookback_days

Lookback-Fenster für die VaR-Berechnung.

Core v1:
160 Handelstage

### portfolio_heat_pct

Summe des offenen Risikos bis zu den Stops geteilt durch Portfolio Value.

### open_risk_to_stop_pct

Rohwert des offenen Risikos aller Positionen bis zu ihren Stop-Referenzen.

### risk_budget_utilization_pct

Auslastung des erlaubten Risikobudgets.

Wertebereich:
0.0 bis 100.0

## Leverage and Liquidity Metrics

### margin_utilization_pct

Tatsächlich gebundene Broker-Margin relativ zum Portfolio Value.

Falls nicht zuverlässig verfügbar:
margin_utilization_available = false

### margin_utilization_available

Boolean.

Gibt an, ob margin_utilization_pct belastbar verfügbar ist.

### effective_leverage_ratio

Nominales Gesamtexposure geteilt durch Portfolio Value.

Beispiele:

0.70 = 70 Prozent investiert
1.00 = voll investiert
1.50 = 1,5-fach gehebelt

Core v1 erlaubt maximal 1.0.

### cash_buffer_liquidity_pct

Sofort verfügbare, nicht gebundene Liquidität relativ zum Portfolio Value.

## Concentration and Correlation Metrics

### peak_asset_correlation_20d

Höchste 20-Tage-Korrelation zwischen zwei aktuell relevanten Assets.

Wertebereich:
-1.0 bis +1.0

### peak_correlation_pair

Objekt mit den beiden Assets, die peak_asset_correlation_20d verursachen.

Felder:

- asset_1
- asset_2
- correlation

### max_single_asset_exposure_pct

Größter Einzelpositionsanteil am Portfolio.

Wertebereich:
0.0 bis 100.0

### herfindahl_hirschman_index

HHI-Konzentrationswert des Portfolios.

Wertebereich:
0.0 bis 1.0

Interpretation:

- nahe 0.20: breit verteilt bei 5 gleichgewichteten Positionen
- ab 0.25: Konzentrationswarnung
- ab 0.30: keine weitere Verschlechterung
- ab 0.40: harte Konzentrationszone

## Market Stress Metrics

### systemic_volatility_z_score

Abweichung der aktuellen systemischen Marktvolatilität vom historischen Mittel.

Interpretation:

- 0.0 = normal
- 1.0 = erhöht
- 2.0 = Stress
- 3.0 = Extremstress

### implied_volatility_skew

Optionales Feld.

Misst die Schiefe der Optionsvolatilitäten, falls belastbare Optionsdaten verfügbar sind.

Core v1:
optional, nicht blockierend.

### implied_volatility_skew_available

Boolean.

Gibt an, ob implied_volatility_skew verfügbar und belastbar ist.

## Beispielstruktur

{
  "risk_state_metrics": {
    "portfolio_risk": {
      "intraday_drawdown_today_pct": 1.8,
      "intraday_drawdown_available": true,
      "max_drawdown_trailing_30d_pct": 4.2,
      "var_99_1d_pct": 3.1,
      "var_99_1d_trend": "STABLE",
      "var_99_1d_change_5d_pct_points": 0.2,
      "expected_shortfall_99_1d_pct": 4.0,
      "var_method": "parametric_normal",
      "var_lookback_days": 160,
      "portfolio_heat_pct": 1.4,
      "open_risk_to_stop_pct": 1.4,
      "risk_budget_utilization_pct": 56.0
    },
    "leverage_and_liquidity": {
      "margin_utilization_pct": 12.0,
      "margin_utilization_available": true,
      "effective_leverage_ratio": 0.70,
      "cash_buffer_liquidity_pct": 30.0
    },
    "concentration_and_correlation": {
      "peak_asset_correlation_20d": 0.78,
      "peak_correlation_pair": {
        "asset_1": "QQQ",
        "asset_2": "SMH",
        "correlation": 0.78
      },
      "max_single_asset_exposure_pct": 16.875,
      "herfindahl_hirschman_index": 0.24
    },
    "market_stress": {
      "systemic_volatility_z_score": 1.4,
      "implied_volatility_skew": null,
      "implied_volatility_skew_available": false
    }
  }
}

## Nicht erlaubt

Risk Metrics dürfen nicht direkt Marktaktionen auslösen.

Risk Metrics dürfen nicht mit Guardrails verwechselt werden.

Ein hoher Risk-Metric-Wert ist zunächst ein Warnsignal.
Erst Python Guardrails entscheiden binär über Blockaden oder FORCE_CASH_ONLY.

## Codex-Hinweis

Codex darf diese Metriken später implementieren.

Warum:
Die Berechnungen sind numerisch, regelbasiert und testbar.

Wie:
Codex implementiert später Risk-Metric-Funktionen, Tests mit bekannten Beispielwerten und Parquet-Ausgabe.

Codex darf keine zusätzlichen Risk Metrics oder Schwellenwerte eigenständig ergänzen.
