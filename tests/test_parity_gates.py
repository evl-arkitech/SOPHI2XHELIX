"""Tests for Base Rung Parity Gates (Levels 1 to 4)."""

import pytest
from doublehelix.orchestrator.parity_gates import evaluate_base_rung


def test_base_rung_1_frame_budget_pass():
    alpha = {"spatial_invariants_valid": True}
    beta = {"avg_frame_time_ms": 12.0, "allocations_in_loop": 0}
    passed, reason = evaluate_base_rung("LEVEL_1_KERNEL", alpha, beta)
    assert passed is True
    assert "verified" in reason.lower() or "stable" in reason.lower()


def test_base_rung_1_frame_budget_fail():
    alpha = {"spatial_invariants_valid": True}
    beta = {"avg_frame_time_ms": 18.5, "allocations_in_loop": 0}
    passed, reason = evaluate_base_rung("LEVEL_1_KERNEL", alpha, beta)
    assert passed is False
    assert "breached" in reason.lower()


def test_base_rung_1_allocations_fail():
    alpha = {"spatial_invariants_valid": True}
    beta = {"avg_frame_time_ms": 10.0, "allocations_in_loop": 3}
    passed, reason = evaluate_base_rung("LEVEL_1_KERNEL", alpha, beta)
    assert passed is False
    assert "allocations detected" in reason.lower()


def test_base_rung_2_tunneling_pass_and_fail():
    alpha = {"spatial_invariants_valid": True}
    beta_pass = {"tunneling_errors": 0}
    passed, reason = evaluate_base_rung("LEVEL_2_ECS", alpha, beta_pass)
    assert passed is True

    beta_fail = {"tunneling_errors": 2}
    passed, reason = evaluate_base_rung("LEVEL_2_ECS", alpha, beta_fail)
    assert passed is False
    assert "tunneling" in reason.lower()


def test_base_rung_3_render_pass_and_fail():
    alpha = {}
    beta_pass = {"shader_errors": 0, "visual_anomalies": 0}
    passed, _ = evaluate_base_rung("LEVEL_3_RENDER", alpha, beta_pass)
    assert passed is True

    beta_fail = {"shader_errors": 1, "visual_anomalies": 0}
    passed, _ = evaluate_base_rung("LEVEL_3_RENDER", alpha, beta_fail)
    assert passed is False


def test_base_rung_4_playtest_pass_and_fail():
    alpha = {}
    beta_pass = {"headless_bot_crashes": 0}
    passed, _ = evaluate_base_rung("LEVEL_4_PLAYTEST", alpha, beta_pass)
    assert passed is True

    beta_fail = {"headless_bot_crashes": 4}
    passed, reason = evaluate_base_rung("LEVEL_4_PLAYTEST", alpha, beta_fail)
    assert passed is False
    assert "crashes" in reason.lower() or "bot" in reason.lower()
