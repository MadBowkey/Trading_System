# Station 8 — Order Validator

Status: FINAL
Version: v1.0
Architecture: v1.6.1
Last updated: 2026-05-16
Owner: Trading System Project

## Kurzbeschreibung

Station 8 ist die letzte Prüfinstanz vor der Execution Simulation.

Sie validiert eine bereits erzeugte proposed_order_list gegen technische Order-Integrität, Liquidität, Broker-Regeln, Kosten-/Slippage-Grenzen und Konformität mit dem von Station 7 freigegebenen Zielportfolio.

Station 8 erzeugt keine Orders selbst.

Station 8 verändert keine Strategie.

Station 8 löst kein FORCE_CASH_ONLY aus.

Station 8 erlaubt nur harmlose technische Normalisierung.

Alles Nicht-Harmlose führt zur Ablehnung der gesamten Orderliste.
## Input

Aus Station 7:

- freigegebenes Zielportfolio
- target_weights
- delta_weights
- position_change_plan

Aus Order Proposal Engine:

- proposed_order_list

Markt- und Brokerdaten:

- aktuelle Marktpreise
- Bid / Ask
- Spread
- Liquidity Scores
- Broker-spezifische Constraints
- minimum order size
- tick size
- lot size increment
- order type constraints
- market status

Execution-Simulation-Vorwerte:

- geschätzte Slippage
- geschätzte Gebühren
- geschätzte Gesamtkosten

## Output

Validierte Orderliste oder Ablehnung der gesamten Orderliste.

Felder:

- order_proposal_status: APPROVED / REJECTED
- validated_order_list
- rejected_order_details
- num_orders_proposed
- num_orders_rejected
- audit_event

## Statuslogik

### APPROVED

Validator-Status:

APPROVED

Systemstatus:

NORMAL_CONTINUE

Pipeline:

CONTINUE

### DOWNGRADED durch harmlose technische Normalisierung

Validator-Status:

DOWNGRADED

Systemstatus:

NORMAL_CONTINUE

Pipeline:

CONTINUE

Order Proposal Status:

APPROVED

### REJECTED durch Ausführbarkeits-, Liquiditäts-, Broker- oder Kostenverletzung

Validator-Status:

REJECTED

Systemstatus:

NO_NEW_ACTIONS

Pipeline:

STOP_BEFORE_EXECUTION_SIMULATION

Order Proposal Status:

REJECTED

### BLOCKED / TECHNICAL_ERROR durch invalide Orderdaten

Validator-Status:

BLOCKED / TECHNICAL_ERROR

Systemstatus:

SAFE_HOLD / NO_NEW_ACTIONS

Pipeline:

STOP

Order Proposal Status:

REJECTED

## Wichtig

Station 8 arbeitet order-list-binär.

Es gibt in Core-v1 keine Teilfreigabe einzelner Orders.

Wenn eine Order kritisch abgelehnt wird, wird die gesamte proposed_order_list abgelehnt.

Station 8 darf nicht:

- Orders erzeugen
- Strategie verändern
- Richtung ändern
- BUY in SELL ändern
- SELL in BUY ändern
- Assets ersetzen
- Assets hinzufügen
- Ordergröße erhöhen
- Mindestlot künstlich erreichen
- LIMIT in MARKET umwandeln
- MARKET in LIMIT umwandeln
- Limitpreise strategisch verschieben
- Liquidationen erzwingen
- FORCE_CASH_ONLY auslösen

## Wichtig

Station 8 arbeitet order-list-binär.

Es gibt in Core-v1 keine Teilfreigabe einzelner Orders.

Wenn eine Order kritisch abgelehnt wird, wird die gesamte proposed_order_list abgelehnt.

Station 8 darf nicht:

- Orders erzeugen
- Strategie verändern
- Richtung ändern
- BUY in SELL ändern
- SELL in BUY ändern
- Assets ersetzen
- Assets hinzufügen
- Ordergröße erhöhen
- Mindestlot künstlich erreichen
- LIMIT in MARKET umwandeln
- MARKET in LIMIT umwandeln
- Limitpreise strategisch verschieben
- Liquidationen erzwingen
- FORCE_CASH_ONLY auslösen

## Regeln

### VAL_ORD_001 — Technische Order-Integrität

Prüfung:

Ist die proposed_order_list technisch vollständig, typkonform und eindeutig?

Pflichtfelder:

- symbol
- asset_id
- side
- quantity
- order_type
- limit_price bei LIMIT
- reference_to_station_7_target
- reference_to_position_change_plan

