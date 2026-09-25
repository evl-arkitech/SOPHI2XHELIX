"""Tests for HelixState and elevation tiers."""

from doublehelix.state import create_initial_state, ASCENDING_TIERS, BetaTelemetry


def test_initial_state_defaults():
    state = create_initial_state(max_cycles_per_tier=3)
    assert state["tier"] == "LEVEL_1_KERNEL"
    assert state["current_cycle"] == 0
    assert state["max_cycles_per_tier"] == 3
    assert state["allocations_in_loop"] == 0
    assert state["headless_bot_crashes"] == 0
    assert state["visual_anomalies"] == 0


def test_ascending_tiers_order():
    assert ASCENDING_TIERS == [
        "LEVEL_1_KERNEL",
        "LEVEL_2_ECS",
        "LEVEL_3_RENDER",
        "LEVEL_4_PLAYTEST",
        "CONVERGED"
    ]


def test_telemetry_schema():
    tel = BetaTelemetry(
        exit_code=0,
        avg_frame_time_ms=12.4,
        allocations_in_loop=0,
        tunneling_errors=0,
        shader_errors=0,
        visual_anomalies=0,
        headless_bot_crashes=0
    )
    assert tel.avg_frame_time_ms == 12.4
    assert tel.allocations_in_loop == 0
