"""Agent 7: Workflow & Agent Capabilities Auditor (Cross-Strand Metacognitive Auditor).

Dedicated to auditing Double Helix Upward Slice workflows, parity gate enforcement,
circuit breaker state machines, ANAT cognitive trajectories, and evaluating the
empirical capability envelope of all Strand Alpha, Strand Beta, and Hermes agents.
"""

import time
import inspect
from typing import Dict, List, Any, Optional, Tuple, Callable
from pydantic import BaseModel, Field

from doublehelix.state import HelixState, ASCENDING_TIERS, create_initial_state
from doublehelix.agents.base import LLMAgentClient


AUDITOR_SYSTEM_PROMPT = """You are the Workflow & Agent Capabilities Auditor (Agent 7) in the Double Helix Neural Agent Engine.
Your specialized cognitive responsibility is:
1. Audit dual-strand upward slice workflows: verify that state transitions across LEVEL_1_KERNEL -> LEVEL_2_ECS -> LEVEL_3_RENDER -> LEVEL_4_PLAYTEST -> CONVERGED strictly satisfy empirical parity gates.
2. Detect false promotions, circuit breaker bypasses, cycle overflow, or unhandled exceptions in the dual-strand execution loop.
3. Audit Agent Capabilities: systematically evaluate Strand Alpha (ECS Architect, Systems Coder, Spatial Math), Strand Beta (Playtest Bot, Frame Profiler, Visual Auditor), and Hermes Sovereign Cortex.
4. Verify formal mathematical invariants (T_frame <= 16.6ms, Delta_M == 0, CCD tunneling == 0, 0 NaN pixels, 10,000 tick bot fuzzing convergence).
5. Generate actionable remediation recommendations and capability maturity assessments.
"""


# ============================================================================
# AUDIT DATA MODELS & SCHEMAS
# ============================================================================

class AgentCapabilityDescriptor(BaseModel):
    """Specification of an agent's operational capability envelope and invariants."""
    agent_id: str
    name: str
    role: str
    strand: str  # "STRAND_ALPHA", "STRAND_BETA", "HERMES_SOVEREIGN", "CROSS_STRAND"
    description: str
    capabilities: List[str] = Field(default_factory=list)
    formal_invariants: List[str] = Field(default_factory=list)
    interface_methods: List[str] = Field(default_factory=list)
    status: str = "HEALTHY"  # "HEALTHY", "DEGRADED", "UNTESTED", "FAILED"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CapabilityProbeResult(BaseModel):
    """Result from dynamic empirical probing of an agent's capability."""
    agent_id: str
    probe_name: str
    passed: bool
    latency_ms: float
    details: str
    issues: List[str] = Field(default_factory=list)


class CapabilityAuditReport(BaseModel):
    """Comprehensive evaluation of all system agent capabilities."""
    timestamp: float = Field(default_factory=time.time)
    total_agents: int = 0
    healthy_agents: int = 0
    degraded_agents: int = 0
    failed_agents: int = 0
    capability_maturity_score: float = 0.0  # 0.0 to 100.0%
    probes_run: int = 0
    probes_passed: int = 0
    probe_results: List[CapabilityProbeResult] = Field(default_factory=list)
    agent_descriptors: Dict[str, AgentCapabilityDescriptor] = Field(default_factory=dict)
    gap_analysis: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


class WorkflowStepAudit(BaseModel):
    """Audit result for an individual workflow transition or phase."""
    step_name: str
    tier: Optional[str] = None
    passed: bool = True
    invariants_checked: List[str] = Field(default_factory=list)
    violations: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class WorkflowAuditReport(BaseModel):
    """Audit assessment for the dual-strand upward slice execution workflow."""
    timestamp: float = Field(default_factory=time.time)
    workflow_name: str = "dual_strand_upward_slice"
    passed: bool = True
    steps_audited: int = 0
    violations_count: int = 0
    warnings_count: int = 0
    step_results: List[WorkflowStepAudit] = Field(default_factory=list)
    circuit_breaker_healthy: bool = True
    parity_gate_integrity_score: float = 100.0  # 0.0 to 100.0%
    violations: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


class SystemAuditReport(BaseModel):
    """Unified executive report combining workflow and capability audits."""
    timestamp: float = Field(default_factory=time.time)
    overall_status: str = "HEALTHY"  # "HEALTHY", "WARNING", "CRITICAL"
    overall_score: float = 100.0     # 0.0 to 100.0%
    workflow_audit: WorkflowAuditReport
    capability_audit: CapabilityAuditReport
    executive_summary: str = ""
    critical_findings: List[str] = Field(default_factory=list)
    remediation_roadmap: List[str] = Field(default_factory=list)


# ============================================================================
# AGENT 7: WORKFLOW & AGENT CAPABILITIES AUDITOR
# ============================================================================

