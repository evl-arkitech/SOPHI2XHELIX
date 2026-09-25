"""Unit and integration tests for SOPHI-Runtime: Poincare Incubator, Cellular Sheaf, Tesla Optics, CLL Session Channels."""

import math
import numpy as np
import pytest
from doublehelix.runtime.sheaf_sophi import (
    PoincareDifferentialIncubator,
    DifferenceRecord,
    SubliminalHypothesis,
    GrothendieckCellularSheaf,
    TeslaMonoidalOptic,
    LinearSessionChannel,
    LinearSessionEndpoint,
)


def test_poincare_differential_incubator_sieve_and_epiphany():
    incubator = PoincareDifferentialIncubator(alpha=0.05, beta=1.0, theta_sieve=5.0)

    # Ingest difference records
    rec = incubator.ingest_difference({"spatial_delta": [0.5, 0.2]}, epistemic_entropy=0.8)
    assert rec.record_id.startswith("diff_")
    assert len(incubator.records_buffer) == 1

    # Seed an inelegant hypothesis (high Kolmogorov, low log-likelihood)
    h_poor = incubator.seed_hypothesis("hyp_poor", "verbose_brute_force", kolmogorov_proxy=200.0, log_likelihood=1.0)
    assert h_poor.conscious_epiphany is False
    assert h_poor.aesthetic_score > incubator.theta_sieve

    # Seed an elegant hypothesis (low Kolmogorov, high log-likelihood)
    h_elegant = incubator.seed_hypothesis("hyp_elegant", "compact_harmonic_law", kolmogorov_proxy=20.0, log_likelihood=10.0)
    # Score = 0.05 * 20.0 - 1.0 * 10.0 = 1.0 - 10.0 = -9.0 <= 5.0 -> epiphany immediately
    assert h_elegant.conscious_epiphany is True
    assert len(incubator.epiphany_history) >= 1

    # Run incubation step on poor hypothesis after boosting its resonance
    h_poor.resonance = 1.8
    h_poor.log_likelihood = 8.0
    epiphanies = incubator.incubate_step(dt=0.1)
    assert isinstance(epiphanies, list)


def test_grothendieck_cellular_sheaf_cohomology():
    # 3-node triangular cell complex
    nodes = ["alpha", "beta", "gamma"]
    sheaf = GrothendieckCellularSheaf(node_ids=nodes, stalk_dim=2)

    # Add cycle edges with identity and rotation restriction maps
    sheaf.add_edge("alpha", "beta", "e_ab")
    sheaf.add_edge("beta", "gamma", "e_bg")
    sheaf.add_edge("gamma", "alpha", "e_ga")

    # Verify coboundary matrix delta^0
    delta0 = sheaf.build_coboundary_matrix()
    assert delta0.shape == (6, 6)

    # Verify Sheaf Laplacian L_F = (delta^0)^T delta^0
    L_F = sheaf.build_sheaf_laplacian()
    assert L_F.shape == (6, 6)
    assert np.allclose(L_F, L_F.T)  # Exactly symmetric
    eigs = np.linalg.eigvalsh(L_F)
    assert np.all(eigs >= -1e-8)   # Positive semi-definite

    # Spectral analysis
    spec = sheaf.spectral_analysis()
    assert spec["harmonic_dimension_h0"] == 2  # Identity restriction on cycle has 2D consensus
    assert spec["spectral_gap_lambda2"] > 0.0

    # Dirichlet energy and gradient descent
    x0 = np.array([
        [10.0, -5.0],
        [0.0, 5.0],
        [-5.0, 0.0]
    ], dtype=np.float64)

    e0 = sheaf.dirichlet_energy(x0)
    assert e0 > 0.0

    # Dissipate discord over 20 steps
    x_curr = x0.copy()
    for _ in range(20):
        x_curr = sheaf.dissipate_discord_step(x_curr, eta=0.1)

    e_final = sheaf.dirichlet_energy(x_curr)
    assert e_final < e0 * 0.1  # Over 90% discord dissipated

    # Projection onto consensus kernel
    x_proj = sheaf.project_to_consensus(x0)
    e_proj = sheaf.dirichlet_energy(x_proj)
    assert np.isclose(e_proj, 0.0, atol=1e-6)


def test_tesla_monoidal_optic_mental_sandbox():
    optic = TeslaMonoidalOptic(
        name="ballistics_anticipator",
        initial_params={"gain": 1.2, "bias": 0.1, "damping": 0.05},
        wear_tolerance=50.0
    )

    nominal_state = {"vel_x": 5.0, "vel_y": 2.0}

    # Forward view
    projected = optic.view(nominal_state)
    assert "proj_vel_x" in projected
    assert "proj_vel_y" in projected

    # Backward update with synthetic stress feedback
    stress = {"vel_x": 2.0, "vel_y": 1.0}
    residual, cycle_stress = optic.update(nominal_state, stress)
    assert cycle_stress == 3.0
    assert optic.accumulated_mental_wear == 3.0
    assert optic.simulation_cycles == 1

    # Counterfactual burn-in run
    shocks = [{"vel_x": 4.0, "vel_y": 2.0}, {"vel_x": 3.0, "vel_y": 1.0}]
    burn_in_res = optic.run_mental_burn_in(nominal_state, shocks)
    assert burn_in_res["passed"] is True
    assert burn_in_res["cycles_completed"] == 2

    # Monoidal composition
    optic_b = TeslaMonoidalOptic(name="acoustic_anticipator", initial_params={"gain": 0.8})
    composed = optic.compose(optic_b)
    assert "ballistics_anticipator_x_acoustic_anticipator" in composed.name


def test_linear_session_channel_deadlock_free_confluence():
    channel = LinearSessionChannel(channel_id="ch_test_sophi")

    # Initial states
    assert channel.client.linear_tokens == 1
    assert channel.server.linear_tokens == 1

    # Execute cut-elimination transaction
    req = {"command": "SYNCHRONIZE_RUNG", "payload": [1, 2, 3]}

    def server_handler(request: dict) -> dict:
        return {"status": "SUCCESS", "echo_sum": sum(request["payload"])}

    response = channel.execute_transaction(req, server_handler)

    assert response["status"] == "SUCCESS"
    assert response["echo_sum"] == 6

    # Verify Classical Linear Logic linear exhaustion:
    # Both endpoints consumed (unit termination 1 / _|_), zero tokens leaked
    assert channel.client.linear_tokens == 0
    assert channel.server.linear_tokens == 0
    assert channel.client.active is False
    assert channel.server.active is False

    # Attempting to reuse terminated endpoint must raise linear violation
    with pytest.raises(RuntimeError, match="is terminated"):
        channel.client.send({"stale": True}, channel.server)
