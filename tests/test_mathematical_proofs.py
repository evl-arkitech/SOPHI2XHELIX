"""Tests verifying the Mathematical Proof of Concept for Base Rungs and ANAT."""

import numpy as np
from doublehelix.proofs.invariants import MathematicalProofOfConcept


def test_prove_level_1_timing_and_zero_alloc():
    # Pass case: frame time 12ms <= 16.6ms, 0 heap allocs
    passed, proof = MathematicalProofOfConcept.prove_level_1_timing_and_zero_alloc(
        measured_frame_time_ms=12.4,
        heap_blocks_allocated=0
    )
    assert passed is True
    assert "THEOREM PROVEN" in proof

    # Fail case: frame time 19ms
    passed, proof = MathematicalProofOfConcept.prove_level_1_timing_and_zero_alloc(
        measured_frame_time_ms=19.2,
        heap_blocks_allocated=0
    )
    assert passed is False
    assert "PROOF REFUTED" in proof


def test_prove_level_2_swept_ccd_kinematics():
    p0 = np.array([50.0, 50.0], dtype=np.float32)
    v = np.array([1200.0, 0.0], dtype=np.float32)  # fast velocity towards wall
    radius = 5.0
    bounds = (0.0, 100.0, 0.0, 100.0)
    dt = 1.0 / 60.0

    proven, toi, proof = MathematicalProofOfConcept.prove_level_2_swept_ccd_kinematics(
        p0=p0, v=v, radius=radius, obstacle_bounds=bounds, dt=dt
    )
    assert proven is True
    assert 0.0 <= toi <= 1.0
    assert "P(Tunneling) = 0.0" in proof


def test_prove_level_3_perceptual_boundedness():
    framebuffer = np.ones((100, 100, 3), dtype=np.float32) * 0.5
    bounded, proof = MathematicalProofOfConcept.prove_level_3_perceptual_boundedness(framebuffer)
    assert bounded is True
    assert "PROVEN BOUNDED" in proof

    # Inject NaN
    framebuffer[50, 50, 0] = np.nan
    bounded, proof = MathematicalProofOfConcept.prove_level_3_perceptual_boundedness(framebuffer)
    assert bounded is False
    assert "DIVERGENCE DETECTED" in proof


def test_prove_level_4_ergodic_reachability():
    passed, proof = MathematicalProofOfConcept.prove_level_4_ergodic_reachability(
        visited_states_count=50,
        total_possible_states=50,
        ticks_simulated=1000,
        crashes_observed=0
    )
    assert passed is True
    assert "Convergence Proven: True" in proof


def test_prove_anat_hopfield_cccp_energy():
    e_initial = 12.5
    e_final = 10.1
    decreased, proof = MathematicalProofOfConcept.prove_anat_hopfield_cccp_energy_decrease(e_initial, e_final)
    assert decreased is True
    assert "Monotonic Convergence Proven: True" in proof


def test_prove_anat_rome_rank_one_identity():
    W = np.eye(32, dtype=np.float32)
    k = np.random.randn(32).astype(np.float32)
    v = np.random.randn(32).astype(np.float32)

    diff = v - (W @ k)
    delta_W = np.outer(diff, k) / (np.dot(k, k) + 1e-6)

    exact, residual, proof = MathematicalProofOfConcept.prove_anat_rome_rank_one_identity(
        W_original=W, delta_W=delta_W, key_k=k, target_v=v
    )
    assert exact is True
    assert residual < 1e-4
    assert "Algebraic Identity Proven: True" in proof


def test_prove_theorem_1_windkessel_variance_attenuation():
    passed, H_sq, proof = MathematicalProofOfConcept.prove_theorem_1_windkessel_variance_attenuation(
        C_r=2.0, R_r=0.5, omega=10.0, sigma_a=2.0, lambda_bar=10.0, delta=1e-4
    )
    assert passed is True
    assert H_sq < 1.0
    assert "Zero Buffer Overflow Bound Proven: True" in proof


def test_prove_theorem_2_nirodha_bounded_divergence():
    passed, epsilon_Tr, proof = MathematicalProofOfConcept.prove_theorem_2_nirodha_bounded_divergence(
        A_spectral_norm=1.2, T_r=8, sigma_y_sq=1.0, sigma_m_sq=1.0
    )
    assert passed is True
    assert epsilon_Tr > 0.0
    assert "Bounded Posterior Convergence Proven: True" in proof


def test_prove_theorem_3_laplacian_consensus_and_causal_annihilation():
    # Connected 3-agent cycle -> consensus proven
    passed, rate, proof = MathematicalProofOfConcept.prove_theorem_3_laplacian_consensus_and_causal_annihilation(
        gamma=0.5
    )
    assert passed is True
    assert rate > 0.5
    assert "Causal Consensus Proven: True" in proof

    # Disconnected (uncoupled) 3-agent graph -> consensus rejected (DAT illusion disproven)
    uncoupled_adj = np.zeros((3, 3), dtype=np.float64)
    passed_uncoupled, _, proof_uncoupled = MathematicalProofOfConcept.prove_theorem_3_laplacian_consensus_and_causal_annihilation(
        adjacency_matrix=uncoupled_adj, gamma=0.5
    )
    assert passed_uncoupled is False
    assert "Causal Consensus Proven: False" in proof_uncoupled


def test_prove_theorem_4_non_ergodic_ruin_prevention():
    passed, metrics, proof = MathematicalProofOfConcept.prove_theorem_4_non_ergodic_ruin_prevention(
        n_steps=150, n_trajectories=100
    )
    assert passed is True
    assert metrics["naive_ruin_rate"] >= 0.95
    assert metrics["ergodic_ruin_rate"] == 0.0
    assert metrics["g_ergodic"] > 0.0
    assert "Non-Ergodic Superiority Proven: True" in proof


def test_prove_theorem_5_cellular_sheaf_cohomology_nullification():
    passed, lambda_2, proof = MathematicalProofOfConcept.prove_theorem_5_cellular_sheaf_cohomology_nullification(
        n_agents=3, stalk_dim=2, timesteps=30
    )
    assert passed is True
    assert lambda_2 > 0.0
    assert "Cohomological Discord Nullification Proven: True" in proof


def test_prove_theorem_6_linear_session_deadlock_freedom_and_confluence():
    passed, metrics, proof = MathematicalProofOfConcept.prove_theorem_6_linear_session_deadlock_freedom_and_confluence(
        n_interactions=15
    )
    assert passed is True
    assert metrics["deadlocks_detected"] == 0
    assert metrics["confluence_violations"] == 0
    assert metrics["total_tokens_leaked"] == 0
    assert "Classical Linear Logic Session Protocol Proven: True" in proof


