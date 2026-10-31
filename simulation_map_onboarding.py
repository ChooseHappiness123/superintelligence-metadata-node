import time
from liquidity_pressure_monitor import LiquidityPressureMonitor
from emergency_kill_switch import EmergencyKillSwitch

class SimulationMapOnboarding:
    def __init__(self):
        self.kill_switch = EmergencyKillSwitch()
        self.pressure_monitor = LiquidityPressureMonitor(self.kill_switch)
        self.historical_claims_ledger = {
            "Phase_33": {"claimed": "Global Multi-Node Mesh Layer", "observable_onchain": "Initial local telemetry catch endpoints"},
            "Phase_34": {"claimed": "Autonomous Execution Sentinel Matrix", "observable_onchain": "Frozen structural health monitoring shields"},
            "Phase_35": {"claimed": "Sovereign Cross-Chain Pipeline Core", "observable_onchain": "Local deBridge data harvesters and risk overlays"}
        }

    def compile_visual_onboarding_state(self, current_pool: dict, recent_outflows: dict, newcomer_allocation_usd: float) -> dict:
        """
        PHASE_36_ZAGGING_ACTIVE: Compiles the un-gatekept interactive onboarding map matrix. 
        Structures live data, historical deltas, and risk calculations with absolute transparency.
        """
        # 1. Fetch Live Pool Pressure Signals Natively
        pressure_state = self.pressure_monitor.evaluate_pool_pressure(current_pool, recent_outflows)
        pool_depth_usd = current_pool.get("current_pool_depth_usd", 1.0)
        
        # 2. Compute "Size to Zero" Allocation Ratio
        # High-IQ Calculation: Determine newcomer exposure relative to total available liquidity depth
        exposure_ratio = newcomer_allocation_usd / pool_depth_usd
        suggested_allocation = newcomer_allocation_usd if exposure_ratio < 0.01 else float(round(pool_depth_usd * 0.0011, 2))
        
        # 3. Assemble Visual Component Layout Coordinates
        interactive_map_schema = {
            "timestamp": time.time(),
            "onboarding_node_active": True,
            "global_kill_switch_tripped": pressure_state.get("kill_switch_triggered", False),
            "visual_canvas_elements": {
                "node_1_liquidity_depth": {
                    "label": "Live Available Pool Capacity",
                    "value_usd": pool_depth_usd,
                    "source_link": "https://pond0x.com"
                },
                "node_2_historical_delta_map": {
                    "label": "Marketed Claims vs Observable Delivery Ledger",
                    "historical_matrix": self.historical_claims_ledger
                },
                "node_3_risk_pressure_overlay": {
                    "label": "Combined Vault Outflow Pressure",
                    "ratio": pressure_state.get("calculated_pressure_ratio", 0.0),
                    "action_threshold": self.pressure_monitor.critical_pressure_ratio
                },
                "node_4_size_to_zero_calculator": {
                    "user_input_exposure_usd": float(newcomer_allocation_usd),
                    "implied_depth_take_pct": float(round(exposure_ratio * 100.0, 4)),
                    "mathematical_safety_cap_usd": float(suggested_allocation),
                    "onboarding_recommendation": "PROCEED_WITH_AGENCY" if exposure_ratio < 0.01 else "EXCESSIVE_DILUTION_RISK_SIZE_DOWN"
                }
            },
            "onboarding_ritual_choice_paths": {
                "path_alpha_accept": "I verify the raw on-chain facts and choose to interact with complete exposure awareness.",
                "path_omega_exit": "I reject narrative speculation and deploy the one-click exit routing path to zero out."
            }
        }
        
        return interactive_map_schema
