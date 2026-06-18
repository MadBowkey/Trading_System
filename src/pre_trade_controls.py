"""Deterministic controls for the Pre-Trade-Control-Dry-Run demo.

This module deliberately models no broker connection, live market data,
persistent ledger, reconciliation, or real order execution.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_DOWN
from typing import Any


OFFICIAL_FILL_STATUSES = {"FULL", "PARTIAL", "NO_FILL", "FAILED"}
SAFETY_NOTICE = (
    "No live order was placed. No CURRENT_CONFIRMED portfolio state was created."
)

PROPOSED_ORDER_REQUIRED_FIELDS = (
    "proposed_order_ref",
    "run_id",
    "asset_id",
    "symbol",
    "side",
    "order_type",
    "quantity",
    "limit_price",
    "allow_short",
    "proposed_at",
    "market_data_snapshot_ref",
    "portfolio_state_ref",
)


class DemoInputError(ValueError):
    """Raised when a demo scenario violates its declared input contract."""


def _decimal_string(value: Any, field: str) -> Decimal:
    if not isinstance(value, str):
        raise DemoInputError(f"{field} must be a decimal string")
    try:
        return Decimal(value)
    except InvalidOperation as exc:
        raise DemoInputError(f"{field} must be a valid decimal string") from exc


def _utc_iso(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise DemoInputError(f"{field} must be a UTC ISO timestamp ending in Z")
    try:
        datetime.fromisoformat(value.removesuffix("Z") + "+00:00")
    except ValueError as exc:
        raise DemoInputError(f"{field} must be a valid UTC ISO timestamp") from exc


def _money(value: Decimal) -> str:
    return format(value.quantize(Decimal("0.01")), "f")


def _quantity(value: Decimal) -> str:
    normalized = value.normalize()
    return format(normalized, "f")


def validate_pre_order(order: dict[str, Any]) -> dict[str, Any]:
    missing = [field for field in PROPOSED_ORDER_REQUIRED_FIELDS if field not in order]
    if missing:
        return {
            "status": "CONTRACT_INVALID",
            "reason": f"Missing required fields: {', '.join(missing)}",
        }

    if not order.get("decision_ref") and not order.get("position_change_plan_ref"):
        return {
            "status": "CONTRACT_INVALID",
            "reason": "Missing decision_ref or position_change_plan_ref",
        }

    try:
        quantity = _decimal_string(order["quantity"], "quantity")
        if quantity <= 0:
            raise DemoInputError("quantity must be greater than zero")
        _utc_iso(order["proposed_at"], "proposed_at")

        order_type = order["order_type"]
        if order_type == "LIMIT":
            limit_price = _decimal_string(order["limit_price"], "limit_price")
            if limit_price <= 0:
                raise DemoInputError("limit_price must be greater than zero")
        elif order_type == "MARKET":
            if order["limit_price"] is not None:
                raise DemoInputError("MARKET order must have limit_price = null")
        else:
            raise DemoInputError("order_type must be LIMIT or MARKET")

        if order["side"] not in {"BUY", "SELL"}:
            raise DemoInputError("side must be BUY or SELL")
        if not isinstance(order["allow_short"], bool):
            raise DemoInputError("allow_short must be boolean")
    except DemoInputError as exc:
        return {"status": "CONTRACT_INVALID", "reason": str(exc)}

    return {
        "status": "CONTRACT_READY",
        "reason": "ProposedOrder contract is complete and formally valid.",
    }


def evaluate_station_8(
    scenario: dict[str, Any], order: dict[str, Any]
) -> dict[str, Any]:
    context = scenario["station_8_context"]
    liquidity = context["liquidity"]
    costs = context["costs"]

    if not context["station_7_approved_target"]["plan_compliance"]:
        return {
            "validator_status": "REJECTED",
            "order_proposal_status": "REJECTED",
            "pipeline_action": "STOP_BEFORE_EXECUTION_SIMULATION",
            "reason": "Order would violate the Station-7-approved target plan.",
        }

    order_size_pct = _decimal_string(
        liquidity["order_size_pct_of_20d_adv"],
        "order_size_pct_of_20d_adv",
    )
    max_order_size_pct = _decimal_string(
        liquidity["max_order_size_pct_of_20d_adv"],
        "max_order_size_pct_of_20d_adv",
    )
    if order_size_pct > max_order_size_pct:
        return {
            "validator_status": "REJECTED",
            "order_proposal_status": "REJECTED",
            "pipeline_action": "STOP_BEFORE_EXECUTION_SIMULATION",
            "reason": (
                "Order rejected: liquidity limit exceeded "
                f"({order_size_pct}% > {max_order_size_pct}% of 20d ADV)."
            ),
        }

    projected_cost = _decimal_string(
        costs["projected_slippage_plus_commission_pct"],
        "projected_slippage_plus_commission_pct",
    )
    max_cost = _decimal_string(
        costs["max_allowed_cost_pct"], "max_allowed_cost_pct"
    )
    if projected_cost > max_cost:
        return {
            "validator_status": "REJECTED",
            "order_proposal_status": "REJECTED",
            "pipeline_action": "STOP_BEFORE_EXECUTION_SIMULATION",
            "reason": (
                "Order rejected: projected costs exceed configured threshold "
                f"({projected_cost}% > {max_cost}%)."
            ),
        }

    run_id = order["run_id"]
    return {
        "validator_status": "APPROVED",
        "order_proposal_status": "APPROVED",
        "pipeline_action": "CONTINUE",
        "reason": "Order passed Station 8 liquidity, cost, and plan controls.",
        "station_8_validation_ref": f"station8_val_{run_id}",
        "validated_order": {
            **order,
            "order_ref": f"{run_id}_order_001",
            "source_proposed_order_ref": order["proposed_order_ref"],
        },
    }


def simulate_execution(
    scenario: dict[str, Any], station_8: dict[str, Any]
) -> dict[str, Any]:
    order = station_8["validated_order"]
    market = scenario["market_data"]
    quote = market[order["asset_id"]]
    portfolio = scenario["portfolio"]
    fee_model = scenario["fee_model"]
    slippage_model = scenario["slippage_model"]

    requested = _decimal_string(order["quantity"], "quantity")
    available = _decimal_string(quote["available_quantity"], "available_quantity")
    ask = _decimal_string(quote["ask_price"], "ask_price")
    limit_price = _decimal_string(order["limit_price"], "limit_price")
    cash = _decimal_string(portfolio["cash"], "cash")
    commission = _decimal_string(fee_model["commission_per_order"], "commission")
    slippage_bps = _decimal_string(slippage_model["slippage_bps"], "slippage_bps")

    fill_price = (ask * (Decimal("1") + slippage_bps / Decimal("10000"))).quantize(
        Decimal("0.01")
    )

    if fill_price > limit_price:
        filled = Decimal("0")
        fill_status = "NO_FILL"
        reason = "BUY limit price was not reached."
    else:
        affordable = ((cash - commission) / fill_price).to_integral_value(
            rounding=ROUND_DOWN
        )
        filled = min(requested, available, max(Decimal("0"), affordable))
        if filled == requested:
            fill_status = "FULL"
            reason = "Requested quantity was fully available and affordable."
        elif filled > 0:
            fill_status = "PARTIAL"
            reason = (
                "Simulated fill quantity was limited to available liquidity; "
                "the approved order itself was not modified."
            )
        else:
            fill_status = "NO_FILL"
            reason = "No quantity was available and affordable for simulation."

    if fill_status not in OFFICIAL_FILL_STATUSES:
        raise AssertionError(f"Unsupported fill status: {fill_status}")

    applied_commission = commission if filled > 0 else Decimal("0")
    gross_cost = filled * fill_price
    cash_after = cash - gross_cost - applied_commission
    existing_quantity = sum(
        _decimal_string(position["quantity"], "position.quantity")
        for position in portfolio.get("positions", [])
        if position["asset_id"] == order["asset_id"]
    )
    position_quantity = existing_quantity + filled
    position_market_value = position_quantity * ask
    other_position_value = sum(
        _decimal_string(position["market_value"], "position.market_value")
        for position in portfolio.get("positions", [])
        if position["asset_id"] != order["asset_id"]
    )
    total_portfolio_value = cash_after + position_market_value + other_position_value

    simulation_status = "SUCCESS" if fill_status == "FULL" else "PARTIAL"
    run_id = order["run_id"]
    return {
        "simulation_status": simulation_status,
        "fill_status": fill_status,
        "requested_quantity": _quantity(requested),
        "filled_quantity": _quantity(filled),
        "fill_price": _money(fill_price) if filled > 0 else None,
        "commission": _money(applied_commission),
        "reason": reason,
        "simulation_timestamp": scenario["simulation_timestamp"],
        "station_8_validation_ref": station_8["station_8_validation_ref"],
        "source_order_ref": order["order_ref"],
        "post_execution_portfolio": {
            "portfolio_state_ref": f"{run_id}_simulated_post_execution",
            "parent_portfolio_state_ref": portfolio["portfolio_state_ref"],
            "run_id": run_id,
            "timestamp_utc": scenario["simulation_timestamp"],
            "portfolio_state_type": "SIMULATED_POST_EXECUTION",
            "source": "ExecutionSimulator",
            "cash": _money(cash_after),
            "positions": [
                {
                    "asset_id": order["asset_id"],
                    "symbol": order["symbol"],
                    "quantity": _quantity(position_quantity),
                    "market_value": _money(position_market_value),
                }
            ],
            "total_portfolio_value": _money(total_portfolio_value),
            "data_quality_status": "SIMULATED",
            "confirmed": False,
        },
    }


def run_scenario(scenario: dict[str, Any]) -> dict[str, Any]:
    order = scenario["trade_idea"]
    pre_order = validate_pre_order(order)

    station_8: dict[str, Any] | None = None
    simulation: dict[str, Any] | None = None
    if pre_order["status"] == "CONTRACT_READY":
        station_8 = evaluate_station_8(scenario, order)
        if station_8["order_proposal_status"] == "APPROVED":
            simulation = simulate_execution(scenario, station_8)

    reference_chain = {
        "run_id": order.get("run_id"),
        "proposed_order_ref": order.get("proposed_order_ref"),
        "source_proposed_order_ref": (
            station_8["validated_order"]["source_proposed_order_ref"]
            if station_8 and station_8.get("validated_order")
            else None
        ),
        "order_ref": (
            station_8["validated_order"]["order_ref"]
            if station_8 and station_8.get("validated_order")
            else None
        ),
        "station_8_validation_ref": (
            station_8.get("station_8_validation_ref") if station_8 else None
        ),
        "source_order_ref": simulation.get("source_order_ref") if simulation else None,
        "input_portfolio_state_ref": order.get("portfolio_state_ref"),
        "simulated_portfolio_state_ref": (
            simulation["post_execution_portfolio"]["portfolio_state_ref"]
            if simulation
            else None
        ),
    }

    if pre_order["status"] != "CONTRACT_READY":
        reason = pre_order["reason"]
    elif simulation:
        reason = simulation["reason"]
    else:
        reason = station_8["reason"] if station_8 else "Station 8 was not reached."

    return {
        "scenario": scenario["scenario"],
        "management_label": scenario["management_label"],
        "trade_idea": order,
        "pre_order_status": pre_order["status"],
        "station_8_decision": station_8,
        "simulation_performed": simulation is not None,
        "simulation": simulation,
        "reason": reason,
        "reference_chain": reference_chain,
        "safety_boundary": {
            "notice": SAFETY_NOTICE,
            "live_order_placed": False,
            "persistent_ledger_written": False,
            "reconciliation_performed": False,
            "current_confirmed_created": False,
        },
    }


def run_scenarios(document: dict[str, Any]) -> dict[str, Any]:
    scenarios = document.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        raise DemoInputError("Demo document must contain a non-empty scenarios list")
    return {
        "report_name": "Pre-Trade-Control-Dry-Run",
        "report_version": "1.0",
        "results": [run_scenario(scenario) for scenario in scenarios],
        "safety_notice": SAFETY_NOTICE,
    }
