"""Telemetry extraction and parser for Container 3 (Headless Game Runtime).

Extracts metrics between __METRICS_START__ and __METRICS_END__ delimiters,
and falls back to stdout/stderr string analysis as specified in the Double Helix specification.
"""

import json
import re
import logging
from typing import Dict, Any

logger = logging.getLogger("TelemetryParser")


def parse_telemetry_output(
    stdout: str,
    stderr: str,
    returncode: int,
    total_time_ms: float,
    ticks: int
) -> Dict[str, Any]:
    """Extracts structured telemetry from stdout/stderr profiling output."""
    # 1. Primary: Match JSON block between __METRICS_START__ and __METRICS_END__
    pattern = r"__METRICS_START__\s*(\{.*?\})\s*__METRICS_END__"
    match = re.search(pattern, stdout, re.DOTALL)

    if match:
        try:
            data = json.loads(match.group(1))
            # Ensure required keys exist
            return {
                "exit_code": data.get("exit_code", returncode),
                "avg_frame_time_ms": float(data.get("avg_frame_time_ms", total_time_ms / max(ticks, 1))),
                "allocations_in_loop": int(data.get("allocations_in_loop", 0)),
                "tunneling_errors": int(data.get("tunneling_errors", 0)),
                "shader_errors": int(data.get("shader_errors", 0)),
                "visual_anomalies": int(data.get("visual_anomalies", 0)),
                "headless_bot_crashes": int(data.get("headless_bot_crashes", 1 if returncode != 0 else 0)),
                "raw_stdout": stdout[:2000]
            }
        except Exception as e:
            logger.debug("Failed to decode JSON block between metrics delimiters (%s); falling back to heuristic parsing", e)

    # 2. Specification Fallback: Heuristic stdout/stderr string parsing from PDF p. 10
    allocations_in_loop = 0 if "ALLOC_IN_UPDATE: 0" in stdout else (1 if "ALLOC" in stdout else 0)
    tunneling_errors = 1 if "COLLISION_TUNNELING" in stdout else 0
    shader_errors = 1 if "SHADER_COMPILATION_FAILED" in stderr else 0
    headless_bot_crashes = 1 if returncode != 0 else 0

    return {
        "exit_code": returncode,
        "avg_frame_time_ms": round(total_time_ms / max(ticks, 1), 3),
        "allocations_in_loop": allocations_in_loop,
        "tunneling_errors": tunneling_errors,
        "shader_errors": shader_errors,
        "visual_anomalies": 0,
        "headless_bot_crashes": headless_bot_crashes,
        "raw_stdout": stdout[:2000]
    }
