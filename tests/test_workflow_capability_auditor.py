"""Tests for Agent 7: Workflow & Agent Capabilities Auditor.

Validates:
1. Workflow auditing across ascending elevation tiers, circuit breakers, and parity gates.
2. Invariant violation detection (timing, allocations, tunneling, visual anomalies, bot crashes).
3. Chronological execution trace auditing for non-sequential tier skips.
4. Agent capability introspection and interface contract checking.
5. Dynamic empirical capability calibration probes across Strand Alpha, Strand Beta, and Hermes.
6. Unified SystemAuditReport generation.
7. DoubleHelixOrchestrator integration.
8. Hermes 3 Tool Dispatcher integration.
"""

import pytest
from typing import Dict, Any

from doublehelix.agents.auditor import (
    WorkflowCapabilityAuditor,
    AgentCapabilityDescriptor,
    WorkflowAuditReport,
    CapabilityAuditReport,
    SystemAuditReport,
)
from doublehelix.state import create_initial_state
from doublehelix.orchestrator.helix_engine import DoubleHelixOrchestrator
from doublehelix.hermes.tools import DoubleHelixHermesDispatcher


def test_auditor_initialization_and_descriptors():
    auditor = WorkflowCapabilityAuditor()
    descriptors = auditor.get_registered_descriptors()

    assert len(descriptors) >= 8
    expected_agents = [
        "agent_1_ecs_architect",
        "agent_2_system_coder",
        "agent_3_spatial_math",
        "agent_4_playtest_bot",
        "agent_5_frame_profiler",
        "agent_6_visual_auditor",
        "agent_hermes_singularity",
        "agent_7_workflow_auditor",
    ]
    for agent_id in expected_agents:
        assert agent_id in descriptors
        desc = descriptors[agent_id]
        assert desc.status == "HEALTHY"
        assert len(desc.capabilities) > 0
        assert len(desc.interface_methods) > 0
        assert len(desc.formal_invariants) > 0


def test_workflow_auditing_clean_state():
    auditor = WorkflowCapabilityAuditor()
    state = create_initial_state()

    report = auditor.audit_workflow(state=state)
    assert isinstance(report, WorkflowAuditReport)
    assert report.passed is True
    assert report.violations_count == 0
    assert report.circuit_breaker_healthy is True
    assert report.parity_gate_integrity_score == 100.0


def test_workflow_auditing_circuit_breaker_trip():
    auditor = WorkflowCapabilityAuditor()
    state = create_initial_state(max_cycles_per_tier=3)
    state["current_cycle"] = 4  # Exceeds max_cycles_per_tier

    report = auditor.audit_workflow(state=state)
    assert report.passed is False
    assert report.circuit_breaker_healthy is False
    assert report.violations_count >= 1
    assert any("Circuit breaker breached" in v for v in report.violations)


def test_workflow_auditing_converged_anomaly_detection():
    auditor = WorkflowCapabilityAuditor()
    state = create_initial_state()
    state["tier"] = "CONVERGED"
    state["avg_frame_time_ms"] = 24.5  # Breaches 16.6ms
    state["allocations_in_loop"] = 5    # Breaches zero-alloc
    state["headless_bot_crashes"] = 2   # Breaches zero-crash

    report = auditor.audit_workflow(state=state)
    assert report.passed is False
    assert report.violations_count >= 3
    assert any("frame time" in v for v in report.violations)
    assert any("dynamic allocations" in v for v in report.violations)
    assert any("bot crashes" in v for v in report.violations)


def test_workflow_auditing_execution_trace():
    auditor = WorkflowCapabilityAuditor()

    # Valid trace: sequential ascent
    valid_trace = [
        {"tier": "LEVEL_1_KERNEL", "cycle": 1, "elevate": True},
        {"tier": "LEVEL_2_ECS", "cycle": 1, "elevate": True},
        {"tier": "LEVEL_3_RENDER", "cycle": 1, "elevate": True},
        {"tier": "LEVEL_4_PLAYTEST", "cycle": 1, "elevate": True},
        {"tier": "CONVERGED", "cycle": 1, "elevate": True}
    ]
    clean_report = auditor.audit_workflow(execution_trace=valid_trace)
    assert clean_report.passed is True

    # Flawed trace: non-sequential jump (skipping LEVEL_2_ECS)
    flawed_trace = [
        {"tier": "LEVEL_1_KERNEL", "cycle": 1, "elevate": True},
        {"tier": "LEVEL_3_RENDER", "cycle": 1, "elevate": True}
    ]
    flawed_report = auditor.audit_workflow(execution_trace=flawed_trace)
    assert flawed_report.passed is False
    assert any("Non-sequential tier ascension" in v for v in flawed_report.violations)


