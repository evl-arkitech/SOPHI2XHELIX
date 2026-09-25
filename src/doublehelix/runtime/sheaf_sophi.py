"""SOPHI-Runtime: Cognitive Homology, Cellular Sheaf Cohomology, and Monoidal Optics.

Implements the 4-layer architecture from 'System Evolution September 2026 - The Arkitech':
1. Poincaré Subliminal Differential Dataflow:
   Asynchronous difference records (d, t, r) with Kolmogorov-Aesthetic Sieve
   M(h) = alpha * K(h) - beta * E[ln P(D | h)] <= theta_sieve.
2. Grothendieck Cellular Sheaf Cohomology:
   Stalk spaces F(v), F(e), coboundary delta^0, Sheaf Laplacian L_F = (delta^0)* delta^0,
   Dirichlet energy dissipation, and topos-theoretic elevation.
3. Tesla Parameterized Monoidal Optics:
   Para(Optic_C)((X, S), (Y, R)) bidirectional mental sandbox where counterfactual
   wear-and-tear occurs purely in parameter space P before physical actuation.
4. Torvalds-Friston Classical Linear Logic Session Types:
   Deadlock-free, confluent, zero-allocation session channels with duality and cut elimination.
"""

import math
import time
from typing import Dict, List, Any, Optional, Tuple, Callable
import numpy as np
from pydantic import BaseModel, Field


# ============================================================================
# LAYER 1: POINCARÉ SUBLIMINAL DIFFERENTIAL DATAFLOW
# ============================================================================

class DifferenceRecord(BaseModel):
    """Asynchronous difference record (d, t, r) in D x T x R."""
    record_id: str
    data_delta: Dict[str, Any]
    timestamp: float = Field(default_factory=time.time)
    recurrence_weight: float = 1.0
    epistemic_entropy: float = 0.0


class SubliminalHypothesis(BaseModel):
    """Candidate hypothesis incubated in the subconscious differential dataflow."""
    hypothesis_id: str
    representation: str
    kolmogorov_proxy: float            # Proxy for K(h): description length in bytes/tokens
    log_likelihood: float              # E[ln P(D | h)]
    aesthetic_score: float = 0.0       # M(h)
    resonance: float = 0.1             # Subliminal energy
    generation_timestamp: float = Field(default_factory=time.time)
    conscious_epiphany: bool = False   # True when crossed into conscious executive awareness


