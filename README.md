# Circadian Phase Angle of Entrainment & Internal Desynchrony Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](https://github.com/alphaparkinc/genpark-personal-agent-circadian-phase-angle-entrainment-skill)
[![OpenClaw Ready](https://img.shields.io/badge/OpenClaw-Compatible-purple.svg)](https://github.com/alphaparkinc/genpark-personal-agent-circadian-phase-angle-entrainment-skill)
[![MCP Protocol](https://img.shields.io/badge/MCP-Standard-orange.svg)](https://modelcontextprotocol.io/)

A sovereign personal agent capability for computational chronobiology, evaluating phase angles of entrainment ($\psi$), internal circadian desynchrony, and photic Phase Response Curve (PRC) adjustments.

## Architecture

```mermaid
flowchart TD
    Markers["Biomarkers: DLMO (Melatonin Onset) & CBTmin"] --> AngleCalc["Phase Angle Calculator (psi_DLMO_SO & psi_CBT_Wake)"]
    SleepSchedule["Sleep Log: Sleep Onset & Awakening Time"] --> AngleCalc
    AngleCalc --> ICDS["Internal Circadian Desynchrony Scoring (ICDS: 0-100)"]
    ICDS --> PRCEngine["Photic PRC Engine (Advance / Delay / Dead Zone)"]
    PRCEngine --> ActionPlan["OpenClaw / Hermes Solar & Screen Curfew Guidance"]
```

## Quickstart

```python
from client import CircadianPhaseAngleClient

client = CircadianPhaseAngleClient()

# Calculate internal phase angle of entrainment
res = client.calculate_phase_angle_of_entrainment(
    dlmo_time_str="21:45",
    sleep_onset_time_str="23:30",
    wake_time_str="07:15"
)

print("psi (DLMO -> Sleep Onset):", res["psi_dlmo_to_sleep_onset_hours"], "h")
print("Desynchrony Score:", res["internal_circadian_desynchrony_score"], "/ 100")
print("Status:", res["status"])
```

## MCP Server Integration

Add to your `claude_desktop_config.json` or OpenClaw tool registry:

```json
{
  "mcpServers": {
    "circadian-phase-angle": {
      "command": "python",
      "args": ["/path/to/genpark-personal-agent-circadian-phase-angle-entrainment-skill/mcp_server.py"]
    }
  }
}
```

## License
MIT License.
