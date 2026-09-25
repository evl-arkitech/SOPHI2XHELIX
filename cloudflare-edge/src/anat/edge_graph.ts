/**
 * ANAT Explorable World Graph G = (V, E, W) Edge Implementation.
 * 
 * Provides sub-millisecond edge memory routing and cognitive sector traversal.
 */

import { ANATNode, ANATEdge } from "../types";

export const ANAT_EDGE_NODES: ANATNode[] = [
  { node_id: "N01_SCRATCH", functional_name: "Active Executive Scratchpad", sector: "EX", biological_counterpart: "dlPFC Microcircuits", synthetic_architecture: "Sliding-Window Attention + Fast-Weights" },
  { node_id: "N02_GATE", functional_name: "Gating & Routing Arbiter", sector: "EX", biological_counterpart: "Striatal Basal Ganglia loops", synthetic_architecture: "Non-linear Gated Attention / MoE Router" },
  { node_id: "N03_SILENT", functional_name: "Activity-Silent State Buffer", sector: "EX", biological_counterpart: "Short-Term Synaptic Plasticity", synthetic_architecture: "Dynamic Linear RNN / Fast-Weight Cache" },
  { node_id: "N04_SEPARATE", functional_name: "High-Dimensional Separator", sector: "EP", biological_counterpart: "Dentate Gyrus Granule Cells", synthetic_architecture: "Sparse Encoders / Locality-Sensitive Hashing" },
  { node_id: "N05_ATTRACT", functional_name: "Continuous Energy Attractor", sector: "EP", biological_counterpart: "Hippocampal CA3 Collaterals", synthetic_architecture: "Continuous Modern Hopfield Network" },
  { node_id: "N06_COMPARE", functional_name: "State Comparator Hub", sector: "EP", biological_counterpart: "Hippocampal CA1 Readout", synthetic_architecture: "Bidirectional Cross-Attention Verification" },
  { node_id: "N07_GRAPH", functional_name: "Associative Relational Index", sector: "EP", biological_counterpart: "Medial Temporal Hippocampus", synthetic_architecture: "HippoRAG Knowledge Graph + PageRank" },
  { node_id: "N08_TITANS", functional_name: "Surprise-Gated Memory Core", sector: "TT", biological_counterpart: "Midbrain-PFC Plastic Core", synthetic_architecture: "Titans Neural Long-Term Memory" },
  { node_id: "N09_SURPRISE", functional_name: "Prediction Error Detector", sector: "TT", biological_counterpart: "VTA/SNc Dopamine System", synthetic_architecture: "Loss Gradient Evaluator" },
  { node_id: "N10_PARAM", functional_name: "Parametric Knowledge Mantle", sector: "PR", biological_counterpart: "Neocortical Deep Layers", synthetic_architecture: "Transformer Feedforward Parameters (MLP)" },
  { node_id: "N11_TRIPLE", functional_name: "Offline Replay Synchronizer", sector: "PR", biological_counterpart: "SWS Triple Coupling Oscillations", synthetic_architecture: "Generative Latent Replay Scheduler" },
  { node_id: "N12_REGULAR", functional_name: "Metaplastic Synapse Guard", sector: "PR", biological_counterpart: "Synaptic Tagging & Capture", synthetic_architecture: "Elastic Weight Consolidation (EWC) / SI" },
  { node_id: "N13_DESTAB", functional_name: "Labilization Engine", sector: "ED", biological_counterpart: "Ubiquitin-Proteasome System", synthetic_architecture: "GluN2B-style Scaffolding Cleavage" },
  { node_id: "N14_SURGERY", functional_name: "Direct Factual Editor", sector: "ED", biological_counterpart: "Post-Retrieval Restabilization", synthetic_architecture: "ROME / MEMIT Low-Rank Solver" },
  { node_id: "N15_HORROR_FRAMEWORK", functional_name: "Structural Horror & Psychological Runtime", sector: "EX", biological_counterpart: "Amygdala-Insular Tension Controller", synthetic_architecture: "Two-Tier Director/Stalker + Sanity Pipeline" },
  { node_id: "N16_GRAPHICS_ARCHITECTURE", functional_name: "Real-Time Graphics & Shading Architecture", sector: "EX", biological_counterpart: "Visual Cortex (V1-V4)", synthetic_architecture: "Decoupled Visibility + Clustered Froxel + Cook-Torrance" },
  { node_id: "N17_DISTINCTION_ARCHITECTURE", functional_name: "Architecture of Distinction & Sensory Web Craft", sector: "EX", biological_counterpart: "Somatosensory Aesthetics", synthetic_architecture: "Kinetic Typography + Magnetic Affordances + Biquad Audio" }
];

