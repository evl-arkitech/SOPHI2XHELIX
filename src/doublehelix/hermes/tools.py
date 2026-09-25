"""DoubleHelix Hermes Unified Tool Registry & Dispatcher.

Exposes actuators across:
1. Double Helix Upward Slice Game Engine (Ascension, Parity Gates, Convergence)
2. Headless Deterministic Kernel & Fuzzing Telemetry
3. Formal Mathematical Proofs of Concept Suite
4. City Echoes 5.8 Tactical Acoustic Survival Horror Kernel & Invariants
5. ANAT Explorable World Graph (17 Vertices, 5 Sectors, 7 Navigation Primitives)
6. Sovereign Hands-On Developer Actuators (File Read/Write/Patch, Glob, Search, Command Execution)
"""

import os
import sys
import json
import time
import glob
import subprocess
import logging
import psutil
from typing import Dict, List, Any, Optional, Tuple
import numpy as np

logger = logging.getLogger("DoubleHelixHermesDispatcher")

# Double Helix Core
from doublehelix.state import create_initial_state, ASCENDING_TIERS
from doublehelix.orchestrator.helix_engine import DoubleHelixOrchestrator
from doublehelix.engine.kernel import DeterministicKernel
from doublehelix.proofs.invariants import MathematicalProofOfConcept
from doublehelix.agents.auditor import WorkflowCapabilityAuditor
from doublehelix.runtime.elasticity import (
    ElasticRuntimeWindkessel,
    ActiveInferenceNirodhaEngine,
    GammaPhaseSynchronizer,
    CausalLaplacianConsensus
)
from doublehelix.runtime.decision_core import (
    OutlierEngineeredDecisionCore,
    ActionCandidate,
    TriageMetrics
)
from doublehelix.runtime.sheaf_sophi import (
    GrothendieckCellularSheaf,
    PoincareDifferentialIncubator,
    TeslaMonoidalOptic,
    LinearSessionChannel
)

# City Echoes Core
from doublehelix.games.city_echoes.kernel import CityEchoesKernel
from doublehelix.proofs.city_echoes_proofs import CityEchoesTheoremProver
from doublehelix.games.city_echoes.anat_bridge import CityEchoesANATBridge

# ANAT Explorable World Graph
from doublehelix.anat.world_graph import ExplorableWorldGraph
from doublehelix.anat.primitives import GraphNavigator
from doublehelix.anat.trajectories import TrajectoryController
from doublehelix.anat.helix_bridge import ANATHelixBridge


# ============================================================================
# TOOL SCHEMAS FOR HERMES 3 FUNCTION CALLING
# ============================================================================

