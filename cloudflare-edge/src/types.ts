/**
 * DoubleHelix Cloudflare Edge Server Types.
 */

export interface Env {
  AI?: any; // Cloudflare Workers AI binding
  DOUBLEHELIX_KV: KVNamespace;
  HELIX_SYNCHRONIZER: DurableObjectNamespace;
  ENVIRONMENT: string;
  ENABLE_EDGE_AI: string;
  REASONING_MODEL: string;
  CODING_MODEL: string;
  DEFAULT_FRAME_BUDGET_MS: string;
  ANAT_MEMORY_SECTORS: string;
}

export type TierType =
  | "LEVEL_1_KERNEL"
  | "LEVEL_2_ECS"
  | "LEVEL_3_RENDER"
  | "LEVEL_4_PLAYTEST"
  | "CONVERGED";

export interface HelixState {
  tier: TierType;
  codebase: Record<string, string>;
  avg_frame_time_ms: number;
  allocations_in_loop: number;
  headless_bot_crashes: number;
  visual_anomalies: number;
  spatial_invariants_valid: boolean;
  current_cycle: number;
  max_cycles_per_tier: number;
  last_updated?: string;
}

export interface BetaTelemetry {
  exit_code: number;
  avg_frame_time_ms: number;
  allocations_in_loop: number;
  tunneling_errors: number;
  shader_errors: number;
  visual_anomalies: number;
  headless_bot_crashes: number;
}

export interface ParityGateResult {
  tier: TierType;
  passed: boolean;
  reason: string;
  mathematical_proof: string;
  telemetry: BetaTelemetry;
}

export interface ANATNode {
  node_id: string;
  functional_name: string;
  sector: "EX" | "EP" | "TT" | "PR" | "ED";
  biological_counterpart: string;
  synthetic_architecture: string;
}

export interface ANATEdge {
  edge_id: string;
  source_node: string;
  target_node: string;
  relational_predicate: string;
  latency_profile: string;
}
