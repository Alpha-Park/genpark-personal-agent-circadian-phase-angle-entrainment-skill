"""
Circadian Phase Angle of Entrainment & Internal Desynchrony Engine.
Provides deterministic, zero-dependency modeling of DLMO to Sleep-Onset phase angle (psi),
CBTmin-to-Wake relationships, circadian misalignment scoring, and Phase Response Curve (PRC) shifts.
"""

from typing import Dict, Any, List, Optional


class CircadianPhaseAngleClient:
    """
    Deterministic client for calculating circadian phase angles of entrainment and PRC phase shifts.
    Pure Python standard library implementation based on human circadian chronobiology literature.
    """

    def __init__(self):
        pass

    def _parse_time_to_hours(self, time_str: str) -> float:
        """Parse HH:MM string into fractional hours (0.0 - 24.0)."""
        parts = time_str.strip().split(":")
        h = float(parts[0])
        m = float(parts[1]) if len(parts) > 1 else 0.0
        return (h + m / 60.0) % 24.0

    def calculate_phase_angle_of_entrainment(
        self,
        dlmo_time_str: str,
        sleep_onset_time_str: str,
        wake_time_str: str,
        cbt_min_time_str: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calculates phase angle of entrainment (psi):
        - psi_DLMO_SO = Sleep Onset - DLMO (normative: 1.5 - 2.5 hours)
        - psi_CBT_Wake = Wake - CBTmin (normative: 1.5 - 2.5 hours)
        Evaluates internal circadian desynchrony score (ICDS, 0-100).
        """
        t_dlmo = self._parse_time_to_hours(dlmo_time_str)
        t_so = self._parse_time_to_hours(sleep_onset_time_str)
        t_wake = self._parse_time_to_hours(wake_time_str)

        # Delta DLMO to Sleep Onset (accounting for midnight wraparound)
        delta_dlmo_so = (t_so - t_dlmo) % 24.0
        if delta_dlmo_so > 12.0:
            delta_dlmo_so = delta_dlmo_so - 24.0  # DLMO occurred after attempted sleep onset

        # CBTmin estimation if not provided: standard CBTmin is ~7 hours after DLMO or ~2 hours before habitual wake
        if cbt_min_time_str:
            t_cbt = self._parse_time_to_hours(cbt_min_time_str)
        else:
            t_cbt = (t_dlmo + 7.0) % 24.0

        delta_cbt_wake = (t_wake - t_cbt) % 24.0
        if delta_cbt_wake > 12.0:
            delta_cbt_wake = delta_cbt_wake - 24.0  # Waking occurred before CBTmin

        # Normative target: delta_dlmo_so in [1.5, 2.5] hours
        dlmo_dev = 0.0
        if delta_dlmo_so < 1.5:
            dlmo_dev = (1.5 - delta_dlmo_so) * 25.0
        elif delta_dlmo_so > 2.5:
            dlmo_dev = (delta_dlmo_so - 2.5) * 15.0

        # Normative target: delta_cbt_wake in [1.5, 2.5] hours
        cbt_dev = 0.0
        if delta_cbt_wake < 1.5:
            cbt_dev = (1.5 - delta_cbt_wake) * 25.0  # High penalty for waking before CBTmin nadir
        elif delta_cbt_wake > 2.5:
            cbt_dev = (delta_cbt_wake - 2.5) * 15.0

        icds_score = round(min(100.0, max(0.0, dlmo_dev + cbt_dev)), 1)

        is_waking_in_circadian_night = delta_cbt_wake < 0.5
        is_sleeping_before_dlmo = delta_dlmo_so < 0.5

        if icds_score <= 15.0:
            status = "OPTIMAL_CIRCADIAN_ENTRAINMENT"
            recommendation = "Internal phase angle perfectly aligned. Melatonin surge precedes sleep onset by optimal ~2 hours."
        elif is_waking_in_circadian_night:
            status = "BIOLOGICAL_NIGHT_AWAKENING_INERTIA"
            recommendation = "Waking before core body temperature minimum nadir triggers profound sleep inertia. Delay wake time or advance DLMO."
        elif is_sleeping_before_dlmo:
            status = "DELAYED_CIRCADIAN_PHASE_MISALIGNMENT"
            recommendation = "Attempting sleep before dim light melatonin onset. Expect extended sleep latency. Implement bright light restriction 2h prior to bed."
        else:
            status = "MODERATE_PHASE_ANGLE_DISPERSION"
            recommendation = "Moderate phase dispersion. Stabilize morning light pulse within 30 minutes of awakening to anchor central suprachiasmatic nucleus."

        return {
            "dlmo_time": dlmo_time_str,
            "sleep_onset_time": sleep_onset_time_str,
            "wake_time": wake_time_str,
            "cbt_min_time": f"{int(t_cbt):02d}:{int((t_cbt % 1) * 60):02d}",
            "psi_dlmo_to_sleep_onset_hours": round(delta_dlmo_so, 2),
            "psi_cbt_min_to_wake_hours": round(delta_cbt_wake, 2),
            "internal_circadian_desynchrony_score": icds_score,
            "is_waking_in_circadian_night": is_waking_in_circadian_night,
            "status": status,
            "clinical_guidance": recommendation
        }

    def predict_prc_phase_shift(
        self,
        light_lux: float,
        exposure_time_str: str,
        dlmo_time_str: str,
        exposure_duration_hours: float = 1.0
    ) -> Dict[str, Any]:
        """
        Predicts circadian phase shift (advance or delay) from photic exposure based on human Phase Response Curve (PRC).
        - Light exposure 0-4h after CBTmin (~7h after DLMO) produces phase advances (+ shift).
        - Light exposure 0-4h before CBTmin (evening/first half of night) produces phase delays (- shift).
        """
        t_exp = self._parse_time_to_hours(exposure_time_str)
        t_dlmo = self._parse_time_to_hours(dlmo_time_str)
        t_cbt = (t_dlmo + 7.0) % 24.0

        # Relative circadian time relative to CBTmin
        rel_time = (t_exp - t_cbt) % 24.0
        if rel_time > 12.0:
            rel_time = rel_time - 24.0  # -12 to +12 hours relative to CBTmin

        # Photic efficacy multiplier (logarithmic saturation above 1000 lux)
        if light_lux < 50.0:
            lux_factor = 0.05
        elif light_lux < 500.0:
            lux_factor = 0.35
        elif light_lux < 2500.0:
            lux_factor = 0.75
        else:
            lux_factor = 1.0

        # PRC shape approximation:
        # rel_time in [-6, 0]: Delay region (shifts rhythm later)
        # rel_time in [0, +6]: Advance region (shifts rhythm earlier)
        max_shift_hours = 1.8 * exposure_duration_hours * lux_factor

        if 0.0 <= rel_time <= 6.0:
            shift_type = "PHASE_ADVANCE"
            magnitude_hours = round(max_shift_hours * (1.0 - (rel_time / 6.0)), 2)
            shift_hours = magnitude_hours
            effect = f"Advances central circadian clock earlier by +{shift_hours} hours."
        elif -6.0 <= rel_time < 0.0:
            shift_type = "PHASE_DELAY"
            magnitude_hours = round(max_shift_hours * (1.0 - (abs(rel_time) / 6.0)), 2)
            shift_hours = -magnitude_hours
            effect = f"Delays central circadian clock later by -{abs(shift_hours)} hours."
        else:
            shift_type = "DEAD_ZONE"
            shift_hours = 0.0
            effect = "Exposure occurred in the subjective daytime dead zone; negligible circadian phase shift."

        return {
            "exposure_time": exposure_time_str,
            "cbt_min_reference": f"{int(t_cbt):02d}:{int((t_cbt % 1) * 60):02d}",
            "hours_relative_to_cbt_min": round(rel_time, 2),
            "light_lux": light_lux,
            "shift_type": shift_type,
            "predicted_phase_shift_hours": shift_hours,
            "circadian_impact": effect
        }
