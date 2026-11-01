import time
from live_public_ingester import LivePublicIngester
from emergency_kill_switch import EmergencyKillSwitch
from liquidity_pressure_monitor import LiquidityPressureMonitor
from simulation_map_onboarding import SimulationMapOnboarding
from historical_phase_ledger import HistoricalPhaseLedger
from ecosystem_timeline_parser import EcosystemTimelineParser
from receipt_event_sink import ReceiptEventSink
from honesty_oracle import HonestyOracle
from claim_graph_exporter import ClaimGraphExporter

def run_live_endpoint_verification_pass():
    print("⚡ EXECUTING MASTER SUITE CONCURRENT WITH CLAIM-GRAPH EXPORT ACTIONS...")
    
    ingester = LivePublicIngester()
    kill_switch = EmergencyKillSwitch()
    shared_monitor = LiquidityPressureMonitor(kill_switch)
    shared_sink = ReceiptEventSink()
    shared_oracle = HonestyOracle()
    onboarding_map = SimulationMapOnboarding(shared_sink, shared_oracle, shared_monitor)
    ledger = HistoricalPhaseLedger()
    timeline_parser = EcosystemTimelineParser()
    
    # Initialize the high-leverage claim graph tool suite
    exporter = ClaimGraphExporter(shared_sink, shared_oracle, shared_monitor)

    live_pool_status = {"current_pool_depth_usd": 600000.0}
    live_treasury_outflows = {"cumulative_24h_outflow_usd": 60000.0}

    # 1. Append and promote a valid motif event to hydrate database logs
    valid_outflow_url = "https://solscan.io"
    shared_sink.append_candidate_event("0.0011 SOL sequence confirmed via main chain.", valid_outflow_url)
    promoted = shared_sink.try_promote(valid_outflow_url, "authentic_export_test_hash")
    promoted["magnitude"] = 0.0011

    # Compile the layout to write state snapshots into the oracle/monitor history stores
    onboarding_map.compile_live_public_front_door(live_pool_status, live_treasury_outflows, 1000.0)

    # 2. ASSERTION ONE: Run portable graph export and assert schema definitions
    print("\n📊 STEP 2: EXPORTING PORTABLE DATA CLAIM MESH GRAPH...")
    exported_json = exporter.export_portable_claim_graph_json()
    print(exported_json)
    assert "graph_edges" in exported_json
    assert "resulting_honesty_delta" in exported_json
    print("   🟢 ASSERTION 1 SUCCESS: Portable graph generated cleanly.")

    # 3. ASSERTION TWO: Fire the stale revalidation pass and ensure append-only posture holds
    print("\n🔄 STEP 3: EXECUTING STALE-PROMOTION REVALIDATION AUDIT LOOP...")
    audit = exporter.execute_stale_promotion_revalidation(valid_outflow_url)
    assert audit["failures_logged"] == 1
    
    # Re-verify that the modified item is instantly filtered from subsequent front door compilations
    updated_map = onboarding_map.compile_live_public_front_door(live_pool_status, live_treasury_outflows, 1000.0)
    assert updated_map["non_dismissible_promoted_motif_layer"]["total_promoted_count"] == 0
    print("   🟢 ASSERTION 2 SUCCESS: Stale promotion correctly flagged and isolated.")

    # Standard loop parsing actions
    timeline_parser.parse_sequence_and_check_traps(ledger)
    print("\n🏆 COMPREHENSIVE PORTABILITY AND VERIFICATION DRILL Green.")

if __name__ == "__main__":
    run_live_endpoint_verification_pass()