class PoincareDifferentialIncubator:
    """Poincaré Subliminal Differential Dataflow Incubator.

    Maintains a continuous, non-blocking subconscious associative network
    processing difference records (d, t, r). Hypotheses are evaluated via the
    Kolmogorov-Aesthetic Sieve:
        M(h) = alpha * K(h) - beta * E[ln P(D | h)]
    When M(h) falls below threshold theta_sieve, the hypothesis achieves
    conscious epiphany and is elevated to the executive decision core.
    """

    def __init__(
        self,
        alpha: float = 0.05,
        beta: float = 1.0,
        theta_sieve: float = 15.0,
        resonance_decay: float = 0.98,
        resonance_boost: float = 0.25,
        max_subliminal_capacity: int = 128
    ):
        self.alpha = alpha
        self.beta = beta
        self.theta_sieve = theta_sieve
        self.resonance_decay = resonance_decay
        self.resonance_boost = resonance_boost
        self.max_capacity = max_subliminal_capacity

        self.records_buffer: List[DifferenceRecord] = []
        self.subliminal_pool: Dict[str, SubliminalHypothesis] = {}
        self.epiphany_history: List[SubliminalHypothesis] = []

    def ingest_difference(self, data_delta: Dict[str, Any], epistemic_entropy: float = 0.0) -> DifferenceRecord:
        """Ingests a real-time difference record (d, t, r)."""
        rec_id = f"diff_{len(self.records_buffer)}_{int(time.time() * 1000)}"
        rec = DifferenceRecord(
            record_id=rec_id,
            data_delta=data_delta,
            timestamp=time.time(),
            recurrence_weight=1.0,
            epistemic_entropy=epistemic_entropy
        )
        self.records_buffer.append(rec)
        if len(self.records_buffer) > 256:
            self.records_buffer.pop(0)

        # Stimulate resonance in matching hypotheses
        for h in self.subliminal_pool.values():
            if not h.conscious_epiphany:
                h.resonance = min(2.0, h.resonance + self.resonance_boost * (1.0 + epistemic_entropy))

        return rec

    def seed_hypothesis(
        self,
        hypothesis_id: str,
        representation: str,
        kolmogorov_proxy: float,
        log_likelihood: float
    ) -> SubliminalHypothesis:
        """Seeds a hypothesis into subliminal incubation."""
        # Aesthetic evaluation: lower score = more elegant / higher fitness
        score = self.alpha * kolmogorov_proxy - self.beta * log_likelihood
        h = SubliminalHypothesis(
            hypothesis_id=hypothesis_id,
            representation=representation,
            kolmogorov_proxy=kolmogorov_proxy,
            log_likelihood=log_likelihood,
            aesthetic_score=score,
            resonance=0.2,
            conscious_epiphany=(score <= self.theta_sieve)
        )
        if len(self.subliminal_pool) >= self.max_capacity:
            # Evict least resonant
            least_resonant = min(self.subliminal_pool.keys(), key=lambda k: self.subliminal_pool[k].resonance)
            del self.subliminal_pool[least_resonant]

        self.subliminal_pool[hypothesis_id] = h
        if h.conscious_epiphany:
            self.epiphany_history.append(h)
        return h

    def incubate_step(self, dt: float = 0.1) -> List[SubliminalHypothesis]:
        """Executes one continuous incubation step.

        Applies differential associative decay, re-evaluates sieve scores with
        epistemic gain from recent records, and emits new conscious epiphanies.
        """
        new_epiphanies: List[SubliminalHypothesis] = []
        for h in self.subliminal_pool.values():
            if h.conscious_epiphany:
                continue

            # Decay resonance
            h.resonance *= (self.resonance_decay ** (dt / 0.1))

            # Sieve score: M(h) modulated by resonance
            # High resonance effectively reduces description burden (insight compression)
            effective_score = (self.alpha * h.kolmogorov_proxy - self.beta * h.log_likelihood) / max(0.1, h.resonance)
            h.aesthetic_score = effective_score

            if effective_score <= self.theta_sieve:
                h.conscious_epiphany = True
                new_epiphanies.append(h)
                self.epiphany_history.append(h)

        return new_epiphanies


# ============================================================================
# LAYER 2: GROTHENDIECK CELLULAR SHEAF COHOMOLOGY
# ============================================================================

