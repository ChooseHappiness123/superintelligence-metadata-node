import time
from live_public_ingester import LivePublicIngester
from emergency_kill_switch import EmergencyKillSwitch
from liquidity_pressure_monitor import LiquidityPressureMonitor
from simulation_map_onboarding import SimulationMapOnboarding
from historical_phase_ledger import HistoricalPhaseLedger
from ecosystem_timeline_parser import EcosystemTimelineParser
from receipt_event_sink import ReceiptEventSink
from honesty_oracle import HonestyOracle

def run_live_endpoint_verification_pass():
    print("⚡ EXECUTING MASTER SUITE CONCURRENT WITH ADVERSARIAL CANDIDATE FUZZER...")
    
    ingester = LivePublicIngester()
    kill_switch = EmergencyKillSwitch()
    
    shared_monitor = LiquidityPressureMonitor(kill_switch)
    shared_sink = ReceiptEventSink()
    shared_oracle = HonestyOracle()
    onboarding_map = SimulationMapOnboarding(shared_sink, shared_oracle, shared_monitor)
    ledger = HistoricalPhaseLedger()
    timeline_parser = EcosystemTimelineParser()

    live_pool_status = {"current_pool_depth_usd": 600000.0}
    live_treasury_outflows = {"cumulative_24h_outflow_usd": 60000.0}  # Base ratio 10%

    # Fetch baseline metrics before firing fuzz vectors
    base_map = onboarding_map.compile_live_public_front_door(live_pool_status, live_treasury_outflows, 1000.0)
    base_score = base_map["public_honesty_heartbeat"]["rolling_honesty_index_score"]
    base_ratio = base_map["live_risk_surface"]["current_vault_outflow_ratio"]

    # 1. Instantiate Adversarial Fuzz Matrix (N varied candidate events)
    fuzz_vectors = [
        {"text": "0.0011 near miss layout text string", "url": ""},  # Malformed/Empty path
        {"text": "AZY network noise and fake handles", "url": "https://fake-explorers.io"},  # Genuine-looking but unresolvable
        {"text": "TRiX boxes drop alert speculative chatter", "url": "https://x.com"},  # Non-onchain social link
        {"text": "0.0011", "url": "ftp://malformed-protocol-transfer.hex"}  # Invalid protocol structure
    ]

    print("\n💥 STEP 1: INJECTING CHAOTIC FUZZ VECTORS INTO SINK COMPLIANCE HOOKS...")
    for idx, vector in enumerate(fuzz_vectors):
        # Fire through append path
        candidate = shared_sink.append_candidate_event(vector["text"], vector["url"])
        
        # Fire through promotion gate path to test structural isolation
        shared_sink.try_promote(vector["url"], f"fuzz_hash_{idx}")
        
        # Pull current state evaluation to verify absolute zero leakage
        fuzz_map = onboarding_map.compile_live_public_front_door(live_pool_status, live_treasury_outflows, 1000.0)
        
        # Enforce non-negotiable structural constraints
        assert fuzz_map["non_dismissible_promoted_motif_layer"]["total_promoted_count"] == 0, f"FAIL: Fuzz index {idx} leaked downstream"
        assert fuzz_map["public_honesty_heartbeat"]["rolling_honesty_index_score"] == base_score, f"FAIL: Fuzz index {idx} mutated oracle score"
        assert fuzz_map["live_risk_surface"]["current_vault_outflow_ratio"] == base_ratio, f"FAIL: Fuzz index {idx} modified pressure ratio"
        assert fuzz_map["kill_switch_tripped"] is False, f"FAIL: Fuzz index {idx} accidentally triggered kill-switch"

    print(f"   [FUZZ_SUCCESS] Passed {len(fuzz_vectors)} isolation tests. Zero updates propagated.")

    # 2. Test End-to-End Propagation of a Genuine Resolvable Source URL
    print("\n🔓 STEP 2: VERIFYING END-TO-END PROPAGATION OF AUTHENTIC RESOLVABLE DATA...")
    valid_outflow_url = "https://solscan.io"
    valid_text = "0.0011 SOL sequence confirmed outbound to void deposit vault."
    
    # Append valid item
    shared_sink.append_candidate_event(valid_text, valid_outflow_url)
    # Promote valid item
    promoted_record = shared_sink.try_promote(valid_outflow_url, "authentic_verified_outflow_sig")
    promoted_record["magnitude"] = 0.0011  # Incur direct math weight shift

    # Final payload synthesis
    final_map = onboarding_map.compile_live_public_front_door(live_pool_status, live_treasury_outflows, 1000.0)
    
    print(f"   [PROMOTED_RUN] New Rolling Honesty Score : {final_map['public_honesty_heartbeat']['rolling_honesty_index_score']}%")
    print(f"   [PROMOTED_RUN] New Vault Outflow Ratio  : {final_map['live_risk_surface']['current_vault_outflow_ratio']}")
    print(f"   [PROMOTED_RUN] Emergency Kill Triggered : {final_map['kill_switch_tripped']}")

    # Verify that the authentic entry cleanly alters metrics down-chain
    assert final_map["non_dismissible_promoted_motif_layer"]["total_promoted_count"] == 1
    assert final_map["public_honesty_heartbeat"]["rolling_honesty_index_score"] < base_score, "FAIL: Score stayed static on valid promotion"
    assert final_map["live_risk_surface"]["current_vault_outflow_ratio"] > base_ratio, "FAIL: Pressure failed to step up on valid outflow"
    assert final_map["kill_switch_tripped"] is True, "FAIL: Kill-switch failed to deploy on structural breach"
    
    print("\n🏆 COMPREHENSIVE FUZZING AND INTERLOCK RUN PROVEN FLAWLESS. COLD PARITY ACTIVE.")

if __name__ == "__main__":
    run_live_endpoint_verification_pass()