class WorkflowCapabilityAuditor:
    """Specialized Agent for auditing Double Helix workflows and agent capabilities."""

    def __init__(self, reasoning_client: Optional[LLMAgentClient] = None):
        self.reasoning_client = reasoning_client
        self._registered_agents: Dict[str, Any] = {}
        self._register_default_descriptors()

    def _register_default_descriptors(self):
        """Initializes canonical capability descriptors for the standard Double Helix agent mesh."""
        self._descriptors: Dict[str, AgentCapabilityDescriptor] = {
            "agent_1_ecs_architect": AgentCapabilityDescriptor(
                agent_id="agent_1_ecs_architect",
                name="ECSArchitectAgent",
                role="ECS & Engine Architect",
                strand="STRAND_ALPHA",
                description="Designs data-oriented component schemas, zero-allocation memory arena pools, and static entity buffers.",
                capabilities=[
                    "Data-oriented Struct-of-Arrays (SoA) layout synthesis",
                    "Static memory pool sizing & pre-allocated ring buffer design",
                    "Garbage collection pause elimination contract formulation",
                    "Tier-specific architectural contract generation"
                ],
                formal_invariants=[
                    "Proof 1.2: Delta_M = 0 (zero dynamic heap allocation in hot loop)",
                    "Cache-friendly contiguous struct alignment"
                ],
                interface_methods=["design_tier_architecture"]
            ),
            "agent_2_system_coder": AgentCapabilityDescriptor(
                agent_id="agent_2_system_coder",
                name="SystemCoderAgent",
                role="Systems & Shader Coder",
                strand="STRAND_ALPHA",
                description="Synthesizes deterministic game loop code, WGSL/GLSL shaders, and applies surgical remediation patches.",
                capabilities=[
                    "Zero-allocation hot tick update & render loop implementation",
                    "WGSL/GLSL shader offscreen render pipeline synthesis",
                    "Markdown code fence extraction & sanitization",
                    "Surgical telemetry breach remediation patch application"
                ],
                formal_invariants=[
                    "Deterministic execution under fixed dt = 16.6667ms",
                    "Zero compiler or shader validation warnings",
                    "Zero dynamic heap allocations in inner loop"
                ],
                interface_methods=["synthesize_code", "apply_remediation_patch", "extract_code"]
            ),
            "agent_3_spatial_math": AgentCapabilityDescriptor(
                agent_id="agent_3_spatial_math",
                name="SpatialMathPhysicsAgent",
                role="Spatial Math & Physics Agent",
                strand="STRAND_ALPHA",
                description="Validates kinematic continuous collision detection (CCD), BVH spatial hashing, and symplectic integration.",
                capabilities=[
                    "Continuous Collision Detection (CCD) swept-volume proof verification",
                    "Uniform spatial hash grid & BVH partitioning validation",
                    "Quaternions, rotational dynamics & Verlet integration stability proofs",
                    "Spatial failure root-cause diagnosis"
                ],
                formal_invariants=[
                    "Proof 2.1: Swept-volume continuous trajectory p(t*) guarantees 0 tunneling",
                    "Symplectic integration energy conservation"
                ],
                interface_methods=["verify_spatial_invariants", "diagnose_telemetry_failure"]
            ),
            "agent_4_playtest_bot": AgentCapabilityDescriptor(
                agent_id="agent_4_playtest_bot",
                name="HeadlessPlaytestAgent",
                role="Headless Bot / Playtest Agent",
                strand="STRAND_BETA",
                description="Executes stochastic monkey fuzz testing, virtual player actors, and heuristic state exploration.",
                capabilities=[
                    "Stochastic monkey input vector generation",
                    "Multi-bot concurrent fuzz schedule construction",
                    "Deadlock, desync, and unhandled exception detection",
                    "State space reachability validation across entity states"
                ],
                formal_invariants=[
                    "Proof 4.1: Ergodic state exploration with 0 absorbing deadlock traps",
                    "10,000 simulated ticks without crash"
                ],
                interface_methods=["build_fuzz_payload", "evaluate_bot_telemetry"]
            ),
            "agent_5_frame_profiler": AgentCapabilityDescriptor(
                agent_id="agent_5_frame_profiler",
                name="FrameTimeMemoryProfiler",
                role="Frame-Time & Memory Profiler",
                strand="STRAND_BETA",
                description="Measures frame execution timing, enforces the 16.6ms budget, and traps dynamic heap allocations.",
                capabilities=[
                    "Microsecond/millisecond tick loop duration profiling",
                    "Dynamic heap allocation trapping inside hot loop",
                    "FPS estimation & frame budget breach alert generation",
                    "Telemetry vector evaluation against Level 1 contracts"
                ],
                formal_invariants=[
                    "Proof 1.1: T_measured <= 16.6667ms (60 FPS standard)",
                    "Proof 1.2: Delta_M = allocations_in_loop == 0"
                ],
                interface_methods=["evaluate_telemetry"]
            ),
            "agent_6_visual_auditor": AgentCapabilityDescriptor(
                agent_id="agent_6_visual_auditor",
                name="VisualContractAuditor",
                role="Visual Contract & Audio Auditor",
                strand="STRAND_BETA",
                description="Inspects headless offscreen RGB framebuffers to detect visual anomalies, NaN/Inf radiance, and shader errors.",
                capabilities=[
                    "Offscreen RGB24 framebuffer buffer integrity validation",
                    "NaN / Inf color value & visual anomaly scanning",
                    "Shader compilation error aggregation & diagnostics",
                    "Render contract verification against Level 3 criteria"
                ],
                formal_invariants=[
                    "Proof 3.1: Radiance tensor C_{x,y} in R^3 without NaN/Inf, ||C||_inf <= 1.0",
                    "Zero pipeline compilation errors"
                ],
                interface_methods=["evaluate_telemetry", "inspect_framebuffer_buffer"]
            ),
            "agent_hermes_singularity": AgentCapabilityDescriptor(
                agent_id="agent_hermes_singularity",
                name="ANATHermesSingularity",
                role="Sovereign Unified Neural Entity",
                strand="HERMES_SOVEREIGN",
                description="Combines Nous Research Hermes 3 Neural Cortex with the 17-Node ANAT Explorable World Graph memory and Double Helix actuators.",
                capabilities=[
                    "Multi-turn sovereign agentic deliberation loop",
                    "Hermes 3 scratchpad reasoning & XML tool-calling parsing",
                    "17-Node ANAT memory substrate navigation across 5 sectors",
                    "Closed-form ROME Rank-One surgery & EWC memory consolidation",
                    "Actuator dispatch across engine, simulation, proofs, and filesystem"
                ],
                formal_invariants=[
                    "Proof ANAT.1: Modern Continuous Hopfield CCCP monotonic energy descent",
                    "Proof ANAT.2: Exact closed-form ROME rank-one parameter surgery identity"
                ],
                interface_methods=["think", "deliberate_and_act", "chat", "status"]
            ),
            "agent_7_workflow_auditor": AgentCapabilityDescriptor(
                agent_id="agent_7_workflow_auditor",
                name="WorkflowCapabilityAuditor",
                role="Workflow & Agent Capabilities Auditor",
                strand="CROSS_STRAND",
                description="Performs metacognitive auditing of upward slice workflows, parity gates, circuit breakers, and agent capability envelopes.",
                capabilities=[
                    "Dual-strand upward slice workflow & transition verification",
                    "Base Rung Parity Gate integrity & false promotion detection",
                    "Circuit breaker & self-healing remediation pipeline auditing",
                    "Agent capability introspection, dynamic probing, and gap analysis",
                    "ANAT cognitive trajectory workflow verification"
                ],
                formal_invariants=[
                    "Parity Gate Strictness: elev == True iff all empirical contracts satisfied",
                    "Circuit Breaker Bound: current_cycle <= max_cycles_per_tier",
                    "Theorem 4: Non-Ergodic Ruin Prevention & Absorbing Barrier Invariant P(ruin) = 0",
                    "Theorem 5: Cellular Sheaf Laplacian Algebraic Connectivity lambda_2(L_F) > 0 & Discord Dissipation",
                    "Theorem 6: Classical Linear Logic Session Duality, Confluence & Zero Token Leakage"
                ],
                interface_methods=["audit_workflow", "audit_agent_capabilities", "run_full_audit", "probe_agent"]
            )
        }

    # ========================================================================
    # 1. WORKFLOW AUDITING SPECIALIZATION
    # ========================================================================

    def audit_workflow(
        self,
        workflow_type: str = "dual_strand_upward_slice",
        state: Optional[HelixState] = None,
        execution_trace: Optional[List[Dict[str, Any]]] = None,
        anat_bridge: Optional[Any] = None
    ) -> WorkflowAuditReport:
        """Audits the dual-strand execution workflow for invariant violations and gate integrity.

        Args:
            workflow_type: Identifier of the target workflow (default: "dual_strand_upward_slice").
            state: Optional current HelixState snapshot.
            execution_trace: Optional list of step transitions/evaluations recorded during execution.
            anat_bridge: Optional ANATHelixBridge instance to inspect trajectory records.

        Returns:
            WorkflowAuditReport with violation analysis, integrity score, and recommendations.
        """
        report = WorkflowAuditReport(workflow_name=workflow_type)
        violations: List[str] = []
        warnings: List[str] = []
        step_audits: List[WorkflowStepAudit] = []

        # --- A. Audit State Invariants (if state provided) ---
        if state is not None:
            tier = state.get("tier", "UNKNOWN")
            current_cycle = state.get("current_cycle", 0)
            max_cycles = state.get("max_cycles_per_tier", 5)

            # Check Circuit Breaker Bound
            step_cb = WorkflowStepAudit(
                step_name="circuit_breaker_verification",
                tier=tier,
                invariants_checked=["cycle_count_within_bounds"]
            )
            if current_cycle > max_cycles:
                msg = f"Circuit breaker breached: current_cycle ({current_cycle}) > max_cycles_per_tier ({max_cycles}) at {tier}."
                step_cb.violations.append(msg)
                step_cb.passed = False
                report.circuit_breaker_healthy = False
                violations.append(msg)
            else:
                step_cb.metadata["cycle_utilization"] = f"{current_cycle}/{max_cycles}"
            step_audits.append(step_cb)

            # Check Tier-Specific Empirical Telemetry Invariants
            step_telemetry = WorkflowStepAudit(
                step_name="tier_telemetry_invariants",
                tier=tier,
                invariants_checked=[
                    "frame_time_budget",
                    "zero_allocations_in_loop",
                    "tunneling_immunity",
                    "visual_anomalies_zero",
                    "bot_crashes_zero"
                ]
            )

            frame_time = float(state.get("avg_frame_time_ms", 0.0))
            allocations = int(state.get("allocations_in_loop", 0))
            bot_crashes = int(state.get("headless_bot_crashes", 0))
            visual_anomalies = int(state.get("visual_anomalies", 0))
            spatial_valid = bool(state.get("spatial_invariants_valid", True))

            if tier == "CONVERGED":
                # In converged state, all contracts must be valid
                if frame_time > 16.6667:
                    msg = f"Converged state anomaly: frame time ({frame_time:.2f}ms) exceeds 16.6ms standard."
                    step_telemetry.violations.append(msg)
                    violations.append(msg)
                if allocations > 0:
                    msg = f"Converged state anomaly: {allocations} dynamic allocations in hot loop."
                    step_telemetry.violations.append(msg)
                    violations.append(msg)
                if bot_crashes > 0:
                    msg = f"Converged state anomaly: {bot_crashes} bot crashes recorded."
                    step_telemetry.violations.append(msg)
                    violations.append(msg)
                if visual_anomalies > 0:
                    msg = f"Converged state anomaly: {visual_anomalies} visual anomalies detected."
                    step_telemetry.violations.append(msg)
                    violations.append(msg)
                if not spatial_valid:
                    msg = "Converged state anomaly: spatial invariants marked invalid."
                    step_telemetry.violations.append(msg)
                    violations.append(msg)

            step_telemetry.passed = len(step_telemetry.violations) == 0
            step_audits.append(step_telemetry)

        # --- B. Audit Parity Gate Robustness via Boundary Stressing ---
        gate_audit = self._audit_parity_gates_integrity()
        step_audits.append(gate_audit)
        if not gate_audit.passed:
            violations.extend(gate_audit.violations)
        warnings.extend(gate_audit.warnings)

        # --- C. Audit Execution Trace History (if provided) ---
        if execution_trace:
            trace_audit = self._audit_execution_trace(execution_trace)
            step_audits.append(trace_audit)
            if not trace_audit.passed:
                violations.extend(trace_audit.violations)
            warnings.extend(trace_audit.warnings)

        # --- D. Audit ANAT Trajectory Workflow Integration (if provided) ---
        if anat_bridge is not None:
            anat_audit = self._audit_anat_workflow_integration(anat_bridge)
            step_audits.append(anat_audit)
            if not anat_audit.passed:
                violations.extend(anat_audit.violations)
            warnings.extend(anat_audit.warnings)

        # Compute integrity score
        total_checks = sum(len(s.invariants_checked) for s in step_audits)
        total_violations = len(violations)
        integrity_score = max(0.0, 100.0 - (total_violations * 20.0))

        report.steps_audited = len(step_audits)
        report.step_results = step_audits
        report.violations_count = total_violations
        report.warnings_count = len(warnings)
        report.violations = violations
        report.warnings = warnings
        report.parity_gate_integrity_score = integrity_score
        report.passed = (total_violations == 0)

        # Generate workflow recommendations
        if total_violations > 0:
            report.recommendations.append("Apply Trajectory E ROME Rank-One surgery to repair failed invariant parameters.")
            report.recommendations.append("Check circuit breaker cycle counter reset semantics upon tier elevation.")
        if len(warnings) > 0:
            report.recommendations.append("Profile latency in dual-strand gather to optimize tick synchronization.")
        if not report.recommendations:
            report.recommendations.append("All workflow invariants verified: dual-strand synchronization is fully compliant.")

        return report

    def _audit_parity_gates_integrity(self) -> WorkflowStepAudit:
        """Stresses evaluate_base_rung with synthetic boundary vectors to verify gate strictness."""
        from doublehelix.orchestrator.parity_gates import evaluate_base_rung
        audit = WorkflowStepAudit(
            step_name="parity_gate_stress_audit",
            invariants_checked=[
                "level_1_budget_rejection",
                "level_1_alloc_rejection",
                "level_2_tunneling_rejection",
                "level_2_spatial_proof_rejection",
                "level_3_shader_rejection",
                "level_3_visual_anomaly_rejection",
                "level_4_bot_crash_rejection",
                "unknown_tier_rejection"
            ]
        )

        test_cases = [
            ("LEVEL_1_KERNEL", {"spatial_invariants_valid": True}, {"avg_frame_time_ms": 17.5, "allocations_in_loop": 0}, False, "Frame time > 16.6ms did not fail Level 1"),
            ("LEVEL_1_KERNEL", {"spatial_invariants_valid": True}, {"avg_frame_time_ms": 12.0, "allocations_in_loop": 3}, False, "Allocations > 0 did not fail Level 1"),
            ("LEVEL_1_KERNEL", {"spatial_invariants_valid": True}, {"avg_frame_time_ms": 10.0, "allocations_in_loop": 0}, True, "Valid Level 1 telemetry was falsely rejected"),
            ("LEVEL_2_ECS", {"spatial_invariants_valid": True}, {"tunneling_errors": 1}, False, "Tunneling errors > 0 did not fail Level 2"),
            ("LEVEL_2_ECS", {"spatial_invariants_valid": False}, {"tunneling_errors": 0}, False, "Invalid spatial proof did not fail Level 2"),
            ("LEVEL_2_ECS", {"spatial_invariants_valid": True}, {"tunneling_errors": 0}, True, "Valid Level 2 telemetry was falsely rejected"),
            ("LEVEL_3_RENDER", {}, {"shader_errors": 1, "visual_anomalies": 0}, False, "Shader errors did not fail Level 3"),
            ("LEVEL_3_RENDER", {}, {"shader_errors": 0, "visual_anomalies": 2}, False, "Visual anomalies did not fail Level 3"),
            ("LEVEL_3_RENDER", {}, {"shader_errors": 0, "visual_anomalies": 0}, True, "Valid Level 3 telemetry was falsely rejected"),
            ("LEVEL_4_PLAYTEST", {}, {"headless_bot_crashes": 1}, False, "Bot crashes did not fail Level 4"),
            ("LEVEL_4_PLAYTEST", {}, {"headless_bot_crashes": 0}, True, "Valid Level 4 telemetry was falsely rejected"),
            ("INVALID_TIER", {}, {}, False, "Invalid tier string was not rejected")
        ]

        for tier, alpha, beta, expected_elevate, error_desc in test_cases:
            elevate, reason = evaluate_base_rung(tier, alpha, beta)
            if elevate != expected_elevate:
                audit.violations.append(f"Parity Gate Flaw at {tier}: {error_desc}. (Evaluated: elevate={elevate}, reason={reason})")

        audit.passed = len(audit.violations) == 0
        return audit

    def _audit_execution_trace(self, trace: List[Dict[str, Any]]) -> WorkflowStepAudit:
        """Validates that a historical execution trace ascended sequentially without skips."""
        audit = WorkflowStepAudit(
            step_name="execution_trace_chronology",
            invariants_checked=["sequential_tier_ascension", "cycle_reset_on_ascend"]
        )

        seen_tiers: List[str] = []
        for i, entry in enumerate(trace):
            tier = entry.get("tier")
            if tier and (not seen_tiers or seen_tiers[-1] != tier):
                seen_tiers.append(tier)

        # Check sequential ordering in ASCENDING_TIERS
        tier_indices = [ASCENDING_TIERS.index(t) for t in seen_tiers if t in ASCENDING_TIERS]
        for idx in range(len(tier_indices) - 1):
            curr, next_val = tier_indices[idx], tier_indices[idx + 1]
            if next_val != curr + 1:
                audit.violations.append(
                    f"Non-sequential tier ascension detected: {seen_tiers[idx]} -> {seen_tiers[idx + 1]} (Jump index {curr} to {next_val})"
                )

        audit.passed = len(audit.violations) == 0
        audit.metadata["observed_tier_sequence"] = seen_tiers
        return audit

    def _audit_anat_workflow_integration(self, anat_bridge: Any) -> WorkflowStepAudit:
        """Audits ANAT cognitive trajectories and milestone recording."""
        audit = WorkflowStepAudit(
            step_name="anat_cognitive_trajectories",
            invariants_checked=[
                "milestone_triples_integrity",
                "telemetry_surprise_flow",
                "trajectory_e_rome_surgery_available"
            ]
        )

        triples = getattr(anat_bridge, "milestone_triples", [])
        if not triples:
            audit.warnings.append("ANAT bridge has no recorded milestone triples.")
        else:
            audit.metadata["milestone_count"] = len(triples)

        # Verify that Trajectory E ROME surgery can compute rank-one updates
        try:
            import numpy as np
            from doublehelix.anat.trajectories import TrajectoryController
            from doublehelix.anat.world_graph import ExplorableWorldGraph
            graph = getattr(anat_bridge, "world_graph", None) or ExplorableWorldGraph()
            tc = TrajectoryController(graph)
            k_star = np.ones(64, dtype=np.float32)
            v_star = np.ones(64, dtype=np.float32) * 2.0
            res = tc.run_trajectory_e(key_vector=k_star, target_value=v_star)
            if not res.get("rank_one_identity_verified", False):
                audit.violations.append("Trajectory E ROME rank-one surgery identity failed analytical verification.")
        except Exception as e:
            audit.violations.append(f"Failed executing Trajectory E audit probe: {e}")

        audit.passed = len(audit.violations) == 0
        return audit

    # ========================================================================
    # 2. AGENT CAPABILITIES AUDITING SPECIALIZATION
    # ========================================================================

    def get_registered_descriptors(self) -> Dict[str, AgentCapabilityDescriptor]:
        """Returns the dictionary of canonical agent capability descriptors."""
        return self._descriptors.copy()

    def audit_agent_capabilities(
        self,
        agents_map: Optional[Dict[str, Any]] = None,
        run_probes: bool = True
    ) -> CapabilityAuditReport:
        """Audits all registered and live agents, validating interface compliance and capability boundaries.

        Args:
            agents_map: Optional mapping of agent_id -> agent instance.
            run_probes: Whether to execute empirical calibration probes against agents.

        Returns:
            CapabilityAuditReport detailing health, maturity index, probe outcomes, and gaps.
        """
        report = CapabilityAuditReport()
        agents_to_audit = agents_map or {}
        probe_results: List[CapabilityProbeResult] = []

        # Populate descriptors
        for agent_id, desc in self._descriptors.items():
            report.agent_descriptors[agent_id] = desc.model_copy()

        # Check interface compliance of any provided live instances
        for agent_id, agent_instance in agents_to_audit.items():
            desc = report.agent_descriptors.get(agent_id)
            if not desc:
                # Dynamically construct descriptor for custom agent
                desc = AgentCapabilityDescriptor(
                    agent_id=agent_id,
                    name=agent_instance.__class__.__name__,
                    role="Custom Agent",
                    strand="CUSTOM",
                    description=getattr(agent_instance, "__doc__", "Custom Agent") or "Custom Agent",
                    interface_methods=[
                        m for m in dir(agent_instance)
                        if callable(getattr(agent_instance, m)) and not m.startswith("_")
                    ]
                )
                report.agent_descriptors[agent_id] = desc

            # Check expected interface methods
            missing_methods = []
            for method in desc.interface_methods:
                if not hasattr(agent_instance, method) or not callable(getattr(agent_instance, method)):
                    missing_methods.append(method)

            if missing_methods:
                desc.status = "DEGRADED"
                report.gap_analysis.append(
                    f"Agent {agent_id} ({desc.name}) missing required interface methods: {missing_methods}"
                )
            else:
                desc.status = "HEALTHY"

        # Execute dynamic probes if requested
        if run_probes:
            probes = self._execute_capability_probes(agents_to_audit)
            probe_results.extend(probes)

        # Tally statistics
        total = len(report.agent_descriptors)
        passed_probes = sum(1 for p in probe_results if p.passed)
        failed_probes = sum(1 for p in probe_results if not p.passed)

        healthy = sum(1 for d in report.agent_descriptors.values() if d.status == "HEALTHY")
        degraded = sum(1 for d in report.agent_descriptors.values() if d.status == "DEGRADED")
        failed = sum(1 for d in report.agent_descriptors.values() if d.status == "FAILED")

        # Capability Maturity Score: 50% interface & descriptor coverage + 50% probe pass rate
        probe_score = (passed_probes / max(1, len(probe_results))) * 50.0 if probe_results else 50.0
        health_score = (healthy / max(1, total)) * 50.0
        cmi = round(probe_score + health_score, 2)

        report.total_agents = total
        report.healthy_agents = healthy
        report.degraded_agents = degraded
        report.failed_agents = failed
        report.capability_maturity_score = cmi
        report.probes_run = len(probe_results)
        report.probes_passed = passed_probes
        report.probe_results = probe_results

        # Recommendations based on gaps
        if degraded > 0 or failed > 0:
            report.recommendations.append("Remediate degraded agent interfaces to ensure all interface contracts are implemented.")
        if failed_probes > 0:
            report.recommendations.append("Investigate empirical probe failures in Strand Beta profilers or Strand Alpha synthesizers.")
        if not report.recommendations:
            report.recommendations.append("All agent capabilities verified: full operational capability envelope confirmed.")

        return report

    def _execute_capability_probes(self, live_agents: Dict[str, Any]) -> List[CapabilityProbeResult]:
        """Executes empirical non-destructive probe benchmarks against agent capability contracts."""
        probes: List[CapabilityProbeResult] = []

        # Probe 1: FrameTimeMemoryProfiler
        t0 = time.perf_counter()
        try:
            from doublehelix.agents.strand_beta.frame_profiler import FrameTimeMemoryProfiler
            profiler = live_agents.get("agent_5_frame_profiler") or FrameTimeMemoryProfiler()
            valid_res = profiler.evaluate_telemetry({"avg_frame_time_ms": 11.2, "allocations_in_loop": 0})
            invalid_res = profiler.evaluate_telemetry({"avg_frame_time_ms": 25.0, "allocations_in_loop": 2})

            passed = (valid_res["passed"] is True and invalid_res["passed"] is False and len(invalid_res["issues"]) == 2)
            probes.append(CapabilityProbeResult(
                agent_id="agent_5_frame_profiler",
                probe_name="frame_profiler_contract_discrimination",
                passed=passed,
                latency_ms=(time.perf_counter() - t0) * 1000,
                details="Verified discrimination between compliant frame-budget and breached allocation/time telemetry."
            ))
        except Exception as e:
            probes.append(CapabilityProbeResult(
                agent_id="agent_5_frame_profiler",
                probe_name="frame_profiler_contract_discrimination",
                passed=False,
                latency_ms=(time.perf_counter() - t0) * 1000,
                details=f"Probe exception: {e}",
                issues=[str(e)]
            ))

        # Probe 2: VisualContractAuditor
        t0 = time.perf_counter()
        try:
            from doublehelix.agents.strand_beta.visual_auditor import VisualContractAuditor
            auditor = live_agents.get("agent_6_visual_auditor") or VisualContractAuditor()
            clean_res = auditor.evaluate_telemetry({"shader_errors": 0, "visual_anomalies": 0})
            dirty_res = auditor.evaluate_telemetry({"shader_errors": 1, "visual_anomalies": 3})
            buf_res = auditor.inspect_framebuffer_buffer(b"", 10, 10)  # Empty buffer must return error 1

            passed = (clean_res["passed"] is True and dirty_res["passed"] is False and buf_res == 1)
            probes.append(CapabilityProbeResult(
                agent_id="agent_6_visual_auditor",
                probe_name="visual_contract_anomaly_detection",
                passed=passed,
                latency_ms=(time.perf_counter() - t0) * 1000,
                details="Verified offscreen buffer boundary inspection and shader compilation failure aggregation."
            ))
        except Exception as e:
            probes.append(CapabilityProbeResult(
                agent_id="agent_6_visual_auditor",
                probe_name="visual_contract_anomaly_detection",
                passed=False,
                latency_ms=(time.perf_counter() - t0) * 1000,
                details=f"Probe exception: {e}",
                issues=[str(e)]
            ))

        # Probe 3: HeadlessPlaytestAgent
        t0 = time.perf_counter()
        try:
            from doublehelix.agents.strand_beta.playtest_bot import HeadlessPlaytestAgent
            bot_agent = live_agents.get("agent_4_playtest_bot") or HeadlessPlaytestAgent()
            payload = bot_agent.build_fuzz_payload(ticks=500)
            telemetry_pass = bot_agent.evaluate_bot_telemetry({"headless_bot_crashes": 0})
            telemetry_fail = bot_agent.evaluate_bot_telemetry({"headless_bot_crashes": 4})

            passed = (
                payload.get("ticks") == 500 and
                telemetry_pass.get("fuzz_passed") is True and
                telemetry_fail.get("fuzz_passed") is False
            )
            probes.append(CapabilityProbeResult(
                agent_id="agent_4_playtest_bot",
                probe_name="fuzz_schedule_and_crash_detection",
                passed=passed,
                latency_ms=(time.perf_counter() - t0) * 1000,
                details="Verified fuzz payload scheduling, stochastic monkey modes, and bot crash evaluation."
            ))
        except Exception as e:
            probes.append(CapabilityProbeResult(
                agent_id="agent_4_playtest_bot",
                probe_name="fuzz_schedule_and_crash_detection",
                passed=False,
                latency_ms=(time.perf_counter() - t0) * 1000,
                details=f"Probe exception: {e}",
                issues=[str(e)]
            ))

        # Probe 4: SystemCoderAgent Code Extraction
        t0 = time.perf_counter()
        try:
            from doublehelix.agents.strand_alpha.system_coder import SystemCoderAgent
            sample_markdown = "Here is the implementation:\n```python\ndef tick():\n    pass\n```\nAll done."
            extracted = SystemCoderAgent.extract_code(sample_markdown)
            passed = (extracted == "def tick():\n    pass")
            probes.append(CapabilityProbeResult(
                agent_id="agent_2_system_coder",
                probe_name="system_coder_fence_extraction",
                passed=passed,
                latency_ms=(time.perf_counter() - t0) * 1000,
                details="Verified markdown code fence extraction and sanitization without artifacts."
            ))
        except Exception as e:
            probes.append(CapabilityProbeResult(
                agent_id="agent_2_system_coder",
                probe_name="system_coder_fence_extraction",
                passed=False,
                latency_ms=(time.perf_counter() - t0) * 1000,
                details=f"Probe exception: {e}",
                issues=[str(e)]
            ))

        # Probe 5: Hermes Tool Registry & Tag Parsing
        t0 = time.perf_counter()
        try:
            from doublehelix.hermes.client import HermesClient
            client = HermesClient()
            raw_text = "<scratchpad>Evaluating zero-alloc contract...</scratchpad><tool_call>{\"name\": \"advance_helix_slice\", \"arguments\": {}}</tool_call>Ready."
            tools, scratch, clean = client.parse_hermes_response(raw_text)
            passed = (
                scratch == "Evaluating zero-alloc contract..." and
                len(tools) == 1 and
                tools[0]["name"] == "advance_helix_slice" and
                clean == "Ready."
            )
            probes.append(CapabilityProbeResult(
                agent_id="agent_hermes_singularity",
                probe_name="hermes_tag_parsing_and_tool_dispatch",
                passed=passed,
                latency_ms=(time.perf_counter() - t0) * 1000,
                details="Verified Hermes 3 scratchpad reasoning tags and XML tool call extraction."
            ))
        except Exception as e:
            probes.append(CapabilityProbeResult(
                agent_id="agent_hermes_singularity",
                probe_name="hermes_tag_parsing_and_tool_dispatch",
                passed=False,
                latency_ms=(time.perf_counter() - t0) * 1000,
                details=f"Probe exception: {e}",
                issues=[str(e)]
            ))

        # Probe 6: Windkessel Elasticity Low-Pass Filtering
        t0 = time.perf_counter()
        try:
            from doublehelix.runtime.elasticity import ElasticRuntimeWindkessel, WindkesselConfig
            wk = ElasticRuntimeWindkessel(WindkesselConfig(compliance=2.0, resistance=0.5))
            att_low = wk.power_spectral_amplification(1.0)
            att_high = wk.power_spectral_amplification(20.0)
            passed = (att_low < 1.0 and att_high < 0.01 and wk.Q_max > 0)
            probes.append(CapabilityProbeResult(
                agent_id="agent_7_workflow_auditor",
                probe_name="windkessel_elasticity_frequency_attenuation",
                passed=passed,
                latency_ms=(time.perf_counter() - t0) * 1000,
                details="Verified somatic vascular compliance C_r and high-frequency task burst attenuation O(w^-2)."
            ))
        except Exception as e:
            probes.append(CapabilityProbeResult(
                agent_id="agent_7_workflow_auditor",
                probe_name="windkessel_elasticity_frequency_attenuation",
                passed=False,
                latency_ms=(time.perf_counter() - t0) * 1000,
                details=f"Probe exception: {e}",
                issues=[str(e)]
            ))

        # Probe 7: Nirodha Active Inference Divergence Reset
        t0 = time.perf_counter()
        try:
            import numpy as np
            from doublehelix.runtime.elasticity import ActiveInferenceNirodhaEngine, NirodhaResetConfig
            ne = ActiveInferenceNirodhaEngine(NirodhaResetConfig(theta_reset=2.0))
            low_e = ne.compute_free_energy_surrogate(np.array([1.0, 1.0]), np.array([1.0, 1.0]))
            trig_low, _ = ne.evaluate_cessation_trigger(low_e)
            high_e = ne.compute_free_energy_surrogate(np.array([10.0, 10.0]), np.array([1.0, 1.0]))
            trig_high, _ = ne.evaluate_cessation_trigger(high_e)
            pruned = ne.execute_nirodha_reset({"goal": "60 FPS", "scratchpad": "stale reflection"})
            passed = (trig_low is False and trig_high is True and "scratchpad" not in pruned)
            probes.append(CapabilityProbeResult(
                agent_id="agent_7_workflow_auditor",
                probe_name="nirodha_active_inference_divergence_reset",
                passed=passed,
                latency_ms=(time.perf_counter() - t0) * 1000,
                details="Verified free energy surrogate E_t evaluation and recursive monologue context cessation."
            ))
        except Exception as e:
            probes.append(CapabilityProbeResult(
                agent_id="agent_7_workflow_auditor",
                probe_name="nirodha_active_inference_divergence_reset",
                passed=False,
                latency_ms=(time.perf_counter() - t0) * 1000,
                details=f"Probe exception: {e}",
                issues=[str(e)]
            ))

        # Probe 8: Causal Laplacian Consensus & Non-Causal Annihilation
        t0 = time.perf_counter()
        try:
            import numpy as np
            from doublehelix.runtime.elasticity import CausalLaplacianConsensus
            adj_connected = np.array([[0.0, 1.0], [1.0, 0.0]])
            adj_disconnected = np.array([[0.0, 0.0], [0.0, 0.0]])
            res_conn = CausalLaplacianConsensus.verify_consensus_viability(adj_connected)
            res_disc = CausalLaplacianConsensus.verify_consensus_viability(adj_disconnected)
            passed = (res_conn["causally_connected"] is True and res_disc["causally_connected"] is False)
            probes.append(CapabilityProbeResult(
                agent_id="agent_7_workflow_auditor",
                probe_name="causal_laplacian_consensus_spectral_gap",
                passed=passed,
                latency_ms=(time.perf_counter() - t0) * 1000,
                details="Verified algebraic connectivity lambda_2(L) > 0 and annihilation of uncoupled DAT consensus."
            ))
        except Exception as e:
            probes.append(CapabilityProbeResult(
                agent_id="agent_7_workflow_auditor",
                probe_name="causal_laplacian_consensus_spectral_gap",
                passed=False,
                latency_ms=(time.perf_counter() - t0) * 1000,
                details=f"Probe exception: {e}",
                issues=[str(e)]
            ))

        # Probe 9: Ergodicity Ruin Gate & Absorbing Barrier Invariant
        t0 = time.perf_counter()
        try:
            from doublehelix.runtime.decision_core import OutlierEngineeredDecisionCore, ActionCandidate
            core = OutlierEngineeredDecisionCore()
            actions = [
                ActionCandidate(
                    action_id="ruinous_action",
                    description="High EV but absorbs ruin",
                    expected_yield=2.0,
                    ruin_probability=0.10
                ),
                ActionCandidate(
                    action_id="safe_action",
                    description="Consistent growth without ruin",
                    expected_yield=0.20,
                    ruin_probability=0.0
                )
            ]
            chosen, rollout_results = core.evaluate_and_decide(actions)
            ruin_filtered = any(r.action_id == "ruinous_action" and r.ruin_detected for r in rollout_results)
            safe_chosen = (chosen is not None and chosen.action_id == "safe_action")
            passed = ruin_filtered and safe_chosen
            probes.append(CapabilityProbeResult(
                agent_id="agent_7_workflow_auditor",
                probe_name="ergodicity_ruin_gate_absorbing_barrier",
                passed=passed,
                latency_ms=(time.perf_counter() - t0) * 1000,
                details="Verified absorbing barrier invariant: eliminated high-EV ruinous action in favor of ergodic viable action."
            ))
        except Exception as e:
            probes.append(CapabilityProbeResult(
                agent_id="agent_7_workflow_auditor",
                probe_name="ergodicity_ruin_gate_absorbing_barrier",
                passed=False,
                latency_ms=(time.perf_counter() - t0) * 1000,
                details=f"Probe exception: {e}",
                issues=[str(e)]
            ))

        # Probe 10: Cellular Sheaf Laplacian & Discord Dissipation
        t0 = time.perf_counter()
        try:
            import numpy as np
            from doublehelix.runtime.sheaf_sophi import GrothendieckCellularSheaf
            sheaf = GrothendieckCellularSheaf(node_ids=["a1", "a2", "a3"], stalk_dim=2)
            sheaf.add_edge("a1", "a2", "e12")
            sheaf.add_edge("a2", "a3", "e23")
            sheaf.add_edge("a3", "a1", "e31")
            spectral = sheaf.spectral_analysis()
            gap = spectral["spectral_gap_lambda2"]

            # Energy dissipation
            x0 = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]], dtype=np.float64)
            e0 = sheaf.dirichlet_energy(x0)
            x_step = sheaf.dissipate_discord_step(x0, eta=0.1)
            e1 = sheaf.dirichlet_energy(x_step)

            passed = (gap > 1e-4) and (e1 < e0)
            probes.append(CapabilityProbeResult(
                agent_id="agent_7_workflow_auditor",
                probe_name="cellular_sheaf_laplacian_dirichlet_decay",
                passed=passed,
                latency_ms=(time.perf_counter() - t0) * 1000,
                details="Verified algebraic connectivity lambda_2(L_F) > 0 and monotonic Sheaf Dirichlet energy dissipation."
            ))
        except Exception as e:
            probes.append(CapabilityProbeResult(
                agent_id="agent_7_workflow_auditor",
                probe_name="cellular_sheaf_laplacian_dirichlet_decay",
                passed=False,
                latency_ms=(time.perf_counter() - t0) * 1000,
                details=f"Probe exception: {e}",
                issues=[str(e)]
            ))

        # Probe 11: Linear Session Channel Confluence & Zero Token Leakage
        t0 = time.perf_counter()
        try:
            from doublehelix.runtime.sheaf_sophi import LinearSessionChannel
            channel = LinearSessionChannel(channel_id="probe_11_channel")
            res = channel.execute_transaction({"cmd": "echo", "arg": "sophi"}, lambda req: {"reply": f"ack_{req['arg']}"})
            no_leakage = (channel.client.linear_tokens == 0 and channel.server.linear_tokens == 0)
            confluent = (res.get("reply") == "ack_sophi")
            passed = no_leakage and confluent
            probes.append(CapabilityProbeResult(
                agent_id="agent_7_workflow_auditor",
                probe_name="linear_session_channel_confluence_and_zero_leakage",
                passed=passed,
                latency_ms=(time.perf_counter() - t0) * 1000,
                details="Verified Classical Linear Logic dual cut elimination, confluence, and zero capability token leakage."
            ))
        except Exception as e:
            probes.append(CapabilityProbeResult(
                agent_id="agent_7_workflow_auditor",
                probe_name="linear_session_channel_confluence_and_zero_leakage",
                passed=False,
                latency_ms=(time.perf_counter() - t0) * 1000,
                details=f"Probe exception: {e}",
                issues=[str(e)]
            ))

        return probes

    # ========================================================================
    # 3. UNIFIED FULL SYSTEM AUDIT
    # ========================================================================

    def run_full_audit(
        self,
        state: Optional[HelixState] = None,
        execution_trace: Optional[List[Dict[str, Any]]] = None,
        anat_bridge: Optional[Any] = None,
        agents_map: Optional[Dict[str, Any]] = None,
        run_probes: bool = True
    ) -> SystemAuditReport:
        """Executes a full metacognitive audit across both workflows and agent capabilities.

        Returns:
            SystemAuditReport containing consolidated findings, scores, and remediation roadmap.
        """
        workflow_audit = self.audit_workflow(
            state=state,
            execution_trace=execution_trace,
            anat_bridge=anat_bridge
        )
        capability_audit = self.audit_agent_capabilities(
            agents_map=agents_map,
            run_probes=run_probes
        )

        # Composite overall score: 50% workflow integrity + 50% capability maturity
        overall_score = round(
            (workflow_audit.parity_gate_integrity_score * 0.5) +
            (capability_audit.capability_maturity_score * 0.5),
            2
        )

        # Overall Status
        if workflow_audit.passed and capability_audit.failed_agents == 0 and capability_audit.probes_passed == capability_audit.probes_run:
            status = "HEALTHY"
        elif workflow_audit.violations_count > 0 or capability_audit.failed_agents > 0:
            status = "CRITICAL"
        else:
            status = "WARNING"

        critical_findings: List[str] = []
        critical_findings.extend(workflow_audit.violations)
        critical_findings.extend(capability_audit.gap_analysis)

        summary = (
            f"Double Helix Metacognitive Audit Completed. Status: {status} (Score: {overall_score}%). "
            f"Workflows: {'PASS' if workflow_audit.passed else 'FAIL'} (Gate Integrity: {workflow_audit.parity_gate_integrity_score}%, Violations: {workflow_audit.violations_count}). "
            f"Agent Capabilities: {capability_audit.healthy_agents}/{capability_audit.total_agents} healthy, "
            f"{capability_audit.probes_passed}/{capability_audit.probes_run} empirical calibration probes passed "
            f"(CMI: {capability_audit.capability_maturity_score}%)."
        )

        roadmap: List[str] = []
        roadmap.extend(workflow_audit.recommendations)
        roadmap.extend(capability_audit.recommendations)
        # Deduplicate while preserving order
        dedup_roadmap = list(dict.fromkeys(roadmap))

        return SystemAuditReport(
            overall_status=status,
            overall_score=overall_score,
            workflow_audit=workflow_audit,
            capability_audit=capability_audit,
            executive_summary=summary,
            critical_findings=critical_findings,
            remediation_roadmap=dedup_roadmap
        )

    # ========================================================================
    # 4. COGNITIVE REASONING EXTENSION (LLM-ASSISTED AUDIT)
    # ========================================================================

    async def cognitive_audit_trace(
        self,
        workflow_report: WorkflowAuditReport,
        capability_report: CapabilityAuditReport
    ) -> str:
        """Invokes the Reasoning LLM for deep cognitive analysis of audit telemetry and edge cases."""
        if not self.reasoning_client:
            return "Cognitive LLM client not configured; deterministic empirical audit conclusive."

        prompt = f"""Audit Telemetry Report:
Workflow Status: {'PASS' if workflow_report.passed else 'FAIL'}
Workflow Gate Integrity: {workflow_report.parity_gate_integrity_score}%
Workflow Violations: {workflow_report.violations}
Workflow Warnings: {workflow_report.warnings}

Capability Maturity Index: {capability_report.capability_maturity_score}%
Probes: {capability_report.probes_passed}/{capability_report.probes_run} passed
Agent Gaps: {capability_report.gap_analysis}

Perform metacognitive analysis on potential hidden race conditions, subtle zero-allocation leaks,
and recommend architectural enhancements for the Double Helix upwards slice."""

        messages = [
            {"role": "system", "content": AUDITOR_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
        return await self.reasoning_client.chat_completion(messages, temperature=0.0)