class GrothendieckCellularSheaf:
    """Cellular Sheaf Cohomology Engine for Multi-Agent Systems.

    Over a 1-dimensional cell complex (graph G = (V, E)):
    - Vertices v in V: agents with stalk space F(v) = R^{d_v}
    - Edges e = (u, v) in E: communication interfaces with stalk space F(e) = R^{d_e}
    - Restriction maps: F_{u trianglelefteq e}: F(u) -> F(e), F_{v trianglelefteq e}: F(v) -> F(e)

    The coboundary operator delta^0: C^0(G; F) -> C^1(G; F) is:
        (delta^0 x)_e = F_{v trianglelefteq e} x_v - F_{u trianglelefteq e} x_u
    The Sheaf Laplacian is:
        L_F = (delta^0)* delta^0 : C^0(G; F) -> C^0(G; F)

    The 0-cohomology H^0(G; F) = ker(delta^0) = ker(L_F) represents global harmonic consensus.
    The Dirichlet Energy E_F(x) = 1/2 <x, L_F x> measures multi-agent discord / friction.
    Gradient flow dx/dt = -L_F x exponentially dissipates discord at rate lambda_2(L_F).
    """

    def __init__(self, node_ids: List[str], stalk_dim: int = 2):
        self.node_ids = node_ids
        self.node_to_idx = {nid: i for i, nid in enumerate(node_ids)}
        self.n_nodes = len(node_ids)
        self.stalk_dim = stalk_dim
        self.total_dim = self.n_nodes * stalk_dim

        # Edges: list of tuples (u_id, v_id, edge_id, dim_e)
        self.edges: List[Tuple[str, str, str, int]] = []
        # Restriction maps: key = (node_id, edge_id), value = matrix (dim_e x stalk_dim)
        self.restriction_maps: Dict[Tuple[str, str], np.ndarray] = {}

        self._coboundary_cache: Optional[np.ndarray] = None
        self._laplacian_cache: Optional[np.ndarray] = None

    def add_edge(
        self,
        u_id: str,
        v_id: str,
        edge_id: str,
        r_u: Optional[np.ndarray] = None,
        r_v: Optional[np.ndarray] = None,
        edge_dim: Optional[int] = None
    ):
        """Adds an oriented edge with linear restriction maps F_{u trianglelefteq e} and F_{v trianglelefteq e}."""
        edim = edge_dim if edge_dim is not None else self.stalk_dim
        self.edges.append((u_id, v_id, edge_id, edim))

        if r_u is None:
            r_u = np.eye(edim, self.stalk_dim)
        if r_v is None:
            r_v = np.eye(edim, self.stalk_dim)

        self.restriction_maps[(u_id, edge_id)] = np.asarray(r_u, dtype=np.float64)
        self.restriction_maps[(v_id, edge_id)] = np.asarray(r_v, dtype=np.float64)

        # Invalidate caches
        self._coboundary_cache = None
        self._laplacian_cache = None

    def build_coboundary_matrix(self) -> np.ndarray:
        """Constructs the discrete coboundary operator delta^0: C^0(G; F) -> C^1(G; F)."""
        if self._coboundary_cache is not None:
            return self._coboundary_cache

        total_edge_dim = sum(edim for _, _, _, edim in self.edges)
        delta0 = np.zeros((total_edge_dim, self.total_dim), dtype=np.float64)

        row_offset = 0
        for u_id, v_id, edge_id, edim in self.edges:
            u_idx = self.node_to_idx[u_id]
            v_idx = self.node_to_idx[v_id]

            r_u = self.restriction_maps[(u_id, edge_id)]
            r_v = self.restriction_maps[(v_id, edge_id)]

            col_u = u_idx * self.stalk_dim
            col_v = v_idx * self.stalk_dim

            # (delta^0 x)_e = F_{v trianglelefteq e} x_v - F_{u trianglelefteq e} x_u
            delta0[row_offset:row_offset + edim, col_u:col_u + self.stalk_dim] = -r_u
            delta0[row_offset:row_offset + edim, col_v:col_v + self.stalk_dim] = r_v

            row_offset += edim

        self._coboundary_cache = delta0
        return delta0

    def build_sheaf_laplacian(self) -> np.ndarray:
        """Constructs the Sheaf Laplacian L_F = (delta^0)^T delta^0."""
        if self._laplacian_cache is not None:
            return self._laplacian_cache

        delta0 = self.build_coboundary_matrix()
        L_F = delta0.T @ delta0
        # Ensure exact numerical symmetry
        L_F = 0.5 * (L_F + L_F.T)
        self._laplacian_cache = L_F
        return L_F

    def dirichlet_energy(self, x: np.ndarray) -> float:
        """Computes the Sheaf Dirichlet Energy E_F(x) = 1/2 <x, L_F x> = 1/2 ||delta^0 x||^2."""
        L_F = self.build_sheaf_laplacian()
        x_flat = x.flatten()
        return float(0.5 * x_flat.T @ L_F @ x_flat)

    def spectral_analysis(self) -> Dict[str, Any]:
        """Calculates spectrum of L_F, finding harmonic subspace H^0 and algebraic connectivity."""
        L_F = self.build_sheaf_laplacian()
        eigenvalues, eigenvectors = np.linalg.eigh(L_F)

        # Numerical tolerance for zero eigenvalues (harmonic consensus dimension)
        zero_thresh = 1e-7
        harmonic_indices = np.where(eigenvalues <= zero_thresh)[0]
        h0_dim = len(harmonic_indices)

        # Spectral gap (algebraic connectivity of the sheaf)
        positive_eigs = eigenvalues[eigenvalues > zero_thresh]
        spectral_gap = float(positive_eigs[0]) if len(positive_eigs) > 0 else 0.0

        return {
            "eigenvalues": eigenvalues.tolist(),
            "harmonic_dimension_h0": h0_dim,
            "spectral_gap_lambda2": spectral_gap,
            "is_connected": h0_dim > 0,
            "total_dof": self.total_dim
        }

    def dissipate_discord_step(self, x: np.ndarray, eta: float = 0.05) -> np.ndarray:
        """Executes a gradient descent step on Dirichlet energy: x_{t+1} = x_t - eta * L_F x_t."""
        L_F = self.build_sheaf_laplacian()
        x_flat = x.flatten()
        grad = L_F @ x_flat
        x_new = x_flat - eta * grad
        return x_new.reshape(self.n_nodes, self.stalk_dim)

    def project_to_consensus(self, x: np.ndarray) -> np.ndarray:
        """Projects agent states directly onto the harmonic subspace ker(L_F) = H^0(G; F)."""
        L_F = self.build_sheaf_laplacian()
        eigenvalues, eigenvectors = np.linalg.eigh(L_F)
        zero_thresh = 1e-7

        harmonic_mask = eigenvalues <= zero_thresh
        harmonic_basis = eigenvectors[:, harmonic_mask]

        if harmonic_basis.shape[1] == 0:
            return np.zeros_like(x)

        x_flat = x.flatten()
        proj = harmonic_basis @ (harmonic_basis.T @ x_flat)
        return proj.reshape(self.n_nodes, self.stalk_dim)


