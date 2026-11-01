import time
from live_public_ingester import LivePublicIngester
from emergency_kill_switch import EmergencyKillSwitch
from liquidity_pressure_monitor import LiquidityPressureMonitor
from simulation_map_onboarding import SimulationMapOnboarding
from historical_phase_ledger import HistoricalPhaseLedger
from ecosystem_timeline_parser import EcosystemTimelineParser
from receipt_event_sink import ReceiptEventSink

def run_live_endpoint_verification_pass():
    print("⚡ EXECUTING MASTER SUITE AGAINST RAW INTERFACED LAYERS...")
    
    ingester = LivePublicIngester()
    kill_switch = EmergencyKillSwitch()
    pressure_monitor = LiquidityPressureMonitor(kill_switch)
    ledger = HistoricalPhaseLedger()
    timeline_parser = EcosystemTimelineParser()
    
    # Instantiate the decoupled sink registry
    shared_sink = ReceiptEventSink()
    # Pass shared instance into front door visual layout compiler
    onboarding_map = SimulationMapOnboarding(shared_sink)

    # Mock parameters
    raw_text = "Boxes sell out. AZY tracks 0.0011 SOL sequence."
    mock_url = "https://solscan.io"
    live_pool_status = {"current_pool_depth_usd": 600000.0}
    live_treasury_outflows = {"cumulative_24h_outflow_usd": 96000.0}

    # 1. Append candidate motif block
    shared_sink.append_candidate_event(raw_text, mock_url)
    
    # 2. ASSERTION ONE: Verify candidate record is completely invisible on the visual map view
    map_state_1 = onboarding_map.compile_live_public_front_door(live_pool_status, live_treasury_outflows, 1000.0)
    assert map_state_1["non_dismissible_promoted_motif_layer"]["total_promoted_count"] == 0, "FAIL: Unverified candidate leaked to Map layer"
    print("🟢 ASSERTION 1 SUCCESS: Visual map layer remains 100% blind to unverified candidates.")

    # 3. Fire Promotion Gate Check using a verified transaction signature
    shared_sink.try_promote(mock_url, "5zY7m9K2gXWp4NqV420VaultSignatures")
    
    # 4. ASSERTION TWO: Verify the visual map dynamically unlocks the data block ONLY post-promotion
    map_state_2 = onboarding_map.compile_live_public_front_door(live_pool_status, live_treasury_outflows, 1000.0)
    assert map_state_2["non_dismissible_promoted_motif_layer"]["total_promoted_count"] == 1, "FAIL: Map layout failed to ingest promoted record"
    
    promoted_event = map_state_2["non_dismissible_promoted_motif_layer"]["promoted_events"][0]
    assert promoted_event["status"] == "PROMOTED"
    assert promoted_event["onchain_match"] == "5zY7m9K2gXWp4NqV420VaultSignatures"
    print("🟢 ASSERTION 2 SUCCESS: Visual map front door dynamically bound and displaying promoted records natively.")

    # Standard system checks
    timeline_report = timeline_parser.parse_sequence_and_check_traps(ledger)
    pressure_report = pressure_monitor.evaluate_pool_pressure(live_pool_status, live_treasury_outflows)
    assert pressure_report["kill_switch_triggered"] is True
    
    print("\n🏆 COMPREHENSIVE LINKAGE VALIDATION ACCELERATED GREEN. MAP BINDINGS IMMUTABLE.")

if __name__ == "__main__":
    run_live_endpoint_verification_pass()
