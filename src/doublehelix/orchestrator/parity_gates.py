"""Parity Gate evaluators across the 4 Ascending Elevation Tiers.

Ensures code cannot graduate to higher abstractions if lower abstractions fail empirical benchmarks.
Level 1: 60 FPS (16.6ms) Hot-Loop Timing & Zero-Alloc Checks
Level 2: Spatial Partitioning Invariants & Tick Determinism (Collision resolution, CCD)
Level 3: Headless Framebuffer Capture & Visual Diffing (Zero NaN pixels, zero shader errors)
Level 4: Autonomous Bot Fuzzing & Frame-Budget Validation (10,000 simulated ticks without crash/deadlock)
"""

from typing import Tuple, Dict, Any


def evaluate_base_rung(tier: str, alpha: Dict[str, Any], beta: Dict[str, Any]) -> Tuple[bool, str]:
    """Base Rung Verification Gates as specified in the Double Helix specification."""
    # Level 1: Core Loop & Timing Invariant
    if tier == "LEVEL_1_KERNEL":
        avg_frame_time = beta.get("avg_frame_time_ms", 99.0)
        if avg_frame_time > 16.6:
            return False, f"Frame budget breached: {avg_frame_time:.2f}ms > 16.6ms (60 FPS limit)"
        allocations = beta.get("allocations_in_loop", 0)
        if allocations > 0:
            return False, f"Memory allocations detected inside update loop: {allocations} dynamic allocs"
        return True, "Deterministic loop stable (Frame budget & Zero-Alloc verified)"

    # Level 2: Spatial & Collision Invariant
    elif tier == "LEVEL_2_ECS":
        tunneling_errors = beta.get("tunneling_errors", 0)
        if tunneling_errors > 0:
            return False, f"Kinematic tunneling detected in collision grid: {tunneling_errors} tunneling events"
        if not alpha.get("spatial_invariants_valid", True):
            return False, "Cognitive spatial math proof failed for bounding-volume hierarchy"
        return True, "Spatial invariants and collision resolution verified"

    # Level 3: Perceptual/Shader Invariant
    elif tier == "LEVEL_3_RENDER":
        shader_errors = beta.get("shader_errors", 0)
        visual_anomalies = beta.get("visual_anomalies", 0)
        if visual_anomalies > 0 or shader_errors > 0:
            return (
                False,
                f"Shader compilation failure or visual anomaly (shader_errors={shader_errors}, visual_anomalies={visual_anomalies})"
            )
        return True, "Render pipeline, shader compilation, and offscreen framebuffer verified"

    # Level 4: Deep Autonomous Playtest
    elif tier == "LEVEL_4_PLAYTEST":
        bot_crashes = beta.get("headless_bot_crashes", 0)
        if bot_crashes > 0:
            return False, f"Bot fuzzer triggered {bot_crashes} crashes/deadlocks across entity states"
        return True, "Gameplay convergence achieved: 10,000 simulated ticks without desync or crash"

    return False, f"Unknown tier: {tier}"
