"""Tests for Neurocomputational Elasticity, Contemplative Dynamics & Causal Runtime.

Validates the implementation of principles in runtime/NeuroCompElasticity.md:
1. Elastic Runtime Windkessel (Somatic compliance C_r, resistance R_r, low-pass attenuation, zero overflow).
2. Active Inference Nirodha Engine (Precision reweighting, free energy surrogate E_t, context pruning).
3. Gamma-Band Phase Synchrony (Kuramoto order parameter R(t), decentralized sub-agent binding).
4. Causal Laplacian Swarm Consensus (Algebraic connectivity lambda_2(L) > 0, DAT illusion disproven).
"""

import pytest
import math
import numpy as np
from typing import Dict, Any

from doublehelix.runtime.elasticity import (
    WindkesselConfig,
    ElasticRuntimeWindkessel,
    NirodhaResetConfig,
    ActiveInferenceNirodhaEngine,
    GammaPhaseSynchronizer,
    CausalLaplacianConsensus,
)


def test_elastic_runtime_windkessel_attenuation_and_sizing():
    config = WindkesselConfig(
        compliance=3.0,
        resistance=0.4,
        target_lambda_bar=15.0,
        sigma_a=2.5,
        delta_overflow_tolerance=1e-4
    )
    windkessel = ElasticRuntimeWindkessel(config)

    # Relaxation time tau_r = R_r * C_r = 1.2
    assert abs(windkessel.tau_r - 1.2) < 1e-5

    # Attenuation check: at high frequency w = 20 rad/s, |H(w)|^2 must be strongly attenuated
    H_sq_low = windkessel.power_spectral_amplification(omega=1.0)
    H_sq_high = windkessel.power_spectral_amplification(omega=20.0)
    assert H_sq_low < 1.0
    assert H_sq_high < 0.01  # Strong high-frequency suppression
    assert H_sq_high < H_sq_low

    # Optimal Q_max sizing
    assert windkessel.Q_max > config.target_lambda_bar * windkessel.tau_r


def test_elastic_runtime_windkessel_ingest_and_drain():
    windkessel = ElasticRuntimeWindkessel(WindkesselConfig(compliance=2.0, resistance=0.5))

    # Ingest a burst of tasks
    for i in range(10):
        accepted = windkessel.ingest({"task_id": f"task_{i}", "payload": f"data_{i}"}, weight=1.0)
        assert accepted is True

    metrics_before = windkessel.get_metrics()
    assert metrics_before["queue_occupancy"] == 10.0
    assert metrics_before["somatic_pressure"] == 5.0  # 10 / 2.0

    # Drain through resistance
    drained = windkessel.drain(dt=0.5)
    assert len(drained) > 0
    assert windkessel._total_drained == len(drained)

    metrics_after = windkessel.get_metrics()
    assert metrics_after["queue_occupancy"] < 10.0


def test_nirodha_engine_free_energy_and_cessation():
    engine = ActiveInferenceNirodhaEngine(NirodhaResetConfig(theta_reset=3.0, scheduled_reset_period_T_r=5))

    # 1. Low divergence: no cessation triggered
    internal_mu = np.array([1.0, 1.0])
    grounded_y = np.array([1.1, 0.9])
    energy = engine.compute_free_energy_surrogate(internal_mu, grounded_y)
    assert energy < 1.0

    triggered, reason = engine.evaluate_cessation_trigger(energy)
    assert triggered is False

    # 2. High divergence E_t >= theta_reset: triggers Nirodha Cessation
    divergent_mu = np.array([5.0, 5.0])
    high_energy = engine.compute_free_energy_surrogate(divergent_mu, grounded_y)
    assert high_energy >= 3.0

    triggered, reason = engine.evaluate_cessation_trigger(high_energy)
    assert triggered is True
    assert "Free energy surrogate" in reason

    # 3. Context Pruning execution
    contaminated_context = {
        "goal": "Reach 60 FPS deterministic convergence",
        "scratchpad": "Recursive self-talk that was hallucinating incorrect invariants...",
        "monologue_trace": ["thought 1", "thought 2", "thought 3"],
        "grounded_state": {"avg_frame_time_ms": 11.2, "allocations_in_loop": 0}
    }
    pruned = engine.execute_nirodha_reset(contaminated_context)
    assert pruned["intermediate_monologue_purged"] is True
    assert "scratchpad" not in pruned
    assert "monologue_trace" not in pruned
    assert pruned["task_contract"] == "Reach 60 FPS deterministic convergence"
    assert pruned["grounded_state"]["allocations_in_loop"] == 0

    # Theoretical compact KL divergence bound
    kl_bound = engine.calculate_kl_divergence_bound(A_spectral_norm=1.1)
    assert math.isfinite(kl_bound)
    assert kl_bound > 0.0


def test_gamma_phase_synchronizer_coherence():
    sync = GammaPhaseSynchronizer(target_frequency_hz=40.0)

    # Register 3 sub-agents
    sync.register_subagent("agent_alpha", initial_phase=0.0)
    sync.register_subagent("agent_beta", initial_phase=0.0)
    sync.register_subagent("agent_auditor", initial_phase=0.0)

    # Complete coherence (all phases aligned at 0.0)
    coherence = sync.compute_phase_coherence()
    assert abs(coherence - 1.0) < 1e-4
    assert sync.is_synchronized(coherence_threshold=0.85) is True

    # Perturb agent_beta phase out of sync
    sync.update_phase("agent_beta", delta_phase=math.pi)
    coherence_perturbed = sync.compute_phase_coherence()
    assert coherence_perturbed < 0.6
    assert sync.is_synchronized(coherence_threshold=0.85) is False


def test_causal_laplacian_consensus_and_dat_annihilation():
    # 1. Strongly connected 4-agent tournament graph
    adj_connected = np.array([
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0, 0.0]
    ], dtype=np.float64)

    res_connected = CausalLaplacianConsensus.verify_consensus_viability(adj_connected, task_coupling_gamma=0.5)
    assert res_connected["causally_connected"] is True
    assert res_connected["consensus_certified"] is True
    assert res_connected["algebraic_connectivity_lambda_2"] > 0.0
    assert res_connected["exponential_convergence_rate"] > 0.5

    # 2. Disconnected / uncoupled agents (2 disjoint pairs)
    adj_disconnected = np.array([
        [0.0, 1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
        [0.0, 0.0, 1.0, 0.0]
    ], dtype=np.float64)

    res_disconnected = CausalLaplacianConsensus.verify_consensus_viability(adj_disconnected, task_coupling_gamma=0.5)
    assert res_disconnected["causally_connected"] is False
    assert res_disconnected["consensus_certified"] is False

    # 3. DAT Spurious Correlation Bound calculation
    # Evaluates expected maximum spurious correlation across K=1000 retrospective windows
    dat_bound = CausalLaplacianConsensus.evaluate_dat_spurious_correlation_bound(num_windows_K=1000, sample_length_M=500)
    assert 0.0 < dat_bound < 0.5
