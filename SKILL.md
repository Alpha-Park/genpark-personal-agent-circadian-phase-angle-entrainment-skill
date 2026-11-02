---
name: genpark-personal-agent-circadian-phase-angle-entrainment-skill
description: Deterministic evaluation of circadian phase angle of entrainment (psi), internal desynchrony scoring, and photic Phase Response Curve (PRC) adjustments.
version: 1.0.0
author: GenPark Autonomous Agents Ecosystem
license: MIT
tags:
  - personal-agent
  - ai-agent
  - openclaw
  - genpark
  - mcp
  - mcp-server
  - model-context-protocol
  - python
  - zero-dependency
  - wellness
  - productivity
  - production-ready
---

# Circadian Phase Angle of Entrainment & Internal Desynchrony Skill

## Overview
The `genpark-personal-agent-circadian-phase-angle-entrainment-skill` equips personal sovereign agents with rigorous chronobiological modeling of phase angles of entrainment ($\psi$). The temporal relationship between the central pacemaker (suprachiasmatic nucleus) rhythm—indexed by Dim Light Melatonin Onset (DLMO) and Core Body Temperature minimum ($CBT_{\min}$)—and sleep-wake behavior governs sleep latency, restorative sleep depth, and morning sleep inertia. This skill computes internal phase discrepancies and predicts light-induced phase shifts via empirical human Phase Response Curves (PRC).

## Physiological Model & Mathematics
1. **Phase Angle $\psi_{\text{DLMO}-\text{SO}}$**:
   $$\psi_{\text{DLMO}-\text{SO}} = t_{\text{Sleep Onset}} - t_{\text{DLMO}}$$
   - Normative physiological range: $+1.5\text{ to }+2.5\text{ hours}$.
   - Values $< 1.0\text{ h}$ indicate sleep attempts prior to the biological night opening, causing protracted sleep onset latency.
2. **Phase Angle $\psi_{\text{CBTmin}-\text{Wake}}$**:
   $$\psi_{\text{CBTmin}-\text{Wake}} = t_{\text{Wake}} - t_{\text{CBTmin}}$$
   - Normative physiological range: $+1.5\text{ to }+2.5\text{ hours}$.
   - Values $< 0.5\text{ h}$ force awakening during the biological temperature nadir, resulting in severe sleep inertia and hypothermia sensation.
3. **Internal Circadian Desynchrony Score ($ICDS$)**:
   $$\text{ICDS} = \text{Penalty}(\psi_{\text{DLMO}-\text{SO}}) + \text{Penalty}(\psi_{\text{CBTmin}-\text{Wake}})$$
4. **Photic Phase Response Curve ($PRC$)**:
   - Post-$CBT_{\min}$ photic pulse ($0\text{ to }+6\text{ h}$): Induces phase advance ($+\Delta\phi$, shifting rhythms earlier).
   - Pre-$CBT_{\min}$ evening photic pulse ($-6\text{ to }0\text{ h}$): Induces phase delay ($-\Delta\phi$, shifting rhythms later).

## Tools & Endpoints
- `calculate_phase_angle_of_entrainment`: Computes $\psi$ phase angles, assesses internal desynchrony score, and warns of biological night awakenings.
- `predict_prc_phase_shift`: Predicts circadian clock phase advances or delays from light exposure intensity, timing, and duration.
