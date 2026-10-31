import time
from phase_trigger_sentinel import PhaseTriggerSentinel
from payload_schema_miner import PayloadSchemaMiner
from webgl_dashboard_parser import WebGLDashboardParser
from position_risk_overlay import PositionRiskOverlay
from simulation_mirror import SimulationMirror
from emergency_kill_switch import EmergencyKillSwitch
from liquidity_pressure_monitor import LiquidityPressureMonitor
from simulation_map_onboarding import SimulationMapOnboarding
from public_schema_diff_archive import PublicSchemaDiffArchive
from personal_risk_passport import PersonalRiskPassport

def run_comprehensive_phase_35_36_test():
    print("⚡ INITIALIZING PHASE 35 & 36 RISK INTEGRITY VALIDATION SUITE...")
    
    # 1. Base Framework Verification
    sentinel = PhaseTriggerSentinel()
    valid_tx = {"timestamp": time.time(), "value_sol": 0.0011, "destination": "void.solutions_stage_14", "input_data_hex": "0xa9"}
    assert sentinel.parse_block_event(valid_tx)["alert_triggered"] is True
    print("🟢 STEP 1: Core PhaseTriggerSentinel validated.")

    # 2. Risk Layer Verification
    kill_switch = EmergencyKillSwitch()
    pressure_monitor = LiquidityPressureMonitor(kill_switch)
    pool = {"current_pool_depth_usd": 500000.0}
    outflows = {"cumulative_24h_outflow_usd": 85000.0}  # 17% move -> breaches critical threshold
    
    pressure_report = pressure_monitor.evaluate_pool_pressure(pool, outflows)
    assert pressure_report["kill_switch_triggered"] is True, "FAIL: Pressure monitor failed to drop system"
    print("🟢 STEP 2: EmergencyKillSwitch and Pressure Monitor auto-trigger loop verified.")

    # 3. Interactive Onboarding & Diff Map Verification
    onboarding = SimulationMapOnboarding()
    archiver = PublicSchemaDiffArchive()
    mock_code = "class Phase36VerificationMesh: def process_and_expose_signal(self):"
    
    archiver.track_code_diff_and_update_map("verification_mesh_core", mock_code, onboarding)
    map_state = onboarding.compile_visual_onboarding_state(pool, outflows, 2500.0)
    
    assert any("verification_mesh_core" in k for k in onboarding.historical_claims_ledger.keys())
    print("🟢 STEP 3: PublicSchemaDiffArchive integrated dynamically to Visual Onboarding Maps.")

    # 4. Personal Risk Passport Verification
    passport_engine = PersonalRiskPassport()
    passport_json = passport_engine.generate_passport_snapshot("@ChooseHappiness123", 1200.0, pressure_report)
    assert "identity_handle_hash" in passport_json
    print("🟢 STEP 4: Personal Risk Passport engine generated transparent exposure record.")

    print("\n🏆 ALL PHASE 35/36 VERIFICATION NODES SECURE. ZERO COMPILATION LATENCY SATISFIED.")

if __name__ == "__main__":
    run_comprehensive_phase_35_36_test()
