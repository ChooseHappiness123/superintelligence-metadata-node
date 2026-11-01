import time

class HonestyOracle:
    def __init__(self):
        self.base_score = 100.0
        self.critical_penalty_weight = 33.3
        self.motif_penalty_weight = 5.0
        self.velocity_floor = 1.44
        # Append-only ledger storing rolling historical score snapshots
        self.score_history_log = []

    def calculate_rolling_honesty_delta(self, timeline_report: dict, pressure_report: dict, promoted_motifs: list = None) -> dict:
        """
        Computes the unified rolling system convergence metric. Evaluates structural 
        on-chain pressure side-by-side with verified promoted narrative events.
        """
        rolling_score = self.base_score
        penalties_incurred = 0
        justifications = []
        triggering_url = "SYSTEM_INITIALIZATION"

        # 1. Evaluate chronological loop trap state
        if timeline_report.get("status") == "NARRATIVE_TRAP_TRIGGERED":
            penalties_incurred += 1
            rolling_score -= self.critical_penalty_weight
            justifications.append("CRITICAL: Repetitive token launch-to-collapse sequence identified without on-chain recovery.")

        # 2. Evaluate pool liquidity depth outbound leak parameters
        if pressure_report.get("kill_switch_triggered", False):
            penalties_incurred += 1
            rolling_score -= self.critical_penalty_weight
            justifications.append("CRITICAL: Vault outbound drift has breached acceptable threshold boundaries.")

        # 3. Evaluate verified promoted motif parameters (dynamic re-scoring window)
        if promoted_motifs:
            for event in promoted_motifs:
                triggering_url = event.get("source_url", "UNKNOWN_SOURCE")
                # Apply dynamic adjustments if a promoted motif correlates with cluster pressure vectors
                if event.get("motif") in ["0.0011", "azy", "boxes"]:
                    rolling_score -= self.motif_penalty_weight
                    justifications.append(f"MOTIF_ALERT: Verified token activity pattern found via: {triggering_url}")

        final_score = max(0.0, round(rolling_score, 1))
        
        snapshot = {
            "timestamp": time.time(),
            "rolling_honesty_score_pct": float(final_score),
            "verification_status": "NOMINAL_STABLE" if final_score > 70.0 else "SYSTEM_DEGRADED_SIZE_ZERO_RECOMMENDED",
            "audit_penalties_triggered": penalties_incurred,
            "forensic_justifications": justifications,
            "triggering_source_url": triggering_url,
            "grounding_velocity_floor": self.velocity_floor
        }
        
        # Log snapshot into the append-only historical store
        self.score_history_log.append(snapshot)
        return snapshot
