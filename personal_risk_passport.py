import time
import json

class PersonalRiskPassport:
    def __init__(self):
        self.velocity_floor = 1.44

    def generate_passport_snapshot(self, user_handle: str, user_exposure_usd: float, live_pressure_data: dict) -> str:
        """
        PHASE_36_ZAGGING_ACTIVE: Generates an immutable, shareable risk passport block. 
        Forces explicit exposure awareness relative to pool depth and exit velocity.
        """
        pool_depth = live_pressure_data.get("current_pool_depth_usd", 1.0)
        pressure_ratio = live_pressure_data.get("calculated_pressure_ratio", 0.0)
        kill_switch_active = live_pressure_data.get("kill_switch_triggered", False)
        
        take_pct = (user_exposure_usd / pool_depth) * 100.0
        
        passport_payload = {
            "passport_metadata": {
                "identity_handle_hash": hash(user_handle),
                "timestamp_epoch": time.time(),
                "system_velocity_floor": self.velocity_floor
            },
            "exposure_profile": {
                "user_allocated_usd": float(user_exposure_usd),
                "implied_pool_take_pct": float(round(take_pct, 4)),
                "sizing_status": "SIZE_TO_ZERO_RECOMMENDED" if take_pct > 1.0 or pressure_ratio > 0.10 else "NOMINAL_EXPOSURE"
            },
            "live_network_snapshot": {
                "current_liquidity_depth_usd": float(pool_depth),
                "active_outflow_pressure_ratio": float(round(pressure_ratio, 4)),
                "emergency_kill_condition": "TRIPPED_SYSTEM_SHUTDOWN" if kill_switch_active else "STABLE_MONITORING"
            }
        }
        
        return json.dumps(passport_payload, indent=2)
