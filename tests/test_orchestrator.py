"""Tests for DoubleHelixOrchestrator and dual-strand ascension."""

import pytest
from doublehelix.orchestrator.helix_engine import DoubleHelixOrchestrator
from doublehelix.state import create_initial_state


def test_orchestrator_promote_tier():
    orchestrator = DoubleHelixOrchestrator()
    state = create_initial_state()

    assert state["tier"] == "LEVEL_1_KERNEL"
    state = orchestrator._promote_tier(state)
    assert state["tier"] == "LEVEL_2_ECS"
    state = orchestrator._promote_tier(state)
    assert state["tier"] == "LEVEL_3_RENDER"
    state = orchestrator._promote_tier(state)
    assert state["tier"] == "LEVEL_4_PLAYTEST"
    state = orchestrator._promote_tier(state)
    assert state["tier"] == "CONVERGED"


def test_orchestrator_evaluate_base_rungs():
    orchestrator = DoubleHelixOrchestrator()

    # Base Rung 1
    elevate, msg = orchestrator._evaluate_base_rung(
        "LEVEL_1_KERNEL",
        alpha={"spatial_invariants_valid": True},
        beta={"avg_frame_time_ms": 5.4, "allocations_in_loop": 0}
    )
    assert elevate is True

    # Base Rung 2
    elevate, msg = orchestrator._evaluate_base_rung(
        "LEVEL_2_ECS",
        alpha={"spatial_invariants_valid": True},
        beta={"tunneling_errors": 0}
    )
    assert elevate is True

    # Base Rung 3
    elevate, msg = orchestrator._evaluate_base_rung(
        "LEVEL_3_RENDER",
        alpha={},
        beta={"shader_errors": 0, "visual_anomalies": 0}
    )
    assert elevate is True

    # Base Rung 4
    elevate, msg = orchestrator._evaluate_base_rung(
        "LEVEL_4_PLAYTEST",
        alpha={},
        beta={"headless_bot_crashes": 0}
    )
    assert elevate is True
