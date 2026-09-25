"""Outlier-Engineered Agentic Framework (OEAF) & Ergodic Decision Core.

Translates human outlier performance mechanisms under high-stakes shock into an
algorithmic framework:
1. Somatic Attentional Triage (PFC Preserver, Aviate-Navigate-Communicate protocol)
2. Recognition-Primed Heuristic Generator (Kahneman-Klein Dual Process, Domain Validity)
3. Epistemic Decoupling Sandbox (Stanovich Type 2 forward rollout, Absorbing Barrier Invariant)
4. Sensemaking Reset Watchdog ("Drop Your Tools" Protocol on Bayesian Surprise)
5. Constrained Log-Growth Policy:
   pi* = argmax_{a in A_viable} E[ln(1 + r(s, a))] where P(ruin | a) = 0.
"""

import math
import time
from typing import Dict, List, Any, Optional, Tuple, Callable
import numpy as np
from pydantic import BaseModel, Field


# ============================================================================
# DATA STRUCTURES & CONFIGURATION
# ============================================================================

class ActionCandidate(BaseModel):
    """Candidate action evaluated by the decision core."""
    action_id: str
    description: str
    expected_yield: float = 0.0          # Multiplicative growth factor r
    ruin_probability: float = 0.0        # P(s_{t+1} in S_absorb)
    payload: Dict[str, Any] = Field(default_factory=dict)
    stress_cost: float = 0.0             # Internal physical / parameter wear
    epistemic_value: float = 0.0         # Information gain under active inference


class TriageMetrics(BaseModel):
    """Real-time invariant metrics for Somatic Attentional Triage."""
    token_budget_ratio: float = 0.2      # [0, 1] - ratio of context consumed
    recursion_depth: int = 1
    max_recursion_depth: int = 8
    memory_pressure: float = 0.3        # [0, 1]
    last_action_latency_ms: float = 12.0
    invariant_breach: bool = False


class EpistemicRolloutResult(BaseModel):
    """Result of sandboxed counterfactual forward simulation."""
    action_id: str
    approved: bool
    ruin_detected: bool
    projected_log_growth: float
    simulated_stress: float
    shadow_state_snapshot: Dict[str, Any]
    rejection_reason: Optional[str] = None


# ============================================================================
# MODULE 1: SOMATIC ATTENTIONAL TRIAGE (PFC PRESERVER)
# ============================================================================

class SomaticAttentionalTriage:
    """Enforces the 'Aviate, Navigate, Communicate' protocol.

    Priorities:
    - Priority 1 (Aviate): Invariant check (token budget, memory pressure, execution state).
    - Priority 2 (Navigate): Operational path (goal navigation, strategy evaluation).
    - Priority 3 (Communicate): External tool dispatching and output emission.

    If system invariants are stressed, external tool calling and output generation
    are gated until state stabilization, preventing catecholaminergic context saturation.
    """

    def __init__(
        self,
        token_ceiling: float = 0.85,
        max_recursion: int = 8,
        memory_ceiling: float = 0.90
    ):
        self.token_ceiling = token_ceiling
        self.max_recursion = max_recursion
        self.memory_ceiling = memory_ceiling
        self.gated_events_count: int = 0

    def audit_triage(self, metrics: TriageMetrics) -> Tuple[bool, str, int]:
        """Audits current somatic health. Returns (can_actuate, reason, active_priority)."""
        # Priority 1: Aviate (Survival / State Invariant)
        if metrics.invariant_breach:
            self.gated_events_count += 1
            return False, "TRIAGE HALT [Aviate]: System invariant breach detected. External actions gated.", 1

        if metrics.token_budget_ratio >= self.token_ceiling:
            self.gated_events_count += 1
            return False, f"TRIAGE HALT [Aviate]: Token context pressure {metrics.token_budget_ratio:.1%} >= {self.token_ceiling:.1%}. Must prune.", 1

        if metrics.recursion_depth >= self.max_recursion:
            self.gated_events_count += 1
            return False, f"TRIAGE HALT [Aviate]: Recursion depth {metrics.recursion_depth} reached maximum {self.max_recursion}.", 1

        if metrics.memory_pressure >= self.memory_ceiling:
            self.gated_events_count += 1
            return False, f"TRIAGE HALT [Aviate]: Memory pressure {metrics.memory_pressure:.1%} exceeds threshold {self.memory_ceiling:.1%}.", 1

        # Priority 2: Navigate (Operational Planning)
        # Priority 3: Communicate (External Actuation Cleared)
        return True, "TRIAGE CLEAR [Communicate]: Invariants nominal. External actuation authorized.", 3


