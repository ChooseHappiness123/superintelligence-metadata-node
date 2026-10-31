import time
from live_public_ingester import LivePublicIngester
from ecosystem_timeline_parser import EcosystemTimelineParser
from liquidity_pressure_monitor import LiquidityPressureMonitor
from emergency_kill_switch import EmergencyKillSwitch

class SimulationMapOnboarding:
    def __init__(self):
        self.kill_switch = EmergencyKillSwitch()
        self.pressure_monitor = LiquidityPressureMonitor(self.kill_switch)
        self.timeline_parser = EcosystemTimelineParser()
        self.ingester = LivePublicIngester()

    def compile_live_public_front_door(self, current_pool: dict, recent_outflows: dict, user_allocation: float) -> dict:
        """
        Pulls from identical live RPC engines and chronological timeline arrays to force
        an un-dismissible, source-linked verification state directly onto the entry layout.
        """
        # 1. Fetch current on-chain state and audit loop traps
        eth_rpc_snapshot = self.ingester.fetch_latest_ethereum_block_metrics()
        timeline_report = self.timeline_parser.parse_sequence_and_check_traps()
        pressure_state = self.pressure_monitor.evaluate_pool_pressure(current_pool, recent_outflows)
        
        pool_depth_usd = current_pool.get("current_pool_depth_usd", 1.0)
        pressure_ratio = pressure_state.get("calculated_pressure_ratio", 0.0)

        # 2. Map direct mathematical threat status based on public flow thresholds
        if pressure_ratio >= self.pressure_monitor.critical_pressure_ratio or timeline_report["status"] == "NARRATIVE_TRAP_TRIGGERED":
            active_threat_level = "CRITICAL_RED_BREACH"
        else:
            active_threat_level = "NOMINAL_MONITORING"

        # 3. Formulate the explicit, non-dismissible entry payload
        entry_map_schema = {
            "timestamp": time.time(),
            "rpc_backbone_link": eth_rpc_snapshot.get("source_verification_link"),
            "system_threat_level": active_threat_level,
            "kill_switch_tripped": pressure_state.get("kill_switch_triggered", False),
            
            "non_dismissible_forensic_layer": {
                "headline": "⚠️ CRITICAL SYSTEM TIMELINE DISCIPLINE WARNING",
                "trap_detected": timeline_report["status"] == "NARRATIVE_TRAP_TRIGGERED",
                "alert_summary": "Repetitive launch-to-collapse sequence identified across cluster markers (PNDC -> PORK -> wPOND).",
                "verified_event_history": self.timeline_parser.chronological_events
            },
            
            "live_risk_surface": {
                "available_liquidity_depth_usd": float(pool_depth_usd),
                "current_vault_outflow_ratio": float(round(pressure_ratio, 4)),
                "action_threshold_ceiling": self.pressure_monitor.critical_pressure_ratio,
                "user_implied_exposure_pct": float(round((user_allocation / pool_depth_usd) * 100.0, 4))
            },
            
            "onboarding_choice_paths": {
                "proceed_with_agency": "I acknowledge the source-linked outflows, historical deltas, and size my risk accordingly.",
                "one_click_exit": "Deploy local fallback paths to reduction tools."
            }
        }

        return entry_map_schema
