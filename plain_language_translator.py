import time

class PlainLanguageTranslator:
    def __init__(self):
        self.velocity_floor = 1.44

    def translate_event_to_plain_text(self, harvested_frame: dict, monitor_status: dict) -> dict:
        """
        PHASE_36_ZAGGING_ACTIVE: Converts technical deBridge, Solscan, and Geoff payloads
        into a clear, one-sentence plain language summary linked directly to the on-chain proof.
        """
        tx_hash = harvested_frame.get("tx_hash", "0x00")
        source_link = harvested_frame.get("source_verification_link", f"https://solscan.io{tx_hash}")
        amount_sol = harvested_frame.get("value_sol", 0.0)
        destination = harvested_frame.get("destination_address", "unknown_vault")
        pressure_ratio = monitor_status.get("calculated_pressure_ratio", 0.0)
        
        # Build the zero-narrative plain language sentence string
        explanation_sentence = (
            f"This {amount_sol} SOL transfer went to address {destination[:8]}... "
            f"which interacts with known vault points — current liquidity pressure ratio is at {pressure_ratio:.4f}. "
            f"Source Proof: {source_link}"
        )
        
        translation_payload = {
            "timestamp": time.time(),
            "plain_text_explanation": explanation_sentence,
            "source_proof_link": source_link,
            "system_velocity_clamp": self.velocity_floor
        }
        
        return translation_payload
