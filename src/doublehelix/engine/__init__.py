"""Deterministic game engine core modules."""

from doublehelix.engine.memory_pool import StaticMemoryArena, AllocationTrap
from doublehelix.engine.spatial import ContinuousCollisionDetector
from doublehelix.engine.renderer import HeadlessRenderer
from doublehelix.engine.bot_fuzzer import AutonomousBotFuzzer
from doublehelix.engine.kernel import DeterministicKernel

__all__ = [
    "StaticMemoryArena",
    "AllocationTrap",
    "ContinuousCollisionDetector",
    "HeadlessRenderer",
    "AutonomousBotFuzzer",
    "DeterministicKernel",
]
