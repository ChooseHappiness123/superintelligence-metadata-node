import time

class PersonalThresholdBinder:
    def __init__(self, max_acceptable_pressure: float = 0.12, min_honesty_floor: float = 75.0):
        # Personal local configuration boundaries
        self.max_acceptable_pressure = max_acceptable_pressure
        self.min_honesty_floor = min_honesty_floor

    def evaluate_personal_threshold_breach(self, live_map_payload: dict) -> dict:
        """
        Evaluates system status against personal risk boundaries. Triggers the 
        kill-switch path immediately if pressure ratio or honesty scores breach lines.
        """
        current_pressure = live_map_payload.get("live_risk_surface", {}).get("current_vault_outflow_ratio", 0.0)
        current_honesty = live_map_payload.get("public_honesty_heartbeat", {}).get("rolling_honesty_index_score", 100.0)
        triggering_url = live_map_payload.get("live_risk_surface", {}).get("triggering_source_url", "UNKNOWN_SOURCE")

        pressure_breached = current_pressure > self.max_acceptable_pressure
        honesty_breached = current_honesty < self.min_honesty_floor
        personal_kill_activated = pressure_breached or honesty_breached

        return {
            "timestamp": time.time(),
            "personal_constraints": {
                "configured_max_pressure": self.max_acceptable_pressure,
                "configured_min_honesty": self.min_honesty_floor
            },
            "breach_status": {
                "pressure_limit_exceeded": pressure_breached,
                "honesty_floor_compromised": honesty_breached,
                "personal_threshold_hit_marker": personal_kill_activated,
                "triggering_source_url": triggering_url
            },
            "enforced_strategy": "TRIGGER_IMMEDIATE_LOCAL_REDUCTION" if personal_kill_activated else "MONITORING_WITHIN_BOUNDS"
        }
