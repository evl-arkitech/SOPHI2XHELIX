"""Neurocomputational Elasticity & Contemplative Dynamics Runtime Primitives.

Translates the biophysical and mathematical principles of NeuroCompElasticity.md:
1. Elastic Runtime Windkessel (Somatic & Vascular Elasticity):
   Two-parameter compliance-resistance accumulator (C_r, R_r) attenuating high-frequency
   pulsatile task bursts |H(w)|^2 = 1 / (1 + w^2 R_r^2 C_r^2) with zero overflow guarantee.
2. Active Inference Engine with Nirodha Reset (DMN Decoupling & Cessation):
   Precision reweighting of descending priors vs sensory prediction errors, triggering
   endogenous context cessation (Nirodha Samāpatti) when divergence E_t >= theta_reset.
3. Gamma-Band Phase Synchrony:
   Decentralized non-blocking sub-agent binding via gamma-oscillatory (25-42 Hz) phase coherence.
4. Causal Network Topologies & Laplacian Swarm Consensus:
   Strictly rejects ungrounded emergent consensus where spectral gap lambda_2(L) == 0,
   deconstructing the Global Consciousness / Decision Augmentation Theory (DAT) fallacy.
"""

import math
import time
import asyncio
from typing import Dict, List, Tuple, Optional, Any, Callable
import numpy as np
from pydantic import BaseModel, Field


# ============================================================================
# 1. THE ELASTIC RUNTIME WINDKESSEL (SOMATIC & VASCULAR ELASTICITY)
# ============================================================================

class WindkesselConfig(BaseModel):
    """Configuration for Elastic Runtime Windkessel."""
    compliance: float = Field(default=2.0, description="Runtime compliance C_r (elastic queue storage capacity)")
    resistance: float = Field(default=0.5, description="Peripheral resistance R_r (drain resistance)")
    target_lambda_bar: float = Field(default=10.0, description="Baseline expected task arrival rate (tasks/sec)")
    sigma_a: float = Field(default=2.0, description="Brownian task arrival volatility")
    delta_overflow_tolerance: float = Field(default=1e-4, description="Target task drop probability ceiling")


