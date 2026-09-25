"""Test suite for DoubleHelix City Echoes Game Engine Rebuild.

Verifies:
- 5 Analytical Mathematical Proofs of Concept
- Ballistic Penetration & Spall Kinematics
- Inverse-Square Acoustic Attenuation & Wall Transmission Loss
- Biometric Oxygen Depletion & Low-Pass Filter Modulation
- Scotopic Dark Adaptation & Asymmetric Creep Gait
- Zero-Allocation Deterministic Game Kernel
- ANAT Explorable World Graph Cognitive Bridge
"""

import math
import pytest

from doublehelix.games.city_echoes.models import (
    SLUG_12GAUGE, HANDGUN_9MM, MATERIAL_DRYWALL_DOUBLE, MATERIAL_WOOD_SPF_STUD,
    MATERIAL_HOLLOW_CORE_DOOR, MATERIAL_SOLID_OAK_DOOR, BiometricState, RoundEconomy
)
from doublehelix.games.city_echoes.ballistics import BallisticsSimulator
from doublehelix.games.city_echoes.acoustics import AcousticsEngine
from doublehelix.games.city_echoes.environment import ColonialHouseHallway
from doublehelix.games.city_echoes.fuzzer_bots import CreepCadenceController, StalkerIntruderBot
from doublehelix.games.city_echoes.kernel import CityEchoesKernel
from doublehelix.games.city_echoes.anat_bridge import CityEchoesANATBridge
from doublehelix.proofs.city_echoes_proofs import CityEchoesTheoremProver


def test_city_echoes_all_mathematical_proofs():
    """Verifies all 7 formal theorems pass Q.E.D."""
    proofs = CityEchoesTheoremProver.prove_all()
    assert proofs["all_passed"] is True
    assert proofs["theorems_verified"] == 7
    assert proofs["proofs"]["rain_occlusion"]["passed"] is True
    assert proofs["proofs"]["multilevel_hierarchy"]["passed"] is True


def test_rain_occlusion_and_acoustic_invariance():
    """Confirms rain particles cannot enter interior volume and interior SPL is attenuated >= 22 dB."""
    proof = CityEchoesTheoremProver.prove_rain_occlusion_invariance()
    assert proof["passed"] is True
    assert proof["interior_density_zero"] is True
    assert proof["spl_inside_db"] <= 48.0
    assert proof["cutoff_inside_hz"] == 450.0
    assert proof["spl_outside_db"] == 70.0


def test_multilevel_structural_hierarchy():
    """Confirms monotonic acoustic TL progression and ballistic partitioning."""
    proof = CityEchoesTheoremProver.prove_multilevel_structural_hierarchy()
    assert proof["passed"] is True
    assert proof["monotonic_tl_progression"] is True
    assert proof["bunker_blast_door_stopped_slug"] is True



def test_12gauge_slug_drywall_penetration():
    """12-Gauge slug (3260J) punches through double drywall with exit velocity > 400 m/s."""
    penetrated, exit_v, residual_ke = BallisticsSimulator.calculate_penetration(
        SLUG_12GAUGE, MATERIAL_DRYWALL_DOUBLE
    )
    assert penetrated is True
    assert exit_v > 400.0
    assert residual_ke > 2500.0


def test_9mm_stopped_by_2x4_stud():
    """9mm FMJ (482.76J) is stopped by dense 2x4 spruce-pine-fir stud (2100J)."""
    penetrated, exit_v, residual_ke = BallisticsSimulator.calculate_penetration(
        HANDGUN_9MM, MATERIAL_WOOD_SPF_STUD
    )
    assert penetrated is False
    assert exit_v == 0.0
    assert residual_ke == 0.0


def test_acoustic_exhaustion_gasp_at_9m():
    """82 dB exhaustion gasp at 9.0m through closed door breaches 30 dB suburban noise floor."""
    spl, audible = AcousticsEngine.evaluate_sound_propagation(
        event=AcousticEventWrapper(82.0, 0.0, 9.0),
        listener_x=0.0,
        listener_y=0.0,
        barrier_tl_db=12.0
    )
    assert spl > 50.0
    assert audible is True


def test_oak_door_muffles_sneaker():
    """42 dB sneak footsteps behind solid oak door (STC 24 dB) at 4m are masked by ambient 30 dB."""
    spl = AcousticsEngine.compute_spl(source_db=42.0, distance_m=4.0, transmission_loss_db=24.0)
    assert spl < 30.0
    assert AcousticsEngine.is_audible(spl) is False


def test_biometrics_oxygen_and_filter():
    """Oxygen drains linearly to 0 at 12s, low-pass filter drops non-linearly."""
    bio = BiometricState()
    assert bio.oxygen_level == 1.0
    assert bio.low_pass_filter_cutoff_hz == 20000.0

    bio.is_holding_breath = True
    bio.tick(6.0)
    assert math.isclose(bio.oxygen_level, 0.5, abs_tol=1e-3)
    assert bio.low_pass_filter_cutoff_hz < 10000.0

    event = bio.tick(6.0) # Hits 12s
    assert event == "EXHAUSTION_BETRAYAL"
    assert bio.exhaustion_triggered is True


def test_scotopic_dark_adaptation():
    """Scotopic recovery: shock phase < 0.35s (<0.10 exposure), > 50% recovery at 1.8s."""
    shock = ColonialHouseHallway.calculate_scotopic_adaptation(0.2)
    assert shock < 0.10

    adapt = ColonialHouseHallway.calculate_scotopic_adaptation(1.8)
    assert adapt > 0.50
    assert adapt < 1.28


def test_creep_cadence_ratio():
    """Asymmetric creeping gait must maintain cadence ratio > 1.5x."""
    ratio = CreepCadenceController.get_cadence_ratio()
    assert ratio > 1.50


def test_city_echoes_deterministic_kernel():
    """Executes 600 ticks of City Echoes: verifies 0 allocations in hot loop, < 16.6ms frame time."""
    kernel = CityEchoesKernel()
    metrics = kernel.run_simulation(total_ticks=600)
    assert metrics["exit_code"] == 0
    assert metrics["allocations_in_loop"] == 0
    assert metrics["avg_frame_time_ms"] < 16.6
    assert metrics["tunneling_errors"] == 0
    assert metrics["visual_anomalies"] == 0
    assert metrics["last_frame_data_url"].startswith("data:image/bmp;base64,")


def test_anat_bridge_tactical_dispatch():
    """Verifies tactical events trigger ANAT cognitive trajectories."""
    bridge = CityEchoesANATBridge()
    res_a = bridge.dispatch_acoustic_event(sound_db=78.0, source_type="GlassCrunch")
    assert res_a["anat_trajectory"] == "TRAJECTORY_A"
    assert len(res_a["nodes_activated"]) > 0

    res_b = bridge.dispatch_wall_breach(slug_velocity=452.73, spall_chunks=12)
    assert res_b["anat_trajectory"] == "TRAJECTORY_B"
    assert res_b["encoded"] is True


class AcousticEventWrapper:
    def __init__(self, source_db, x, y):
        self.source_db = source_db
        self.pos_x = x
        self.pos_y = y
        self.barrier_tl_db = 0.0