Fehlerfall:

Pflichtfelder fehlen, Datentypen sind falsch, side ist ungültig, quantity ist ungültig oder die Orderliste ist malformed.

Validator-Status:

BLOCKED / TECHNICAL_ERROR

Systemstatus:

SAFE_HOLD / NO_NEW_ACTIONS

Pipeline:

STOP

Order Proposal Status:

REJECTED

### VAL_ORD_002 — Liquiditäts-Check

Prüfung:

Ist jede Order im Verhältnis zu Liquidität, ADV und Marktstatus ausführbar?

Beispiel:

Order Size > 5 Prozent ADV.

Fehlerfall:

Liquiditätsgrenze verletzt.

Validator-Status:

REJECTED

Systemstatus:

NO_NEW_ACTIONS

Pipeline:

STOP_BEFORE_EXECUTION_SIMULATION

Order Proposal Status:

REJECTED

### VAL_ORD_003 — Broker-/Tick-Size-/Lot-Normalisierung

Prüfung:

Kann eine Order durch harmlose technische Normalisierung brokerkonform gemacht werden?

DOWNGRADED ist nur bei folgenden harmlosen technischen Anpassungen erlaubt:

- Tick-Size-Rundung
- BUY-Limit: nur abrunden
- SELL-Limit: nur aufrunden
- maximale Abweichung: < 1 Tick
- Lot-Size-Rundung: Quantity nur abrunden
- niemals aufstocken
- rechnerische Null-Orders nur entfernen, wenn sie planneutral sind

Nicht erlaubt:

- Ordergröße erhöhen
- Erhöhung zur Erreichung eines Mindestlots
- BUY / SELL ändern
- LIMIT / MARKET ändern
- strategische Preisverschiebung
- Asset ersetzen
- Asset hinzufügen
- Teilfreigabe

Nicht normalisierbare Orders führen zur Ablehnung der gesamten Orderliste.

DOWNGRADED:

Systemstatus:

NORMAL_CONTINUE

Pipeline:

CONTINUE

Order Proposal Status:

APPROVED

REJECTED:

Systemstatus:

NO_NEW_ACTIONS

Pipeline:

STOP_BEFORE_EXECUTION_SIMULATION

Order Proposal Status:

REJECTED

### VAL_ORD_004 — Kosten / Slippage

Prüfung:

Überschreiten geschätzte Slippage, Spread-Kosten oder Gebühren die konfigurierte Schwelle?

Fehlerfall:

Kosten-/Slippage-Schwelle verletzt.

Validator-Status:

REJECTED

Systemstatus:

NO_NEW_ACTIONS

Pipeline:

STOP_BEFORE_EXECUTION_SIMULATION

Order Proposal Status:

REJECTED

### VAL_ORD_005 — Normalisierte Orderliste verletzt Zielplan / Post-Trade-Konformität

Prüfung:

Ist die final normalisierte Orderliste noch mit dem von Station 7 freigegebenen Zielportfolio und dem Station-6-Delta-Plan vereinbar?

Fehlerfall:

Die normalisierte Orderliste würde den freigegebenen Zielplan, die genehmigten Deltas oder eine bereits geprüfte Post-Trade-Grenze verletzen.

Validator-Status:

REJECTED

Systemstatus:

NO_NEW_ACTIONS

Pipeline:

STOP_BEFORE_EXECUTION_SIMULATION

Order Proposal Status:

REJECTED

## Finale Audit-Regeln Station 8

1. Standardfelder aus allgemeiner Audit-Struktur übernehmen.
2. Ein Summary-Event pro Run, keine Einzel-Order-Events.
3. rejected_order_details enthält betroffene Orders als JSON-Array.
4. Bei DOWNGRADED immer original_value + enforced_value.
5. REJECTED -> system_status: NO_NEW_ACTIONS + pipeline_action: STOP_BEFORE_EXECUTION_SIMULATION.
6. BLOCKED / TECHNICAL_ERROR -> SAFE_HOLD + STOP.
7. Kein FORCE_CASH_ONLY in Station 8.
8. Keine Teilfreigabe: gesamte Orderliste ist binär APPROVED oder REJECTED.

## Decimal Context Handling

Station 8 nutzt Decimal für preis- und mengenrelevante Normalisierung.

setup_decimal_context() muss beim Start jedes relevanten OrderValidator-Ausführungskontexts aufgerufen werden.

Der Decimal Context darf nicht implizit aus dem Main-Thread vorausgesetzt werden.

