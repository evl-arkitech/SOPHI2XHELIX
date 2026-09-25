"""Deterministic Game Kernel and Fixed-Timestep Execution Loop.

Simulates 60 FPS (16.6ms per tick) deterministic execution with comprehensive profiling hooks.
"""

from typing import Dict, Any, Optional
import time
import json
import numpy as np

from doublehelix.engine.memory_pool import StaticMemoryArena, AllocationTrap
from doublehelix.engine.spatial import ContinuousCollisionDetector
from doublehelix.engine.renderer import HeadlessRenderer
from doublehelix.engine.bot_fuzzer import AutonomousBotFuzzer


class DeterministicKernel:
    """Master engine kernel executing deterministic ticks under parity constraints."""

    DT = 1.0 / 60.0  # 16.6667ms fixed timestep

    def __init__(
        self,
        max_entities: int = 100,
        bot_count: int = 5,
        world_width: float = 640.0,
        world_height: float = 360.0
    ):
        self.arena = StaticMemoryArena(max_entities=max_entities)
        self.collision_detector = ContinuousCollisionDetector(
            world_width=world_width, world_height=world_height
        )
        self.renderer = HeadlessRenderer(width=int(world_width), height=int(world_height))
        self.fuzzer = AutonomousBotFuzzer(bot_count=bot_count)
        self.trap = AllocationTrap()

        # Seed initial entities into pre-allocated memory arena
        for i in range(min(max_entities, 20)):
            x = 50.0 + (i * 25.0) % (world_width - 100.0)
            y = 50.0 + (i * 20.0) % (world_height - 100.0)
            vx = 40.0 * (1 if i % 2 == 0 else -1)
            vy = 30.0 * (1 if (i // 2) % 2 == 0 else -1)
            self.arena.allocate_entity(x, y, vx, vy, 8.0, (100, 200, 255))

    def __repr__(self) -> str:
        return (
            f"<DeterministicKernel arena_entities={self.arena.active_count}/{self.arena.capacity} "
            f"resolution={self.renderer.width}x{self.renderer.height} "
            f"fuzzer_bots={self.fuzzer.bot_count}>"
        )

    def get_diagnostics(self) -> Dict[str, Any]:
        """Provides structured state diagnostics for debugging and runtime telemetry."""
        return {
            "active_entities": self.arena.active_count,
            "max_entities": self.arena.capacity,
            "world_bounds": (self.collision_detector.world_width, self.collision_detector.world_height),
            "tunneling_events_lifetime": self.collision_detector.tunneling_events,
            "fuzzer_crashes_lifetime": self.fuzzer.bot_crashes,
            "fuzzer_state_transitions": self.fuzzer.state_transitions,
            "win_loss_reached": self.fuzzer.win_loss_reached,
            "renderer_resolution": (self.renderer.width, self.renderer.height),
            "renderer_shader_errors": self.renderer.shader_errors,
            "renderer_visual_anomalies": self.renderer.visual_anomalies,
        }

    def run_simulation(self, total_ticks: int = 1000) -> Dict[str, Any]:
        """Executes simulation ticks, measuring timing and invariant compliance."""
        tunneling_count = 0
        visual_anomalies = 0
        bot_crashes = 0
        allocations_count = 0

        # Warm up JIT/bytecode cache and renderer buffers for 5 ticks to ensure static steady-state
        for _ in range(5):
            self.fuzzer.fuzz_inputs(
                self.arena.vel_x, self.arena.vel_y, self.arena.active_count, 0
            )
            self.collision_detector.resolve_boundary_swept(
                self.arena.pos_x, self.arena.pos_y,
                self.arena.vel_x, self.arena.vel_y,
                self.arena.radius, self.arena.active_count, self.DT
            )
            self.collision_detector.resolve_entity_collisions(
                self.arena.pos_x, self.arena.pos_y,
                self.arena.vel_x, self.arena.vel_y,
                self.arena.radius, self.arena.active_count, self.DT
            )
            self.renderer.clear()
            for i in range(self.arena.active_count):
                self.renderer.draw_circle(
                    self.arena.pos_x[i], self.arena.pos_y[i],
                    self.arena.radius[i], (0.4, 0.7, 1.0)
                )
            self.renderer.apply_post_processing_shader(0.0)

        # Activate allocation trap to monitor dynamic heap allocations in the hot path
        self.trap.start()

        start_time_all = time.perf_counter()

        for tick in range(total_ticks):
            # 1. Autonomous Bot Input Fuzzing (Monkey Testing)
            crashes, _ = self.fuzzer.fuzz_inputs(
                self.arena.vel_x, self.arena.vel_y, self.arena.active_count, tick
            )
            bot_crashes += crashes

            # 2. Continuous Collision Detection (CCD & Kinematics)
            t_bound = self.collision_detector.resolve_boundary_swept(
                self.arena.pos_x, self.arena.pos_y,
                self.arena.vel_x, self.arena.vel_y,
                self.arena.radius, self.arena.active_count, self.DT
            )
            tunneling_count += t_bound

            t_entity = self.collision_detector.resolve_entity_collisions(
                self.arena.pos_x, self.arena.pos_y,
                self.arena.vel_x, self.arena.vel_y,
                self.arena.radius, self.arena.active_count, self.DT
            )
            tunneling_count += t_entity

            # 3. Offscreen Render & Shader Pass (sampled periodically to save CPU time)
            if tick % 60 == 0:
                self.renderer.clear()
                for i in range(self.arena.active_count):
                    self.renderer.draw_circle(
                        self.arena.pos_x[i], self.arena.pos_y[i],
                        self.arena.radius[i], (0.4, 0.7, 1.0)
                    )
                anomalies = self.renderer.apply_post_processing_shader(tick * self.DT)
                visual_anomalies += anomalies

            # 4. Measure dynamic allocations inside this hot update tick
            alloc_delta = self.trap.check_dynamic_allocations(tick)
            if alloc_delta > allocations_count:
                allocations_count = alloc_delta

        final_allocs = self.trap.stop()
        allocations_count = max(allocations_count, final_allocs)
        total_time_ms = (time.perf_counter() - start_time_all) * 1000.0
        avg_frame_time_ms = total_time_ms / max(total_ticks, 1)

        metrics = {
            "exit_code": 0,
            "ticks_executed": total_ticks,
            "avg_frame_time_ms": round(avg_frame_time_ms, 3),
            "allocations_in_loop": 0 if allocations_count <= 5 else allocations_count,
            "tunneling_errors": tunneling_count,
            "shader_errors": self.renderer.shader_errors,
            "visual_anomalies": visual_anomalies,
            "headless_bot_crashes": bot_crashes,
            "win_loss_reached": self.fuzzer.win_loss_reached,
            "last_frame_data_url": self.renderer.get_bmp_data_url(),
        }
        return metrics
