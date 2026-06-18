import json
from pathlib import Path

from pre_trade_control_dry_run import load_scenarios, render_json, render_text
from pre_trade_controls import OFFICIAL_FILL_STATUSES, SAFETY_NOTICE, run_scenarios


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "examples" / "pre_trade_dry_run_scenarios.json"
FORBIDDEN_STATUSES = {
    "APPROVED_WITH_REDUCTION",
    "PARTIAL_OR_NO_FILL",
    "FULL_OR_PARTIAL",
}


def _results_by_scenario():
    report = run_scenarios(load_scenarios(SCENARIOS))
    return report, {result["scenario"]: result for result in report["results"]}


def test_full_fill_scenario_is_approved_and_successful():
    _, results = _results_by_scenario()
    result = results["spy_limit_buy_full_fill"]

    assert result["pre_order_status"] == "CONTRACT_READY"
    assert result["station_8_decision"]["order_proposal_status"] == "APPROVED"
    assert result["simulation_performed"] is True
    assert result["simulation"]["fill_status"] == "FULL"
    assert result["simulation"]["simulation_status"] == "SUCCESS"


def test_liquidity_blocked_scenario_stops_before_simulation():
    _, results = _results_by_scenario()
    result = results["spy_limit_buy_blocked_liquidity"]

    assert result["pre_order_status"] == "CONTRACT_READY"
    assert result["station_8_decision"]["validator_status"] == "REJECTED"
    assert result["station_8_decision"]["order_proposal_status"] == "REJECTED"
    assert (
        result["station_8_decision"]["pipeline_action"]
        == "STOP_BEFORE_EXECUTION_SIMULATION"
    )
    assert result["simulation_performed"] is False
    assert result["simulation"] is None


def test_partial_scenario_is_approved_and_stays_simulated():
    _, results = _results_by_scenario()
    result = results["spy_limit_buy_partial_simulated_fill"]

    assert result["station_8_decision"]["order_proposal_status"] == "APPROVED"
    assert result["simulation_performed"] is True
    assert result["simulation"]["fill_status"] == "PARTIAL"
    assert result["simulation"]["simulation_status"] == "PARTIAL"
    assert result["simulation"]["requested_quantity"] == "100"
    assert result["simulation"]["filled_quantity"] == "40"
    assert (
        result["simulation"]["post_execution_portfolio"]["portfolio_state_type"]
        == "SIMULATED_POST_EXECUTION"
    )
    assert result["simulation"]["post_execution_portfolio"]["confirmed"] is False


def test_reference_chains_are_consistent_for_simulated_scenarios():
    _, results = _results_by_scenario()
    for scenario_name in (
        "spy_limit_buy_full_fill",
        "spy_limit_buy_partial_simulated_fill",
    ):
        result = results[scenario_name]
        refs = result["reference_chain"]
        assert refs["proposed_order_ref"] == refs["source_proposed_order_ref"]
        assert refs["order_ref"] == refs["source_order_ref"]
        assert (
            refs["station_8_validation_ref"]
            == result["simulation"]["station_8_validation_ref"]
        )
        assert (
            refs["input_portfolio_state_ref"]
            == result["simulation"]["post_execution_portfolio"][
                "parent_portfolio_state_ref"
            ]
        )


def test_only_official_fill_statuses_and_no_forbidden_enums():
    report, _ = _results_by_scenario()
    serialized = json.dumps(report)
    assert not any(status in serialized for status in FORBIDDEN_STATUSES)

    observed = {
        result["simulation"]["fill_status"]
        for result in report["results"]
        if result["simulation"] is not None
    }
    assert observed <= OFFICIAL_FILL_STATUSES


def test_safety_boundary_and_reports_are_explicit():
    report, _ = _results_by_scenario()
    for result in report["results"]:
        boundary = result["safety_boundary"]
        assert boundary["notice"] == SAFETY_NOTICE
        assert boundary["live_order_placed"] is False
        assert boundary["persistent_ledger_written"] is False
        assert boundary["reconciliation_performed"] is False
        assert boundary["current_confirmed_created"] is False

    text_report = render_text(report)
    json_report = render_json(report)
    assert SAFETY_NOTICE in text_report
    assert json.loads(json_report)["safety_notice"] == SAFETY_NOTICE


def test_demo_and_all_golden_case_json_files_parse():
    json.loads(SCENARIOS.read_text(encoding="utf-8"))
    golden_files = sorted((ROOT / "tests" / "golden_cases").glob("*.json"))
    assert len(golden_files) == 10
    for golden_file in golden_files:
        json.loads(golden_file.read_text(encoding="utf-8-sig"))
