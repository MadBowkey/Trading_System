# Specification Index

Status: CURRENT
Architecture: v1.6.1
Last updated: 2026-06-18

## Zweck

Diese Datei ist ein reiner Index.

Sie enthaelt keine laufenden Gate-Snapshots und keine Handoff-Bewertung. Der aktuelle Uebergabestand steht in `specs/99_handoff_snapshot_current.md`.

## Canonical source

GitHub `main` is the canonical technical project state.

## Workflow files

- specs/93_new_chat_transition_protocol.md
- specs/94_start_audit_protocol.md
- specs/95_operational_workflow_rules.md
- specs/96_frozen_project_state.md
- specs/96_practical_new_chat_handoff_steps.md
- specs/97_new_chat_handoff_prompt_v1.md
- specs/98_spec_index.md
- specs/99_handoff_snapshot_current.md

## Core specs

- specs/00_project_overview_v1_6_1.md
- specs/01_architecture_overview_v1_6_1.md
- specs/02_llm_output_schema_v1.md
- specs/03_risk_metrics_v1.md
- specs/04_guardrails_v1.md
- specs/05_deductive_rules_v1.md
- specs/06_validator_pipeline_v1.md
- specs/07_station_1_pre_llm_validator.md
- specs/08_station_2_llm_meta_manager.md
- specs/09_station_3_technical_schema_validator.md
- specs/10_station_4_business_logic_validator.md
- specs/11_station_5_market_risk_validator.md
- specs/12_station_6_portfolio_engine.md
- specs/13_station_7_post_trade_risk_validator.md
- specs/14_station_8_order_validator.md
- specs/15_audit_log_core_v1.md
- specs/16_execution_simulator_core_v1.md
- specs/17_pre_order_proposed_order_contract_core_v1.md
- specs/18_portfolio_state_ledger_core_v1.md

## Config files

- config/rule_registry.yaml
- config/risk_guardrails.yaml
- config/regime_matrix.yaml
- config/indicator_registry.yaml
- config/universe.example.yaml

## Golden cases

- tests/golden_cases/station_3_technical_schema_validator_cases.json
- tests/golden_cases/station_4_business_logic_validator_cases.json
- tests/golden_cases/station_5_market_risk_validator_cases.json
- tests/golden_cases/station_6_portfolio_engine_cases.json
- tests/golden_cases/station_7_post_trade_risk_validator_cases.json
- tests/golden_cases/station_8_order_validator_cases.json
- tests/golden_cases/audit_log_core_v1_cases.json
- tests/golden_cases/execution_simulator_core_v1_cases.json
- tests/golden_cases/pre_order_contract_core_v1_cases.json
- tests/golden_cases/portfolio_state_ledger_core_v1_cases.json
