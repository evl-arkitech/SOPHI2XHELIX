"""Unit and integration tests for Outlier-Engineered Decision Core (OEAF)."""

import math
import numpy as np
import pytest
from doublehelix.runtime.decision_core import (
    ActionCandidate,
    TriageMetrics,
    SomaticAttentionalTriage,
    RecognitionPrimedGenerator,
    EpistemicDecouplingSandbox,
    SensemakingResetWatchdog,
    OutlierEngineeredDecisionCore,
)


def test_somatic_attentional_triage_priorities():
    triage = SomaticAttentionalTriage(token_ceiling=0.80, max_recursion=5, memory_ceiling=0.90)

    # 1. Healthy state -> Can actuate
    healthy = TriageMetrics(token_budget_ratio=0.3, recursion_depth=2, memory_pressure=0.4, invariant_breach=False)
    can_act, reason, priority = triage.audit_triage(healthy)
    assert can_act is True
    assert priority == 3

    # 2. Invariant breach -> Priority 1 (Aviate) halt
    breached = TriageMetrics(invariant_breach=True)
    can_act, reason, priority = triage.audit_triage(breached)
    assert can_act is False
    assert priority == 1
    assert "TRIAGE HALT [Aviate]" in reason

    # 3. Context saturation -> Priority 1 (Aviate) halt
    saturated = TriageMetrics(token_budget_ratio=0.85)
    can_act, reason, priority = triage.audit_triage(saturated)
    assert can_act is False
    assert priority == 1
    assert "Token context pressure" in reason


def test_recognition_primed_generator_domain_validity():
    rpg = RecognitionPrimedGenerator(validity_threshold=0.70)

    # Register prototype
    act_prototype = ActionCandidate(action_id="act_cached_solution", description="Proven heuristic candidate")
    rpg.register_prototype("pattern_stable_state", act_prototype)

    # High domain validity -> System 1 satisficing mode
    v_high = rpg.compute_domain_validity(feedback_latency_ms=10.0, environment_noise_sigma=0.05, historical_accuracy=0.95)
    assert v_high >= 0.70
    mode_high, candidate_high = rpg.evaluate_heuristic_mode(v_high, "pattern_stable_state")
    assert mode_high == "SATISFICING"
    assert candidate_high is not None
    assert candidate_high.action_id == "act_cached_solution"

    # Low domain validity -> Gated to First Principles
    v_low = rpg.compute_domain_validity(feedback_latency_ms=300.0, environment_noise_sigma=2.5, historical_accuracy=0.30)
    assert v_low < 0.70
    mode_low, candidate_low = rpg.evaluate_heuristic_mode(v_low, "pattern_stable_state")
    assert mode_low == "FIRST_PRINCIPLES"
    assert candidate_low is None


def test_epistemic_decoupling_sandbox_absorbing_barrier():
    sandbox = EpistemicDecouplingSandbox(max_ruin_tolerance=0.0)
    current_state = {"wealth": 100.0, "status": "active"}

    # Action A: High expected yield (+100%), but 5% ruin probability
    action_a = ActionCandidate(
        action_id="action_trap",
        description="High EV trap with absorbing barrier",
        expected_yield=1.0,
        ruin_probability=0.05
    )

    # Action B: Modest expected yield (+20%), strictly 0% ruin probability
    action_b = ActionCandidate(
        action_id="action_viable",
        description="Ergodically viable positive log-growth",
        expected_yield=0.20,
        ruin_probability=0.0
    )

    # Action C: Negative expected yield (-10%), 0% ruin
    action_c = ActionCandidate(
        action_id="action_loss",
        description="Safe loss",
        expected_yield=-0.10,
        ruin_probability=0.0
    )

    best_action, rollouts = sandbox.select_optimal_viable_policy(current_state, [action_a, action_b, action_c])

    # Action A must be rejected despite higher nominal return because P(ruin) > 0
    rollout_a = next(r for r in rollouts if r.action_id == "action_trap")
    assert rollout_a.approved is False
    assert rollout_a.ruin_detected is True
    assert "P(ruin) = 0.0500 > 0.0" in rollout_a.rejection_reason

    # Action B must be selected: highest E[ln(1 + r)] among viable candidates
    assert best_action is not None
    assert best_action.action_id == "action_viable"
    assert math.isclose(best_action.expected_yield, 0.20)


def test_sensemaking_reset_watchdog_drop_your_tools():
    watchdog = SensemakingResetWatchdog(surprise_threshold=2.0)

    # Small error -> no reset
    obs_nominal = np.array([1.0, 2.0, 3.0])
    pred_nominal = np.array([1.1, 2.0, 2.9])
    reset_needed, error_val, _ = watchdog.evaluate_prediction_error(obs_nominal, pred_nominal)
    assert reset_needed is False
    assert error_val < 2.0

    # Massive surprise shock -> triggers "Drop Your Tools" protocol
    obs_shock = np.array([10.0, 20.0, 30.0])
    pred_shock = np.array([1.0, 2.0, 3.0])
    reset_needed, error_val, reason = watchdog.evaluate_prediction_error(obs_shock, pred_shock)
    assert reset_needed is True
    assert "SENSEMAKING BREACH" in reason

    # Execution of Drop Your Tools
    polluted_context = {
        "scratchpad": "Unbounded speculative monologue hallucinating incorrect solutions...",
        "stale_hypotheses": ["hyp_1", "hyp_2"],
        "goal": "Preserve real-time 60 FPS deterministic loop"
    }
    grounded_facts = {"engine_tick": 420, "frame_time_ms": 11.2}

    purged = watchdog.execute_drop_your_tools(polluted_context, grounded_facts)
    assert "stale_hypotheses" not in purged
    assert purged["task_contract"] == "Preserve real-time 60 FPS deterministic loop"
    assert purged["grounded_facts"]["engine_tick"] == 420
    assert purged["status"] == "RE_ANCHORED_FROM_FIRST_PRINCIPLES"


def test_outlier_engineered_decision_core_end_to_end():
    core = OutlierEngineeredDecisionCore()

    candidates = [
        ActionCandidate(action_id="act_ruin", description="Ruin trap", expected_yield=3.0, ruin_probability=0.20),
        ActionCandidate(action_id="act_viable_high", description="Viable high", expected_yield=0.40, ruin_probability=0.0),
        ActionCandidate(action_id="act_viable_low", description="Viable low", expected_yield=0.10, ruin_probability=0.0)
    ]

    triage_ok = TriageMetrics(token_budget_ratio=0.2, recursion_depth=1, memory_pressure=0.2)
    decision = core.decide(triage_metrics=triage_ok, candidate_actions=candidates)

    assert decision["decision"] == "COMMITTED"
    assert decision["selected_action"]["action_id"] == "act_viable_high"
    assert decision["ruins_averted"] == 1

    # Check telemetry
    telem = core.get_telemetry()
    assert telem["total_decisions_made"] == 1
    assert telem["total_ruins_averted"] == 1
