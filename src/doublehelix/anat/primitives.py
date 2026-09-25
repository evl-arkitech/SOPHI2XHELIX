"""The Seven Operational Graph Navigation Primitives from ANAT.

Formally implements:
1. OBSERVE(node_id)
2. HOP(source_node, edge_id)
3. GATING_CHECK(node_id, threshold)
4. DIFFUSE(graph_node, query_entities, steps) via Personalized PageRank
5. SETTLE_ENERGY(hopfield_node, input_state) via CCCP Modern Hopfield
6. DESTABILIZE(param_node, target_layer, key)
7. ENOUGH()
"""

from typing import Dict, Any, List, Optional, Tuple
import numpy as np

from doublehelix.anat.world_graph import ExplorableWorldGraph
from doublehelix.anat.models import Node, Edge


class GraphNavigator:
    """Executes operational graph navigation primitives over the Explorable World Graph."""

    def __init__(self, graph: ExplorableWorldGraph):
        self.graph = graph
        self.current_node_id: str = "N01_SCRATCH"
        self.active_memory_tensors: Dict[str, np.ndarray] = {}

    def observe(self, node_id: str) -> Dict[str, Any]:
        """OBSERVE: Inspects state, activation norms, and connectivity without mutating values."""
        node = self.graph.get_node(node_id)
        if not node:
            raise KeyError(f"Node {node_id} does not exist in graph.")

        outgoing = self.graph.get_outgoing_edges(node_id)
        incoming = self.graph.get_incoming_edges(node_id)
        tensor = self.active_memory_tensors.get(node_id)
        norm = float(np.linalg.norm(tensor)) if tensor is not None else 0.0

        return {
            "node_id": node.node_id,
            "functional_name": node.functional_name,
            "sector": node.sector.value,
            "architecture": node.synthetic_architecture,
            "activation_norm": norm,
            "outgoing_edges": [e.edge_id for e in outgoing],
            "incoming_edges": [e.edge_id for e in incoming]
        }

    def hop(self, source_node: str, edge_id: str) -> str:
        """HOP: Traverses explicit directed edge, transferring activation to target."""
        edge = self.graph.edges.get(edge_id)
        if not edge:
            raise KeyError(f"Edge {edge_id} does not exist.")
        if edge.source_node != source_node:
            raise ValueError(f"Edge {edge_id} originates at {edge.source_node}, not {source_node}")

        # Transfer tensor activation
        if source_node in self.active_memory_tensors:
            self.active_memory_tensors[edge.target_node] = self.active_memory_tensors[source_node].copy()

        self.current_node_id = edge.target_node
        return edge.target_node

    def gating_check(self, node_id: str, value: float, threshold: float = 0.5) -> bool:
        """GATING_CHECK: Evaluates whether basal ganglia routing or surprise permits onward signal."""
        return value >= threshold

    def diffuse(
        self,
        query_indices: List[int],
        alpha: float = 0.85,
        steps: int = 20
    ) -> np.ndarray:
        """DIFFUSE: Executes Personalized PageRank over N07_GRAPH:

        p^(t+1) = (1 - alpha) * p_0 + alpha * A * D^(-1) * p^(t)
        Guaranteed to converge to stationary probability distribution by Perron-Frobenius theorem.
        """
        adj, node_ids = self.graph.get_adjacency_matrix()
        n = len(node_ids)
        if n == 0:
            return np.array([])

        # Out-degree normalization
        d = adj.sum(axis=1)
        d_inv = np.zeros_like(d)
        nonzero_mask = d > 0
        d_inv[nonzero_mask] = 1.0 / d[nonzero_mask]
        p_transition = adj * d_inv[:, None]  # Column-stochastic / row-transition

        # Teleport vector p0
        p0 = np.zeros(n, dtype=np.float32)
        if query_indices:
            for q in query_indices:
                if 0 <= q < n:
                    p0[q] = 1.0 / len(query_indices)
        else:
            p0[:] = 1.0 / n

        p = p0.copy()
        for _ in range(steps):
            dangling_mass = float(np.sum(p[~nonzero_mask]))
            p = (1.0 - alpha) * p0 + alpha * (p_transition.T @ p + dangling_mass * p0)
            p = p / (float(np.sum(p)) + 1e-12)

        return p

    def settle_energy(
        self,
        stored_patterns: np.ndarray,
        query_state: np.ndarray,
        beta: float = 1.0,
        max_iter: int = 10,
        tol: float = 1e-5
    ) -> Tuple[np.ndarray, float]:
        """SETTLE_ENERGY: Runs Concave-Convex Procedure (CCCP) energy minimization on N05_ATTRACT.

        xi^(t+1) = X * softmax(beta * X^T * xi^(t))
        Energy function:
        E(xi) = -1/beta * log(sum(exp(beta * X_i^T * xi))) + 1/2 * ||xi||^2
        Guaranteed monotonic energy decrease: Delta E <= 0 until convergence.
        """
        X = stored_patterns  # shape: (d, N)
        xi = query_state.copy()  # shape: (d,)

        def compute_energy(v: np.ndarray) -> float:
            scores = beta * (X.T @ v)
            max_s = np.max(scores)
            logsumexp = max_s + np.log(np.sum(np.exp(scores - max_s)) + 1e-12)
            return float(- (1.0 / beta) * logsumexp + 0.5 * np.dot(v, v))

        curr_energy = compute_energy(xi)
        for _ in range(max_iter):
            # Softmax projection
            scores = beta * (X.T @ xi)
            exp_scores = np.exp(scores - np.max(scores))
            weights = exp_scores / (np.sum(exp_scores) + 1e-12)
            next_xi = X @ weights

            delta = np.linalg.norm(next_xi - xi)
            xi = next_xi
            curr_energy = compute_energy(xi)

            if delta < tol:
                break

        return xi, curr_energy

    def destabilize(self, target_node: str = "N10_PARAM") -> bool:
        """DESTABILIZE: Cleaves synaptic constraints in N10_PARAM, unlocking parameters for surgery."""
        node = self.graph.get_node(target_node)
        if node:
            node.metadata["labilized"] = True
            return True
        return False

    def enough(self, evidence_score: float, threshold: float = 0.8) -> bool:
        """ENOUGH: Halting signal terminating graph exploration when sufficient evidence is gathered."""
        return evidence_score >= threshold
