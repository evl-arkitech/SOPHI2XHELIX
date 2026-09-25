"""City Echoes - Suburban Colonial House Environment & Tactical Hallway.

Reconstructs Sector 3: The Abyssal Outpost:
- Narrow second-floor suburban hallway: exactly 36 inches wide (0.9144m) x 12.0m long.
- Electrical breaker box cutting exterior power.
- Volumetric amber flashlight cone (3200K, 35 deg spread, 15m reach).
- Scotopic dark adaptation curve: pupil shock (<0.35s) -> rhodopsin logarithmic recovery.
- Acoustic debris chunks scattered across floor (shattered lath, 2x4 framing, gypsum cores).
"""

import math
from typing import List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class AcousticDebrisChunk:
    """A physical chunk of plaster/glass on the floor acting as an acoustic trap."""
    x: float
    y: float
    radius: float = 0.15 # 15cm trigger radius
    sound_db: float = 78.0 # Shattered glass / drywall crunch
    triggered: bool = False


@dataclass
class TacticalFlashlight:
    """Volumetric amber tactical flashlight casting long shadows down the hallway."""
    is_on: bool = True
    color_temp_k: int = 3200
    beam_angle_deg: float = 35.0
    reach_meters: float = 15.0
    intensity_lumens: float = 800.0


from doublehelix.games.city_echoes.models import LevelID, LevelConfig


LEVEL_CONFIGS: dict[LevelID, LevelConfig] = {
    LevelID.LEVEL_1_COLONIAL_HOUSE: LevelConfig(
        level_id=LevelID.LEVEL_1_COLONIAL_HOUSE,
        name="Suburban Colonial House - Master Suite",
        roof_height=5.95,
        interior_x_bounds=(-8.0, 8.0),
        interior_z_bounds=(-7.0, 7.0),
        porch_bounds=(1.9, 7.1, -9.5, -7.0, 2.9),
        exterior_rain_spl_db=70.0,
        interior_roof_tl_db=22.0,
        reverb_time_rt60_sec=0.45,
    ),
    LevelID.LEVEL_2_URBAN_TENEMENT: LevelConfig(
        level_id=LevelID.LEVEL_2_URBAN_TENEMENT,
        name="Urban Tenement - 4th Floor Corridor & Apt 4B",
        roof_height=3.60,
        interior_x_bounds=(-12.0, 12.0),
        interior_z_bounds=(-6.0, 6.0),
        porch_bounds=(-2.0, 2.0, 6.0, 8.5, 0.0), # Fire Escape exterior balcony
        exterior_rain_spl_db=74.0,
        interior_roof_tl_db=14.0, # Thin plaster/lath ceiling
        reverb_time_rt60_sec=0.75,
    ),
    LevelID.LEVEL_3_SUBTERRANEAN_BUNKER: LevelConfig(
        level_id=LevelID.LEVEL_3_SUBTERRANEAN_BUNKER,
        name="Sector 7 Subterranean Research Outpost",
        roof_height=4.80,
        interior_x_bounds=(-16.0, 16.0),
        interior_z_bounds=(-14.0, 14.0),
        porch_bounds=None, # Subterranean underground bunker
        exterior_rain_spl_db=0.0, # Zero exterior rain deep subterranean
        interior_roof_tl_db=80.0,
        reverb_time_rt60_sec=2.40,
    ),
}


def is_point_interior(level_id: LevelID, x: float, y: float, z: float) -> bool:
    """Returns True if (x, y, z) is physically inside the building volume below the roof."""
    cfg = LEVEL_CONFIGS[level_id]
    in_x = cfg.interior_x_bounds[0] <= x <= cfg.interior_x_bounds[1]
    in_z = cfg.interior_z_bounds[0] <= z <= cfg.interior_z_bounds[1]
    in_y = 0.0 <= y < cfg.roof_height
    return in_x and in_z and in_y