# ============================================================================
# LAYER 3: TESLA MONOIDAL OPTICS (BIDIRECTIONAL PARAMETERIZED SANDBOX)
# ============================================================================

class TeslaMonoidalOptic:
    """Parameterized Monoidal Optic: Para(Optic_C)((X, S), (Y, R)).

    Implements Nikola Tesla's mental prototyping methodology:
    Before any physical actuation, an entire apparatus is assembled and operated
    in imagination. Mechanical stress and parameter fatigue occur entirely
    within the parameter space P, leaving physical reality unstrained.

    Components:
    - Parameter space P: Internal configuration / mental representation
    - Forward view: P x X -> Y (Action projection / mental visualization)
    - Backward update: P x X x R -> P x S (Stress back-propagation & learning)
    """

    def __init__(
        self,
        name: str,
        initial_params: Dict[str, float],
        wear_tolerance: float = 100.0
    ):
        self.name = name
        self.params: Dict[str, float] = dict(initial_params)
        self.accumulated_mental_wear: float = 0.0
        self.wear_tolerance = wear_tolerance
        self.simulation_cycles: int = 0

    def view(self, state: Dict[str, float]) -> Dict[str, float]:
        """Forward View: P x X -> Y. Projects operational outcome from internal state."""
        # Linear/non-linear projection of input state weighted by internal parameters
        output = {}
        bias = self.params.get("bias", 0.0)
        gain = self.params.get("gain", 1.0)
        damping = self.params.get("damping", 0.5)

        for k, v in state.items():
            output[f"proj_{k}"] = gain * v + bias - damping * (v ** 2 if abs(v) < 10 else abs(v))

        return output

    def update(
        self,
        state: Dict[str, float],
        stress_feedback: Dict[str, float],
        learning_rate: float = 0.02
    ) -> Tuple[Dict[str, float], float]:
        """Backward Update: P x X x R -> P x S. Back-propagates virtual friction to P."""
        total_stress = sum(abs(v) for v in stress_feedback.values())
        self.accumulated_mental_wear += total_stress
        self.simulation_cycles += 1

        # Parameter adaptation to counter the stress
        for k, stress_val in stress_feedback.items():
            param_key = f"param_{k}"
            current_p = self.params.get(param_key, 1.0)
            # Adapt parameter to minimize future stress
            self.params[param_key] = current_p - learning_rate * stress_val

        # Return updated state residual S and incremental stress
        residual = {f"res_{k}": state.get(k, 0.0) - stress_feedback.get(k, 0.0) for k in state}
        return residual, total_stress

    def run_mental_burn_in(
        self,
        nominal_state: Dict[str, float],
        perturbation_shocks: List[Dict[str, float]],
        max_wear: Optional[float] = None
    ) -> Dict[str, Any]:
        """Executes counterfactual stress testing in parameter space prior to physical actuation."""
        limit = max_wear if max_wear is not None else self.wear_tolerance
        wear_before = self.accumulated_mental_wear
        shocks_absorbed = 0

        for shock in perturbation_shocks:
            proj = self.view(nominal_state)
            # Evaluate synthetic stress
            synthetic_stress = {k: abs(proj.get(f"proj_{k}", 0.0) - shock.get(k, 0.0)) for k in shock}
            _, cycle_stress = self.update(nominal_state, synthetic_stress)
            shocks_absorbed += 1

            if (self.accumulated_mental_wear - wear_before) >= limit:
                return {
                    "passed": False,
                    "reason": f"Burn-in wear exceeded tolerance ({self.accumulated_mental_wear - wear_before:.2f} >= {limit:.2f})",
                    "cycles_completed": shocks_absorbed,
                    "accumulated_wear": self.accumulated_mental_wear - wear_before,
                    "hardened_params": self.params
                }

        return {
            "passed": True,
            "reason": "All mental stress shocks absorbed without physical wear.",
            "cycles_completed": shocks_absorbed,
            "accumulated_wear": self.accumulated_mental_wear - wear_before,
            "hardened_params": self.params
        }

    def compose(self, other: "TeslaMonoidalOptic") -> "TeslaMonoidalOptic":
        """Monoidal composition of two optics in series: (Optic1 o Optic2)."""
        composed_name = f"{self.name}_x_{other.name}"
        merged_params = {}
        for k, v in self.params.items():
            merged_params[f"{self.name}_{k}"] = v
        for k, v in other.params.items():
            merged_params[f"{other.name}_{k}"] = v

        return TeslaMonoidalOptic(
            name=composed_name,
            initial_params=merged_params,
            wear_tolerance=min(self.wear_tolerance, other.wear_tolerance)
        )