Für Core-v1 gilt:

- synchroner Main-Thread: setup_decimal_context() beim Start von Station 8
- threading.Thread: setup_decimal_context() im Thread
- loop.run_in_executor(): setup_decimal_context() im Worker
- asyncio.to_thread(): setup_decimal_context() in der Target-Funktion
- multiprocessing.Process: setup_decimal_context() im Prozess
- reine asyncio Tasks im selben Event-Loop: kein zusätzlicher Pflichtaufruf pro Task, aber OrderValidator initialisiert seinen Context explizit beim Start

NaN / Inf werden zusätzlich über to_decimal().is_finite() abgelehnt.

InvalidOperation wird importiert und im Context als Trap gesetzt.

## Decimal Utility und Normalisierungslogik

```python
from decimal import (
    Decimal,
    ROUND_DOWN,
    ROUND_UP,
    InvalidOperation,
    getcontext
)
from typing import Any, Dict


def setup_decimal_context() -> None:
    """
    Configure Decimal arithmetic for Station 8.

    Must be called during OrderValidator initialization
    in each relevant worker/thread/process context.
    """
    ctx = getcontext()
    ctx.prec = 28
    ctx.rounding = ROUND_DOWN
    ctx.traps[InvalidOperation] = True
    ctx.Emax = 999999
    ctx.Emin = -999999


def to_decimal(value) -> Decimal:
    """Safe conversion plus finite check."""
    try:
        dec = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("Invalid numeric input")

    if not dec.is_finite():
        raise ValueError("Numeric input is not finite")

    return dec


def normalize_tick_price(
    price: float | Decimal | str,
    tick_size: float | Decimal | str,
    side: str,
    order_type: str = "LIMIT"
) -> Dict[str, Any]:
    """Conservative side-aware tick-size normalization."""
    try:
        price_dec = to_decimal(price)
        tick_dec = to_decimal(tick_size)
    except ValueError as exc:
        return {
            "success": False,
            "enforced_price": None,
            "reason": str(exc),
            "normalization_type": "TICK_SIZE_ROUNDING"
        }

    if order_type.upper() != "LIMIT" or price_dec <= 0 or tick_dec <= 0:
        return {
            "success": False,
            "enforced_price": None,
            "reason": "Invalid input for tick normalization",
            "normalization_type": "TICK_SIZE_ROUNDING"
        }

    side_upper = side.upper()
    tick_units = price_dec / tick_dec

    if side_upper == "BUY":
        enforced_ticks = tick_units.to_integral_value(rounding=ROUND_DOWN)
    elif side_upper == "SELL":
        enforced_ticks = tick_units.to_integral_value(rounding=ROUND_UP)
    else:
        return {
            "success": False,
            "enforced_price": None,
            "reason": "Invalid side",
            "normalization_type": "TICK_SIZE_ROUNDING"
        }

    enforced = enforced_ticks * tick_dec

    if enforced <= 0:
        return {
            "success": False,
            "enforced_price": None,
            "reason": f"Enforced price {str(enforced)} <= 0",
            "original": str(price_dec),
            "normalization_type": "TICK_SIZE_ROUNDING"
        }

    deviation_ticks = abs(enforced - price_dec) / tick_dec

    if deviation_ticks >= Decimal("1"):
        return {
            "success": False,
            "enforced_price": None,
            "reason": f"Deviation {str(deviation_ticks)} ticks >= 1 tick limit",
            "original": str(price_dec),
            "normalization_type": "TICK_SIZE_ROUNDING"
        }

    return {
        "success": True,
        "enforced_price": str(enforced),
        "deviation_ticks": str(deviation_ticks),
        "original": str(price_dec),
        "side": side_upper,
        "order_type": order_type.upper(),
        "tick_size": str(tick_dec),
        "normalization_type": "TICK_SIZE_ROUNDING"
    }


def normalize_quantity(
    quantity: float | Decimal | str,
    lot_size_increment: int | Decimal | str
) -> Dict[str, Any]:
    """Conservative lot-size normalization."""
    try:
        quantity_dec = to_decimal(quantity)
        lot_dec = to_decimal(lot_size_increment)
    except ValueError as exc:
        return {
            "success": False,
            "enforced_quantity": None,
            "reason": str(exc),
            "normalization_type": "LOT_SIZE_CHECK"
        }

    if quantity_dec <= 0 or lot_dec <= 0:
        return {
            "success": False,
            "enforced_quantity": None,
            "reason": "Invalid input",
            "normalization_type": "LOT_SIZE_CHECK"
        }

    if quantity_dec < lot_dec:
        return {
            "success": False,
            "enforced_quantity": None,
            "reason": f"Quantity {str(quantity_dec)} below lot_size_increment {str(lot_dec)}. Upward adjustment forbidden.",
            "lot_size_increment": str(lot_dec),
            "original": str(quantity_dec),
            "normalization_type": "LOT_SIZE_CHECK"
        }

    lot_units = quantity_dec / lot_dec
    enforced_lots = lot_units.to_integral_value(rounding=ROUND_DOWN)
    enforced = enforced_lots * lot_dec

    if enforced == quantity_dec:
        return {
            "success": True,
            "enforced_quantity": str(enforced),
            "quantity_changed": False,
            "original": str(quantity_dec),
            "lot_size_increment": str(lot_dec),
            "normalization_type": "LOT_SIZE_ROUNDING"
        }

    if enforced < quantity_dec:
        return {
            "success": True,
            "enforced_quantity": str(enforced),
            "quantity_changed": True,
            "deviation": str(quantity_dec - enforced),
            "original": str(quantity_dec),
            "lot_size_increment": str(lot_dec),
            "normalization_type": "LOT_SIZE_ROUNDING"
        }

    return {
        "success": False,
        "enforced_quantity": None,
        "reason": "Unexpected lot normalization state",
        "lot_size_increment": str(lot_dec),
        "original": str(quantity_dec),
        "normalization_type": "LOT_SIZE_CHECK"
    }
```
## Audit-Log-Beispiele

