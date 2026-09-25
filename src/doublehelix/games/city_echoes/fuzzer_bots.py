"""City Echoes - Autonomous Actor Fuzzing & Behavioral State Machines.

Simulates asymmetric tactical actors under empirical constraints:
- Creep Gait: Asymmetric cadence (lead probe 0.88s vs follow step 0.48s; ratio > 1.5x)
- Stalker Predatory Pause: Freeze window between 4.0s and 7.5s
- Occupant Hold-Breath & Aim Stability: Dead still barrel during hold, panic gasp upon exhaustion
"""

import random
from typing import Tuple, Optional
from doublehelix.games.city_echoes.models import BiometricState


class CreepCadenceController:
    """Controls asymmetric creeping gait along the narrow corridor."""

    LEAD_PROBE_INTERVAL = 0.88    # Deliberate toe-testing stride
    FOLLOW_STEP_INTERVAL = 0.48   # Rapid follow-through step

    def __init__(self):
        self.is_lead_step = True
        self.step_timer = 0.0

    @classmethod
    def get_cadence_ratio(cls) -> float:
        return cls.LEAD_PROBE_INTERVAL / cls.FOLLOW_STEP_INTERVAL

    def update(self, dt: float) -> bool:
        """Returns True on the exact tick a foot makes floor contact."""
        self.step_timer += dt
        target_interval = self.LEAD_PROBE_INTERVAL if self.is_lead_step else self.FOLLOW_STEP_INTERVAL
        if self.step_timer >= target_interval:
            self.step_timer = 0.0
            self.is_lead_step = not self.is_lead_step
            return True
        return False


class StalkerIntruderBot:
    """Predatory AI listening for acoustic spikes and creeping through the house."""

    def __init__(self, pos_x: float = 0.45, pos_y: float = 0.0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.cadence = CreepCadenceController()
        self.is_paused = False
        self.pause_duration = 5.0
        self.pause_timer = 0.0
        self.alert_level = 0.0 # 0.0 to 1.0
        self.target_y: Optional[float] = None

    def tick(self, dt: float) -> Tuple[float, float, bool]:
        """
        Advances intruder position.
        Returns: (pos_x, pos_y, stepped_this_tick)
        """
        stepped = False
        if self.is_paused:
            self.pause_timer += dt
            if self.pause_timer >= self.pause_duration:
                self.is_paused = False
                self.pause_timer = 0.0
        else:
            if self.cadence.update(dt):
                stepped = True
                # Move forward along hallway
                self.pos_y += 0.35

                self.step_count = getattr(self, "step_count", 0) + 1
                # Deterministic predatory pause window [4.0, 7.5]s every 12 steps
                if (self.step_count % 12) == 0:
                    self.is_paused = True
                    self.pause_duration = 4.0 + float((self.step_count % 35) * 0.1)
                    self.pause_timer = 0.0

        return self.pos_x, self.pos_y, stepped

    def hear_sound(self, spl_db: float, source_y: float):
        """Reacts to sounds exceeding the 30 dB suburban noise floor."""
        if spl_db > 30.0:
            self.alert_level = min(1.0, self.alert_level + (spl_db - 30.0) * 0.05)
            self.target_y = source_y
            self.is_paused = False # Break pause to hunt


class OccupantHidingBot:
    """Defender hiding in bedroom closet holding breath and aiming 12-gauge shotgun."""

    def __init__(self, pos_x: float = 0.45, pos_y: float = 9.5):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.biometrics = BiometricState()
        self.has_fired = False

    def tick(self, dt: float, intruder_dist: float) -> Optional[str]:
        """
        Updates occupant decision tree.
        Holds breath when intruder is close (< 6.0m).
        """
        if intruder_dist < 6.0 and not self.biometrics.is_holding_breath and not self.biometrics.exhaustion_triggered:
            self.biometrics.is_holding_breath = True

        event = self.biometrics.tick(dt)
        return event # 'EXHAUSTION_BETRAYAL' or None