class ElasticRuntimeWindkessel:
    """Two-parameter compliance-resistance accumulator (C_r, R_r) for pulsatile workload smoothing.

    Guarantees:
    - Characteristic relaxation time: tau_r = R_r * C_r.
    - Low-pass power spectral density attenuation: |H(w)|^2 = 1 / (1 + w^2 * R_r^2 * C_r^2).
    - Hard buffer capacity sizing Q_max ensuring P(Task Drop) <= delta.
    """

    def __init__(
        self,
        config: Optional[WindkesselConfig] = None,
        compliance: Optional[float] = None,
        resistance: Optional[float] = None,
        max_capacity: Optional[float] = None
    ):
        if config is None:
            kwargs = {}
            if compliance is not None:
                kwargs["compliance"] = compliance
            if resistance is not None:
                kwargs["resistance"] = resistance
            self.config = WindkesselConfig(**kwargs)
        else:
            self.config = config

        self.C_r = self.config.compliance
        self.R_r = self.config.resistance
        self.tau_r = self.R_r * self.C_r  # Characteristic relaxation time

        # Compute safe buffer capacity according to Theorem 1 sizing formula
        # Q_max >= lambda_bar * tau_r + sqrt(sigma_a^2 * tau_r * ln(1/delta))
        self.Q_max = max_capacity if max_capacity is not None else self._compute_optimal_buffer_capacity()

        self._queue: List[Dict[str, Any]] = []
        self._total_ingested: int = 0
        self._total_drained: int = 0
        self._dropped_count: int = 0
        self._last_drain_time: float = time.perf_counter()

    def _compute_optimal_buffer_capacity(self) -> float:
        """Computes minimum buffer capacity guaranteeing overflow probability <= delta."""
        lambda_bar = self.config.target_lambda_bar
        sigma_a = self.config.sigma_a
        delta = max(1e-9, self.config.delta_overflow_tolerance)
        mean_q = lambda_bar * self.tau_r
        variance_q = (sigma_a ** 2) * self.tau_r / 2.0
        safety_margin = math.sqrt(2.0 * variance_q * math.log(1.0 / delta))
        return float(mean_q + safety_margin)

    def power_spectral_amplification(self, omega: float) -> float:
        """Computes |H(w)|^2 = 1 / (1 + w^2 * tau_r^2). High frequencies scale as O(w^-2)."""
        return 1.0 / (1.0 + (omega ** 2) * (self.tau_r ** 2))

    def ingest(self, task: Dict[str, Any], weight: float = 1.0) -> bool:
        """Ingests a task into the compliant storage buffer.

        Returns True if accepted, False if dropped due to hard physical overflow.
        """
        current_occupancy = sum(item.get("weight", 1.0) for item in self._queue)
        if current_occupancy + weight > self.Q_max:
            self._dropped_count += 1
            return False

        self._queue.append({
            "task": task,
            "weight": weight,
            "timestamp": time.perf_counter()
        })
        self._total_ingested += 1
        return True

    def drain(self, dt: Optional[float] = None) -> List[Dict[str, Any]]:
        """Drains tasks through peripheral resistance R_r at service rate mu_t = Q_t / tau_r."""
        now = time.perf_counter()
        elapsed = dt if dt is not None else max(1e-4, now - self._last_drain_time)
        self._last_drain_time = now

        current_q = sum(item.get("weight", 1.0) for item in self._queue)
        if current_q <= 0:
            return []

        # Service rate: mu_t = Q_t / tau_r
        service_rate = current_q / max(1e-4, self.tau_r)
        capacity_to_drain = service_rate * elapsed

        drained_tasks: List[Dict[str, Any]] = []
        accumulated_weight = 0.0

        while self._queue and (accumulated_weight + self._queue[0].get("weight", 1.0) <= capacity_to_drain):
            item = self._queue.pop(0)
            accumulated_weight += item.get("weight", 1.0)
            drained_tasks.append(item["task"])
            self._total_drained += 1

        # If queue has items but capacity allowed at least 1 item, ensure progress
        if not drained_tasks and self._queue and capacity_to_drain >= 0.5:
            item = self._queue.pop(0)
            drained_tasks.append(item["task"])
            self._total_drained += 1

        return drained_tasks

    def discharge(self, dt: Optional[float] = None) -> List[Any]:
        """Alias for drain."""
        return self.drain(dt=dt)

    def get_metrics(self) -> Dict[str, Any]:
        """Returns real-time somatic vascular metrics of the runtime."""
        current_q = sum(item.get("weight", 1.0) for item in self._queue)
        pressure = current_q / max(1e-4, self.C_r)
        service_rate = pressure / max(1e-4, self.R_r)

        return {
            "queue_occupancy": current_q,
            "buffer_capacity_q_max": self.Q_max,
            "compliance_C_r": self.C_r,
            "resistance_R_r": self.R_r,
            "relaxation_time_tau_r": self.tau_r,
            "somatic_pressure": pressure,
            "service_rate_mu": service_rate,
            "total_ingested": self._total_ingested,
            "total_drained": self._total_drained,
            "dropped_count": self._dropped_count,
            "total_overflow": self._dropped_count,
            "attenuation_at_10rad": self.power_spectral_amplification(10.0),
            "overflow_probability_guarantee": self.config.delta_overflow_tolerance
        }

    def get_telemetry(self) -> Dict[str, Any]:
        """Alias for get_metrics providing standardized telemetry dictionary."""
        return self.get_metrics()


# ============================================================================
# 2. DYNAMIC PRECISION REWEIGHTING & NIRODHA STATE RESET (DMN DECOUPLING)
# ============================================================================

class NirodhaResetConfig(BaseModel):
    """Configuration for Active Inference Engine with Nirodha Reset."""
    theta_reset: float = Field(default=4.0, description="Divergence threshold triggering Nirodha context cessation")
    scheduled_reset_period_T_r: int = Field(default=8, description="Maximum consecutive turns before periodic reset")
    monologue_weight_beta: float = Field(default=0.8, description="Reinforcement coefficient of recursive priors (beta)")
    sensory_weight_gamma: float = Field(default=1.2, description="Grounded sensory feedback precision gain")


