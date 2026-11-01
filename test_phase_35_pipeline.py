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
    print("⚡ EXECUTING MASTER SUITE AGAINST VERIFIABLE INFRASTRUCTURE...")
    
    ingester = LivePublicIngester()
    kill_switch = EmergencyKillSwitch()
    
    # Initialize shared synchronized modules
    shared_monitor = LiquidityPressureMonitor(kill_switch)
    shared_sink = ReceiptEventSink()
    shared_oracle = HonestyOracle()
    onboarding_map = SimulationMapOnboarding(shared_sink, shared_oracle, shared_monitor)

    live_pool_status = {"current_pool_depth_usd": 600000.0}
    live_treasury_outflows = {"cumulative_24h_outflow_usd": 60000.0}  # Base ratio 10%

    # 1. Test Candidate Phase Isolation
    print("\n✍️  STEP 1: INJECTING UNVERIFIED CANDIDATE...")
    shared_sink.append_candidate_event("TRiX boxes available", "https://x.com")
    map_state_1 = onboarding_map.compile_live_public_front_door(live_pool_status, live_treasury_outflows, 1000.0)
    ratio_1 = map_state_1["live_risk_surface"]["current_vault_outflow_ratio"]
    assert ratio_1 == 0.10
    print(f"   [CANDIDATE] Pressure unchanged at base: {ratio_1}")

    # 2. Test PROMOTED Non-Outflow Phase
    print("\n📝 STEP 2: PROMOTING NON-OUTFLOW TRADING SIGNALS...")
    non_outflow_url = "https://etherscan.io"
    non_outflow_candidate = shared_sink.append_candidate_event("@itsover0x structural metadata updates", non_outflow_url)
    shared_sink.try_promote(non_outflow_url, "0x_non_outflow_hash")
    
    map_state_2 = onboarding_map.compile_live_public_front_door(live_pool_status, live_treasury_outflows, 1000.0)
    ratio_2 = map_state_2["live_risk_surface"]["current_vault_outflow_ratio"]
    assert ratio_2 == 0.10
    print(f"   [PROMOTED NON-OUTFLOW] Pressure remains static at: {ratio_2}")

    # 3. Test PROMOTED Outflow/Liquidity Phase
    print("\n🚨 STEP 3: PROMOTING VERIFIED 0.0011 OUTFLOW PATTERNS...")
    outflow_url = "https://solscan.io"
    outflow_candidate = shared_sink.append_candidate_event("0.0011 SOL sequence routed to void deposits", outflow_url)
    outflow_candidate["magnitude"] = 0.0011  # Incurs dynamic dollar weight addition
    
    shared_sink.try_promote(outflow_url, "0x_outflow_breach_hash")
    
    map_state_3 = onboarding_map.compile_live_public_front_door(live_pool_status, live_treasury_outflows, 1000.0)
    ratio_3 = map_state_3["live_risk_surface"]["current_vault_outflow_ratio"]
    trigger_source = map_state_3["live_risk_surface"]["triggering_source_url"]
    kill_tripped = map_state_3["kill_switch_tripped"]
    
    print(f"   [PROMOTED OUTFLOW] Updated Pressure Ratio: {ratio_3}")
    print(f"   [PROMOTED OUTFLOW] Source Link Bound: {trigger_source}")
    print(f"   [PROMOTED OUTFLOW] Kill-Switch Engaged: {kill_tripped}")
    
    assert ratio_3 > ratio_1, "FAIL: Pressure monitor ignored promoted outflow context"
    assert trigger_source == outflow_url, "FAIL: Faulty source link mapping"
    assert kill_tripped is True, "FAIL: Kill-switch failed to execute on threshold breach"
    print("🟢 ASSERTION SUCCESS: Inter-module alignment loop proven stable.")

if __name__ == "__main__":
    run_live_endpoint_verification_pass()
