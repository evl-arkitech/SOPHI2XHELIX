"""Tests for ANAT Explorable World Graph, Primitives, and Trajectories."""

import os
import numpy as np
from doublehelix.anat.world_graph import ExplorableWorldGraph
from doublehelix.anat.primitives import GraphNavigator
from doublehelix.anat.trajectories import TrajectoryController
from doublehelix.anat.helix_bridge import ANATHelixBridge


def test_explorable_world_graph_loading():
    graph = ExplorableWorldGraph()
    # Check vertices and edges loaded from CSV
    assert len(graph.nodes) >= 14
    assert "N01_SCRATCH" in graph.nodes
    assert "N05_ATTRACT" in graph.nodes
    assert "N10_PARAM" in graph.nodes
    assert len(graph.edges) >= 18

    # Verify sector assignments
    assert graph.nodes["N01_SCRATCH"].sector.value == "EX"
    assert graph.nodes["N05_ATTRACT"].sector.value == "EP"
    assert graph.nodes["N08_TITANS"].sector.value == "TT"
    assert graph.nodes["N10_PARAM"].sector.value == "PR"
    assert graph.nodes["N13_DESTAB"].sector.value == "ED"


def test_graph_navigation_primitives():
    graph = ExplorableWorldGraph()
    nav = GraphNavigator(graph)

    # OBSERVE
    obs = nav.observe("N01_SCRATCH")
    assert obs["node_id"] == "N01_SCRATCH"
    assert "E01" in obs["outgoing_edges"]

    # GATING_CHECK
    assert nav.gating_check("N02_GATE", 0.9, threshold=0.5) is True
    assert nav.gating_check("N02_GATE", 0.2, threshold=0.5) is False

    # HOP
    nav.active_memory_tensors["N01_SCRATCH"] = np.ones(10, dtype=np.float32)
    next_node = nav.hop("N01_SCRATCH", "E01")
    assert next_node == "N02_GATE"
    assert "N02_GATE" in nav.active_memory_tensors

    # DIFFUSE (Personalized PageRank)
    probs = nav.diffuse(query_indices=[0], alpha=0.85, steps=10)
    assert len(probs) == len(graph.nodes)
    assert abs(np.sum(probs) - 1.0) < 1e-4  # Probability distribution sums to 1.0

    # SETTLE_ENERGY (Modern Hopfield CCCP)
    stored = np.random.randn(16, 4).astype(np.float32)
    query = np.random.randn(16).astype(np.float32)
    settled, energy = nav.settle_energy(stored, query, beta=1.0)
    assert settled.shape == (16,)
    assert isinstance(energy, float)

    # DESTABILIZE & ENOUGH
    assert nav.destabilize("N10_PARAM") is True
    assert nav.enough(0.85, threshold=0.8) is True


def test_anat_five_trajectories():
    graph = ExplorableWorldGraph()
    ctrl = TrajectoryController(graph)

    # Trajectory A
    res_a = ctrl.run_trajectory_a(input_vector=np.ones(64, dtype=np.float32) * 2.0)
    assert res_a["trajectory"] == "TRAJECTORY_A"
    assert "N01_SCRATCH" in res_a["route"]

    # Trajectory B
    res_b = ctrl.run_trajectory_b(context_vector=np.ones(64, dtype=np.float32), surprise_magnitude=1.5)
    assert res_b["trajectory"] == "TRAJECTORY_B"
    assert res_b["surprise_magnitude"] == 1.5

    # Trajectory C
    res_c = ctrl.run_trajectory_c(partial_cue=np.ones(64, dtype=np.float32))
    assert res_c["trajectory"] == "TRAJECTORY_C"
    assert "N05_ATTRACT" in res_c["route"]

    # Trajectory D
    res_d = ctrl.run_trajectory_d(lambda_reg=0.5)
    assert res_d["trajectory"] == "TRAJECTORY_D"
    assert "N11_TRIPLE" in res_d["route"]

    # Trajectory E
    key_k = np.ones(64, dtype=np.float32)
    target_v = np.ones(64, dtype=np.float32) * 5.0
    res_e = ctrl.run_trajectory_e(key_k, target_v)
    assert res_e["trajectory"] == "TRAJECTORY_E"
    assert res_e["rank_one_identity_verified"] is True


def test_anat_helix_bridge_integration():
    bridge = ANATHelixBridge()

    # Route Strand Alpha
    alpha_res = bridge.route_strand_alpha_synthesis("LEVEL_2_ECS", "Design Continuous Collision Detection")
    assert alpha_res["memory_graph_trajectory"] == "TRAJECTORY_C"
    assert "hopfield_energy" in alpha_res

    # Route Strand Beta
    beta_res = bridge.route_strand_beta_telemetry("LEVEL_1_KERNEL", {"avg_frame_time_ms": 18.0, "allocations_in_loop": 1})
    assert beta_res["surprise_scalar"] > 0.0

    # Remediation surgery
    surgery_res = bridge.apply_remediation_surgery("LEVEL_1_KERNEL", "Eliminate dynamic heap allocations")
    assert surgery_res["surgery_verified"] is True
