"""City Echoes - Core Physics, Ballistics, Acoustic, and Biometric Models.

Grounded in rigorous empirical benchmarks and mathematical invariants:
- 12-Gauge slug (28.3g at 480 m/s = 3260.16 Joules) vs drywall & SPF 2x4 framing.
- Decibel Sound Pressure Level (SPL) with inverse-square decay & Transmission Loss (TL).
- Respiratory Oxygen Gating: linear decay to 0.0 at 12s, non-linear low-pass filter (350Hz - 20kHz).
- Exhaustion Gasp: 82 dB projecting through interior doors across a 9.0-meter alert radius.
- Asymmetric Economy: 4-minute round (240s = 14,400 ticks at 60 FPS), Team Pooling payouts.
"""

from dataclasses import dataclass
from typing import Tuple, List, Optional
import math


@dataclass(frozen=True)
class MaterialPhysics:
    """Architectural barrier resistance and acoustic transmission loss."""
    name: str
    shear_work_joules: float        # Work required to shear/perforate material
    stc_transmission_loss_db: float # Sound Transmission Class decibel loss
    thickness_mm: float             # Physical barrier thickness
    ricochet_critical_angle_deg: float = 15.0 # Critical angle for glance vs penetration


MATERIAL_DRYWALL_SINGLE = MaterialPhysics("Drywall_1/2in", shear_work_joules=180.0, stc_transmission_loss_db=6.0, thickness_mm=12.7)
MATERIAL_DRYWALL_DOUBLE = MaterialPhysics("Drywall_DoubleSheet", shear_work_joules=360.0, stc_transmission_loss_db=12.0, thickness_mm=25.4)
MATERIAL_WOOD_SPF_STUD = MaterialPhysics("2x4_SPF_Stud", shear_work_joules=2100.0, stc_transmission_loss_db=18.0, thickness_mm=89.0)
MATERIAL_HOLLOW_CORE_DOOR = MaterialPhysics("HollowCoreDoor", shear_work_joules=320.0, stc_transmission_loss_db=12.0, thickness_mm=35.0)
MATERIAL_SOLID_OAK_DOOR = MaterialPhysics("SolidOakDoor", shear_work_joules=2800.0, stc_transmission_loss_db=24.0, thickness_mm=45.0)
MATERIAL_SHATTERED_GLASS = MaterialPhysics("ShatteredGlass", shear_work_joules=40.0, stc_transmission_loss_db=0.0, thickness_mm=4.0)

# Multi-Level Architectural Materials
MATERIAL_WOOD_LATH_PLASTER = MaterialPhysics("WoodLath_Plaster", shear_work_joules=120.0, stc_transmission_loss_db=6.0, thickness_mm=19.0)
MATERIAL_REINFORCED_CONCRETE = MaterialPhysics("ReinforcedConcrete_300mm", shear_work_joules=18000.0, stc_transmission_loss_db=45.0, thickness_mm=300.0)
MATERIAL_STEEL_BLAST_DOOR = MaterialPhysics("SteelBlastDoor_Hydraulic", shear_work_joules=12000.0, stc_transmission_loss_db=35.0, thickness_mm=50.0)
MATERIAL_ROOF_SHINGLE_BARRIER = MaterialPhysics("RoofShingle_AtticBarrier", shear_work_joules=950.0, stc_transmission_loss_db=22.0, thickness_mm=150.0)

from enum import Enum

class LevelID(str, Enum):
    LEVEL_1_COLONIAL_HOUSE = "level_1_colonial_house"
    LEVEL_2_URBAN_TENEMENT = "level_2_urban_tenement"
    LEVEL_3_SUBTERRANEAN_BUNKER = "level_3_subterranean_bunker"


@dataclass(frozen=True)
class LevelConfig:
    """Tactical spatial, acoustic, and environmental boundaries for a level."""
    level_id: LevelID
    name: str
    roof_height: float
    interior_x_bounds: Tuple[float, float]
    interior_z_bounds: Tuple[float, float]
    exterior_rain_spl_db: float
    interior_roof_tl_db: float
    reverb_time_rt60_sec: float
    porch_bounds: Optional[Tuple[float, float, float, float, float]] = None # (x_min, x_max, z_min, z_max, y_height)