def get_min_rain_height_at(level_id: LevelID, x: float, z: float) -> float:
    """
    Computes the physical elevation where a falling rain particle terminates (splatters).
    Enforces absolute roof and exterior platform occlusion:
    - If over interior roof: terminates at roof_height (e.g. Y=5.95), never entering interior.
    - If over porch roof: terminates at porch height (Y=2.9).
    - If outside: falls down to ground level (Y=0.0).
    """
    cfg = LEVEL_CONFIGS[level_id]
    if cfg.porch_bounds is not None:
        px_min, px_max, pz_min, pz_max, py = cfg.porch_bounds
        if px_min <= x <= px_max and pz_min <= z <= pz_max:
            return py

    in_x = cfg.interior_x_bounds[0] <= x <= cfg.interior_x_bounds[1]
    in_z = cfg.interior_z_bounds[0] <= z <= cfg.interior_z_bounds[1]
    if in_x and in_z:
        return cfg.roof_height
    return 0.0


def is_rain_particle_valid(level_id: LevelID, x: float, y: float, z: float) -> bool:
    """
    Mathematical Invariant: Rain particles can NEVER exist inside any interior room.
    Density in Omega_interior is identically 0.0.
    """
    if is_point_interior(level_id, x, y, z):
        return False
    min_y = get_min_rain_height_at(level_id, x, z)
    return y >= min_y


@dataclass
class ColonialHouseHallway:
    """Architectural layout of the narrow 36-inch second floor corridor."""
    level_id: LevelID = LevelID.LEVEL_1_COLONIAL_HOUSE
    width_meters: float = 0.9144 # Exactly 36 inches wide
    length_meters: float = 12.0
    breaker_power_active: bool = False # Power cut by intruder
    flashlight: TacticalFlashlight = field(default_factory=TacticalFlashlight)
    debris_chunks: List[AcousticDebrisChunk] = field(default_factory=list)

    def __post_init__(self):
        if not self.debris_chunks:
            # Seed debris from fresh 12-gauge slug drywall breach
            self.debris_chunks = [
                AcousticDebrisChunk(x=0.45, y=3.2),
                AcousticDebrisChunk(x=0.30, y=4.5),
                AcousticDebrisChunk(x=0.60, y=6.0),
                AcousticDebrisChunk(x=0.40, y=8.2),
                AcousticDebrisChunk(x=0.50, y=9.5),
            ]

    # Static spatial tuples for zero-allocation hot checking
    DEBRIS_X = (0.45, 0.30, 0.60, 0.40, 0.50)
    DEBRIS_Y = (3.2, 4.5, 6.0, 8.2, 9.5)
    DEBRIS_R_SQ = (0.0225, 0.0225, 0.0225, 0.0225, 0.0225)
    DEBRIS_DB = (78.0, 78.0, 78.0, 78.0, 78.0)
    N_DEBRIS = 5

    def test_footstep_on_debris(self, foot_x: float, foot_y: float) -> Optional[float]:
        """Detects if player footstep triggers an acoustic debris crunch trap (zero allocations)."""
        for i in range(self.N_DEBRIS):
            dx = foot_x - self.DEBRIS_X[i]
            dy = foot_y - self.DEBRIS_Y[i]
            if dx * dx + dy * dy <= self.DEBRIS_R_SQ[i]:
                if i < len(self.debris_chunks):
                    self.debris_chunks[i].triggered = True
                return self.DEBRIS_DB[i]
        return None

    @staticmethod
    def calculate_scotopic_adaptation(time_since_blackout_sec: float) -> float:
        """
        Scotopic dark adaptation curve:
        - t < 0.35s: pupil shock blindness (exposure = 0.04)
        - 0.35s <= t <= 3.2s: rhodopsin logarithmic expansion up to 1.28
        """
        if time_since_blackout_sec < 0.35:
            return 0.04
        t_adapt = min(3.2, time_since_blackout_sec)
        adapt_progress = (t_adapt - 0.35) / (3.2 - 0.35)
        # Logarithmic expansion modeled as square root growth
        return 0.04 + (1.28 - 0.04) * math.sqrt(adapt_progress)