### Erfolgs-Audit — Vollständig valide Orderliste

```json
{
  "run_id": "run_20260516_0145_ord_000",
  "timestamp": "2026-05-16T01:44:50Z",
  "station": "Station_8_OrderValidator",
  "rule_id": null,
  "validator_status": "APPROVED",
  "system_status": "NORMAL_CONTINUE",
  "pipeline_action": "CONTINUE",
  "order_proposal_status": "APPROVED",
  "asset_id": null,
  "reason": "Proposed order list passed all Station 8 checks.",
  "num_orders_proposed": 2,
  "num_orders_rejected": 0,
  "rejected_order_details": [],
  "audit_hash": "<hash>"
}
```

### VAL_ORD_001 — Technische Order-Integrität

```json
{
  "run_id": "run_20260516_0145_ord_001",
  "timestamp": "2026-05-16T01:45:00Z",
  "station": "Station_8_OrderValidator",
  "rule_id": "VAL_ORD_001",
  "validator_status": "BLOCKED",
  "system_status": "SAFE_HOLD",
  "pipeline_action": "STOP",
  "order_proposal_status": "REJECTED",
  "asset_id": "QQQ",
  "reason": "Missing side or quantity in proposed_order_list for QQQ",
  "num_orders_proposed": 1,
  "num_orders_rejected": 1,
  "rejected_order_details": [
    {
      "asset_id": "QQQ",
      "reason": "Missing side or quantity."
    }
  ],
  "audit_hash": "<hash>"
}
```
### VAL_ORD_002 — Liquiditäts-Check

```json
{
  "run_id": "run_20260516_0145_ord_002",
  "timestamp": "2026-05-16T01:45:10Z",
  "station": "Station_8_OrderValidator",
  "rule_id": "VAL_ORD_002",
  "validator_status": "REJECTED",
  "system_status": "NO_NEW_ACTIONS",
  "pipeline_action": "STOP_BEFORE_EXECUTION_SIMULATION",
  "order_proposal_status": "REJECTED",
  "asset_id": "SMH",
  "reason": "Order size 45% of 20d ADV for SMH violates liquidity limit",
  "num_orders_proposed": 1,
  "num_orders_rejected": 1,
  "rejected_order_details": [
    {
      "asset_id": "SMH",
      "reason": "Order size exceeds liquidity limit."
    }
  ],
  "audit_hash": "<hash>"
}
```

### VAL_ORD_003 — Harmlose Tick-Normalisierung

