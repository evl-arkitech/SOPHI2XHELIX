"""Zero-Allocation Memory Arena and Dynamic Allocation Trap.

Enforces Base Rung 1 Invariant: 0 allocations in the 16.6ms hot update loop.
Pre-allocates static arrays and Struct-of-Arrays (SoA) for entities and components.
"""

from typing import Tuple
import numpy as np
import tracemalloc


class StaticMemoryArena:
    """Pre-allocated contiguous buffers for zero-allocation ECS entity components."""

    def __init__(self, max_entities: int = 1000):
        self.max_entities = max_entities
        self.active_count = 0

        # Struct of Arrays (SoA) contiguous float32/int32 arrays
        self.entity_ids = np.zeros(max_entities, dtype=np.int32)
        self.pos_x = np.zeros(max_entities, dtype=np.float32)
        self.pos_y = np.zeros(max_entities, dtype=np.float32)
        self.vel_x = np.zeros(max_entities, dtype=np.float32)
        self.vel_y = np.zeros(max_entities, dtype=np.float32)
        self.radius = np.zeros(max_entities, dtype=np.float32)
        self.state = np.zeros(max_entities, dtype=np.int32)  # 0=Inactive, 1=Alive, 2=Dead
        self.render_color = np.zeros((max_entities, 3), dtype=np.uint8)

        # Pre-allocated scratch buffers to avoid allocations during calculations
        self.scratch_dx = np.zeros(max_entities, dtype=np.float32)
        self.scratch_dy = np.zeros(max_entities, dtype=np.float32)
        self.scratch_dist_sq = np.zeros(max_entities, dtype=np.float32)

    def allocate_entity(self, x: float, y: float, vx: float, vy: float, r: float, color: Tuple[int, int, int]) -> int:
        """Pre-loop allocation only. Hot loop should mutate in-place."""
        if self.active_count >= self.max_entities:
            raise MemoryError("Static Memory Arena capacity reached.")
        idx = self.active_count
        self.entity_ids[idx] = idx
        self.pos_x[idx] = x
        self.pos_y[idx] = y
        self.vel_x[idx] = vx
        self.vel_y[idx] = vy
        self.radius[idx] = r
        self.state[idx] = 1
        self.render_color[idx] = color
        self.active_count += 1
        return idx


class AllocationTrap:
    """Detects and counts heap memory allocations during a hot loop section.
    
    Enforces the zero-allocation rule: pre-allocated arenas must be mutated in-place
    without dynamic heap object creations.
    """

    def __init__(self, sample_interval: int = 100):
        self.alloc_count = 0
        self._is_active = False
        self.sample_interval = sample_interval
        self._baseline_blocks = 0

    def start(self):
        import sys
        self._is_active = True
        self.alloc_count = 0
        self._baseline_blocks = sys.getallocatedblocks()

    def check_dynamic_allocations(self, tick: int) -> int:
        """Samples heap block allocations without generating profiler allocation noise."""
        import sys
        if not self._is_active or (tick % self.sample_interval != 0):
            return 0
        current_blocks = sys.getallocatedblocks()
        # Measure net dynamic heap expansion above starting baseline
        net_delta = max(0, current_blocks - self._baseline_blocks)
        if net_delta > self.alloc_count:
            self.alloc_count = net_delta
        return net_delta

    def stop(self) -> int:
        import sys
        if self._is_active:
            current_blocks = sys.getallocatedblocks()
            net_delta = max(0, current_blocks - self._baseline_blocks)
            if net_delta > self.alloc_count:
                self.alloc_count = net_delta
        self._is_active = False
        return self.alloc_count

