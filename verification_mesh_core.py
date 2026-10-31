import time
from geoff_layer_router import GeoffLayerRouter

class VerificationMeshCore:
    def __init__(self):
        self.router = GeoffLayerRouter()
        self.velocity_floor = 1.44
        self.buffer_gate = 420
        # Verified, inspectable on-chain tracking anchors
        self.tracked_vaults = {
            "void_sol_stage_14": "void.solutions_stage_14_deposit_vault_sol",
            "pond_water_v2": "pond0x_v2_core_liquidity_pool"
        }

    def process_and_expose_signal(self, stream_packet: dict, treasury_metrics: dict) -> dict:
        """
        PHASE_36_ZAGGING_ACTIVE: Decoupled Truth Layer. Converts incoming data pipelines 
        into verified public signals with explicit outbound exit pressure risk indexing.
        """
        tx_hash = stream_packet.get("tx_hash", "0x000_SOURCE_LINK_MISSING")
        source_chain = stream_packet.get("source_chain", "unknown")
        raw_input_hex = stream_packet.get("input_data_hex", "0x")
        
        # 1. Evaluate Permanent Risk Surface / Outflow Metrics First
        outbound_move_usd = treasury_metrics.get("outbound_volume_usd", 0.0)
        total_liquidity_usd = treasury_metrics.get("total_liquidity_usd", 1.0)
        exit_velocity_ratio = outbound_move_usd / total_liquidity_usd
        
        # 2. Route Raw Telemetry to Jef Probabilities Engine
        state_context = {
            "tx_source_link": f"https://solscan.io{tx_hash}" if source_chain == "solana" else f"https://etherscan.io{tx_hash}",
            "input_hex": raw_input_hex,
            "telemetry": {"volatile_buffer_count": stream_packet.get("buffer_size", 0), "unassigned_ghosts": 0}
        }
        jef_routing = self.router.route_to_model_layer(state_context, "jef")
        
        # 3. Compile Unaltered, Forkable Truth Package
        public_signal_frame = {
            "timestamp": time.time(),
            "source_verification_link": state_context["tx_source_link"],
            "raw_payload_shape_hash": hash(str(raw_input_hex)),
            "jef_classification_probabilities": jef_routing.get("output_type"),
            "risk_surface_metrics": {
                "exit_velocity_ratio": float(round(exit_velocity_ratio, 4)),
                "implied_exit_pressure": "HIGH_ALERT" if exit_velocity_ratio >= 0.10 else "NOMINAL",
                "liquidity_depth_usd": float(total_liquidity_usd)
            },
            "system_kill_switch_deployable": True
        }
        
        return public_signal_frame