```json
{
  "run_id": "run_20260516_0145_ord_003",
  "timestamp": "2026-05-16T01:45:22Z",
  "station": "Station_8_OrderValidator",
  "rule_id": "VAL_ORD_003",
  "validator_status": "DOWNGRADED",
  "system_status": "NORMAL_CONTINUE",
  "pipeline_action": "CONTINUE",
  "order_proposal_status": "APPROVED",
  "asset_id": "SPY",
  "normalization_type": "TICK_SIZE_ROUNDING",
  "field_name": "limit_price",
  "side": "BUY",
  "order_type": "LIMIT",
  "tick_size": "0.01",
  "reason": "Tick-size rounding applied. BUY limit 123.459 rounded down to 123.45 within harmless normalization tolerance (< 1 tick).",
  "original_value": "123.459",
  "enforced_value": "123.45",
  "num_orders_proposed": 1,
  "num_orders_rejected": 0,
  "rejected_order_details": [],
  "audit_hash": "<hash>"
}
```
### VAL_ORD_003 — Nicht normalisierbare Lot-Verletzung

```json
{
  "run_id": "run_20260516_0145_ord_004",
  "timestamp": "2026-05-16T01:46:10Z",
  "station": "Station_8_OrderValidator",
  "rule_id": "VAL_ORD_003",
  "validator_status": "REJECTED",
  "system_status": "NO_NEW_ACTIONS",
  "pipeline_action": "STOP_BEFORE_EXECUTION_SIMULATION",
  "order_proposal_status": "REJECTED",
  "asset_id": "SMH",
  "normalization_type": "LOT_SIZE_CHECK",
  "field_name": "quantity",
  "side": "BUY",
  "order_type": "LIMIT",
  "reason": "Order requires lot-size increase to meet broker minimum. Upward quantity adjustment is forbidden.",
  "original_value": "47",
  "enforced_value": null,
  "num_orders_proposed": 1,
  "num_orders_rejected": 1,
  "rejected_order_details": [
    {
      "asset_id": "SMH",
      "proposed_quantity": "47",
      "lot_size_increment": "100",
      "reason": "Would require upward adjustment from 47 to 100. Increasing order size is forbidden."
    }
  ],
  "audit_hash": "<hash>"
}
```

### VAL_ORD_004 — Kosten / Slippage

```json
{
  "run_id": "run_20260516_0145_ord_005",
  "timestamp": "2026-05-16T01:46:25Z",
  "station": "Station_8_OrderValidator",
  "rule_id": "VAL_ORD_004",
  "validator_status": "REJECTED",
  "system_status": "NO_NEW_ACTIONS",
  "pipeline_action": "STOP_BEFORE_EXECUTION_SIMULATION",
  "order_proposal_status": "REJECTED",
  "asset_id": null,
  "reason": "Projected slippage plus commission 0.28% exceeds configured threshold",
  "num_orders_proposed": 2,
  "num_orders_rejected": 2,
  "rejected_order_details": [
    {
      "asset_id": "SPY",
      "reason": "Projected cost threshold exceeded."
    },
    {
      "asset_id": "QQQ",
      "reason": "Projected cost threshold exceeded."
    }
  ],
  "audit_hash": "<hash>"
}
```
### VAL_ORD_005 — Normalisierte Orderliste verletzt Zielplan

```json
{
  "run_id": "run_20260516_0145_ord_006",
  "timestamp": "2026-05-16T01:46:40Z",
  "station": "Station_8_OrderValidator",
  "rule_id": "VAL_ORD_005",
  "validator_status": "REJECTED",
  "system_status": "NO_NEW_ACTIONS",
  "pipeline_action": "STOP_BEFORE_EXECUTION_SIMULATION",
  "order_proposal_status": "REJECTED",
  "asset_id": "SMH",
  "reason": "Normalized order list would violate the Station-7-approved target plan or post-trade constraint.",
  "num_orders_proposed": 1,
  "num_orders_rejected": 1,
  "rejected_order_details": [
    {
      "asset_id": "SMH",
      "reason": "Normalized order would exceed approved target exposure."
    }
  ],
  "audit_hash": "<hash>"
}
```
## Testfälle

### TC_ORD_001 — Fehlende Pflichtfelder

Szenario:

Eine Order in proposed_order_list für QQQ enthält keine side oder quantity.

Erwartetes Ergebnis:

VAL_ORD_001 schlägt an.

Validator-Status:

BLOCKED

Systemstatus:

SAFE_HOLD

Pipeline:

STOP

Order Proposal Status:

REJECTED

### TC_ORD_002 — Liquiditätsverletzung

Szenario:

Eine SMH-Order entspricht 45 Prozent des 20-Tage-ADV.

Erwartetes Ergebnis:

VAL_ORD_002 schlägt an.

Validator-Status:

REJECTED

Systemstatus:

NO_NEW_ACTIONS

Pipeline:

STOP_BEFORE_EXECUTION_SIMULATION

Order Proposal Status:

