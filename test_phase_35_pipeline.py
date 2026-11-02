import time
from live_public_ingester import LivePublicIngester
from emergency_kill_switch import EmergencyKillSwitch
from liquidity_pressure_monitor import LiquidityPressureMonitor
from simulation_map_onboarding import SimulationMapOnboarding
from receipt_event_sink import ReceiptEventSink
from honesty_oracle import HonestyOracle
from claim_graph_exporter import ClaimGraphExporter
from external_receipt_mirror import ExternalReceiptMirror

def run_live_endpoint_verification_pass():
    print("⚡ EXECUTING PHASE 36 MASTER SUITE: RE-VALIDATOR AND MIRROR ARRAYS...")
    
    ingester = LivePublicIngester()
    kill_switch = EmergencyKillSwitch()
    shared_monitor = LiquidityPressureMonitor(kill_switch)
    shared_sink = ReceiptEventSink()
    shared_oracle = HonestyOracle()
    onboarding_map = SimulationMapOnboarding(shared_sink, shared_oracle, shared_monitor)
    exporter = ClaimGraphExporter(shared_sink, shared_oracle, shared_monitor)
    
    # Initialize the external receipt mirror engine
    mirror = ExternalReceiptMirror()

    live_pool_status = {"current_pool_depth_usd": 600000.0}
    live_treasury_outflows = {"cumulative_24h_outflow_usd": 60000.0}

    # 1. Append candidate motif and verify isolation
    target_url = "https://solscan.io"
    candidate = shared_sink.append_candidate_event("0.0011 SOL sequence entry via gymcore endpoints", target_url)
    
    # Assert candidate is completely hidden before promotion
    map_state_1 = onboarding_map.compile_live_public_front_door(live_pool_status, live_treasury_outflows, 1000.0)
    assert map_state_1["non_dismissible_promoted_motif_layer"]["total_promoted_count"] == 0
    print("   🟢 STEP 1: Unverified candidate perfectly isolated from front door layers.")

    # 2. Promote candidate event
    promoted_record = shared_sink.try_promote(target_url, "stale_and_mirror_proof_hash")
    promoted_record["magnitude"] = 0.0011
    
    # Hydrate history logs via map compiler execution
    onboarding_map.compile_live_public_front_door(live_pool_status, live_treasury_outflows, 1000.0)

    # 3. ASSERTION ONE: Run the Stale Promotion Revalidator pass
    print("\n🔄 STEP 2: TRIGGERING REVALIDATION RUN AGAINST DEFECTIVE ENDPOINTS...")
    audit = exporter.execute_stale_promotion_revalidation(target_url)
    assert audit["failures_logged"] == 1
    
    # Verify map surfaces the failure with the original source URL
    map_state_failed = onboarding_map.compile_live_public_front_door(live_pool_status, live_treasury_outflows, 1000.0)
    assert map_state_failed["non_dismissible_promoted_motif_layer"]["stale_revalidation_failures_present"] is True
    print(f"   Revalidation Failure Surfaced. Original Source URL Intact: {target_url}")

    # 4. ASSERTION TWO: Emit payload block to Independent Append-Only External Mirror
    print("\n📡 STEP 3: EXECUTING INDEPENDENT EXTERNAL RECEIPT GIST PAYLOAD EMISSION...")
    mirror_report = mirror.mirror_promoted_event_external(promoted_record)
    
    assert mirror_report["remote_anchor_status"] == "APPEND_SUCCESS"
    assert mirror_report["payload"]["source_url"] == target_url
    assert mirror_report["payload"]["revalidation_failed"] is True
    
    print(f"   External Mirror Synced. Appended Payload Hash: {mirror_report['mirrored_payload_hash']}")
    print("   🟢 ASSERTION SUCCESS: Independent anti-tamper receipt logged.")

if __name__ == "__main__":
    run_live_endpoint_verification_pass()
# --- APPEND-ONLY TEST EXPANSION: EMITTER & BINDER VALIDATION ---
def run_phase_35_append_only_assertions():
    print("Initializing Phase 35 Emitter and Binder assertions...")
    
    # Setup test components
    emitter = AppendOnlyGistEmitter(target_sink_url=None)
    binder = PersonalExitBinder(configuration_path="test_pipeline_config_tmp.json")
    
    # Create temporary local configuration for test validation
    test_config = {
        "personal_risk_profile": {
            "max_drawdown_threshold_pct": 10.0,
            "initial_anchor_value": 1000.0
        }
    }
    with open("test_pipeline_config_tmp.json", "w") as f:
        json.dump(test_config, f)

    # Assertion 1: Candidates produce zero emissions
    assert emitter.emit_event("CANDIDATE_NOTE", {"data": "test"}) == False, "Violation: Candidate emitted a payload!"
    assert emitter.emit_event("PROMOTED", {"data": "success"}) == True, "Failure: Valid PROMOTED event rejected"
    assert emitter.emit_event("REVALIDATION_FAILED", {"data": "fail"}) == True, "Failure: Valid REVALIDATION_FAILED event rejected"
    print("✓ Asserted candidates produce zero emissions.")
    print("✓ Asserted PROMOTED / REVALIDATION_FAILED produce exactly one payload.")

    # Assertion 2: Personal threshold flag appears only on breach
    safe_metrics = {"total_portfolio_value_usd": 950.0} # 5% drawdown (under 10%)
    breach_metrics = {"total_portfolio_value_usd": 850.0} # 15% drawdown (over 10%)
    
    safe_res = binder.check_threshold_bounds(safe_metrics, source_url="https://x.com")
    assert safe_res["personal_threshold_hit"] == False, "Violation: Threshold flagged false-positive breach!"
    
    breach_res = binder.check_threshold_bounds(breach_metrics, source_url="https://x.com")
    assert breach_res["personal_threshold_hit"] == True, "Failure: Target breach missed flag verification!"
    assert "personal threshold hit" in breach_res["msg"], "Failure: Map/delta message string missing!"
    print("✓ Asserted personal threshold flag appears only on breach.")

    # Clean up temp file
    if os.path.exists("test_pipeline_config_tmp.json"):
        os.remove("test_pipeline_config_tmp.json")
    print("All Phase 35 technical validations passed green.")

if __name__ == "__main__":
    run_phase_35_append_only_assertions()
# --- END OF TEST EXPANSION ---
