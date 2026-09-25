"""City Echoes - Inverse-Square Acoustic Propagation and Transmission Loss Engine.

Enforces acoustic stealth invariants:
- Inverse-square decibel attenuation: SPL(d) = SPL_0 - 20*log10(d) - TL
- Suburban ambient noise floor: 30.0 dB SPL
- Exhaustion gasp: 82 dB source projecting across 9.0m through closed doors (>50 dB residual)
- Glass crunch: 78 dB source audible at 3m open hallway and 9m behind hollow-core door
- Solid oak door (STC 24 dB) muffles 42 dB sneak footsteps below 30 dB noise floor
"""

import math
from typing import Tuple, List
from doublehelix.games.city_echoes.models import AcousticEvent


class AcousticsEngine:
    """Evaluates spatial sound pressure level (SPL) decay and wall transmission loss."""

    NOISE_FLOOR_DB = 30.0  # Quiet suburban nocturnal noise floor

    @staticmethod
    def compute_spl(
        source_db: float,
        distance_m: float,
        transmission_loss_db: float = 0.0
    ) -> float:
        """
        Computes Sound Pressure Level (SPL) in dB at distance with barrier loss.
        Formula: SPL = SPL_0 - 20 * log10(max(1.0, distance)) - TL
        """
        if distance_m <= 1.0:
            return max(0.0, source_db - transmission_loss_db)
        distance_decay = 20.0 * math.log10(distance_m)
        return max(0.0, source_db - distance_decay - transmission_loss_db)

    @classmethod
    def is_audible(cls, spl_db: float) -> bool:
        """Sound is audible if it breaches the ambient noise floor (30 dB)."""
        return spl_db > cls.NOISE_FLOOR_DB

    @classmethod
    def evaluate_sound_propagation(
        cls,
        event: AcousticEvent,
        listener_x: float,
        listener_y: float,
        barrier_tl_db: float = 0.0
    ) -> Tuple[float, bool]:
        """Calculates distance, received SPL, and audibility for an observer."""
        dx = listener_x - event.pos_x
        dy = listener_y - event.pos_y
        dist = math.sqrt(dx * dx + dy * dy)
        total_tl = event.barrier_tl_db + barrier_tl_db
        spl = cls.compute_spl(event.source_db, dist, total_tl)
        return spl, cls.is_audible(spl)

    @classmethod
    def compute_rain_occlusion_spl(
        cls,
        level_id: "LevelID",
        listener_x: float,
        listener_y: float,
        listener_z: float,
    ) -> Tuple[float, float]:
        """
        Computes the received rain Sound Pressure Level (dB) and low-pass filter cutoff (Hz).
        Returns (received_spl_db, low_pass_cutoff_hz).
        """
        from doublehelix.games.city_echoes.environment import LEVEL_CONFIGS, is_point_interior
        from doublehelix.games.city_echoes.models import LevelID

        cfg = LEVEL_CONFIGS[level_id]
        if level_id == LevelID.LEVEL_3_SUBTERRANEAN_BUNKER:
            # Deep subterranean bunker is 100% acoustically shielded from surface weather
            return 0.0, 0.0

        is_inside = is_point_interior(level_id, listener_x, listener_y, listener_z)
        if not is_inside:
            # Exterior exposure (porch roof or outdoor balcony): full unoccluded storm
            return cfg.exterior_rain_spl_db, 3500.0

        # Inside: occluded by roof, attic insulation, and joists
        interior_spl = max(0.0, cfg.exterior_rain_spl_db - cfg.interior_roof_tl_db)
        # Low-pass acoustic filter simulates wood/shingle barrier
        cutoff_hz = 450.0
        return interior_spl, cutoff_hz