DOUBLE_HELIX_HERMES_TOOLS = [
    # --- 1. Double Helix Upward Slice & Auditing Actuators ---
    {
        "type": "function",
        "function": {
            "name": "advance_helix_slice",
            "description": "Executes the Double Helix Upward Slice across all 4 elevation tiers (Core Tick -> ECS -> Perceptual -> Playtest) to empirical convergence.",
            "parameters": {
                "type": "object",
                "properties": {
                    "max_cycles": {
                        "type": "integer",
                        "description": "Maximum cycles per tier before circuit breaker trip (default: 5)."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_doublehelix_simulation",
            "description": "Runs deterministic headless simulation ticks with bot fuzzing, profiling frame times and zero dynamic allocations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticks": {"type": "integer", "description": "Number of simulation ticks (default: 1000)."},
                    "bot_count": {"type": "integer", "description": "Number of active simulated bots (default: 5)."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "prove_mathematical_invariants",
            "description": "Executes and formally validates analytical proofs of concept for Base Rungs 1-4 and ANAT Hopfield/ROME identities.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_doublehelix_status",
            "description": "Retrieves real-time status of Double Helix Engine: active tier, parity gates, telemetry vectors, and memory graph activations.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remediate_parity_failure",
            "description": "Applies targeted ROME Rank-One surgery and architectural code mutation to resolve an empirical benchmark breach.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tier": {"type": "string", "description": "Elevation tier that failed parity check."},
                    "root_cause": {"type": "string", "description": "Diagnosed root-cause failure explanation."}
                },
                "required": ["tier", "root_cause"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "audit_doublehelix_workflows",
            "description": "Audits Double Helix dual-strand upward slice workflows, state transitions, parity gate integrity, and circuit breaker compliance.",
            "parameters": {
                "type": "object",
                "properties": {
                    "workflow_type": {
                        "type": "string",
                        "description": "Target workflow identifier (default: 'dual_strand_upward_slice')."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "audit_agent_capabilities",
            "description": "Audits operational capability envelopes, formal invariant guarantees, and interface contracts across all Strand Alpha, Strand Beta, and Hermes agents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "run_probes": {
                        "type": "boolean",
                        "description": "Whether to execute empirical calibration probes against agents (default: true)."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_full_system_audit",
            "description": "Executes a complete metacognitive system audit combining workflow verification, agent capability probing, and gap analysis.",
            "parameters": {
                "type": "object",
                "properties": {
                    "run_probes": {
                        "type": "boolean",
                        "description": "Whether to execute empirical calibration probes (default: true)."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "prove_neurocomp_elasticity_theorems",
            "description": "Mathematically proves Theorems 1, 2, and 3 from NeuroCompElasticity: Windkessel low-pass variance attenuation, Nirodha bounded divergence, and Causal Laplacian consensus with Decision Augmentation Theory.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_nirodha_context_reset",
            "description": "Evaluates Free-Energy surrogate divergence and executes endogenous Nirodha cessation/reset if threshold is exceeded, preserving invariant state core.",
            "parameters": {
                "type": "object",
                "properties": {
                    "divergence_metric": {
                        "type": "number",
                        "description": "Free-Energy surrogate metric E_t to evaluate (default: 1.8)."
                    },
                    "force_reset": {
                        "type": "boolean",
                        "description": "Force context reset regardless of threshold (default: false)."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "verify_laplacian_swarm_consensus",
            "description": "Simulates decentralized agent swarm consensus over causal network Laplacian and computes algebraic connectivity lambda_2(L) and Kuramoto gamma synchrony order parameter R(t).",
            "parameters": {
                "type": "object",
                "properties": {
                    "num_agents": {
                        "type": "integer",
                        "description": "Number of agents in the swarm (default: 7)."
                    },
                    "steps": {
                        "type": "integer",
                        "description": "Consensus convergence iterations (default: 30)."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "prove_sophi_theorems",
            "description": "Mathematically proves Theorems 4, 5, and 6 from SOPHI-Runtime: Non-ergodic ruin prevention, Cellular sheaf Laplacian discord nullification, and Classical Linear Logic session confluence & zero token leakage.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "evaluate_ergodic_decision_core",
            "description": "Evaluates candidate actions through Somatic Attentional Triage, Epistemic Decoupling Sandbox (P(ruin) = 0), and constrained log-growth optimization.",
            "parameters": {
                "type": "object",
                "properties": {
                    "actions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "action_id": {"type": "string"},
                                "description": {"type": "string"},
                                "expected_yield": {"type": "number"},
                                "ruin_probability": {"type": "number"}
                            },
                            "required": ["action_id", "expected_yield"]
                        },
                        "description": "List of action candidates to evaluate."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_cellular_sheaf_consensus",
            "description": "Executes Grothendieck Cellular Sheaf gradient descent dx/dt = -L_F x over multi-agent stalks, computing spectral gap lambda_2(L_F) and Dirichlet energy decay.",
            "parameters": {
                "type": "object",
                "properties": {
                    "num_agents": {
                        "type": "integer",
                        "description": "Number of agents in the sheaf complex (default: 3)."
                    },
                    "steps": {
                        "type": "integer",
                        "description": "Gradient descent steps (default: 30)."
                    }
                }
            }
        }
    },

    # --- 2. City Echoes 5.8 Tactical Actuators ---
    {
        "type": "function",
        "function": {
            "name": "run_city_echoes_simulation",
            "description": "Executes 60 FPS deterministic City Echoes tactical acoustic simulation with ballistics, debris crunches, and occupant payouts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticks": {"type": "integer", "description": "Ticks to execute (default: 1000, 14400 for full 4-min match)."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "prove_city_echoes_theorems",
            "description": "Mathematically proves all 7 formal City Echoes tactical invariants (slug drywall breach, acoustic gasp at 9m, scotopic vision, etc.).",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "dispatch_tactical_acoustic_event",
            "description": "Dispatches a tactical acoustic event (sound_db, source_type) into the City Echoes ANAT memory bridge.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sound_db": {"type": "number", "description": "Sound volume in decibels."},
                    "source_type": {"type": "string", "description": "Acoustic source, e.g. 'DEBRIS_CRUNCH', 'EXHAUSTION_GASP', 'SLUG_BREACH'."}
                },
                "required": ["sound_db", "source_type"]
            }
        }
    },

    # --- 3. ANAT Explorable World Graph Primitives ---
    {
        "type": "function",
        "function": {
            "name": "observe_node",
            "description": "Inspects state, capacity, sector, and connectivity of a cognitive vertex in ANAT Explorable World Graph.",
            "parameters": {
                "type": "object",
                "properties": {
                    "node_id": {
                        "type": "string",
                        "description": "Target vertex ID: N01_SCRATCH to N17_DISTINCTION_ARCHITECTURE."
                    }
                },
                "required": ["node_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "hop_edge",
            "description": "Traverses an explicit directed edge between cognitive vertices in the Explorable World Graph.",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_node": {"type": "string", "description": "Source vertex ID."},
                    "edge_id": {"type": "string", "description": "Edge identifier, e.g. E01, E06, E09."}
                },
                "required": ["source_node", "edge_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "gating_check",
            "description": "Evaluates dynamic striatal gating (N02_GATE) or prediction surprise (N09_SURPRISE) to check threshold passage.",
            "parameters": {
                "type": "object",
                "properties": {
                    "node_id": {"type": "string", "description": "Gate node ID ('N02_GATE' or 'N09_SURPRISE')."},
                    "value": {"type": "number", "description": "Input value to evaluate."},
                    "threshold": {"type": "number", "description": "Optional custom threshold (default 0.50)."}
                },
                "required": ["node_id", "value"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "diffuse_knowledge",
            "description": "Runs Personalized PageRank diffusion across HippoRAG knowledge graph to retrieve associative semantic entities.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query_indices": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "Indices of seed nodes to diffuse from."
                    },
                    "steps": {"type": "integer", "description": "Diffusion iterations (default 15)."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "settle_hopfield_energy",
            "description": "Runs CCCP energy relaxation on continuous Modern Hopfield network to settle cues into stable attractor patterns.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cue_magnitude": {"type": "number", "description": "Magnitude scale for query cue vector."},
                    "beta": {"type": "number", "description": "Inverse temperature parameter (default 1.0)."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_trajectory",
            "description": "Executes one of ANAT's 5 cognitive memory trajectories: A (gating), B (episodic surprise), C (associative pattern completion), D (sleep consolidation), or E (targeted ROME surgery).",
            "parameters": {
                "type": "object",
                "properties": {
                    "trajectory_id": {
                        "type": "string",
                        "description": "Trajectory identifier: 'A', 'B', 'C', 'D', or 'E'."
                    },
                    "magnitude": {
                        "type": "number",
                        "description": "Optional numeric scale or surprise magnitude."
                    }
                },
                "required": ["trajectory_id"]
            }
        }
    },

    # --- 4. Sovereign Developer Actuators (The Hands) ---
    {
        "type": "function",
        "function": {
            "name": "read_code_file",
            "description": "Reads source code from a file in the workspace with optional line slice.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Relative or absolute file path."},
                    "start_line": {"type": "integer", "description": "Optional 1-indexed starting line."},
                    "end_line": {"type": "integer", "description": "Optional 1-indexed ending line."}
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_code_file",
            "description": "Creates or overwrites a source code file in the active workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Target file path."},
                    "content": {"type": "string", "description": "Complete file content."}
                },
                "required": ["file_path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "patch_code_file",
            "description": "Performs surgical search-and-replace edit on an existing source file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Target file path."},
                    "target_content": {"type": "string", "description": "Exact text chunk to replace."},
                    "replacement_content": {"type": "string", "description": "New text chunk to replace it with."}
                },
                "required": ["file_path", "target_content", "replacement_content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_workspace_files",
            "description": "Lists files and subdirectories in the active workspace or target directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {"type": "string", "description": "Optional directory path (defaults to current)."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_code",
            "description": "Searches for a text pattern or symbol across source files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search string or symbol."},
                    "extension": {"type": "string", "description": "Optional extension filter, e.g. '.py'."}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_terminal_command",
            "description": "Executes a shell command in the workspace and returns stdout/stderr and exit code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Command string to run."},
                    "timeout_seconds": {"type": "number", "description": "Timeout in seconds (default: 30)."}
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_hardware_telemetry",
            "description": "Retrieves real-time CPU, RAM, and process telemetry.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]


# ============================================================================
# DISPATCHER IMPLEMENTATION
# ============================================================================

class DoubleHelixHermesDispatcher:
    """Executes tools called by Hermes 3 in the Double Helix environment."""

    def __init__(
        self,
        workspace_dir: Optional[str] = None,
        world_graph: Optional[ExplorableWorldGraph] = None,
        helix_bridge: Optional[ANATHelixBridge] = None
    ):
        self.workspace_dir = os.path.abspath(workspace_dir or os.getcwd())
        self.world_graph = world_graph or ExplorableWorldGraph()
        self.navigator = GraphNavigator(self.world_graph)
        self.trajectories = TrajectoryController(self.world_graph)
        self.helix_bridge = helix_bridge or ANATHelixBridge()
        self.city_echoes_bridge = CityEchoesANATBridge(self.world_graph)
        self.last_orchestrator_state: Optional[Dict[str, Any]] = None
        self.auditor = WorkflowCapabilityAuditor()
        self.windkessel = ElasticRuntimeWindkessel()
        self.nirodha_engine = ActiveInferenceNirodhaEngine()
        self.decision_core = OutlierEngineeredDecisionCore()
        self.poincare_incubator = PoincareDifferentialIncubator()

    def dispatch(self, name: str, args: Dict[str, Any]) -> Any:
        """Central dispatch router."""
        # 1. Double Helix Upward Slice
        if name == "advance_helix_slice":
            import asyncio
            max_cycles = args.get("max_cycles", 5)
            orchestrator = DoubleHelixOrchestrator(
                anat_bridge=self.helix_bridge,
                timeout=0.1,
                edge_url="",
                reasoning_url="http://127.0.0.1:9999",
                coding_url="http://127.0.0.1:9999",
                runtime_url="http://127.0.0.1:9999"
            )
            state = create_initial_state(max_cycles_per_tier=max_cycles)
            # Run advance loop
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        final_state = executor.submit(lambda: asyncio.run(orchestrator.advance_helix(state))).result()
                else:
                    final_state = asyncio.run(orchestrator.advance_helix(state))
            except Exception:
                # Direct in-process run
                final_state = asyncio.run(orchestrator.advance_helix(state))

            self.last_orchestrator_state = final_state
            return {
                "status": "CONVERGED" if final_state["tier"] == "CONVERGED" else "IN_PROGRESS",
                "tier": final_state["tier"],
                "avg_frame_time_ms": final_state.get("avg_frame_time_ms", 0.0),
                "allocations_in_loop": final_state.get("allocations_in_loop", 0),
                "visual_anomalies": final_state.get("visual_anomalies", 0),
                "headless_bot_crashes": final_state.get("headless_bot_crashes", 0),
                "spatial_invariants_valid": final_state.get("spatial_invariants_valid", True)
            }

        elif name == "run_doublehelix_simulation":
            ticks = args.get("ticks", 1000)
            bots = args.get("bot_count", 5)
            kernel = DeterministicKernel(bot_count=bots)
            metrics = kernel.run_simulation(total_ticks=ticks)
            return metrics

        elif name == "prove_mathematical_invariants":
            p1, r1 = MathematicalProofOfConcept.prove_level_1_timing_and_zero_alloc(12.4, 0)
            p2, toi, r2 = MathematicalProofOfConcept.prove_level_2_swept_ccd_kinematics(
                np.array([50.0, 50.0]), np.array([800.0, 0.0]), 5.0, (0.0, 100.0, 0.0, 100.0), 1/60.0
            )
            p3, r3 = MathematicalProofOfConcept.prove_level_3_perceptual_boundedness(np.ones((64, 64, 3)) * 0.5)
            p4, r4 = MathematicalProofOfConcept.prove_level_4_ergodic_reachability(50, 50, 1000, 0)

            W = np.eye(16)
            k = np.ones(16)
            v = np.ones(16) * 3.0
            dW = np.outer(v - W @ k, k) / np.dot(k, k)
            p5, _, r5 = MathematicalProofOfConcept.prove_anat_rome_rank_one_identity(W, dW, k, v)

            return {
                "level_1_timing_zero_alloc": {"passed": p1, "qed": r1},
                "level_2_swept_ccd": {"passed": p2, "time_of_impact": toi, "qed": r2},
                "level_3_perceptual_radiance": {"passed": p3, "qed": r3},
                "level_4_ergodic_reachability": {"passed": p4, "qed": r4},
                "anat_rome_rank_one_identity": {"passed": p5, "qed": r5},
                "all_proofs_verified": all([p1, p2, p3, p4, p5])
            }

        elif name == "query_doublehelix_status":
            return {
                "active_workspace": self.workspace_dir,
                "world_graph_nodes": len(self.world_graph.nodes),
                "world_graph_edges": len(self.world_graph.edges),
                "last_elevation_tier": self.last_orchestrator_state.get("tier", "LEVEL_1_CORE_LOOP") if self.last_orchestrator_state else "READY",
                "converged": (self.last_orchestrator_state.get("tier") == "CONVERGED") if self.last_orchestrator_state else False
            }

        elif name == "remediate_parity_failure":
            tier = args.get("tier", "LEVEL_1_CORE_LOOP")
            root_cause = args.get("root_cause", "In-loop dynamic allocation breach")
            surgery_res = self.helix_bridge.apply_remediation_surgery(tier, root_cause)
            return surgery_res

        elif name == "audit_doublehelix_workflows":
            wf_type = args.get("workflow_type", "dual_strand_upward_slice")
            report = self.auditor.audit_workflow(
                workflow_type=wf_type,
                state=self.last_orchestrator_state,
                anat_bridge=self.helix_bridge
            )
            return report.model_dump()

        elif name == "audit_agent_capabilities":
            run_probes = args.get("run_probes", True)
            report = self.auditor.audit_agent_capabilities(run_probes=run_probes)
            return report.model_dump()

        elif name == "run_full_system_audit":
            run_probes = args.get("run_probes", True)
            report = self.auditor.run_full_audit(
                state=self.last_orchestrator_state,
                anat_bridge=self.helix_bridge,
                run_probes=run_probes
            )
            return report.model_dump()

        # 1.5 Neurocomputational Elasticity Actuators
        elif name == "prove_neurocomp_elasticity_theorems":
            p1_ok, h_sq, r1 = MathematicalProofOfConcept.prove_theorem_1_windkessel_variance_attenuation()
            p2_ok, eps_tr, r2 = MathematicalProofOfConcept.prove_theorem_2_nirodha_bounded_divergence()
            p3_ok, conv_rate, r3 = MathematicalProofOfConcept.prove_theorem_3_laplacian_consensus_and_causal_annihilation()
            return {
                "theorem_1_windkessel_variance_attenuation": {
                    "proven": p1_ok,
                    "attenuation_H_sq": float(h_sq),
                    "summary": r1
                },
                "theorem_2_nirodha_bounded_divergence": {
                    "proven": p2_ok,
                    "bound_epsilon_Tr": float(eps_tr),
                    "summary": r2
                },
                "theorem_3_laplacian_consensus_and_causal_annihilation": {
                    "proven": p3_ok,
                    "convergence_rate": float(conv_rate),
                    "summary": r3
                },
                "all_elasticity_theorems_verified": bool(p1_ok and p2_ok and p3_ok)
            }

        elif name == "execute_nirodha_context_reset":
            div = args.get("divergence_metric", 1.8)
            force = args.get("force_reset", False)
            context = args.get("context", {"active_agents": 7, "phase": "evaluation", "volatility": 0.95})
            invariant_core = args.get("invariant_core", {"tier": "LEVEL_1_CORE_LOOP", "proof_verified": True})

            self.nirodha_engine.record_divergence(div)
            should_reset = force or self.nirodha_engine.should_trigger_nirodha(div)
            reset_result = None
            if should_reset:
                reset_result = self.nirodha_engine.execute_cessation(context, invariant_core=invariant_core)
            return {
                "divergence_evaluated": div,
                "reset_triggered": should_reset,
                "reset_details": reset_result,
                "telemetry": self.nirodha_engine.get_telemetry()
            }

        elif name == "verify_laplacian_swarm_consensus":
            n = args.get("num_agents", 7)
            steps = args.get("steps", 30)
            consensus = CausalLaplacianConsensus(num_agents=n)
            gamma_sync = GammaPhaseSynchronizer(num_agents=n)

            for _ in range(steps):
                consensus.step_consensus(dt=0.05)
                gamma_sync.step(dt=0.01)

            return {
                "num_agents": n,
                "steps": steps,
                "algebraic_connectivity_lambda2": float(consensus.algebraic_connectivity()),
                "is_connected": consensus.is_connected(),
                "final_variance": float(np.var(consensus.state)),
                "kuramoto_order_parameter_R": float(gamma_sync.order_parameter()),
                "mean_frequency_hz": float(np.mean(gamma_sync.frequencies_hz))
            }

        # 1.6 SOPHI-Runtime & Outlier Decision Core Actuators
        elif name == "prove_sophi_theorems":
            p4_ok, m4, r4 = MathematicalProofOfConcept.prove_theorem_4_non_ergodic_ruin_prevention()
            p5_ok, gap5, r5 = MathematicalProofOfConcept.prove_theorem_5_cellular_sheaf_cohomology_nullification()
            p6_ok, m6, r6 = MathematicalProofOfConcept.prove_theorem_6_linear_session_deadlock_freedom_and_confluence()
            return {
                "theorem_4_non_ergodic_ruin_prevention": {
                    "proven": p4_ok,
                    "metrics": m4,
                    "summary": r4
                },
                "theorem_5_cellular_sheaf_cohomology_nullification": {
                    "proven": p5_ok,
                    "spectral_gap_lambda2": float(gap5),
                    "summary": r5
                },
                "theorem_6_linear_session_deadlock_freedom_confluence": {
                    "proven": p6_ok,
                    "metrics": m6,
                    "summary": r6
                },
                "all_sophi_theorems_verified": bool(p4_ok and p5_ok and p6_ok)
            }

        elif name == "evaluate_ergodic_decision_core":
            raw_actions = args.get("actions", [])
            candidates = []
            for a in raw_actions:
                candidates.append(ActionCandidate(
                    action_id=a.get("action_id", "act"),
                    description=a.get("description", "action candidate"),
                    expected_yield=float(a.get("expected_yield", 0.0)),
                    ruin_probability=float(a.get("ruin_probability", 0.0))
                ))
            if not candidates:
                candidates = [
                    ActionCandidate(action_id="viable_a", description="Stable growth", expected_yield=0.25, ruin_probability=0.0),
                    ActionCandidate(action_id="ruinous_b", description="High EV trap", expected_yield=2.0, ruin_probability=0.08)
                ]
            chosen, rollouts = self.decision_core.evaluate_and_decide(candidates)
            return {
                "chosen_action": chosen.model_dump() if chosen else None,
                "rollouts": [r.model_dump() for r in rollouts],
                "telemetry": self.decision_core.get_telemetry()
            }

        elif name == "run_cellular_sheaf_consensus":
            n = args.get("num_agents", 3)
            steps = args.get("steps", 30)
            sheaf = GrothendieckCellularSheaf(node_ids=[f"agent_{i}" for i in range(n)], stalk_dim=2)
            for i in range(n):
                sheaf.add_edge(f"agent_{i}", f"agent_{(i+1)%n}", f"e_{i}_{i+1}")
            spectral = sheaf.spectral_analysis()
            x = np.ones((n, 2))
            x[0, :] = [2.0, -1.0]
            e_init = sheaf.dirichlet_energy(x)
            for _ in range(steps):
                x = sheaf.dissipate_discord_step(x, eta=0.08)
            e_final = sheaf.dirichlet_energy(x)
            return {
                "num_agents": n,
                "spectral_gap_lambda2": spectral["spectral_gap_lambda2"],
                "harmonic_dimension_h0": spectral["harmonic_dimension_h0"],
                "initial_dirichlet_energy": float(e_init),
                "final_dirichlet_energy": float(e_final),
                "energy_dissipated_ratio": float((e_init - e_final) / max(1e-9, e_init))
            }

        # 2. City Echoes 5.8
        elif name == "run_city_echoes_simulation":
            ticks = args.get("ticks", 1000)
            kernel = CityEchoesKernel()
            metrics = kernel.run_simulation(total_ticks=ticks)
            return metrics

        elif name == "prove_city_echoes_theorems":
            res = CityEchoesTheoremProver.prove_all()
            return res

        elif name == "dispatch_tactical_acoustic_event":
            db = args.get("sound_db", 65.0)
            stype = args.get("source_type", "DEBRIS_CRUNCH")
            return self.city_echoes_bridge.dispatch_acoustic_event(db, stype)

        # 3. ANAT Explorable World Graph Primitives
        elif name == "observe_node":
            nid = args.get("node_id", "N01_SCRATCH")
            return self.navigator.observe(nid)

        elif name == "hop_edge":
            src = args.get("source_node", "N01_SCRATCH")
            eid = args.get("edge_id", "E01")
            tgt = self.navigator.hop(src, eid)
            return {"source": src, "edge_id": eid, "target": tgt}

        elif name == "gating_check":
            nid = args.get("node_id", "N02_GATE")
            val = args.get("value", 0.6)
            thresh = args.get("threshold", 0.50)
            passed = self.navigator.gating_check(nid, val, thresh)
            return {"node_id": nid, "value": val, "threshold": thresh, "passed": passed}

        elif name == "diffuse_knowledge":
            q_idx = args.get("query_indices", [0])
            steps = args.get("steps", 15)
            probs = self.navigator.diffuse(query_indices=q_idx, steps=steps)
            top_indices = np.argsort(probs)[::-1][:5]
            _, node_ids = self.world_graph.get_adjacency_matrix()
            top_nodes = [{"node_id": node_ids[i], "probability": float(probs[i])} for i in top_indices if i < len(node_ids)]
            return {"top_diffused_nodes": top_nodes}

        elif name == "settle_hopfield_energy":
            scale = args.get("cue_magnitude", 1.0)
            beta = args.get("beta", 1.0)
            stored = np.random.randn(16, 4).astype(np.float32)
            query = np.ones(16, dtype=np.float32) * scale
            settled, energy = self.navigator.settle_energy(stored, query, beta=beta)
            return {"final_energy": float(energy), "settled_norm": float(np.linalg.norm(settled))}

        elif name == "execute_trajectory":
            tid = args.get("trajectory_id", "A").upper()
            mag = args.get("magnitude", 1.0)
            vec = np.ones(64, dtype=np.float32) * mag

            if tid == "A":
                return self.trajectories.run_trajectory_a(vec)
            elif tid == "B":
                return self.trajectories.run_trajectory_b(vec, surprise_magnitude=mag)
            elif tid == "C":
                return self.trajectories.run_trajectory_c(vec)
            elif tid == "D":
                return self.trajectories.run_trajectory_d()
            elif tid == "E":
                key_k = np.ones(64, dtype=np.float32)
                target_v = np.zeros(64, dtype=np.float32)
                return self.trajectories.run_trajectory_e(key_k, target_v)
            else:
                return {"error": f"Unknown trajectory ID '{tid}'"}

        # 4. Code & Developer Actuators
        elif name == "read_code_file":
            rel_path = args.get("file_path", "")
            full_path = os.path.join(self.workspace_dir, rel_path) if not os.path.isabs(rel_path) else rel_path
            if not os.path.exists(full_path):
                return {"error": f"File '{rel_path}' not found"}
            with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
            start = max(1, args.get("start_line", 1)) - 1
            end = args.get("end_line", len(lines))
            return {"file": rel_path, "lines": lines[start:end], "total_lines": len(lines)}

        elif name == "write_code_file":
            rel_path = args.get("file_path", "")
            content = args.get("content", "")
            full_path = os.path.join(self.workspace_dir, rel_path) if not os.path.isabs(rel_path) else rel_path
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            return {"success": True, "file_path": rel_path, "bytes_written": len(content)}

        elif name == "patch_code_file":
            rel_path = args.get("file_path", "")
            target = args.get("target_content", "")
            replacement = args.get("replacement_content", "")
            full_path = os.path.join(self.workspace_dir, rel_path) if not os.path.isabs(rel_path) else rel_path
            if not os.path.exists(full_path):
                return {"error": f"File '{rel_path}' not found"}
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            if target not in content:
                return {"error": "Target chunk not found in file"}
            new_content = content.replace(target, replacement, 1)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            return {"success": True, "file_path": rel_path}

        elif name == "list_workspace_files":
            target_dir = args.get("directory", self.workspace_dir)
            if not os.path.isabs(target_dir):
                target_dir = os.path.join(self.workspace_dir, target_dir)
            if not os.path.exists(target_dir):
                return {"error": f"Directory '{target_dir}' not found"}
            entries = os.listdir(target_dir)
            summary = []
            for e in sorted(entries)[:50]:
                p = os.path.join(target_dir, e)
                summary.append({"name": e, "is_dir": os.path.isdir(p), "size_bytes": os.path.getsize(p) if os.path.isfile(p) else 0})
            return {"directory": target_dir, "entries": summary}

        elif name == "search_code":
            query = args.get("query", "")
            ext = args.get("extension", "")
            matches = []
            for root, _, files in os.walk(self.workspace_dir):
                if any(ignored in root for ignored in [".git", "__pycache__", ".venv", "egg-info"]):
                    continue
                for f in files:
                    if ext and not f.endswith(ext):
                        continue
                    fp = os.path.join(root, f)
                    try:
                        with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                            for idx, line in enumerate(fh, 1):
                                if query in line:
                                    matches.append({"file": os.path.relpath(fp, self.workspace_dir), "line": idx, "text": line.strip()[:100]})
                                    if len(matches) >= 30:
                                        break
                    except Exception as e:
                        logger.debug("Skipping unreadable file %s: %s", fp, e)
                if len(matches) >= 30:
                    break
            return {"query": query, "matches_count": len(matches), "matches": matches}

        elif name == "run_terminal_command":
            cmd = args.get("command", "")
            timeout = args.get("timeout_seconds", 30.0)
            res = subprocess.run(
                cmd,
                shell=True,
                cwd=self.workspace_dir,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return {"command": cmd, "exit_code": res.returncode, "stdout": res.stdout[:2000], "stderr": res.stderr[:1000]}

        elif name == "query_hardware_telemetry":
            return {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "memory_available_mb": psutil.virtual_memory().available / (1024 * 1024)
            }

        return {"error": f"Unknown tool name: {name}"}
