"""Tests for telemetry extraction and formatting."""

from doublehelix.runtime.telemetry import parse_telemetry_output


def test_parse_telemetry_delimited():
    stdout = """
    Engine initializing...
    Allocating arenas...
    __METRICS_START__
    {"exit_code": 0, "avg_frame_time_ms": 1.25, "allocations_in_loop": 0, "tunneling_errors": 0, "shader_errors": 0, "visual_anomalies": 0, "headless_bot_crashes": 0}
    __METRICS_END__
    Shutdown complete.
    """
    metrics = parse_telemetry_output(stdout=stdout, stderr="", returncode=0, total_time_ms=1250.0, ticks=1000)
    assert metrics["avg_frame_time_ms"] == 1.25
    assert metrics["allocations_in_loop"] == 0
    assert metrics["tunneling_errors"] == 0
    assert metrics["visual_anomalies"] == 0
    assert metrics["headless_bot_crashes"] == 0


def test_parse_telemetry_fallback():
    stdout = "ALLOC_IN_UPDATE: 0\nCOLLISION_TUNNELING detected in tick 45\n"
    stderr = "SHADER_COMPILATION_FAILED: line 42 syntax error\n"
    metrics = parse_telemetry_output(stdout=stdout, stderr=stderr, returncode=1, total_time_ms=2000.0, ticks=1000)
    assert metrics["allocations_in_loop"] == 0
    assert metrics["tunneling_errors"] == 1
    assert metrics["shader_errors"] == 1
    assert metrics["headless_bot_crashes"] == 1