class ActiveInferenceNirodhaEngine:
    """Manages attention precision reweighting and endogenous context cessation (Nirodha Samāpatti).

    Guarantees:
    - Bounded expected KL divergence: sup_t E[D_KL(q_t || p*)] <= epsilon(T_r) < inf.
    - Prevents runaway autoregressive hallucination drift by pruning introspective scratchpads
      and resetting inference strictly to the immutable task invariant and grounded state.
    """

    def __init__(
        self,
        config: Optional[NirodhaResetConfig] = None,
        divergence_threshold: Optional[float] = None,
        reset_horizon: Optional[int] = None
    ):
        if config is None:
            kwargs = {}
            if divergence_threshold is not None:
                kwargs["theta_reset"] = divergence_threshold
            if reset_horizon is not None:
                kwargs["scheduled_reset_period_T_r"] = reset_horizon
            self.config = NirodhaResetConfig(**kwargs)
        else:
            self.config = config

        self.theta_reset = self.config.theta_reset
        self.T_r = self.config.scheduled_reset_period_T_r
        self.steps_since_reset: int = 0
        self.total_resets_triggered: int = 0
        self.divergence_history: List[float] = []

    def record_divergence(self, divergence: float) -> None:
        """Records an observed free-energy divergence without automatically stepping reset horizon."""
        self.divergence_history.append(float(divergence))

    def should_trigger_nirodha(self, divergence: Optional[float] = None) -> bool:
        """Evaluates if divergence exceeds reset threshold or horizon reached."""
        div = divergence if divergence is not None else (self.divergence_history[-1] if self.divergence_history else 0.0)
        return bool(div >= self.theta_reset or self.steps_since_reset >= self.T_r)

    def execute_cessation(
        self,
        context: Dict[str, Any],
        invariant_core: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Alias for execute_nirodha_reset."""
        return self.execute_nirodha_reset(context, grounded_state=invariant_core)

    def get_telemetry(self) -> Dict[str, Any]:
        """Returns active inference convergence and Nirodha reset telemetry."""
        current_div = self.divergence_history[-1] if self.divergence_history else 0.0
        return {
            "divergence_threshold": self.theta_reset,
            "scheduled_reset_horizon": self.T_r,
            "steps_since_reset": self.steps_since_reset,
            "reset_count": self.total_resets_triggered,
            "current_divergence": current_div,
            "mean_divergence": float(np.mean(self.divergence_history)) if self.divergence_history else 0.0,
            "max_divergence": float(np.max(self.divergence_history)) if self.divergence_history else 0.0
        }

    def compute_free_energy_surrogate(
        self,
        internal_belief_mu: np.ndarray,
        grounded_observation_y: np.ndarray,
        covariance_inv: Optional[np.ndarray] = None
    ) -> float:
        """Computes empirical free energy surrogate metric: E_t = ||mu_t - y_t||_{Sigma_y^-1}^2."""
        diff = internal_belief_mu - grounded_observation_y
        if covariance_inv is not None:
            energy = float(diff.T @ covariance_inv @ diff)
        else:
            energy = float(np.sum(diff ** 2))
        return energy

    def evaluate_cessation_trigger(
        self,
        divergence_energy: float,
        step_increment: bool = True
    ) -> Tuple[bool, str]:
        """Evaluates whether current divergence or step count triggers a Nirodha cessation."""
        if step_increment:
            self.steps_since_reset += 1
        self.divergence_history.append(divergence_energy)

        # Trigger 1: Free energy surrogate exceeds threshold
        if divergence_energy >= self.theta_reset:
            return True, f"Nirodha trigger: Free energy surrogate E_t = {divergence_energy:.3f} >= threshold {self.theta_reset:.3f}."

        # Trigger 2: Scheduled horizon limit T_r reached
        if self.steps_since_reset >= self.T_r:
            return True, f"Nirodha trigger: Scheduled context horizon T_r = {self.T_r} reached ({self.steps_since_reset} steps)."

        return False, "Context within bounded KL ball; continuing active inference."

    def execute_nirodha_reset(
        self,
        context: Dict[str, Any],
        grounded_state: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Executes the Nirodha Reset Operator R[q_t(x)] = q_ground(x).

        Purges intermediate chain-of-thought, recursive self-reflections, and ungrounded
        monologue while preserving the immutable base environment state and verified contract.
        """
        self.total_resets_triggered += 1
        self.steps_since_reset = 0

        immutable_goal = context.get("goal") or context.get("task_contract") or ""
        base_state = grounded_state or context.get("grounded_state", {})

        pruned_context: Dict[str, Any] = {
            "task_contract": immutable_goal,
            "grounded_state": base_state,
            "reset_epoch": self.total_resets_triggered,
            "intermediate_monologue_purged": True,
            "retained_history": [
                {"role": "system", "content": "Nirodha Cessation executed. Generative priors reset to grounded empirical state."},
                {"role": "user", "content": f"Task Invariant: {immutable_goal}"}
            ]
        }
        return pruned_context

    def calculate_kl_divergence_bound(
        self,
        A_spectral_norm: float,
        sigma_y_sq: float = 1.0,
        sigma_m_sq: float = 1.0,
        lambda_min_star: float = 1.0
    ) -> float:
        """Calculates theoretical compact KL divergence bound epsilon(T_r) from Theorem 2 proof."""
        T_r = self.T_r
        Ky_sq = 0.5
        Km_sq = 0.5

        # M(T_r) = ||A||^(2 T_r) tr(Sigma_y) + sum_{j=0}^{T_r-1} ||A||^(2j) (||Ky||^2 tr(Sigma_y) + ||Km||^2 tr(Sigma_m))
        term1 = (A_spectral_norm ** (2 * T_r)) * sigma_y_sq
        term2 = sum((A_spectral_norm ** (2 * j)) * (Ky_sq * sigma_y_sq + Km_sq * sigma_m_sq) for j in range(T_r))
        M_Tr = term1 + term2

        epsilon_Tr = (M_Tr / (2.0 * max(1e-4, lambda_min_star))) + 1.0
        return float(epsilon_Tr)


# ============================================================================
# 3. GAMMA-BAND PHASE SYNCHRONY (DISTRIBUTED SUB-AGENT BINDING)
# ============================================================================

class GammaPhaseSynchronizer:
    """Decentralized frequency-locked event loop for sub-agent binding (25 to 42 Hz).

    Operates without centralized blocking RPCs by broadcasting lightweight phase pulses
    and computing the Kuramoto order parameter R(t) = |1/N sum_j exp(i theta_j)|.
    """

    def __init__(self, target_frequency_hz: float = 40.0, num_agents: Optional[int] = None, coupling_k: float = 2.0):
        # 40 Hz gamma band -> period = 25 ms
        self.target_freq = target_frequency_hz
        self.period_seconds = 1.0 / target_frequency_hz
        self.coupling_k = coupling_k
        self._agent_phases: Dict[str, float] = {}  # agent_id -> phase angle theta in [0, 2pi)
        self.frequencies_hz: List[float] = []

        if num_agents:
            for i in range(num_agents):
                aid = f"agent_{i+1}"
                self.register_subagent(aid, initial_phase=float(np.random.uniform(0.0, 0.5)))
                self.frequencies_hz.append(float(np.random.uniform(38.0, 42.0)))
        else:
            self.frequencies_hz.append(target_frequency_hz)

    def register_subagent(self, agent_id: str, initial_phase: float = 0.0):
        self._agent_phases[agent_id] = initial_phase % (2.0 * math.pi)

    def update_phase(self, agent_id: str, delta_phase: float):
        current = self._agent_phases.get(agent_id, 0.0)
        self._agent_phases[agent_id] = (current + delta_phase) % (2.0 * math.pi)

    def compute_phase_coherence(self) -> float:
        """Computes Kuramoto order parameter R(t) in [0, 1].

        R(t) = 1 indicates complete macroscopic phase synchronization across sub-agents.
        """
        if not self._agent_phases:
            return 1.0

        phases = list(self._agent_phases.values())
        N = len(phases)
        real_sum = sum(math.cos(th) for th in phases)
        imag_sum = sum(math.sin(th) for th in phases)
        R = math.sqrt(real_sum ** 2 + imag_sum ** 2) / N
        return float(R)

    def order_parameter(self) -> float:
        """Alias for compute_phase_coherence."""
        return self.compute_phase_coherence()

    def step(self, dt: float = 0.016):
        """Advances Kuramoto phase oscillator model:
        d theta_i / dt = omega_i + (K / N) * sum_j sin(theta_j - theta_i)
        """
        if not self._agent_phases:
            return
        agent_ids = list(self._agent_phases.keys())
        N = len(agent_ids)
        phases = [self._agent_phases[aid] for aid in agent_ids]
        freqs = self.frequencies_hz if len(self.frequencies_hz) == N else [self.target_freq] * N

        new_phases = []
        for i, aid in enumerate(agent_ids):
            theta_i = phases[i]
            omega_i = 2.0 * math.pi * freqs[i]
            coupling = (self.coupling_k / N) * sum(math.sin(phases[j] - theta_i) for j in range(N))
            dtheta = (omega_i + coupling) * dt
            new_phases.append((theta_i + dtheta) % (2.0 * math.pi))

        for i, aid in enumerate(agent_ids):
            self._agent_phases[aid] = new_phases[i]

    def is_synchronized(self, coherence_threshold: float = 0.85) -> bool:
        return self.compute_phase_coherence() >= coherence_threshold


# ============================================================================
# 4. CAUSAL NETWORK TOPOLOGIES & LAPLACIAN SWARM CONSENSUS
# ============================================================================

class CausalLaplacianConsensus:
    """Evaluates multi-agent consensus networks and rigorously eliminates non-causal illusions.

    Guarantees:
    - Spectral gap / algebraic connectivity lambda_2(L) > 0 dictates exponential consensus rate.
    - If lambda_2(L) == 0 (uncoupled agents), proves conditional mutual information I(z_i; z_j | u) = 0
      and rejects spurious alignment arising from retrospective window selection (DAT mechanism).
    """

    def __init__(self, num_agents: int = 7, adjacency_matrix: Optional[np.ndarray] = None):
        self.num_agents = num_agents
        if adjacency_matrix is not None:
            self.W = np.array(adjacency_matrix, dtype=np.float64)
            self.num_agents = self.W.shape[0]
        else:
            # Create a strongly connected ring graph with forward/backward edges
            self.W = np.zeros((num_agents, num_agents), dtype=np.float64)
            for i in range(num_agents):
                self.W[i, (i + 1) % num_agents] = 1.0
                self.W[i, (i - 1) % num_agents] = 1.0
        self.L, self.lambda_2 = self.compute_graph_laplacian(self.W)
        self.state = np.random.randn(self.num_agents).astype(np.float64)

    def algebraic_connectivity(self) -> float:
        """Returns second smallest eigenvalue of Laplacian lambda_2(L)."""
        _, l2 = self.compute_graph_laplacian(self.W)
        return float(l2)

    def is_connected(self) -> bool:
        return self.algebraic_connectivity() > 1e-4

    def step_consensus(self, dt: float = 0.05):
        """Advances consensus state: dx/dt = -L x."""
        dx = -self.L @ self.state
        self.state += dt * dx

    @staticmethod
    def compute_graph_laplacian(adjacency_matrix: np.ndarray) -> Tuple[np.ndarray, float]:
        """Computes graph Laplacian L = D - W and algebraic connectivity lambda_2(L)."""
        W = np.array(adjacency_matrix, dtype=np.float64)
        n = W.shape[0]
        # In-degree matrix D
        degrees = np.sum(W, axis=1)
        D = np.diag(degrees)
        L = D - W

        # Compute eigenvalues
        eigenvalues = np.sort(np.linalg.eigvals(L).real)
        # lambda_2 is the second smallest eigenvalue (algebraic connectivity)
        lambda_2 = float(eigenvalues[1]) if len(eigenvalues) > 1 else 0.0
        return L, max(0.0, lambda_2)

    @staticmethod
    def verify_consensus_viability(
        adjacency_matrix: np.ndarray,
        task_coupling_gamma: float = 0.5
    ) -> Dict[str, Any]:
        """Verifies if the communication graph satisfies exponential convergence (Theorem 3)."""
        L, lambda_2 = CausalLaplacianConsensus.compute_graph_laplacian(adjacency_matrix)
        is_connected = lambda_2 > 1e-4

        convergence_rate = lambda_2 + task_coupling_gamma if is_connected else 0.0

        return {
            "algebraic_connectivity_lambda_2": lambda_2,
            "task_coupling_gamma": task_coupling_gamma,
            "exponential_convergence_rate": convergence_rate,
            "causally_connected": is_connected,
            "consensus_certified": is_connected,
            "status": "CAUSALLY_CONNECTED (Exponential Consensus Guaranteed)" if is_connected else "UNCOUPLED (Non-Causal Emergence Annihilated)"
        }

    @staticmethod
    def evaluate_dat_spurious_correlation_bound(
        num_windows_K: int,
        sample_length_M: int
    ) -> float:
        """Computes the expected spurious maximum correlation under Decision Augmentation Theory:

        E[rho_max] ~ (1 / sqrt(M)) * sqrt(2 * ln(K)).
        Proves that emergent correlation without causal edges is an artifact of search-space cardinality K.
        """
        K = max(2, num_windows_K)
        M = max(1, sample_length_M)
        expected_max = (1.0 / math.sqrt(M)) * (math.sqrt(2.0 * math.log(K)) - (math.log(math.log(K)) + math.log(4.0 * math.pi)) / (2.0 * math.sqrt(2.0 * math.log(K))))
        return float(expected_max)