def test_agent_capabilities_probing():
    auditor = WorkflowCapabilityAuditor()
    report = auditor.audit_agent_capabilities(run_probes=True)

    assert isinstance(report, CapabilityAuditReport)
    assert report.total_agents >= 8
    assert report.healthy_agents >= 8
    assert report.degraded_agents == 0
    assert report.probes_run >= 5
    assert report.probes_passed == report.probes_run
    assert report.capability_maturity_score == 100.0

    probe_names = [p.probe_name for p in report.probe_results]
    assert "frame_profiler_contract_discrimination" in probe_names
    assert "visual_contract_anomaly_detection" in probe_names
    assert "fuzz_schedule_and_crash_detection" in probe_names
    assert "system_coder_fence_extraction" in probe_names
    assert "hermes_tag_parsing_and_tool_dispatch" in probe_names
    assert "ergodicity_ruin_gate_absorbing_barrier" in probe_names
    assert "cellular_sheaf_laplacian_dirichlet_decay" in probe_names
    assert "linear_session_channel_confluence_and_zero_leakage" in probe_names
    assert report.probes_run == 11
    assert report.probes_passed == 11


def test_agent_capabilities_live_instance_gap_analysis():
    auditor = WorkflowCapabilityAuditor()

    # Mock an incomplete agent that lacks required interface methods
    class DegradedPlaytestAgent:
        pass  # Missing build_fuzz_payload and evaluate_bot_telemetry

    degraded_map = {
        "agent_4_playtest_bot": DegradedPlaytestAgent()
    }

    report = auditor.audit_agent_capabilities(agents_map=degraded_map, run_probes=False)
    assert report.degraded_agents >= 1
    assert "agent_4_playtest_bot" in report.agent_descriptors
    assert report.agent_descriptors["agent_4_playtest_bot"].status == "DEGRADED"
    assert len(report.gap_analysis) >= 1
    assert any("missing required interface methods" in g for g in report.gap_analysis)


def test_full_system_audit_synthesis():
    auditor = WorkflowCapabilityAuditor()
    state = create_initial_state()

    full_report = auditor.run_full_audit(state=state, run_probes=True)
    assert isinstance(full_report, SystemAuditReport)
    assert full_report.overall_status == "HEALTHY"
    assert full_report.overall_score == 100.0
    assert "Double Helix Metacognitive Audit Completed" in full_report.executive_summary
    assert len(full_report.remediation_roadmap) > 0


def test_orchestrator_auditor_integration():
    orchestrator = DoubleHelixOrchestrator()
    assert hasattr(orchestrator, "auditor")
    assert isinstance(orchestrator.auditor, WorkflowCapabilityAuditor)

    state = create_initial_state()
    wf_report = orchestrator.audit_workflow(state=state)
    assert wf_report.passed is True

    cap_report = orchestrator.audit_agent_capabilities(run_probes=True)
    assert cap_report.capability_maturity_score == 100.0

    sys_report = orchestrator.run_system_audit(state=state, run_probes=True)
    assert sys_report.overall_status == "HEALTHY"


def test_hermes_tool_dispatcher_auditing():
    dispatcher = DoubleHelixHermesDispatcher()
    assert hasattr(dispatcher, "auditor")

    # 1. Audit Workflows
    wf_res = dispatcher.dispatch("audit_doublehelix_workflows", {"workflow_type": "dual_strand_upward_slice"})
    assert wf_res["passed"] is True
    assert wf_res["parity_gate_integrity_score"] == 100.0

    # 2. Audit Agent Capabilities
    cap_res = dispatcher.dispatch("audit_agent_capabilities", {"run_probes": True})
    assert cap_res["capability_maturity_score"] == 100.0
    assert cap_res["healthy_agents"] >= 8

    # 3. Full System Audit
    sys_res = dispatcher.dispatch("run_full_system_audit", {"run_probes": True})
    assert sys_res["overall_status"] == "HEALTHY"
    assert sys_res["overall_score"] == 100.0
