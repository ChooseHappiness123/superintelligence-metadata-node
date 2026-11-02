import time
from live_public_ingester import LivePublicIngester
from emergency_kill_switch import EmergencyKillSwitch
from liquidity_pressure_monitor import LiquidityPressureMonitor
from simulation_map_onboarding import SimulationMapOnboarding
from receipt_event_sink import ReceiptEventSink
from honesty_oracle import HonestyOracle
from claim_graph_exporter import ClaimGraphExporter
from personal_threshold_binder import PersonalThresholdBinder

def run_live_endpoint_verification_pass():
    print("⚡ EXECUTING MASTER SUITE CONCURRENT WITH STALE REVALIDATOR SUITE...")
    
    ingester = LivePublicIngester()
    kill_switch = EmergencyKillSwitch()
    
    shared_monitor = LiquidityPressureMonitor(kill_switch)
    shared_sink = ReceiptEventSink()
    shared_oracle = HonestyOracle()
    onboarding_map = SimulationMapOnboarding(shared_sink, shared_oracle, shared_monitor)
    exporter = ClaimGraphExporter(shared_sink, shared_oracle, shared_monitor)
    
    # Initialize local threshold binder (Configured to alert at 12% pressure)
    binder = PersonalThresholdBinder(max_acceptable_pressure=0.12, min_honesty_floor=75.0)

    live_pool_status = {"current_pool_depth_usd": 600000.0}
    live_treasury_outflows = {"cumulative_24h_outflow_usd": 72000.0}  # 12% baseline pressure

    # 1. Append and promote a valid motif transaction
    target_url = "https://solscan.io"
    candidate = shared_sink.append_candidate_event("0.0011 SOL sequence active.", target_url)
    shared_sink.try_promote(target_url, "stale_audit_proof_hash")
    candidate["magnitude"] = 0.0011

    # Map snapshot values into history store arrays
    map_state_nominal = onboarding_map.compile_live_public_front_door(live_pool_status, live_treasury_outflows, 1000.0)
    
    # Assert personal threshold is within bounds initially
    personal_check_1 = binder.evaluate_personal_threshold_breach(map_state_nominal)
    assert personal_check_1["breach_status"]["personal_threshold_hit_marker"] is False
    print("   [INITIAL] Personal risk threshold parameters verified within safe bounds.")

    # 2. ASSERTION ONE: Run the Stale Promotion Revalidator Loop
    print("\n🔄 STEP 2: FIRING STALE PROMOTION RE-VALIDATOR SECTOR AUDIT...")
    audit = exporter.execute_stale_promotion_revalidation(target_url)
    assert audit["failures_logged"] == 1
    print(f"   Logged Stale Revalidation Failures Count: {audit['failures_logged']}")

    # 3. ASSERTION TWO: Verify map threat level scales to red and surfaces failure flags
    map_state_failed = onboarding_map.compile_live_public_front_door(live_pool_status, live_treasury_outflows, 1000.0)
    assert map_state_failed["system_threat_level"] == "CRITICAL_RED_BREACH"
    assert map_state_failed["non_dismissible_promoted_motif_layer"]["stale_revalidation_failures_present"] is True
    print("🟢 ASSERTION 1 SUCCESS: Map visual layout correctly isolates stale link decay snapshots.")

    # 4. ASSERTION THREE: Verify personal risk threshold binder captures secondary outflow spikes
    print("\n🚨 STEP 3: TESTING PERSONAL RISK PASSPORT OVERLAY BINDERS...")
    # Simulate an added outflow transaction pushing pressure to 14.5% (breaching user 12% limit)
    secondary_outflow = {"cumulative_24h_outflow_usd": 87000.0}
    map_state_spiked = onboarding_map.compile_live_public_front_door(live_pool_status, secondary_outflow, 1000.0)
    
    personal_check_2 = binder.evaluate_personal_threshold_breach(map_state_spiked)
    print(f"   Personal Threshold Hit Marker State: {personal_check_2['breach_status']['personal_threshold_hit_marker']}")
    print(f"   Enforced Strategy Command Vector  : {personal_check_2['enforced_strategy']}")
    
    assert personal_check_2["breach_status"]["pressure_limit_exceeded"] is True
    assert personal_check_2["enforced_strategy"] == "TRIGGER_IMMEDIATE_LOCAL_REDUCTION"
    print("🟢 ASSERTION 2 SUCCESS: Personal threshold binder auto-triggered exit reduction sequence.")

if __name__ == "__main__":
    run_live_endpoint_verification_pass()

