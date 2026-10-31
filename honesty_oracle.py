import time

class HonestyOracle:
    def __init__(self):
        self.base_score = 100.0
        self.critical_penalty_weight = 33.3
        self.velocity_floor = 1.44

    def calculate_rolling_honesty_delta(self, timeline_report: dict, pressure_report: dict) -> dict:
        """
        Ingests real-time analytics reports and computes a clean mathematical 
        system honesty metric linked directly to on-chain realities.
        """
        rolling_score = self.base_score
        penalties_incurred = 0
        justifications = []

        # 1. Evaluate chronological narrative loop trap state
        if timeline_report.get("status") == "NARRATIVE_TRAP_TRIGGERED":
            penalties_incurred += 1
            rolling_score -= self.critical_penalty_weight
            justifications.append("CRITICAL_ALERT: Repetitive token launch-to-collapse sequence identified without liquidity recovery.")

        # 2. Evaluate pool liquidity depth outbound leak parameters
        if pressure_report.get("kill_switch_triggered", False):
            penalties_incurred += 1
            rolling_score -= self.critical_penalty_weight
            justifications.append("CRITICAL_ALERT: Vault leakage has breached acceptable threshold boundaries.")

        final_score = max(0.0, round(rolling_score, 1))
        
        return {
            "timestamp": time.time(),
            "rolling_honesty_score_pct": float(final_score),
            "verification_status": "NOMINAL_STABLE" if final_score > 70.0 else "SYSTEM_DEGRADED_SIZE_ZERO_RECOMMENDED",
            "audit_penalties_triggered": penalties_incurred,
            "forensic_justifications": justifications,
            "grounding_velocity_floor": self.velocity_floor
        }