# ============================================================================
# MODULE 2: RECOGNITION-PRIMED HEURISTIC GENERATOR (KAHNEMAN-KLEIN)
# ============================================================================

class RecognitionPrimedGenerator:
    """Dual-process decider balancing fast satisficing vs first-principles decomposition.

    Calculates domain validity V(E). If V(E) >= theta_valid, queries associative prototype
    library (Satisficing: evaluate one plausible candidate). If V(E) < theta_valid,
    disables fast heuristics and triggers first-principles decomposition.
    """

    def __init__(self, validity_threshold: float = 0.70):
        self.validity_threshold = validity_threshold
        self.prototype_library: Dict[str, ActionCandidate] = {}

    def register_prototype(self, pattern_signature: str, candidate: ActionCandidate) -> None:
        """Stores a high-validity associative prototype action."""
        self.prototype_library[pattern_signature] = candidate

    def compute_domain_validity(
        self,
        feedback_latency_ms: float,
        environment_noise_sigma: float,
        historical_accuracy: float
    ) -> float:
        """Calculates domain validity metric V(E) in [0, 1].

        High validity requires: low feedback latency, low environmental noise, high predictive accuracy.
        """
        latency_score = math.exp(-feedback_latency_ms / 100.0)
        noise_score = math.exp(-environment_noise_sigma)
        v = 0.4 * latency_score + 0.3 * noise_score + 0.3 * historical_accuracy
        return float(np.clip(v, 0.0, 1.0))

    def evaluate_heuristic_mode(
        self,
        domain_validity: float,
        cues_signature: Optional[str] = None
    ) -> Tuple[str, Optional[ActionCandidate]]:
        """Returns ('SATISFICING', prototype) or ('FIRST_PRINCIPLES', None)."""
        if domain_validity >= self.validity_threshold and cues_signature in self.prototype_library:
            return "SATISFICING", self.prototype_library[cues_signature]
        return "FIRST_PRINCIPLES", None


# ============================================================================
# MODULE 3: EPISTEMIC DECOUPLING SANDBOX (STANOVICH / TESLA-OPTIC)
# ============================================================================

class EpistemicDecouplingSandbox:
    """Executes sandboxed forward-looking rollouts of action candidates.

    Guarantees:
    - Pure cognitive decoupling: Master state is NEVER mutated with unverified candidates.
    - Absorbing Barrier Invariant: Filters out any action where P(s_{t+1} in S_absorb) > 0.
    - Optimizes for Time-Average Log-Growth g = E[ln(1 + r)].
    """

    def __init__(self, max_ruin_tolerance: float = 0.0):
        # Strict zero-ruin tolerance: P(ruin) == 0 required
        self.max_ruin_tolerance = max_ruin_tolerance

    def rollout(
        self,
        candidate: ActionCandidate,
        current_state: Optional[Dict[str, Any]] = None,
        shadow_evaluator: Optional[Callable[[Dict[str, Any], ActionCandidate], Tuple[bool, float, Dict[str, Any]]]] = None
    ) -> EpistemicRolloutResult:
        """Convenience rollout method accepting candidate and optional current state."""
        return self.rollout_candidate(current_state or {}, candidate, shadow_evaluator)

    def rollout_candidate(
        self,
        master_state: Dict[str, Any],
        candidate: ActionCandidate,
        shadow_evaluator: Optional[Callable[[Dict[str, Any], ActionCandidate], Tuple[bool, float, Dict[str, Any]]]] = None
    ) -> EpistemicRolloutResult:
        """Executes forward rollout inside isolated shadow state."""
        # 1. Check intrinsic ruin probability (The Absorbing Barrier Invariant)
        if candidate.ruin_probability > self.max_ruin_tolerance:
            return EpistemicRolloutResult(
                action_id=candidate.action_id,
                approved=False,
                ruin_detected=True,
                projected_log_growth=-math.inf,
                simulated_stress=candidate.stress_cost,
                shadow_state_snapshot=master_state,
                rejection_reason=f"ABSORBING BARRIER VIOLATION: Candidate action has non-zero ruin probability P(ruin) = {candidate.ruin_probability:.4f} > 0.0"
            )

        # 2. Compute time-average log growth rate: g = ln(1 + r)
        effective_factor = 1.0 + candidate.expected_yield
        if effective_factor <= 0.0:
            log_growth = -math.inf
            ruin = True
        else:
            log_growth = float(math.log(effective_factor))
            ruin = False

        if ruin:
            return EpistemicRolloutResult(
                action_id=candidate.action_id,
                approved=False,
                ruin_detected=True,
                projected_log_growth=-math.inf,
                simulated_stress=candidate.stress_cost,
                shadow_state_snapshot=master_state,
                rejection_reason="TERMINAL VALUE ABSORPTION: Multiplicative factor <= 0."
            )

        # 3. If dynamic shadow evaluator is provided, run closed-loop forward simulation
        shadow_state = dict(master_state)
        if shadow_evaluator:
            passed_sim, sim_stress, next_shadow = shadow_evaluator(shadow_state, candidate)
            if not passed_sim:
                return EpistemicRolloutResult(
                    action_id=candidate.action_id,
                    approved=False,
                    ruin_detected=True,
                    projected_log_growth=log_growth,
                    simulated_stress=sim_stress,
                    shadow_state_snapshot=next_shadow,
                    rejection_reason="DYNAMIC SIMULATION BREACH: Shadow simulator triggered state constraint violation."
                )
            shadow_state = next_shadow
        else:
            sim_stress = candidate.stress_cost

        return EpistemicRolloutResult(
            action_id=candidate.action_id,
            approved=True,
            ruin_detected=False,
            projected_log_growth=log_growth,
            simulated_stress=sim_stress,
            shadow_state_snapshot=shadow_state,
            rejection_reason=None
        )

    def select_optimal_viable_policy(
        self,
        master_state: Dict[str, Any],
        candidates: List[ActionCandidate]
    ) -> Tuple[Optional[ActionCandidate], List[EpistemicRolloutResult]]:
        """Filters candidate actions through the absorbing barrier and maximizes log growth."""
        rollout_results = []
        viable_candidates: List[Tuple[float, ActionCandidate, EpistemicRolloutResult]] = []

        for cand in candidates:
            res = self.rollout_candidate(master_state, cand)
            rollout_results.append(res)
            if res.approved and not res.ruin_detected:
                # Score = log_growth - wear_penalty
                net_utility = res.projected_log_growth - 0.01 * res.simulated_stress + 0.05 * cand.epistemic_value
                viable_candidates.append((net_utility, cand, res))

        if not viable_candidates:
            return None, rollout_results

        # Select action maximizing time-average log-growth
        viable_candidates.sort(key=lambda x: x[0], reverse=True)
        best_candidate = viable_candidates[0][1]
        return best_candidate, rollout_results