export const ANAT_EDGE_TOPOGRAPHY: ANATEdge[] = [
  { edge_id: "E01", source_node: "N01_SCRATCH", target_node: "N02_GATE", relational_predicate: "PROJECTS_TO", latency_profile: "Sub-millisecond" },
  { edge_id: "E02", source_node: "N02_GATE", target_node: "N01_SCRATCH", relational_predicate: "GATES", latency_profile: "Dynamic" },
  { edge_id: "E03", source_node: "N01_SCRATCH", target_node: "N03_SILENT", relational_predicate: "PROJECTS_TO", latency_profile: "Immediate decay" },
  { edge_id: "E04", source_node: "N01_SCRATCH", target_node: "N09_SURPRISE", relational_predicate: "PROJECTS_TO", latency_profile: "Token-level" },
  { edge_id: "E05", source_node: "N09_SURPRISE", target_node: "N08_TITANS", relational_predicate: "GATES", latency_profile: "Test-time gradient" },
  { edge_id: "E06", source_node: "N01_SCRATCH", target_node: "N04_SEPARATE", relational_predicate: "PROJECTS_TO", latency_profile: "Event-driven" },
  { edge_id: "E07", source_node: "N04_SEPARATE", target_node: "N05_ATTRACT", relational_predicate: "PROJECTS_TO", latency_profile: "Matrix product" },
  { edge_id: "E08", source_node: "N04_SEPARATE", target_node: "N07_GRAPH", relational_predicate: "PROJECTS_TO", latency_profile: "Graph update" },
  { edge_id: "E09", source_node: "N05_ATTRACT", target_node: "N06_COMPARE", relational_predicate: "RECONSTRUCTS", latency_profile: "Iterative CCCP" },
  { edge_id: "E10", source_node: "N07_GRAPH", target_node: "N06_COMPARE", relational_predicate: "DIFFUSES_ACROSS", latency_profile: "Power iteration" },
  { edge_id: "E11", source_node: "N06_COMPARE", target_node: "N01_SCRATCH", relational_predicate: "PROJECTS_TO", latency_profile: "Context window" },
  { edge_id: "E12", source_node: "N05_ATTRACT", target_node: "N11_TRIPLE", relational_predicate: "PROJECTS_TO", latency_profile: "Batch sample" },
  { edge_id: "E13", source_node: "N07_GRAPH", target_node: "N11_TRIPLE", relational_predicate: "PROJECTS_TO", latency_profile: "Graph crawl" },
  { edge_id: "E14", source_node: "N11_TRIPLE", target_node: "N10_PARAM", relational_predicate: "CONSOLIDATES_INTO", latency_profile: "Offline epoch" },
  { edge_id: "E15", source_node: "N12_REGULAR", target_node: "N10_PARAM", relational_predicate: "GATES", latency_profile: "Regularizer" },
  { edge_id: "E16", source_node: "N09_SURPRISE", target_node: "N13_DESTAB", relational_predicate: "GATES", latency_profile: "Flag set" },
  { edge_id: "E17", source_node: "N13_DESTAB", target_node: "N14_SURGERY", relational_predicate: "GATES", latency_profile: "Causal trace" },
  { edge_id: "E18", source_node: "N14_SURGERY", target_node: "N10_PARAM", relational_predicate: "PROJECTS_TO", latency_profile: "Closed-form" },
  { edge_id: "E19", source_node: "N01_SCRATCH", target_node: "N15_HORROR_FRAMEWORK", relational_predicate: "PROJECTS_TO", latency_profile: "Frame-rate synchronous" },
  { edge_id: "E20", source_node: "N15_HORROR_FRAMEWORK", target_node: "N09_SURPRISE", relational_predicate: "GATES", latency_profile: "Continuous Director 1Hz tick" },
  { edge_id: "E21", source_node: "N01_SCRATCH", target_node: "N16_GRAPHICS_ARCHITECTURE", relational_predicate: "PROJECTS_TO", latency_profile: "Frame-rate synchronous" },
  { edge_id: "E22", source_node: "N16_GRAPHICS_ARCHITECTURE", target_node: "N15_HORROR_FRAMEWORK", relational_predicate: "MODULATES", latency_profile: "Frame-rate continuous" },
  { edge_id: "E23", source_node: "N01_SCRATCH", target_node: "N17_DISTINCTION_ARCHITECTURE", relational_predicate: "PROJECTS_TO", latency_profile: "Continuous input-rate" },
  { edge_id: "E24", source_node: "N17_DISTINCTION_ARCHITECTURE", target_node: "N16_GRAPHICS_ARCHITECTURE", relational_predicate: "MODULATES", latency_profile: "Per-frame synchronous" },
  { edge_id: "E25", source_node: "N17_DISTINCTION_ARCHITECTURE", target_node: "N15_HORROR_FRAMEWORK", relational_predicate: "MODULATES", latency_profile: "Interaction-driven event" }
];

