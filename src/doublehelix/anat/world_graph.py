"""Explorable World Graph G = (V, E, W) implementation.

Loads the full topological node registry and edge topography from the ANAT memory structure,
maintaining an attributed multi-relational graph across the 5 cognitive sectors.
"""

import os
import csv
from typing import Dict, List, Optional, Tuple, Set, Any
import numpy as np

from doublehelix.anat.models import Node, Edge, CognitiveSector, RelationalPredicate


def _infer_sector(node_id: str) -> CognitiveSector:
    """Categorizes nodes into the 5 ANAT cognitive sectors."""
    if node_id in ("N01_SCRATCH", "N02_GATE", "N03_SILENT", "N15_HORROR_FRAMEWORK", "N16_GRAPHICS_ARCHITECTURE", "N17_DISTINCTION_ARCHITECTURE"):
        return CognitiveSector.EXECUTIVE_GATING
    elif node_id in ("N04_SEPARATE", "N05_ATTRACT", "N06_COMPARE", "N07_GRAPH"):
        return CognitiveSector.EPISODIC_BUFFER
    elif node_id in ("N08_TITANS", "N09_SURPRISE"):
        return CognitiveSector.ONLINE_SURPRISE
    elif node_id in ("N10_PARAM", "N11_TRIPLE", "N12_REGULAR"):
        return CognitiveSector.PARAMETRIC_BASE
    elif node_id in ("N13_DESTAB", "N14_SURGERY"):
        return CognitiveSector.LABILIZATION
    return CognitiveSector.EXECUTIVE_GATING


class ExplorableWorldGraph:
    """Attributed multi-relational memory graph G = (V, E, W)."""

    def __init__(self, memory_dir: Optional[str] = None):
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, Edge] = {}
        self.outgoing_adj: Dict[str, List[Edge]] = {}
        self.incoming_adj: Dict[str, List[Edge]] = {}

        if memory_dir is None:
            # Default to anat_memory folder in current workspace
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            memory_dir = os.path.join(base_dir, "anat_memory")
            if not os.path.exists(memory_dir):
                memory_dir = os.path.join(os.getcwd(), "anat_memory")

        self.memory_dir = memory_dir
        self.load_graph_from_csv()

    def load_graph_from_csv(self):
        """Loads vertices from node registry.csv and edges from edge topography.csv."""
        nodes_csv = os.path.join(self.memory_dir, "node registry.csv")
        edges_csv = os.path.join(self.memory_dir, "edge topography.csv")

        if os.path.exists(nodes_csv):
            with open(nodes_csv, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    node_id = row["Node ID"].strip()
                    node = Node(
                        node_id=node_id,
                        functional_name=row["Functional Name"].strip(),
                        biological_counterpart=row["Biological Counterpart"].strip(),
                        synthetic_architecture=row["Synthetic Architecture"].strip(),
                        update_regime=row["Update Regime"].strip(),
                        representational_code=row["Representational Code"].strip(),
                        sector=_infer_sector(node_id)
                    )
                    self.nodes[node_id] = node
                    self.outgoing_adj[node_id] = []
                    self.incoming_adj[node_id] = []

        if os.path.exists(edges_csv):
            with open(edges_csv, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    edge_id = row["Edge ID"].strip()
                    src = row["Source Node"].strip()
                    tgt = row["Target Node"].strip()
                    pred_str = row["Relational Predicate"].strip()
                    predicate = RelationalPredicate(pred_str) if pred_str in RelationalPredicate.__members__ else RelationalPredicate.PROJECTS_TO

                    edge = Edge(
                        edge_id=edge_id,
                        source_node=src,
                        target_node=tgt,
                        relational_predicate=predicate,
                        modulation_trigger=row["Modulation & Trigger Mechanism"].strip(),
                        latency_profile=row["Latency Profile"].strip()
                    )
                    self.edges[edge_id] = edge
                    if src in self.outgoing_adj:
                        self.outgoing_adj[src].append(edge)
                    if tgt in self.incoming_adj:
                        self.incoming_adj[tgt].append(edge)

    def get_node(self, node_id: str) -> Optional[Node]:
        return self.nodes.get(node_id)

    def get_outgoing_edges(self, node_id: str) -> List[Edge]:
        return self.outgoing_adj.get(node_id, [])

    def get_incoming_edges(self, node_id: str) -> List[Edge]:
        return self.incoming_adj.get(node_id, [])

    def get_adjacency_matrix(self) -> Tuple[np.ndarray, List[str]]:
        """Computes the directed binary adjacency matrix A and node index ordering."""
        node_ids = sorted(list(self.nodes.keys()))
        idx_map = {nid: i for i, nid in enumerate(node_ids)}
        n = len(node_ids)
        adj = np.zeros((n, n), dtype=np.float32)

        for edge in self.edges.values():
            if edge.source_node in idx_map and edge.target_node in idx_map:
                u = idx_map[edge.source_node]
                v = idx_map[edge.target_node]
                adj[u, v] = 1.0

        return adj, node_ids

    def __repr__(self) -> str:
        return (
            f"ExplorableWorldGraph(nodes={len(self.nodes)}, "
            f"edges={len(self.edges)}, memory_dir={self.memory_dir!r})"
        )

    def get_diagnostics(self) -> Dict[str, Any]:
        """Provides graph topology diagnostics and health checks."""
        isolated = [
            nid for nid in self.nodes
            if not self.outgoing_adj.get(nid) and not self.incoming_adj.get(nid)
        ]
        sector_counts: Dict[str, int] = {}
        for node in self.nodes.values():
            sec_val = node.sector.value if hasattr(node.sector, "value") else str(node.sector)
            sector_counts[sec_val] = sector_counts.get(sec_val, 0) + 1

        return {
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "isolated_nodes": isolated,
            "has_isolated_nodes": len(isolated) > 0,
            "sector_distribution": sector_counts,
            "memory_dir": self.memory_dir,
            "healthy": len(self.nodes) > 0 and len(self.edges) > 0 and len(isolated) == 0
        }
