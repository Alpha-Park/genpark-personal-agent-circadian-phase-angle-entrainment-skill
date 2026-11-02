"""
MCP Server for Circadian Phase Angle of Entrainment & Internal Desynchrony.
Exposes JSON-RPC endpoints for phase angle calculation (psi) and Phase Response Curve (PRC) predictions.
"""

import json
import sys
from client import CircadianPhaseAngleClient

client = CircadianPhaseAngleClient()


def handle_request(request: dict) -> dict:
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "calculate_phase_angle_of_entrainment",
                        "description": "Calculates circadian phase angle (psi) between DLMO, sleep onset, CBT minimum, and awakening, scoring internal circadian desynchrony.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "dlmo_time_str": {"type": "string", "description": "Dim light melatonin onset time in HH:MM (e.g. '21:30')"},
                                "sleep_onset_time_str": {"type": "string", "description": "Actual or attempted sleep onset time in HH:MM (e.g. '23:30')"},
                                "wake_time_str": {"type": "string", "description": "Habitual or target wake time in HH:MM (e.g. '07:00')"},
                                "cbt_min_time_str": {"type": "string", "description": "Optional core body temperature nadir time in HH:MM (defaults to DLMO + 7h)"}
                            },
                            "required": ["dlmo_time_str", "sleep_onset_time_str", "wake_time_str"]
                        }
                    },
                    {
                        "name": "predict_prc_phase_shift",
                        "description": "Predicts circadian phase shift (advance or delay) from photic exposure using human Phase Response Curve (PRC) kinetics.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "light_lux": {"type": "number", "description": "Illuminance in lux (e.g. 10000 for bright outdoor light, 300 for indoor)"},
                                "exposure_time_str": {"type": "string", "description": "Time of photic exposure in HH:MM (e.g. '07:30')"},
                                "dlmo_time_str": {"type": "string", "description": "Baseline DLMO time in HH:MM (e.g. '21:30')"},
                                "exposure_duration_hours": {"type": "number", "default": 1.0, "description": "Duration of light exposure in hours"}
                            },
                            "required": ["light_lux", "exposure_time_str", "dlmo_time_str"]
                        }
                    }
                ]
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "calculate_phase_angle_of_entrainment":
            res = client.calculate_phase_angle_of_entrainment(
                dlmo_time_str=args.get("dlmo_time_str", "21:30"),
                sleep_onset_time_str=args.get("sleep_onset_time_str", "23:30"),
                wake_time_str=args.get("wake_time_str", "07:00"),
                cbt_min_time_str=args.get("cbt_min_time_str")
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }

        elif tool_name == "predict_prc_phase_shift":
            res = client.predict_prc_phase_shift(
                light_lux=args.get("light_lux", 5000.0),
                exposure_time_str=args.get("exposure_time_str", "07:30"),
                dlmo_time_str=args.get("dlmo_time_str", "21:30"),
                exposure_duration_hours=args.get("exposure_duration_hours", 1.0)
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method {tool_name} not found"}
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32600, "message": "Invalid Request"}
    }


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
