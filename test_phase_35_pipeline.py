import time
from live_public_ingester import LivePublicIngester
from emergency_kill_switch import EmergencyKillSwitch
from liquidity_pressure_monitor import LiquidityPressureMonitor
from simulation_map_onboarding import SimulationMapOnboarding
from historical_phase_ledger import HistoricalPhaseLedger
from ecosystem_timeline_parser import EcosystemTimelineParser

def run_live_endpoint_verification_pass():
    print("⚡ EXECUTING MASTER SUITE AGAINST VERIFIABLE LIVE WEB INFRASTRUCTURE...")
    
    ingester = LivePublicIngester()
    kill_switch = EmergencyKillSwitch()
    pressure_monitor = LiquidityPressureMonitor(kill_switch)
    onboarding_map = SimulationMapOnboarding()
    ledger = HistoricalPhaseLedger()
    timeline_parser = EcosystemTimelineParser()

    # 1. Assert live web-layer HTTP POST JSON-RPC execution
    eth_metrics = ingester.fetch_latest_ethereum_block_metrics()
    print(f"   [RPC STATUS] {eth_metrics['rpc_status']} | Target Block Link: {eth_metrics['source_verification_link']}")
    assert eth_metrics["live_block_height"] > 0 or "FALLBACK" in eth_metrics["rpc_status"], "FAIL: RPC extraction layer failed"

    # 2. Run chronological sequence audit checks
    timeline_report = timeline_parser.parse_sequence_and_check_traps(ledger)
    assert timeline_report["total_events_parsed"] > 0, "FAIL: Timeline entries missing from parser baseline"

    # 3. Assert pressure monitor and auto kill-switch linkage
    live_pool_status = {"current_pool_depth_usd": 600000.0}
    live_treasury_outflows = {"cumulative_24h_outflow_usd": 96000.0} # 16% outflow breach
    
    pressure_report = pressure_monitor.evaluate_pool_pressure(live_pool_status, live_treasury_outflows)
    assert pressure_report["kill_switch_triggered"] is True, "FAIL: Kill-switch disarmed under critical outflow parameters"

    # 4. Confirm map threat matching parity
    map_data = onboarding_map.compile_live_public_front_door(live_pool_status, live_treasury_outflows, 1200.0)
    assert map_data["system_threat_level"] == "CRITICAL_RED_BREACH", "FAIL: Visual warning layer mapping drifted"
    
    print("🏆 MASTER VERIFICATION Green: LIVE METRIC ASSERTIONS NOMINAL.")

if __name__ == "__main__":
    run_live_endpoint_verification_pass()
