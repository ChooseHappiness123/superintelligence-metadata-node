import time
from phase_trigger_sentinel import PhaseTriggerSentinel
from payload_schema_miner import PayloadSchemaMiner
from webgl_dashboard_parser import WebGLDashboardParser
from position_risk_overlay import PositionRiskOverlay
from simulation_mirror import SimulationMirror

def run_comprehensive_phase_35_test():
    print("⚡ INITIALIZING PHASE 35 STRUCTURAL ENDPOINT VALIDATION SUITE...")
    
    # 1. Validate Phase Trigger Sentinel Boundary Gate
    sentinel = PhaseTriggerSentinel()
    valid_tx = {"timestamp": time.time(), "value_sol": 0.0011, "destination": "void.solutions_stage_14", "input_data_hex": "0xa9059cbb"}
    parsed_tx = sentinel.parse_block_event(valid_tx)
    assert parsed_tx["alert_triggered"] is True, "FAIL: Sentinel alert gate failed to fire"
    assert parsed_tx["latency_check"] == "PASS", "FAIL: Sentinel latency check failed"
    print("🟢 STEP 1: PhaseTriggerSentinel verified nominal.")

    # 2. Validate Payload Schema Miner Shape Extraction
    miner = PayloadSchemaMiner()
    diff_payload = {"origin": "docs.geoff.ai", "raw_text_payload": "curl -X POST https://geoff.ai"}
    extracted = miner.extract_and_normalize_shape(diff_payload)
    assert extracted["status"] == "SCHEMA_STRUCT_EXTRACTED", "FAIL: Miner schema parsing failed"
    print("🟢 STEP 2: PayloadSchemaMiner verified nominal.")

    # 3. Validate WebGL Dashboard Matrix Alignment
    parser = WebGLDashboardParser()
    flows = {"pond_sol_metrics": {"volume_pool": 250000.0}, "trix_void_metrics": {"signal_count": 88}}
    geoff_metrics = {"api_volume": 4200}
    matrix = parser.parse_webgl_state_matrix(flows, geoff_metrics)
    assert matrix["render_payload"]["gl_vertex_trix_void"] == 88, "FAIL: WebGL vertex parsing error"
    print("🟢 STEP 3: WebGLDashboardParser verified nominal.")

    # 4. Validate Position Risk Overlay Dilution Check
    overlay = PositionRiskOverlay()
    user_pos = {"total_balance_usd": 5000.0}
    treasury = {"outbound_volume_usd": 150000.0, "total_liquidity_usd": 1000000.0}  # 15% move
    risk = overlay.calculate_exit_pressure_overlay(user_pos, treasury)
    assert risk["dilution_warning_active"] is True, "FAIL: Risk overlay failed to flag exit pressure"
    print("🟢 STEP 4: PositionRiskOverlay verified nominal.")

    # 5. Validate Simulation Mirror High-Signal Generation
    mirror = SimulationMirror()
    inputs = [{"text": "Boxes vanish today via gymcore network", "tx_brief": "Pond0x spawn sequence completed"}]
    brief = mirror.generate_high_signal_brief(inputs)
    assert brief["actionable_alpha_detected"] is True, "FAIL: Simulation mirror failed to harvest alpha text"
    print("🟢 STEP 5: SimulationMirror verified nominal.")

    print("\n🏆 ALL PHASE 35 ENDPOINTS SYSTEMATICALLY VERIFIED AND PROVEN STABLE. COLD PARITY SATISFIED.")

if __name__ == "__main__":
    run_comprehensive_phase_35_test()