export class ANATEdgeRouter {
  getNode(nodeId: string): ANATNode | undefined {
    return ANAT_EDGE_NODES.find((n) => n.node_id === nodeId);
  }

  getOutgoing(nodeId: string): ANATEdge[] {
    return ANAT_EDGE_TOPOGRAPHY.filter((e) => e.source_node === nodeId);
  }

  getIncoming(nodeId: string): ANATEdge[] {
    return ANAT_EDGE_TOPOGRAPHY.filter((e) => e.target_node === nodeId);
  }

  executeTrajectory(trajectoryId: "A" | "B" | "C" | "D" | "E", payload?: any) {
    switch (trajectoryId) {
      case "A":
        return {
          trajectory: "TRAJECTORY_A",
          name: "Real-Time Working Memory and Gated Input Ingestion",
          route: ["N01_SCRATCH", "E01", "N02_GATE", "E02", "N01_SCRATCH"],
          active: true
        };
      case "B":
        return {
          trajectory: "TRAJECTORY_B",
          name: "Surprise-Gated Episodic Encoding",
          route: ["N09_SURPRISE", "E05", "N08_TITANS", "N01_SCRATCH", "E06", "N04_SEPARATE", "E07", "N05_ATTRACT"],
          active: true
        };
      case "C":
        return {
          trajectory: "TRAJECTORY_C",
          name: "Associative Pattern Completion and Multi-Hop Retrieval",
          route: ["N01_SCRATCH", "N04_SEPARATE", "N05_ATTRACT", "E09", "N07_GRAPH", "E10", "N06_COMPARE", "E11", "N01_SCRATCH"],
          active: true
        };
      case "D":
        return {
          trajectory: "TRAJECTORY_D",
          name: "Offline Tripartite Consolidation",
          route: ["N11_TRIPLE", "E12", "N05_ATTRACT", "E13", "N07_GRAPH", "E14", "N10_PARAM", "E15", "N12_REGULAR"],
          active: true
        };
      case "E":
        return {
          trajectory: "TRAJECTORY_E",
          name: "Error-Induced Destabilization and Targeted Reconsolidation",
          route: ["N09_SURPRISE", "E16", "N13_DESTAB", "E17", "N14_SURGERY", "E18", "N10_PARAM"],
          active: true
        };
    }
  }
}
