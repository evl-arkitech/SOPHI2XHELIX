"""City Echoes to ANAT Explorable World Graph Bridge.

Binds tactical survival events to biological/synthetic cognitive trajectories:
- Acoustic Debris Crunch -> Sector PR (Perceptual Sensory Cortex)
- 12-Gauge Slug Drywall Breach -> Node N09 (Surprise Metric & Episodic Encoding)
- Respiratory Hold-Breath Gating -> Node N02 (Gating & Working Memory)
- House Hallway Topography -> Node N07 (Explorable World Graph Retrieval)
- Tactical Posture Mutation -> Node N14 (Targeted ROME Rank-One Surgery)
"""

from typing import Dict, Any, List, Optional
import numpy as np
from doublehelix.anat.world_graph import ExplorableWorldGraph
from doublehelix.anat.trajectories import TrajectoryController


class CityEchoesANATBridge:
    """Synchronizes tactical gameplay events with ANAT Explorable World Graph."""

    def __init__(self, graph: Optional[ExplorableWorldGraph] = None):
        self.graph = graph or ExplorableWorldGraph()
        self.controller = TrajectoryController(self.graph)
        self.cognitive_history: List[Dict[str, Any]] = []

    def dispatch_acoustic_event(self, sound_db: float, source_type: str) -> Dict[str, Any]:
        """Maps acoustic detection to ANAT Perceptual Cortex & Working Memory."""
        input_vec = np.ones(64, dtype=np.float32) * (sound_db / 100.0)
        result = self.controller.run_trajectory_a(input_vec, salience_threshold=0.3)
        entry = {
            "tactical_event": "ACOUSTIC_DETECTION",
            "source_type": source_type,
            "sound_db": sound_db,
            "anat_trajectory": "TRAJECTORY_A",
            "nodes_activated": result["route"],
            "status": result["status"]
        }
        self.cognitive_history.append(entry)
        return entry

    def dispatch_wall_breach(self, slug_velocity: float, spall_chunks: int) -> Dict[str, Any]:
        """12-Gauge slug breach induces high surprise metric, triggering Trajectory B."""
        surprise_val = min(1.0, slug_velocity / 500.0)
        context_vec = np.ones(64, dtype=np.float32) * float(spall_chunks)
        result = self.controller.run_trajectory_b(context_vec, surprise_magnitude=surprise_val)
        entry = {
            "tactical_event": "BALLISTIC_BREACH_SURPRISE",
            "slug_velocity": slug_velocity,
            "surprise_score": surprise_val,
            "anat_trajectory": "TRAJECTORY_B",
            "nodes_activated": result["route"],
            "encoded": True
        }
        self.cognitive_history.append(entry)
        return entry

    def dispatch_hallway_query(self, query_loc: str) -> Dict[str, Any]:
        """Retrieves spatial topology of colonial house via Modern Hopfield CCCP Trajectory C."""
        cue_vec = np.ones(64, dtype=np.float32) * 0.5
        result = self.controller.run_trajectory_c(cue_vec)
        entry = {
            "tactical_event": "TOPOLOGY_RETRIEVAL",
            "query": query_loc,
            "anat_trajectory": "TRAJECTORY_C",
            "nodes_activated": result["route"],
            "final_energy": result["final_energy"]
        }
        self.cognitive_history.append(entry)
        return entry
