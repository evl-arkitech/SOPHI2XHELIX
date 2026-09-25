from __future__ import annotations

"""Container 2: Helix Synchronizer (helix_engine.py).

Master Orchestrator operating as a synchronized dual-strand execution loop in Python.
Runs Strand Alpha (Synthesis) and Strand Beta (Empirical Simulation) concurrently via asyncio.gather,
evaluating cross-strand parity gates at each Base Rung and ascending through elevation tiers.
"""

import asyncio
import os
import logging
from typing import Dict, Any, Tuple, Optional, Callable, List, TYPE_CHECKING
import httpx

from doublehelix.config import settings
from doublehelix.state import HelixState, ASCENDING_TIERS
from doublehelix.orchestrator.parity_gates import evaluate_base_rung
from doublehelix.anat.helix_bridge import ANATHelixBridge

logger = logging.getLogger("DoubleHelixOrchestrator")

if TYPE_CHECKING:
    from doublehelix.agents.auditor import (
        WorkflowCapabilityAuditor,
        WorkflowAuditReport,
        CapabilityAuditReport,
        SystemAuditReport,
    )


class DoubleHelixOrchestrator:
    """Master Orchestrator coordinating Strand Alpha and Strand Beta across the upward slice."""

    def __init__(
        self,
        reasoning_url: Optional[str] = None,
        coding_url: Optional[str] = None,
        runtime_url: Optional[str] = None,
        edge_url: Optional[str] = None,
        timeout: float = 60.0,
        on_rung_evaluated: Optional[Callable[[str, bool, str, Dict[str, Any]], None]] = None,
        anat_bridge: Optional[ANATHelixBridge] = None,
        auditor: Optional[Any] = None
    ):
        self.reasoning_url = reasoning_url or os.getenv("REASONING_LLM_URL", settings.reasoning_llm_url)
        self.coding_url = coding_url or os.getenv("CODING_LLM_URL", settings.coding_llm_url)
        self.runtime_url = runtime_url or os.getenv("RUNTIME_API_URL", settings.runtime_api_url)
        self.edge_url = edge_url if edge_url is not None else os.getenv("EDGE_URL", "https://doublehelix-edge-server.evl-arkitech.workers.dev")
        self.timeout = timeout
        self.on_rung_evaluated = on_rung_evaluated
        self.anat_bridge = anat_bridge or ANATHelixBridge()
        if auditor is None:
            from doublehelix.agents.auditor import WorkflowCapabilityAuditor
            self.auditor = WorkflowCapabilityAuditor()
        else:
            self.auditor = auditor
        self.execution_trace: List[Dict[str, Any]] = []

        # Neurocomputational Elasticity & Contemplative Dynamics Primitives
        from doublehelix.runtime.elasticity import (
            ElasticRuntimeWindkessel,
            ActiveInferenceNirodhaEngine
        )
        from doublehelix.runtime.decision_core import OutlierEngineeredDecisionCore
        from doublehelix.runtime.sheaf_sophi import GrothendieckCellularSheaf

        self.windkessel = ElasticRuntimeWindkessel()
        self.nirodha_engine = ActiveInferenceNirodhaEngine()
        self.decision_core = OutlierEngineeredDecisionCore()
        self.cellular_sheaf = GrothendieckCellularSheaf(
            node_ids=["strand_alpha", "strand_beta", "auditor"],
            stalk_dim=2
        )
        self.cellular_sheaf.add_edge("strand_alpha", "strand_beta", "alpha_beta_contract")
        self.cellular_sheaf.add_edge("strand_beta", "auditor", "beta_auditor_telemetry")
        self.cellular_sheaf.add_edge("auditor", "strand_alpha", "auditor_alpha_feedback")

    def __repr__(self) -> str:
        return (
            f"<DoubleHelixOrchestrator reasoning={self.reasoning_url} "
            f"coding={self.coding_url} runtime={self.runtime_url} "
            f"timeout={self.timeout}s>"
        )

    def get_diagnostics(self) -> Dict[str, Any]:
        """Provides instant debugging state and subsystem connectivity diagnostics."""
        return {
            "reasoning_url": self.reasoning_url,
            "coding_url": self.coding_url,
            "runtime_url": self.runtime_url,
            "edge_url": self.edge_url,
            "timeout": self.timeout,
            "anat_bridge_active": self.anat_bridge is not None,
            "decision_core_active": True,
            "windkessel_buffer_samples": len(self.windkessel.p_buffer),
            "execution_trace_length": len(self.execution_trace),
        }

    async def advance_helix(self, state: HelixState) -> HelixState:
        """Runs Strand Alpha (Synthesis) and Strand Beta (Simulation) concurrently."""
        while state["tier"] != "CONVERGED":
            state["current_cycle"] += 1
            if state["current_cycle"] > state["max_cycles_per_tier"]:
                raise RuntimeError(
                    f"Circuit Breaker: Failed parity at {state['tier']} after {state['max_cycles_per_tier']} cycles."
                )

            # Ingest workload into Windkessel buffer to smooth task bursts
            self.windkessel.ingest({"tier": state["tier"], "cycle": state["current_cycle"]})

            # 1. PARALLEL EXECUTION: Strand Alpha plans/codes, Strand Beta verifies previous
            self.anat_bridge.route_strand_alpha_synthesis(state["tier"], f"Upward slice specification for {state['tier']}")
            synthesis_task = self._run_strand_alpha(state)
            validation_task = self._run_strand_beta(state)

            # Await both strands to reach the base rung simultaneously
            alpha_out, beta_telemetry = await asyncio.gather(synthesis_task, validation_task)

            # Ingest empirical telemetry breaches into N09_SURPRISE and N08_TITANS
            self.anat_bridge.route_strand_beta_telemetry(state["tier"], beta_telemetry)

            # Update state with latest telemetry
            state["avg_frame_time_ms"] = beta_telemetry.get("avg_frame_time_ms", 0.0)
            state["allocations_in_loop"] = beta_telemetry.get("allocations_in_loop", 0)
            state["headless_bot_crashes"] = beta_telemetry.get("headless_bot_crashes", 0)
            state["visual_anomalies"] = beta_telemetry.get("visual_anomalies", 0)
            state["spatial_invariants_valid"] = alpha_out.get("spatial_invariants_valid", True)

            # 2. BASE RUNG PARITY GATE: Inspect cross-strand metrics
            elevate, reason = self._evaluate_base_rung(state["tier"], alpha_out, beta_telemetry)

            # Record step in execution trace for metacognitive workflow auditing
            self.execution_trace.append({
                "tier": state["tier"],
                "cycle": state["current_cycle"],
                "elevate": elevate,
                "reason": reason,
                "telemetry": dict(beta_telemetry),
                "spatial_invariants_valid": state["spatial_invariants_valid"]
            })

            if self.on_rung_evaluated:
                self.on_rung_evaluated(state["tier"], elevate, reason, beta_telemetry)

            # 3. Synchronize with Cloudflare Edge Server (Durable Object & Dashboard)
            if self.edge_url:
                await self._sync_edge(state, elevate, reason, beta_telemetry)

            if elevate:
                print(f"[+] Ascending {state['tier']} -> Next Tier")
                # Consolidate tier ascension milestone into ANAT EWG memory (Trajectory D)
                self.anat_bridge.consolidate_tier_ascension(state["tier"])
                state = self._promote_tier(state)
                state["current_cycle"] = 0
            else:
                print(f"[-] Parity Gate Rejected at {state['tier']}: {reason}. Mutating...")
                # Apply Trajectory E ROME Rank-One surgery and code repair
                self.anat_bridge.apply_remediation_surgery(state["tier"], reason)
                state = await self._remediate_failure(state, alpha_out, beta_telemetry, reason)

        # Final convergence sync with edge
        if self.edge_url:
            await self._sync_edge(state, True, "Ascended to Convergence", {})

        print("[*] Convergence Reached: All Base Rungs Passed.")
        return state

    async def _sync_edge(self, state: HelixState, passed: bool, reason: str, telemetry: dict):
        """Asynchronously dispatches live telemetry and frame state to Cloudflare Edge."""
        if not self.edge_url:
            return
        update_url = f"{self.edge_url.rstrip('/')}/api/helix/update"
        payload = {
            "tier": state["tier"],
            "avg_frame_time_ms": state.get("avg_frame_time_ms", 0.0),
            "allocations_in_loop": state.get("allocations_in_loop", 0),
            "headless_bot_crashes": state.get("headless_bot_crashes", 0),
            "visual_anomalies": state.get("visual_anomalies", 0),
            "spatial_invariants_valid": state.get("spatial_invariants_valid", True),
            "current_cycle": state.get("current_cycle", 0),
            "max_cycles_per_tier": state.get("max_cycles_per_tier", 5),
            "frame_data_url": telemetry.get("last_frame_data_url", "")
        }
        try:
            async with httpx.AsyncClient(timeout=10.0, headers={"User-Agent": "DoubleHelix-Engine/1.0"}) as client:
                await client.post(update_url, json=payload)
        except Exception as e:
            logger.debug("Edge synchronizer update broadcast skipped: %s", e)

    async def _run_strand_alpha(self, state: HelixState) -> Dict[str, Any]:
        """Strand Alpha: Synthesizes mechanics, math proofs, and code structures."""
        # Query Reasoning LLM for spatial invariants & memory safety checks
        tier = state["tier"]
        spatial_invariants_valid = True
        architecture_contract = ""

        # Normalize endpoints
        r_url = self.reasoning_url.rstrip("/")
        c_url = self.coding_url.rstrip("/")
        if not r_url.endswith("/chat/completions"):
            r_url = f"{r_url}/chat/completions"
        if not c_url.endswith("/chat/completions"):
            c_url = f"{c_url}/chat/completions"

        async with httpx.AsyncClient(timeout=self.timeout, headers={"User-Agent": "DoubleHelix-Engine/1.0"}) as client:
            try:
                # 1. Reasoning LLM (Port 8001)
                r_res = await client.post(
                    r_url,
                    json={
                        "model": "reasoning",
                        "messages": [
                            {"role": "system", "content": "Prove spatial invariants and zero-allocation constraints."},
                            {"role": "user", "content": f"Verify invariants for tier {tier}"}
                        ],
                        "temperature": 0.0
                    }
                )
                if r_res.status_code == 200:
                    r_json = r_res.json()
                    r_text = r_json["choices"][0]["message"]["content"]
                    spatial_invariants_valid = "VERIFIED: FALSE" not in r_text.upper()
                    architecture_contract = r_text
            except Exception as e:
                # Retain non-blocking trace if external model is pending
                architecture_contract = f"Local contract for {tier}"

            # 2. Coding LLM (Port 8002)
            try:
                c_res = await client.post(
                    c_url,
                    json={
                        "model": "coding",
                        "messages": [
                            {"role": "system", "content": "Generate zero-allocation, cache-localized game systems."},
                            {"role": "user", "content": f"Synthesize implementation for tier {tier}"}
                        ],
                        "temperature": 0.1
                    }
                )
                if c_res.status_code == 200:
                    c_json = c_res.json()
                    patch = c_json["choices"][0]["message"]["content"]
                    return {
                        "patch": patch,
                        "spatial_invariants_valid": spatial_invariants_valid,
                        "contract": architecture_contract
                    }
            except Exception as e:
                logger.debug("Strand Alpha code synthesis query skipped: %s", e)

        return {
            "patch": "# Synthesized Strand Alpha Code",
            "spatial_invariants_valid": spatial_invariants_valid,
            "contract": architecture_contract
        }

    async def _run_strand_beta(self, state: HelixState) -> Dict[str, Any]:
        """Strand Beta: Runs headless game instance, profiles frames, runs bot tests."""
        sim_url = self.runtime_url.rstrip("/")
        if not sim_url.endswith("/game/simulate"):
            sim_url = f"{sim_url}/game/simulate"

        # Tier-specific ticks: Level 4 Playtest stresses 10,000 ticks
        ticks = settings.level4_sim_ticks if state["tier"] == "LEVEL_4_PLAYTEST" else settings.default_sim_ticks
        bot_count = settings.default_bot_count

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                res = await client.post(
                    sim_url,
                    json={
                        "files": state.get("codebase", {}),
                        "ticks": ticks,
                        "bot_count": bot_count
                    }
                )
                res.raise_for_status()
                return res.json()
            except Exception:
                # Fallback to in-process simulation runner
                from doublehelix.runtime.game_runner import run_simulation, SimRequest
                try:
                    return run_simulation(SimRequest(
                        files=state.get("codebase", {}),
                        ticks=ticks,
                        bot_count=bot_count
                    ))
                except Exception as inner_e:
                    return {
                        "exit_code": 1,
                        "avg_frame_time_ms": 99.0,
                        "allocations_in_loop": 1,
                        "tunneling_errors": 1,
                        "shader_errors": 1,
                        "visual_anomalies": 1,
                        "headless_bot_crashes": 1,
                        "error": str(inner_e)
                    }

    def _evaluate_base_rung(self, tier: str, alpha: dict, beta: dict) -> Tuple[bool, str]:
        """Base Rung Verification Gates."""
        return evaluate_base_rung(tier, alpha, beta)

    def _promote_tier(self, state: HelixState) -> HelixState:
        """Ascends to the next Elevation Tier."""
        current_idx = ASCENDING_TIERS.index(state["tier"])
        state["tier"] = ASCENDING_TIERS[current_idx + 1]
        return state

    async def _remediate_failure(
        self,
        state: HelixState,
        alpha: dict,
        beta: dict,
        reason: str
    ) -> HelixState:
        """Uses the Reasoning LLM to compute the fix for empirical benchmark breaches, then applies patch via Coding LLM."""
        r_url = self.reasoning_url.rstrip("/")
        c_url = self.coding_url.rstrip("/")
        if not r_url.endswith("/chat/completions"):
            r_url = f"{r_url}/chat/completions"
        if not c_url.endswith("/chat/completions"):
            c_url = f"{c_url}/chat/completions"

        diagnosis = ""
        async with httpx.AsyncClient(timeout=self.timeout, headers={"User-Agent": "DoubleHelix-Engine/1.0"}) as client:
            # 1. Reasoning LLM Root Cause Diagnosis
            try:
                diag = await client.post(
                    r_url,
                    json={
                        "model": "reasoning",
                        "messages": [
                            {"role": "user", "content": f"Telemetry failure at {state['tier']}: {reason}. Diagnose:"}
                        ]
                    }
                )
                if diag.status_code == 200:
                    diagnosis = diag.json()["choices"][0]["message"]["content"]
            except Exception as e:
                diagnosis = f"Heuristic analysis for {reason}: {str(e)}"

            # 2. Apply targeted fix via Coding LLM
            try:
                patch = await client.post(
                    c_url,
                    json={
                        "model": "coding",
                        "messages": [
                            {
                                "role": "user",
                                "content": f"Apply fix based on root cause analysis:\n{diagnosis}"
                            }
                        ]
                    }
                )
                if patch.status_code == 200:
                    repaired_code = patch.json()["choices"][0]["message"]["content"]
                    from doublehelix.runtime.decision_core import ActionCandidate
                    candidate = ActionCandidate(
                        action_id=f"remediate_{state['tier']}_{state['current_cycle']}",
                        description=f"Patch for {reason}",
                        expected_yield=0.25,
                        ruin_probability=0.0,
                        payload={"patch": repaired_code}
                    )
                    rollout = self.decision_core.epistemic_sandbox.rollout(candidate, current_state=state)
                    if rollout.approved:
                        state["codebase"]["engine.py"] = repaired_code
                    else:
                        print(f"[!] Remediation rejected by Epistemic Decoupling Sandbox: {rollout.rejection_reason}")
            except Exception as e:
                logger.warning("Parity failure auto-remediation failed: %s", e)

        return state

    def audit_workflow(self, state: Optional[HelixState] = None) -> WorkflowAuditReport:
        """Invokes the Workflow & Agent Capabilities Auditor on the orchestrator workflow."""
        return self.auditor.audit_workflow(
            workflow_type="dual_strand_upward_slice",
            state=state,
            execution_trace=self.execution_trace,
            anat_bridge=self.anat_bridge
        )

    def audit_agent_capabilities(self, run_probes: bool = True) -> CapabilityAuditReport:
        """Audits capability contracts and empirical boundaries across all active Double Helix agents."""
        return self.auditor.audit_agent_capabilities(run_probes=run_probes)

    def run_system_audit(
        self,
        state: Optional[HelixState] = None,
        run_probes: bool = True
    ) -> SystemAuditReport:
        """Runs a complete metacognitive audit of both upward slice workflows and agent capabilities."""
        return self.auditor.run_full_audit(
            state=state,
            execution_trace=self.execution_trace,
            anat_bridge=self.anat_bridge,
            run_probes=run_probes
        )

    def get_runtime_elasticity_metrics(self) -> Dict[str, Any]:
        """Returns somatic vascular Windkessel metrics and Nirodha reset telemetry."""
        return {
            "windkessel": self.windkessel.get_metrics(),
            "nirodha": {
                "total_resets_triggered": self.nirodha_engine.total_resets_triggered,
                "steps_since_reset": self.nirodha_engine.steps_since_reset,
                "theta_reset": self.nirodha_engine.theta_reset,
                "T_r_horizon": self.nirodha_engine.T_r
            }
        }

    def get_decision_core_telemetry(self) -> Dict[str, Any]:
        """Returns Outlier-Engineered Decision Core telemetry and epistemic sandbox metrics."""
        return self.decision_core.get_telemetry()

    def get_cellular_sheaf_telemetry(self) -> Dict[str, Any]:
        """Returns multi-agent Grothendieck Cellular Sheaf spectral metrics and Dirichlet energy."""
        spectral = self.cellular_sheaf.spectral_analysis()
        return {
            "spectral_gap_lambda2": spectral["spectral_gap_lambda2"],
            "harmonic_dimension_h0": spectral["harmonic_dimension_h0"],
            "total_dof": spectral["total_dof"],
            "is_connected": spectral["is_connected"]
        }


