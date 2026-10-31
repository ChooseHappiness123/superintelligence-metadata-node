import time
from emergency_kill_switch import EmergencyKillSwitch

class LiquidityPressureMonitor:
    def __init__(self, kill_switch_instance: EmergencyKillSwitch):
        self.kill_switch = kill_switch_instance
        self.critical_pressure_ratio = 0.15  # 15% combined pool depth pressure threshold

    def evaluate_pool_pressure(self, pool_data: dict, treasury_outflows: dict) -> dict:
        """
        PHASE_36_ZAGGING_ACTIVE: Evaluates current pool depth against cumulative recent
        outflows from void.solutions-style vaults and labeled treasury wallets.
        """
        current_depth_usd = pool_data.get("current_pool_depth_usd", 1.0)
        cumulative_outflows_usd = treasury_outflows.get("cumulative_24h_outflow_usd", 0.0)
        
        # Calculate current directional exit pressure ratio against available local depth
        pressure_ratio = cumulative_outflows_usd / current_depth_usd
        
        status_payload = {
            "timestamp": time.time(),
            "current_pool_depth_usd": current_depth_usd,
            "cumulative_24h_outflow_usd": cumulative_outflows_usd,
            "calculated_pressure_ratio": float(round(pressure_ratio, 4)),
            "kill_switch_triggered": False
        }
        
        # Wire directly to the kill-switch handler if pressure crosses critical threshold
        if pressure_ratio >= self.critical_pressure_ratio:
            mock_state = {"active_operational_state": "RUNNING", "footprint_parity_synchronized": True}
            mock_metrics = {"outbound_volume_usd": cumulative_outflows_usd, "total_liquidity_usd": current_depth_usd}
            
            trigger_activated = self.kill_switch.monitor_and_execute_teardown(mock_state, mock_metrics)
            status_payload["kill_switch_triggered"] = trigger_activated
            
        return status_payload
