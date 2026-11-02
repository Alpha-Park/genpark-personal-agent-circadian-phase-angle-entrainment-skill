"""
Example usage for Circadian Phase Angle of Entrainment Skill.
Demonstrates analyzing phase angle (psi) and predicting light-induced PRC phase shifts.
"""

from client import CircadianPhaseAngleClient


def main():
    client = CircadianPhaseAngleClient()

    print("=== 1. Evaluating Circadian Phase Angle of Entrainment ===")
    psi_res = client.calculate_phase_angle_of_entrainment(
        dlmo_time_str="21:45",
        sleep_onset_time_str="23:30",
        wake_time_str="07:15"
    )
    print(f"DLMO: {psi_res['dlmo_time']} | Sleep Onset: {psi_res['sleep_onset_time']} | Wake: {psi_res['wake_time']}")
    print(f"Estimated CBTmin: {psi_res['cbt_min_time']}")
    print(f"psi (DLMO to Sleep Onset): {psi_res['psi_dlmo_to_sleep_onset_hours']} hours (target: 1.5 - 2.5h)")
    print(f"psi (CBTmin to Wake): {psi_res['psi_cbt_min_to_wake_hours']} hours (target: 1.5 - 2.5h)")
    print(f"Desynchrony Score: {psi_res['internal_circadian_desynchrony_score']} / 100")
    print(f"Status: {psi_res['status']}")
    print(f"Clinical Guidance: {psi_res['clinical_guidance']}")

    print("\n=== 2. Predicting PRC Phase Advance from Morning Sunlight ===")
    prc_res = client.predict_prc_phase_shift(
        light_lux=8000.0,
        exposure_time_str="07:30",
        dlmo_time_str="21:45",
        exposure_duration_hours=0.75
    )
    print(f"Exposure Time: {prc_res['exposure_time']} at {prc_res['light_lux']} lux")
    print(f"Hours relative to CBTmin: {prc_res['hours_relative_to_cbt_min']} h")
    print(f"Shift Type: {prc_res['shift_type']}")
    print(f"Predicted Phase Shift: {prc_res['predicted_phase_shift_hours']} hours")
    print(f"Impact: {prc_res['circadian_impact']}")


if __name__ == "__main__":
    main()
