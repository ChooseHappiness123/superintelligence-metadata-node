import time
from live_public_ingester import LivePublicIngester
from emergency_kill_switch import EmergencyKillSwitch
from liquidity_pressure_monitor import LiquidityPressureMonitor
from simulation_map_onboarding import SimulationMapOnboarding
from personal_risk_passport import PersonalRiskPassport
from plain_language_translator import PlainLanguageTranslator
from anomaly_checklist_linker import AnomalyChecklistLinker
from historical_phase_ledger import HistoricalPhaseLedger

def execute_complete_public_mesh_validation():
    print("⚡ RUNNING FORKABLE LOCAL NODE MASTER TEST CYCLE...")
    
    # Initialize Core Mesh Stack
    ingester = LivePublicIngester()
    kill_switch = EmergencyKillSwitch()
    pressure_monitor = LiquidityPressureMonitor(kill_switch)
    onboarding_map = SimulationMapOnboarding()
    passport_engine = PersonalRiskPassport()
    translator = PlainLanguageTranslator()
    linker = AnomalyChecklistLinker()
    
    # NEW: Initialize Forensic Historical Claim-vs-Delivery Ledger
    ledger = HistoricalPhaseLedger()

    # Mocking high-deviation transaction event from the public stream
    recorded_event = {
        "tx_hash": "3mN2kP9sZ7wX4qV",
        "chain": "solana",
        "value_sol": 0.0011,
        "destination": "void.solutions_stage_14_deposit_vault_sol"
    }
    
    pool_state = {"current_pool_depth_usd": 600000.0}
    outflow_state = {"cumulative_24h_outflow_usd": 96000.0} # 16% outflow breach
    
    print("\n📚 STEP 1: FORENSIC CLAIM-VS-DELIVERY LEDGER ASSERTIONS...")
    delta_report = ledger.generate_delta_report()
    print(f"   Phases Audited: {delta_report['total_phases_catalogued']} | Critical Divergences: {delta_report['critical_divergences_found']}")
    print(f"   Calculated System Honesty Index Score: {delta_report['system_honesty_score']:.1f}%")
    
    # CRITICAL MASTER ASSERTION: Fail build if narrative outruns delivery or leakage exceeds safety
    if delta_report["system_honesty_score"] < 50.0:
        print("❌ BUILD FAILURE ASSERTION: SYSTEM HONESTY INDEX CRITICALLY DEGRADED. EXIT PRESSURE UNACCEPTABLE.")
        raise ValueError("CRITICAL_NARRATIVE_DIVERGENCE_DETECTED_IN_LEDGER")

    print("\n🗺️  STEP 2: GENERATING PUBLIC FRONT DOOR ONBOARDING MAP...")
    map_data = onboarding_map.compile_visual_onboarding_state(pool_state, outflow_state, 1500.0)
    assert map_data["onboarding_node_active"] is True

    print("\n🚨 STEP 3: PARSING DATA AND SCORING VAULT PRESSURE...")
    flow = ingester.ingest_live_transaction_flow(recorded_event)
    pressure_report = pressure_monitor.evaluate_pool_pressure(pool_state, outflow_state)
    assert pressure_report["kill_switch_triggered"] is True

    print("\n🗣️  STEP 4: EMITTING PLAIN-LANGUAGE SUMMARY OVERLAYS...")
    translation = translator.translate_event_to_plain_text(flow, pressure_report)
    print(f"   [TRANSLATED] {translation['plain_text_explanation']}")

    print("\n🎟️  STEP 5: ISSUING DECOUPLED PERSONAL RISK PASSPORTS...")
    passport_json = passport_engine.generate_passport_snapshot("@ChooseHappiness123", 5000.0, pressure_report)
    assert "exposure_profile" in passport_json

    print("\n🔗 STEP 6: AUTOMATICALLY LINKING ANOMALIES TO PRE-FILLED CHECKLISTS...")
    mock_anomaly = {"deviation_score": 4.82, "source_verification_link": flow["source_verification_link"], "tx_hash": flow["tx_hash"]}
    pre_filled_checklist = linker.link_anomaly_to_checklist(mock_anomaly)
    assert "AUTOMATED SYSTEM ALERT" in pre_filled_checklist

    print("\n🏆 SYSTEM INTERACTION COMPLETE: FORKABLE NODE LEDGER & RISK ENGINE VALIDATED NOMINAL.")

if __name__ == "__main__":
    execute_complete_public_mesh_validation()
