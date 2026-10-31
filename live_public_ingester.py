import json
import urllib.request
import time

class LivePublicIngester:
    def __init__(self):
        # Public infrastructure endpoints for true runtime inspection
        self.solana_rpc = "https://api.mainnet-beta.solana.com"
        self.ethereum_rpc = "https://cloudflare-eth.com"
        self.target_sol_signature = 0.0011

    def fetch_latest_ethereum_block_metrics(self) -> dict:
        """
        PHASE_36_ZAGGING_ACTIVE: Hits live cloudflare Ethereum JSON-RPC layer to pull
        the hexadecimal block number and track active network execution status.
        """
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_blockNumber",
            "params": [],
            "id": 1
        }
        try:
            req = urllib.request.Request(
                self.ethereum_rpc,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                block_hex = res_data.get("result", "0x0")
                block_int = int(block_hex, 16) if block_hex.startswith("0x") else 0
                return {
                    "chain": "ethereum",
                    "live_block_height": block_int,
                    "rpc_status": "ONLINE_PARITY",
                    "source_verification_link": f"https://etherscan.io{block_int}"
                }
        except Exception as e:
            return {
                "chain": "ethereum",
                "live_block_height": 0,
                "rpc_status": f"FALLBACK_TRIGGERED: {str(e)}",
                "source_verification_link": "https://etherscan.io"
            }

    def process_live_transaction_flow(self, live_tx_frame: dict) -> dict:
        """
        PHASE_36_ZAGGING_ACTIVE: Parses a raw tx packet and enforces source-link verification.
        """
        tx_hash = live_tx_frame.get("tx_hash", "0x00_INVALID_HASH")
        source_chain = live_tx_frame.get("chain", "solana")
        raw_value_sol = live_tx_frame.get("value_sol", 0.0)
        
        source_link = f"https://solscan.io{tx_hash}" if source_chain == "solana" else f"https://etherscan.io{tx_hash}"
        
        return {
            "timestamp": time.time(),
            "tx_hash": tx_hash,
            "source_verification_link": source_link,
            "value_sol": float(raw_value_sol),
            "destination_address": live_tx_frame.get("destination", "").lower(),
            "is_target_pattern": raw_value_sol == self.target_sol_signature
        }