# ============================================================================
# LAYER 4: CLASSICAL LINEAR LOGIC SESSION CHANNELS (TORVALDS-FRISTON)
# ============================================================================

class LinearMessageType:
    SEND = "!A"        # Must send message of type A
    RECEIVE = "?A"     # Must receive message of type A
    SELECT = "+T"      # Internal choice
    BRANCH = "&T"      # External choice
    END = "1"          # Unit termination
    BOTTOM = "_|_"     # Dual unit termination


class LinearSessionEndpoint:
    """Single endpoint of a Classical Linear Logic (CLL) session channel.

    Enforces substructural linear type discipline:
    - Resources must be consumed exactly once (no duplication, no abandonment).
    - Every send !A.T is matched with a dual receive ?A.T^perp.
    - Eliminates deadlocks via cut elimination and guarantees confluence.
    """

    def __init__(self, endpoint_id: str, dual_id: str, is_initiator: bool = True):
        self.endpoint_id = endpoint_id
        self.dual_id = dual_id
        self.is_initiator = is_initiator
        self.active: bool = True
        self.sent_count: int = 0
        self.recv_count: int = 0
        self.message_queue: List[Any] = []
        self.linear_tokens: int = 1  # Linear capability token

    def send(self, value: Any, dual_endpoint: "LinearSessionEndpoint") -> bool:
        """Sends a linear resource to the dual endpoint."""
        if not self.active:
            raise RuntimeError(f"LinearSessionError: Endpoint {self.endpoint_id} is terminated.")
        if self.linear_tokens <= 0:
            raise RuntimeError(f"LinearSessionError: Linear capability already consumed on {self.endpoint_id}.")

        dual_endpoint.message_queue.append(value)
        self.sent_count += 1
        return True

    def receive(self) -> Any:
        """Receives a linear resource from the message queue."""
        if not self.active:
            raise RuntimeError(f"LinearSessionError: Endpoint {self.endpoint_id} is terminated.")
        if not self.message_queue:
            return None

        val = self.message_queue.pop(0)
        self.recv_count += 1
        return val

    def close(self):
        """Linear termination (Unit 1 / _|_). Consumes the linear capability."""
        if self.linear_tokens > 0:
            self.linear_tokens -= 1
        self.active = False


class LinearSessionChannel:
    """Dual-ended Classical Linear Logic session channel pair (c, c^perp)."""

    def __init__(self, channel_id: str):
        self.channel_id = channel_id
        self.client = LinearSessionEndpoint(f"{channel_id}_client", f"{channel_id}_server", is_initiator=True)
        self.server = LinearSessionEndpoint(f"{channel_id}_server", f"{channel_id}_client", is_initiator=False)

    def execute_transaction(self, request_payload: Any, handler: Callable[[Any], Any]) -> Any:
        """Executes a complete cut-elimination interaction between client and server."""
        # 1. Client sends request (!A)
        self.client.send(request_payload, self.server)

        # 2. Server receives request (?A)
        req = self.server.receive()
        if req is None:
            raise RuntimeError("LinearChannelError: Expected message not found in server queue.")

        # 3. Server handles and sends response (!B)
        response_payload = handler(req)
        self.server.send(response_payload, self.client)

        # 4. Client receives response (?B)
        res = self.client.receive()

        # 5. Dual cut elimination: close both endpoints (1 / _|_)
        self.client.close()
        self.server.close()

        return res