@dataclass(frozen=True)
class ProjectileSpec:
    """Newtonian ballistic projectile specifications."""
    name: str
    mass_kg: float
    muzzle_velocity_mps: float

    @property
    def kinetic_energy_joules(self) -> float:
        return 0.5 * self.mass_kg * (self.muzzle_velocity_mps ** 2)


# Ballistic Projectiles
SLUG_12GAUGE = ProjectileSpec("12-Gauge Slug", mass_kg=0.0283, muzzle_velocity_mps=480.0)      # 3260.16 Joules
HANDGUN_9MM = ProjectileSpec("9mm Luger FMJ", mass_kg=0.00745, muzzle_velocity_mps=360.0)      # 482.76 Joules
RIFLE_545X39 = ProjectileSpec("5.45x39mm 7N6", mass_kg=0.00343, muzzle_velocity_mps=880.0)    # 1328.79 Joules


@dataclass
class BiometricState:
    """Player respiratory state, oxygen curve, and acoustic stealth footprint."""
    max_hold_time_sec: float = 12.0
    hold_time_elapsed: float = 0.0
    is_holding_breath: bool = False
    exhaustion_triggered: bool = False
    heart_rate_bpm: float = 72.0

    @property
    def oxygen_level(self) -> float:
        """Linear oxygen depletion curve from 1.0 to 0.0 over hold duration."""
        if not self.is_holding_breath:
            return 1.0
        decay = 1.0 / self.max_hold_time_sec
        return max(0.0, 1.0 - (self.hold_time_elapsed * decay))

    @property
    def low_pass_filter_cutoff_hz(self) -> float:
        """Quadratic low-pass filter cutoff representing arterial blood thudding and suffocation."""
        f_min = 350.0   # Muffled underwater pulse
        f_max = 20000.0 # Full human audibility
        return f_min + (f_max - f_min) * (self.oxygen_level ** 2)

    @property
    def aim_stability_modifier(self) -> float:
        """Locks barrel dead still during breath hold, shakes violently upon exhaustion."""
        if self.exhaustion_triggered:
            return 3.5 # Violent weapon shake
        if self.is_holding_breath:
            return 0.05 # Dead still barrel
        return 1.0 # Normal standing sway

    def tick(self, dt: float) -> Optional[str]:
        """Advances biometrics by dt seconds. Returns 'EXHAUSTION_BETRAYAL' if air hits 0.0."""
        if self.is_holding_breath:
            self.hold_time_elapsed += dt
            self.heart_rate_bpm = min(150.0, self.heart_rate_bpm + dt * 4.0)
            if self.hold_time_elapsed >= self.max_hold_time_sec:
                self.is_holding_breath = False
                self.exhaustion_triggered = True
                self.hold_time_elapsed = 0.0
                return "EXHAUSTION_BETRAYAL"
        else:
            # Recovery
            self.hold_time_elapsed = max(0.0, self.hold_time_elapsed - dt * 2.0)
            self.heart_rate_bpm = max(72.0, self.heart_rate_bpm - dt * 2.5)
            if self.hold_time_elapsed == 0.0:
                self.exhaustion_triggered = False
        return None


@dataclass
class AcousticEvent:
    """Acoustic impulse emitted into the environment."""
    source_name: str
    source_db: float
    pos_x: float
    pos_y: float
    pos_z: float = 0.0
    barrier_tl_db: float = 0.0


@dataclass
class RoundEconomy:
    """Asymmetric 4-minute extraction and team pooling economics."""
    round_duration_sec: float = 240.0 # Exactly 4 minutes = 14,400 ticks at 60 FPS
    stake_amount: float = 50.0
    occupant_count: int = 3
    intruder_count: int = 1

    @property
    def total_pool(self) -> float:
        return self.stake_amount + (self.stake_amount * self.occupant_count)

    def calculate_intruder_payout(self, total_wipe: bool) -> float:
        """Intruder receives initial stake + (stake * occupants) upon total wipe."""
        return self.total_pool if total_wipe else 0.0

    def calculate_occupant_payout(self, surviving_occupants: int) -> float:
        """Surviving occupants divide intruder investment equally."""
        if surviving_occupants <= 0:
            return 0.0
        return self.stake_amount / surviving_occupants
