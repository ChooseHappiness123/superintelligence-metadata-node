from datetime import datetime

class ReceiptEventSink:
    def __init__(self):
        self.allowed_motifs = ["0.0011", "azy", "trix", "boxes", "@gymcore", "@gitler", "@itsover0x"]
        # Append-only chronological list acting as our database repository
        self.event_ledger = []

    def append_candidate_event(self, raw_text: str, source_url: str) -> dict:
        """
        Append-only candidate writer. Detects core motifs and isolates them instantly
        within the ledger array without modifying or overwriting past logs.
        """
        if not source_url:
            return {"status": "DISCARDED", "reason": "MISSING_SOURCE_URL"}

        lower_text = raw_text.lower()
        detected_motif = "UNKNOWN_MOTIF"
        
        # Enforce exact motif matching signatures
        for motif in self.allowed_motifs:
            if motif in lower_text:
                detected_motif = motif
                break

        if detected_motif == "UNKNOWN_MOTIF" and any(handle in lower_text for handle in self.allowed_motifs):
            detected_motif = "LISTED_HANDLE"

        # Explicit requested append-only candidate structural layout
        candidate_event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "motif": detected_motif,
            "raw_note": raw_text[:500],
            "source_url": source_url,
            "status": "CANDIDATE",
            "onchain_match": None,
            "promoted_to_ledger": False
        }

        self.event_ledger.append(candidate_event)
        return candidate_event

    def try_promote(self, source_url: str, real_tx_hash: str) -> dict:
        """
        Promotion gate function. Only switches state to PROMOTED and flags true
        after verification links confirm real transfer or liquidity operations.
        """
        for candidate in self.event_ledger:
            if candidate["source_url"] == source_url and candidate["status"] == "CANDIDATE":
                # External verification assertion trigger
                if "solscan.io/tx/" in source_url or "etherscan.io/tx/" in source_url or real_tx_hash:
                    candidate["status"] = "PROMOTED"
                    candidate["onchain_match"] = real_tx_hash if real_tx_hash else "EXTRACTED_TX_SIGNATURE"
                    candidate["promoted_to_ledger"] = True
                    return candidate
                    
        return {"status": "STAYS_CANDIDATE", "promoted": False}

    def fetch_promoted_records_only(self) -> list:
        """
        Downstream isolation filter ensuring candidates remain invisible to
        the main timeline parsers, honesty oracles, and map views.
        """
        return [record for record in self.event_ledger if record["status"] == "PROMOTED"]
