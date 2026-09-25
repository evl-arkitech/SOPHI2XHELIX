"""ANAT Explorable World Graph data models.

Defines the mathematical formalization of the graph G = (V, E, W),
operational cognitive sectors, and relational predicates.
"""

from typing import Dict, Any, List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class CognitiveSector(str, Enum):
    EXECUTIVE_GATING = "EX"  # Executive & Dynamic Gating
    EPISODIC_BUFFER = "EP"   # Episodic Fast-Buffer & Associative Routing
    ONLINE_SURPRISE = "TT"   # Online Surprise & Continuous Adaptation (Test-Time)
    PARAMETRIC_BASE = "PR"   # Parametric Base & Synaptic Regularization
    LABILIZATION = "ED"      # Labilization & Model Editing


class RelationalPredicate(str, Enum):
    GATES = "GATES"
    PROJECTS_TO = "PROJECTS_TO"
    RECONSTRUCTS = "RECONSTRUCTS"
    DIFFUSES_ACROSS = "DIFFUSES_ACROSS"
    CONSOLIDATES_INTO = "CONSOLIDATES_INTO"
    DESTABILIZES = "DESTABILIZES"
    MODULATES = "MODULATES"


class Node(BaseModel):
    """Vertex V in the Explorable World Graph."""
    node_id: str
    functional_name: str
    biological_counterpart: str
    synthetic_architecture: str
    update_regime: str
    representational_code: str
    sector: CognitiveSector = CognitiveSector.EXECUTIVE_GATING
    activation_state: Optional[List[float]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Edge(BaseModel):
    """Directed edge E with attributes W in the Explorable World Graph."""
    edge_id: str
    source_node: str
    target_node: str
    relational_predicate: RelationalPredicate
    modulation_trigger: str
    latency_profile: str
    weight: float = 1.0
    active: bool = True
