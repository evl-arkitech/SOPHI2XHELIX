"""Agent 5: Frame-Time & Memory Profiler (Strand Beta - Container 3).

Measures time-per-frame (microseconds/milliseconds), garbage-collection pauses,
VRAM utilization, and enforces zero-allocation constraints inside the hot tick loop.
"""

from typing import Dict, Any, List


class FrameTimeMemoryProfiler:
    """Evaluates frame budgets and zero-allocation invariants from raw runtime output."""

    TARGET_FRAME_TIME_MS = 16.6667  # 60 FPS standard
    BUDGET_WARNING_THRESHOLD_MS = 14.0

    def evaluate_telemetry(self, telemetry: Dict[str, Any]) -> Dict[str, Any]:
        avg_frame_time = float(telemetry.get("avg_frame_time_ms", 99.0))
        allocs_in_loop = int(telemetry.get("allocations_in_loop", 0))

        within_budget = avg_frame_time <= self.TARGET_FRAME_TIME_MS
        zero_alloc = (allocs_in_loop == 0)

        passed = within_budget and zero_alloc

        issues: List[str] = []
        if not within_budget:
            issues.append(
                f"Tick execution time ({avg_frame_time:.2f}ms) breached 16.6ms frame budget (est FPS: {1000.0/max(avg_frame_time, 0.001):.1f})"
            )
        if not zero_alloc:
            issues.append(
                f"Detected {allocs_in_loop} dynamic heap memory allocations inside update loop. Zero-allocation rule breached."
            )

        return {
            "passed": passed,
            "within_budget": within_budget,
            "zero_alloc": zero_alloc,
            "avg_frame_time_ms": avg_frame_time,
            "allocations_in_loop": allocs_in_loop,
            "issues": issues,
            "fps_estimate": 1000.0 / max(avg_frame_time, 0.0001)
        }
