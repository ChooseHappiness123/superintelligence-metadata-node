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
