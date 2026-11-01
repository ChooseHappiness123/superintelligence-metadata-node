import time
from live_public_ingester import LivePublicIngester
from ecosystem_timeline_parser import EcosystemTimelineParser
from liquidity_pressure_monitor import LiquidityPressureMonitor
from emergency_kill_switch import EmergencyKillSwitch
from honesty_oracle import HonestyOracle
from counterfactual_exit_simulator import CounterfactualExitSimulator
from receipt_event_sink import ReceiptEventSink

class SimulationMapOnboarding:
    def __init__(self, shared_sink_instance: ReceiptEventSink, shared_oracle_instance: HonestyOracle, shared_monitor_instance: LiquidityPressureMonitor):
        self.kill_switch = EmergencyKillSwitch()
        self.timeline_parser = EcosystemTimelineParser()
        self.ingester = LivePublicIngester()
        self.exit_sim = CounterfactualExitSimulator()
        # Bind straight to synchronized shared logic references
        self.sink = shared_sink_instance
        self.oracle = shared_oracle_instance
        self.pressure_monitor = shared_monitor_instance

    def compile_live_public_front_door(self, current_pool: dict, recent_outflows: dict, user_allocation: float) -> dict:
        """
        PHASE_36_ZAGGING_ACTIVE: Generates public onboarding map coordinates.
        Sufaces latest pressure ratio, exit conditions, and source links in lockstep.
        """
        eth_rpc_snapshot = self.ingester.fetch_latest_ethereum_block_metrics()
        timeline_report = self.timeline_parser.parse_sequence_and_check_traps()
        
        promoted_motifs = self.sink.fetch_promoted_records_only()
        
        # Interlock: Feed latest promoted item directly to check for outflow contribution updates
        latest_promoted = promoted_motifs[-1] if promoted_motifs else None
        pressure_state = self.pressure_monitor.evaluate_pool_pressure(current_pool, recent_outflows, latest_promoted)
        honesty_report = self.oracle.calculate_rolling_honesty_delta(timeline_report, pressure_state, promoted_motifs)
        
        mock_position = {"total_balance_usd": user_allocation}
        downside_report = self.exit_sim.evaluate_downside_scenarios(mock_position, current_pool, recent_outflows)
        
        pool_depth_usd = current_pool.get("current_pool_depth_usd", 1.0)
        pressure_ratio = pressure_state.get("calculated_pressure_ratio", 0.0)

        if honesty_report["rolling_honesty_score_pct"] <= 50.0 or pressure_ratio >= self.pressure_monitor.critical_pressure_ratio:
            active_threat_level = "CRITICAL_RED_BREACH"
        else:
            active_threat_level = "NOMINAL_MONITORING"

        return {
            "timestamp": time.time(),
            "rpc_backbone_link": eth_rpc_snapshot.get("source_verification_link"),
            "system_threat_level": active_threat_level,
            "kill_switch_tripped": pressure_state.get("kill_switch_triggered", False),
            
            "non_dismissible_promoted_motif_layer": {
                "headline": "🚨 VERIFIED RECEIPT-GRADE ECHO TIMELINES",
                "total_promoted_count": len(promoted_motifs),
                "promoted_events": promoted_motifs
            },
            
            "public_honesty_heartbeat": {
                "rolling_honesty_index_score": honesty_report["rolling_honesty_score_pct"],
                "system_status_tag": honesty_report["verification_status"]
            },
            
            "live_risk_surface": {
                "available_liquidity_depth_usd": float(pool_depth_usd),
                "current_vault_outflow_ratio": float(round(pressure_ratio, 4)),
                "action_threshold_ceiling": self.pressure_monitor.critical_pressure_ratio,
                "triggering_source_url": pressure_state.get("triggering_source_url")
            },
            
            "counterfactual_downside_rehearsal": {
                "user_position_value_usd": float(user_allocation),
                "projected_slippage_pct": downside_report["user_risk_profile"]["estimated_slippage_impact_pct"],
                "recommended_action_posture": downside_report["predictive_action"]
            },
            
            "onboarding_choice_paths": {
                "proceed_with_agency": "I acknowledge the source-linked outflows and size my risk.",
                "one_click_exit": "Deploy local reduction paths."
            }
        }
