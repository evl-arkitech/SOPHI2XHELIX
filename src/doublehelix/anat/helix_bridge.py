"""Integration bridge connecting ANAT Explorable World Graph and Hermes 3 into the Double Helix Engine.

Coordinates cognitive memory routing between:
- Strand Alpha (Synthesis Helix): Pattern completion (Trajectory C), Hermes cognitive deliberation, and targeted code surgery (Trajectory E).
- Strand Beta (Empirical Helix): Surprise encoding (Trajectory B) and tripartite consolidation (Trajectory D).
"""

import logging
from typing import Dict, Any, Optional, List, Tuple
import numpy as np

from doublehelix.anat.world_graph import ExplorableWorldGraph
from doublehelix.anat.trajectories import TrajectoryController
from doublehelix.state import HelixState

logger = logging.getLogger("ANATHelixBridge")


class ANATHelixBridge:
    """Binds the ANAT Explorable World Graph and Hermes 3 into the Double Helix Orchestration loop."""

    def __init__(self, memory_dir: Optional[str] = None, hermes_client: Optional[Any] = None):
        self.world_graph = ExplorableWorldGraph(memory_dir=memory_dir)
        self.trajectory_controller = TrajectoryController(self.world_graph)
        self.hermes_client = hermes_client
        self.milestone_triples: List[Tuple[str, str, str]] = []
        self.cognitive_telemetry_history: List[Dict[str, Any]] = []

    def __repr__(self) -> str:
        return (
            f"<ANATHelixBridge nodes={len(self.world_graph.nodes)} "
            f"edges={len(self.world_graph.edges)} "
            f"milestones={len(self.milestone_triples)} "
            f"hermes={'active' if self.hermes_client else 'none'}>"
        )

    def route_strand_alpha_synthesis(self, tier: str, partial_spec: str) -> Dict[str, Any]:
        """Strand Alpha: Trajectory C (Associative Pattern Completion) retrieves architecture invariants."""
        # Convert spec string to normalized embedding vector
        hash_val = abs(hash(partial_spec))
        rng = np.random.RandomState(hash_val % 10000)
        cue = rng.randn(64).astype(np.float32)
        cue /= (np.linalg.norm(cue) + 1e-6)

        traj_c_res = self.trajectory_controller.run_trajectory_c(partial_cue=cue)

        # Hermes cognitive deliberation if available
        hermes_deliberation = ""
        hermes_scratchpad = ""
        if self.hermes_client:
            try:
                prompt = f"Deliberate on Double Helix Strand Alpha invariants for tier '{tier}': {partial_spec}"
                hermes_msg, _, scratchpad = self.hermes_client.chat(
                    [{"role": "user", "content": prompt}],
                    temperature=0.1
                )
                hermes_deliberation = hermes_msg.get("content", "")
                hermes_scratchpad = scratchpad
            except Exception as e:
                logger.debug("Hermes client deliberation unavailable during Strand Alpha routing: %s", e)

        res = {
            "tier": tier,
            "memory_graph_trajectory": traj_c_res["trajectory"],
            "hopfield_energy": traj_c_res["final_energy"],
            "cross_attention_similarity": traj_c_res["similarity"],
            "graph_diffused_nodes": traj_c_res["diffusion_nodes_activated"],
            "hermes_deliberation": hermes_deliberation
        }
        self.cognitive_telemetry_history.append({"phase": "STRAND_ALPHA_SYNTHESIS", **res})
        return res

    def route_strand_beta_telemetry(self, tier: str, telemetry: Dict[str, Any]) -> Dict[str, Any]:
        """Strand Beta: Injects empirical telemetry breaches into N09_SURPRISE and N08_TITANS (Trajectory B)."""
        # Calculate empirical prediction error / surprise scalar
        frame_time = telemetry.get("avg_frame_time_ms", 0.0)
        allocs = telemetry.get("allocations_in_loop", 0)
        tunneling = telemetry.get("tunneling_errors", 0)
        crashes = telemetry.get("headless_bot_crashes", 0)

        # Surprise magnitude S_t = loss gradient norm
        surprise = 0.0
        if frame_time > 16.6:
            surprise += (frame_time - 16.6) / 16.6
        if allocs > 0:
            surprise += allocs * 1.5
        if tunneling > 0:
            surprise += tunneling * 2.0
        if crashes > 0:
            surprise += crashes * 5.0

        context_vector = np.array([frame_time, float(allocs), float(tunneling), float(crashes)] + [0.0] * 60, dtype=np.float32)
        traj_b_res = self.trajectory_controller.run_trajectory_b(context_vector, surprise_magnitude=surprise)

        res = {
            "tier": tier,
            "surprise_scalar": surprise,
            "titans_gradient_norm": traj_b_res["titans_gradient_norm"],
            "attractor_basins": traj_b_res["attractor_basins_count"]
        }
        self.cognitive_telemetry_history.append({"phase": "STRAND_BETA_TELEMETRY", **res})
        return res

    def apply_remediation_surgery(self, failed_tier: str, root_cause: str) -> Dict[str, Any]:
        """Trajectory E: Error-Induced Destabilization (N13_DESTAB) + ROME Rank-One Surgery (N14_SURGERY)."""
        key_vec = np.zeros(64, dtype=np.float32)
        key_vec[0] = 1.0  # target failure vector key
        target_v = np.zeros(64, dtype=np.float32)
        target_v[0] = 0.0  # target zeroed error

        traj_e_res = self.trajectory_controller.run_trajectory_e(key_vec, target_v)

        # Hermes diagnostic synthesis if available
        remediation_patch = ""
        if self.hermes_client:
            try:
                diag_prompt = f"Diagnose parity failure at {failed_tier}: {root_cause}. Synthesize zero-alloc fix."
                msg, _, _ = self.hermes_client.chat([{"role": "user", "content": diag_prompt}], temperature=0.1)
                remediation_patch = msg.get("content", "")
            except Exception as e:
                logger.debug("Hermes diagnostic synthesis skipped: %s", e)

        return {
            "tier": failed_tier,
            "surgery_verified": traj_e_res["rank_one_identity_verified"],
            "reconstruction_error": traj_e_res["reconstruction_error"],
            "delta_W_norm": traj_e_res["delta_W_norm"],
            "remediation_patch": remediation_patch
        }

    def consolidate_tier_ascension(self, tier: str = "CONVERGED") -> Dict[str, Any]:
        """Trajectory D: Offline Tripartite Consolidation upon passing Base Rungs."""
        res = self.trajectory_controller.run_trajectory_d(lambda_reg=0.25)
        self.milestone_triples.append((tier, "BASE_RUNG_STATUS", "VERIFIED_PASSED"))
        self.milestone_triples.append((tier, "ASCENDED_BY", "DoubleHelix-ANAT-Hermes"))
        return {
            "tier": tier,
            "consolidation": res,
            "milestone_triples": list(self.milestone_triples)
        }