# ============================================================================
# MODULE 4: SENSEMAKING RESET WATCHDOG ("DROP YOUR TOOLS")
# ============================================================================

class SensemakingResetWatchdog:
    """Counters cognitive lockup, normalcy bias, and tool fixation when assumptions fail.

    Computes Bayesian prediction error delta_t = |y_obs - y_pred|. If delta_t > tau_surprise,
    halts execution, flushes short-term scratchpads, and re-anchors planning strictly
    from ground-truth verified raw state.
    """

    def __init__(self, surprise_threshold: float = 1.5):
        self.surprise_threshold = surprise_threshold
        self.reset_count: int = 0
        self.last_surprise: float = 0.0

    def evaluate_prediction_error(
        self,
        observed_vector: np.ndarray,
        predicted_vector: np.ndarray
    ) -> Tuple[bool, float, str]:
        """Calculates prediction discrepancy ||y_obs - y_pred||_2."""
        diff = observed_vector - predicted_vector
        error = float(np.linalg.norm(diff))
        self.last_surprise = error

        if error >= self.surprise_threshold:
            return True, error, f"SENSEMAKING BREACH: Prediction error delta_t = {error:.4f} >= threshold {self.surprise_threshold:.4f}."
        return False, error, f"SENSEMAKING NOMINAL: Prediction error delta_t = {error:.4f} < threshold {self.surprise_threshold:.4f}."

    def execute_drop_your_tools(
        self,
        context: Dict[str, Any],
        grounded_facts: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Flushes obsolete tools, stale intermediate plans, and speculative tokens.

        Preserves immutable task contract and grounded facts.
        """
        self.reset_count += 1
        return {
            "task_contract": context.get("task_contract") or context.get("goal") or "PRESERVED_TASK_CONTRACT",
            "grounded_facts": grounded_facts,
            "purged_monologue_count": len(context.get("scratchpad", "")),
            "drop_your_tools_epoch": self.reset_count,
            "status": "RE_ANCHORED_FROM_FIRST_PRINCIPLES",
            "timestamp": time.time()
        }


# ============================================================================
# UNIFIED OUTLIER-ENGINEERED DECISION CORE
# ============================================================================

class OutlierEngineeredDecisionCore:
    """Master Decision Core coordinating all 4 modules under Ergodic Log-Growth."""

    def __init__(
        self,
        token_ceiling: float = 0.85,
        validity_threshold: float = 0.70,
        surprise_threshold: float = 1.5
    ):
        self.triage = SomaticAttentionalTriage(token_ceiling=token_ceiling)
        self.heuristics = RecognitionPrimedGenerator(validity_threshold=validity_threshold)
        self.sandbox = EpistemicDecouplingSandbox(max_ruin_tolerance=0.0)
        self.watchdog = SensemakingResetWatchdog(surprise_threshold=surprise_threshold)
        self.master_state: Dict[str, Any] = {}
        self.total_decisions_made: int = 0
        self.total_ruins_averted: int = 0

    def decide(
        self,
        triage_metrics: TriageMetrics,
        candidate_actions: List[ActionCandidate],
        observed_sensory: Optional[np.ndarray] = None,
        predicted_sensory: Optional[np.ndarray] = None,
        grounded_facts: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Unified decision pipeline enforcing all outlier performance invariants."""
        self.total_decisions_made += 1

        # Step 1: Somatic Attentional Triage
        can_act, triage_reason, priority_level = self.triage.audit_triage(triage_metrics)
        if not can_act:
            return {
                "decision": "GATED",
                "selected_action": None,
                "reason": triage_reason,
                "priority_level": priority_level,
                "ruin_averted": False
            }

        # Step 2: Sensemaking Reset Check ("Drop Your Tools")
        if observed_sensory is not None and predicted_sensory is not None:
            reset_needed, error_val, reason = self.watchdog.evaluate_prediction_error(
                observed_sensory, predicted_sensory
            )
            if reset_needed:
                clean_context = self.watchdog.execute_drop_your_tools(
                    self.master_state, grounded_facts or {}
                )
                self.master_state = clean_context
                return {
                    "decision": "SENSEMAKING_RESET",
                    "selected_action": None,
                    "reason": reason,
                    "clean_context": clean_context,
                    "ruin_averted": True
                }

        # Step 3: Epistemic Decoupling Sandbox & Absorbing Barrier Invariant
        best_candidate, rollouts = self.sandbox.select_optimal_viable_policy(
            self.master_state, candidate_actions
        )

        ruin_attempts = [r for r in rollouts if r.ruin_detected]
        self.total_ruins_averted += len(ruin_attempts)

        if not best_candidate:
            return {
                "decision": "NO_VIABLE_ACTION",
                "selected_action": None,
                "reason": "All candidate actions violated the Absorbing Barrier Invariant (P(ruin) > 0).",
                "rollouts": [r.model_dump() for r in rollouts],
                "ruins_averted": len(ruin_attempts)
            }

        # Step 4: Commit Approved Safe Action to Master State
        self.master_state[f"decision_{self.total_decisions_made}"] = best_candidate.action_id

        return {
            "decision": "COMMITTED",
            "selected_action": best_candidate.model_dump(),
            "reason": "Action cleared Epistemic Decoupling Sandbox with P(ruin) = 0 and positive time-average log-growth.",
            "projected_log_growth": math.log(1.0 + best_candidate.expected_yield),
            "ruins_averted": len(ruin_attempts),
            "rollouts": [r.model_dump() for r in rollouts]
        }

    @property
    def epistemic_sandbox(self) -> EpistemicDecouplingSandbox:
        return self.sandbox

    def evaluate_and_decide(
        self,
        candidate_actions: List[ActionCandidate],
        triage_metrics: Optional[TriageMetrics] = None
    ) -> Tuple[Optional[ActionCandidate], List[EpistemicRolloutResult]]:
        """Convenience method directly selecting optimal viable policy through epistemic sandboxing."""
        metrics = triage_metrics or TriageMetrics()
        can_act, reason, _ = self.triage.audit_triage(metrics)
        if not can_act:
            return None, []

        best_candidate, rollouts = self.sandbox.select_optimal_viable_policy(
            self.master_state, candidate_actions
        )
        self.total_decisions_made += 1
        ruin_attempts = [r for r in rollouts if r.ruin_detected]
        self.total_ruins_averted += len(ruin_attempts)

        if best_candidate:
            self.master_state[f"decision_{self.total_decisions_made}"] = best_candidate.action_id

        return best_candidate, rollouts

    def get_telemetry(self) -> Dict[str, Any]:
        """Returns decision core operational metrics."""
        return {
            "total_decisions_made": self.total_decisions_made,
            "total_ruins_averted": self.total_ruins_averted,
            "gated_events_count": self.triage.gated_events_count,
            "drop_your_tools_resets": self.watchdog.reset_count,
            "master_state_keys": list(self.master_state.keys())
        }

