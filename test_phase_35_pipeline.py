import time
from live_public_ingester import LivePublicIngester
from emergency_kill_switch import EmergencyKillSwitch
from liquidity_pressure_monitor import LiquidityPressureMonitor
from simulation_map_onboarding import SimulationMapOnboarding
from personal_risk_passport import PersonalRiskPassport
from plain_language_translator import PlainLanguageTranslator
from anomaly_checklist_linker import AnomalyChecklistLinker

def execute_complete_public_mesh_validation():
    print("⚡ RUNNING FORKABLE LOCAL NODE MASTER TEST CYCLE...")
    
    # Instantiate Open Truth Stack Components
    ingester = LivePublicIngester()
    kill_switch = EmergencyKillSwitch()
    pressure_monitor = LiquidityPressureMonitor(kill_switch)
    onboarding_map = SimulationMapOnboarding()
    passport_engine = PersonalRiskPassport()
    translator = PlainLanguageTranslator()
    linker = AnomalyChecklistLinker()

    # Mocking a high-deviation transaction event pulled from a public RPC stream
    recorded_event = {
        "tx_hash": "3mN2kP9sZ7wX4qV",
        "chain": "solana",
        "value_sol": 0.0011,
        "destination": "void.solutions_stage_14_deposit_vault_sol"
    }
    
    # Mocking market depth indexes
    pool_state = {"current_pool_depth_usd": 600000.0}
    outflow_state = {"cumulative_24h_outflow_usd": 96000.0} # 16% outflow breach
    
    print("\n🗺️  STEP 1: GENERATING PUBLIC FRONT DOOR ONBOARDING MAP...")
    map_data = onboarding_map.compile_visual_onboarding_state(pool_state, outflow_state, 1500.0)
    print(f"   Visual Canvas Compiled. Global Kill-Switch Status: {map_data['global_kill_switch_tripped']}")
    assert map_data["onboarding_node_active"] is True

    print("\n🚨 STEP 2: PARSING DATA AND SCORING VAULT PRESSURE...")
    flow = ingester.ingest_live_transaction_flow(recorded_event)
    pressure_report = pressure_monitor.evaluate_pool_pressure(pool_state, outflow_state)
    assert pressure_report["kill_switch_triggered"] is True

    print("\n🗣️  STEP 3: EMITTING PLAIN-LANGUAGE SUMMARY OVERLAYS...")
    translation = translator.translate_event_to_plain_text(flow, pressure_report)
    print(f"   [TRANSLATED] {translation['plain_text_explanation']}")
    assert "Source Proof:" in translation["plain_text_explanation"]

    print("\n🎟️  STEP 4: ISSUING DECOUPLED PERSONAL RISK PASSPORTS...")
    passport_json = passport_engine.generate_passport_snapshot("@ChooseHappiness123", 5000.0, pressure_report)
    assert "exposure_profile" in passport_json

    print("\n🔗 STEP 5: AUTOMATICALLY LINKING ANOMALIES TO PRE-FILLED CHECKLISTS...")
    mock_anomaly = {
        "deviation_score": 4.82,
        "source_verification_link": flow["source_verification_link"],
        "tx_hash": flow["tx_hash"]
    }
    pre_filled_checklist = linker.link_anomaly_to_checklist(mock_anomaly)
    print(pre_filled_checklist)
    assert "AUTOMATED SYSTEM ALERT" in pre_filled_checklist

    print("\n🏆 SYSTEM INTERACTION COMPLETE: LOCAL FORKABLE NODE CONFIGURATION IS VALIDATED.")

if __name__ == "__main__":
    execute_complete_public_mesh_validation()
