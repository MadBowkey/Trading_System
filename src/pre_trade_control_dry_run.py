"""Command-line entry point for the deterministic pre-trade demo."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

from pre_trade_controls import SAFETY_NOTICE, run_scenarios


DEFAULT_SCENARIOS = (
    Path(__file__).resolve().parents[1]
    / "examples"
    / "pre_trade_dry_run_scenarios.json"
)


def load_scenarios(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def render_text(report: dict[str, Any]) -> str:
    lines = [report["report_name"], "=" * len(report["report_name"])]
    for result in report["results"]:
        order = result["trade_idea"]
        station_8 = result["station_8_decision"]
        simulation = result["simulation"]
        lines.extend(
            [
                "",
                f"Scenario: {result['scenario']}",
                f"Management result: {result['management_label']}",
                (
                    "Trade idea: "
                    f"{order['side']} {order['quantity']} {order['symbol']} "
                    f"{order['order_type']} @ {order['limit_price']}"
                ),
                f"Pre-order status: {result['pre_order_status']}",
                "Station 8 decision: "
                + (
                    station_8["order_proposal_status"]
                    if station_8
                    else "NOT REACHED"
                ),
                f"Simulation performed: {'yes' if result['simulation_performed'] else 'no'}",
                "Fill status: " + (simulation["fill_status"] if simulation else "n/a"),
                "Simulation status: "
                + (simulation["simulation_status"] if simulation else "n/a"),
                f"Reason: {result['reason']}",
                "Reference chain: "
                + " -> ".join(
                    str(value)
                    for value in result["reference_chain"].values()
                    if value is not None
                ),
                SAFETY_NOTICE,
            ]
        )
    return "\n".join(lines)


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, ensure_ascii=False, indent=2)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run deterministic SPY LIMIT BUY pre-trade control scenarios."
    )
    parser.add_argument(
        "scenario_file",
        nargs="?",
        type=Path,
        default=DEFAULT_SCENARIOS,
        help="JSON file containing demo scenarios",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json", "both"),
        default="both",
        help="Report output format",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = run_scenarios(load_scenarios(args.scenario_file))
    if args.format in {"text", "both"}:
        print(render_text(report))
    if args.format == "both":
        print("\nJSON report\n===========")
    if args.format in {"json", "both"}:
        print(render_json(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
