import time

class CounterfactualExitSimulator:
    def __init__(self):
        self.velocity_floor = 1.44

    def evaluate_downside_scenarios(self, wallet_position: dict, current_pool: dict, recent_outflows: dict) -> dict:
        """
        Runs scenario paths modeling additional 0.0011-style or treasury outbound shocks 
        to calculate exit time frames and slippage probability under active liquidity pressure.
        """
        user_balance_usd = wallet_position.get("total_balance_usd", 0.0)
        pool_depth_usd = current_pool.get("current_pool_depth_usd", 1.0)
        cumulative_outflows = recent_outflows.get("cumulative_24h_outflow_usd", 0.0)
        
        base_pressure = cumulative_outflows / pool_depth_usd
        
        # Scenario Modeling: Simulating an immediate 2x spike in outbound vault exits
        simulated_shock_outflow = cumulative_outflows * 2.0
        simulated_pressure_ratio = simulated_shock_outflow / pool_depth_usd
        
        # Compute implied liquidity slippage multiplier based on position size relative to depth
        position_take_ratio = user_balance_usd / pool_depth_usd
        projected_slippage_pct = max(1.0, (position_take_ratio * 100.0) * (1.0 + simulated_pressure_ratio))

        return {
            "timestamp": time.time(),
            "simulation_parameters": {
                "base_outflow_pressure": float(round(base_pressure, 4)),
                "modeled_shock_pressure": float(round(simulated_pressure_ratio, 4))
            },
            "user_risk_profile": {
                "position_liquidity_take_pct": float(round(position_take_ratio * 100.0, 4)),
                "projected_slippage_probability_pct": 100.0 if simulated_pressure_ratio >= 0.15 else float(round(simulated_pressure_ratio * 100.0, 2)),
                "estimated_slippage_impact_pct": float(round(projected_slippage_pct, 2)),
                "predicted_exit_window_seconds": 1.5 if projected_slippage_pct < 5.0 else 8.0
            },
            "predictive_action": "EXIT_PATH_CLEAR" if projected_slippage_pct < 5.0 else "IMMEDIATE_TWAP_REDUCTION_REQUIRED"
        }
