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
    onboarding_map = SimulationMapOnboarding()
    ledger = HistoricalPhaseLedger()
    timeline_parser = EcosystemTimelineParser()
    sink = ReceiptEventSink()

    # 1. Append candidate motif block using exact schema layout
    print("\n✍️  STEP 1: APPENDING UNVERIFIED MOTIF CANDIDATE...")
    raw_text = "AZY racks the noise. Stair 7 made noise. 0.0011 transfer pending."
    mock_url = "https://solscan.io"
    
    candidate = sink.append_candidate_event(raw_text, mock_url)
    assert candidate["status"] == "CANDIDATE"
    assert candidate["promoted_to_ledger"] is False
    print(f"   Staged Event Append Confirmed. Initial Status: {candidate['status']}")

    # 2. Assert Downstream Visibility is Zero while in CANDIDATE state
    print("\n🛡️  STEP 2: ENFORCING DOWNSTREAM ISOLATION FILTER...")
    promoted_set = sink.fetch_promoted_records_only()
    assert len(promoted_set) == 0, "FAIL: Unverified candidate leaked downstream"
    print("   Verification Nominal: Candidate remains invisible to timeline and map engines.")

    # 3. Fire Promotion Gate Check using Valid Transfer Proofs
    print("\n🔓 STEP 3: EXECUTING PROMOTION GATE SEPARATION CHECK...")
    promoted_record = sink.try_promote(mock_url, "5zY7m9K2gXWp4NqV420VaultSignatures")
    assert promoted_record["status"] == "PROMOTED"
    assert promoted_record["promoted_to_ledger"] is True
    
    # Verify downstream visibility unlocks exclusively for promoted array items
    updated_promoted_set = sink.fetch_promoted_records_only()
    assert len(updated_promoted_set) == 1
    print(f"   Promotion Nominal. Record status set to: {updated_promoted_set[0]['status']}")

    # 4. Standard Flow Verification Runs
    timeline_report = timeline_parser.parse_sequence_and_check_traps(ledger)
    live_pool_status = {"current_pool_depth_usd": 600000.0}
    live_treasury_outflows = {"cumulative_24h_outflow_usd": 96000.0}
    
    pressure_report = pressure_monitor.evaluate_pool_pressure(live_pool_status, live_treasury_outflows)
    assert pressure_report["kill_switch_triggered"] is True
    
    map_data = onboarding_map.compile_live_public_front_door(live_pool_status, live_treasury_outflows, 5000.0)
    assert map_data["system_threat_level"] == "CRITICAL_RED_BREACH"
    
    print("\n🏆 SYSTEM INTEGRATION GREEN: APPEND-ONLY RECEIPT PROTOCOLS NOMINAL.")

if __name__ == "__main__":
    run_live_endpoint_verification_pass()