REJECTED

### TC_ORD_003 — Harmlose Tick-Size-Normalisierung

Szenario:

Eine SPY BUY-LIMIT-Order hat limit_price 123.459 bei tick_size 0.01.

Erwartetes Ergebnis:

VAL_ORD_003 schlägt an.

Der Preis wird konservativ auf 123.45 abgerundet.

Validator-Status:

DOWNGRADED

Systemstatus:

NORMAL_CONTINUE

Pipeline:

CONTINUE

Order Proposal Status:

APPROVED

### TC_ORD_004 — Nicht normalisierbare Lot-Verletzung

Szenario:

Eine SMH BUY-Order hat quantity 47 bei lot_size_increment 100.

Erwartetes Ergebnis:

VAL_ORD_003 schlägt an.

Die Order darf nicht auf 100 erhöht werden.

Die gesamte Orderliste wird abgelehnt.

Validator-Status:

REJECTED

Systemstatus:

NO_NEW_ACTIONS

Pipeline:

STOP_BEFORE_EXECUTION_SIMULATION

Order Proposal Status:

REJECTED

### TC_ORD_005 — Kosten-/Slippage-Verletzung

Szenario:

Die geschätzten Gesamtkosten aus Slippage und Gebühren betragen 0.28 Prozent und überschreiten die konfigurierte Schwelle.

Erwartetes Ergebnis:

VAL_ORD_004 schlägt an.

Validator-Status:

REJECTED

Systemstatus:

NO_NEW_ACTIONS

Pipeline:

STOP_BEFORE_EXECUTION_SIMULATION

Order Proposal Status:

REJECTED

### TC_ORD_006 — Normalisierte Orderliste verletzt Zielplan

Szenario:

Eine technisch normalisierte Orderliste würde nicht mehr mit dem von Station 7 freigegebenen Zielportfolio übereinstimmen.

Erwartetes Ergebnis:

VAL_ORD_005 schlägt an.

Validator-Status:

REJECTED

Systemstatus:

NO_NEW_ACTIONS

Pipeline:

STOP_BEFORE_EXECUTION_SIMULATION

Order Proposal Status:

REJECTED

### TC_ORD_007 — Vollständig valide Orderliste

Szenario:

Eine proposed_order_list ist vollständig, brokerkonform, liquiditätskonform, kostenkonform und entspricht unverändert dem von Station 7 freigegebenen Zielportfolio.

Erwartetes Ergebnis:

Keine Regel schlägt blockierend an.

Validator-Status:

APPROVED

Systemstatus:

NORMAL_CONTINUE

Pipeline:

CONTINUE

Order Proposal Status:

APPROVED

Execution Simulation darf als nächster Schritt starten.

## Aktueller Status

Diese Station ist fachlich abgenommen.

## Codex-Hinweis

Codex darf diese Station später implementieren.

Warum:

Der Order Validator ist eine deterministische Prüfkomponente vor der Execution Simulation.

Wie:

Codex implementiert später OrderValidator, Decimal Utility, OrderValidationResult, Broker-Normalisierung, Audit-Events und Unit Tests exakt nach dieser Spezifikation.

Codex darf keine Orders erzeugen, keine Strategie verändern, keine Teilfreigabe einführen und keine Ausführungslogik ergänzen.

## Station-8-Freigabereferenz und Order-Referenzen

A) station_8_validation_ref: Pflichtfeld im APPROVED-Output. Es referenziert die konkrete Station-8-Freigabe der validierten Orderliste.

B) validated_order_list[].order_ref: Pflichtfeld je freigegebener Order. Jede freigegebene Order erhält eine eindeutige Referenz.

C) Eindeutigkeitsregel: order_ref ist innerhalb einer station_8_validation_ref eindeutig.

D) Zweck: Execution Simulator und Audit-Log können eindeutig nachvollziehen, welcher simulierte Fill auf welche von Station 8 validierte Order zurückgeht.

## Station-8-Anbindung an ProposedOrder

A) Input-Voraussetzung: Station 8 verarbeitet ausschließlich proposed_order_list-Eingaben mit CONTRACT_READY aus dem Pre-Order / Proposed Order Contract.

B) Traceability-Regel: Jede freigegebene Order in validated_order_list enthält order_ref und source_proposed_order_ref.

C) source_proposed_order_ref verweist exakt auf proposed_order_ref der ursprünglichen ProposedOrder.

D) Referenzkette: proposed_order_ref → source_proposed_order_ref / order_ref → source_order_ref.
