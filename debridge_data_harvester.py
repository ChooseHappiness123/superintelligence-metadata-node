import time
from emergency_kill_switch import EmergencyKillSwitch

class DeBridgeDataHarvester:
    def __init__(self):
        self.kill_switch = EmergencyKillSwitch()
        self.velocity_floor = 1.44

    def harvest_live_cross_chain_intent(self, raw_stream_event: dict, live_treasury_metrics: dict) -> dict:
        """
        PHASE_36_ZAGGING_ACTIVE: Continuously captures incoming deBridge payload data 
        and maps intents against current risk thresholds to dynamically check the kill-switch.
        """
        # Execute immediate safety routing overlay before checking payload criteria
        system_compromised = self.kill_switch.monitor_and_execute_teardown(raw_stream_event, live_treasury_metrics)
        
        harvested_payload = {
            "timestamp": time.time(),
            "tx_hash": raw_stream_event.get("tx_hash", "0x00"),
            "source_chain_id": raw_stream_event.get("source_chain_id", 0),
            "destination_chain_id": raw_stream_event.get("destination_chain_id", 0),
            "intent_amount_usd": raw_stream_event.get("amount_usd", 0.0),
            "system_integrity_check": "COMPROMISED_OFFLINE" if system_compromised else "ONLINE_VERIFIED"
        }
        
        # Enforce baseline velocity calculations on the captured cross-chain stream data
        harvested_payload["calculated_velocity"] = self.velocity_floor if not system_compromised else 0.0
        return harvested_payload
