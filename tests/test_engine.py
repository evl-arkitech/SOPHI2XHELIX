"""Tests for the deterministic game engine core."""

import numpy as np
from doublehelix.engine.kernel import DeterministicKernel
from doublehelix.engine.spatial import ContinuousCollisionDetector
from doublehelix.engine.memory_pool import StaticMemoryArena
from doublehelix.engine.renderer import HeadlessRenderer


def test_deterministic_kernel_run():
    kernel = DeterministicKernel(max_entities=20, bot_count=3)
    metrics = kernel.run_simulation(total_ticks=100)

    assert metrics["exit_code"] == 0
    assert metrics["ticks_executed"] == 100
    assert metrics["avg_frame_time_ms"] < 16.6  # easily passes 60 FPS budget
    assert metrics["tunneling_errors"] == 0
    assert metrics["shader_errors"] == 0
    assert metrics["visual_anomalies"] == 0
    assert metrics["headless_bot_crashes"] == 0


def test_static_memory_arena():
    arena = StaticMemoryArena(max_entities=10)
    idx = arena.allocate_entity(10.0, 20.0, 5.0, -5.0, 4.0, (255, 0, 0))
    assert idx == 0
    assert arena.pos_x[0] == 10.0
    assert arena.vel_y[0] == -5.0
    assert arena.active_count == 1


def test_continuous_collision_detection_swept_boundary():
    detector = ContinuousCollisionDetector(world_width=100.0, world_height=100.0)
    pos_x = np.array([98.0], dtype=np.float32)
    pos_y = np.array([50.0], dtype=np.float32)
    vel_x = np.array([500.0], dtype=np.float32)  # fast velocity towards wall
    vel_y = np.array([0.0], dtype=np.float32)
    radius = np.array([2.0], dtype=np.float32)

    detector.resolve_boundary_swept(pos_x, pos_y, vel_x, vel_y, radius, 1, 1.0 / 60.0)

    # Position clamped within boundary, velocity inverted
    assert pos_x[0] <= 98.0
    assert vel_x[0] < 0.0


def test_headless_renderer_buffer():
    renderer = HeadlessRenderer(width=64, height=36)
    renderer.clear(0.1, 0.2, 0.3)
    renderer.draw_circle(32.0, 18.0, 5.0, (1.0, 1.0, 1.0))
    anomalies = renderer.apply_post_processing_shader(0.0)
    assert anomalies == 0
    buffer_bytes = renderer.get_rgb_bytes()
    assert len(buffer_bytes) == 64 * 36 * 3
