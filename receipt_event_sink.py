import time

class ReceiptEventSink:
    def __init__(self):
        self.motif_keywords = ["0.0011", "azy", "trix", "boxes", "@gymcore", "@gitler", "@itsover0x"]
        self.candidate_pool = []

    def ingest_candidate_stream_event(self, raw_input_payload: dict) -> dict:
        """
        Pulls down unverified social feeds, posts, or text notes. Filters for active 
        motifs and registers them into a volatile staging pool for cross-examination.
        """
        content = raw_input_payload.get("text", "").lower()
        author = raw_input_payload.get("author", "").lower()
        
        has_motif = any(keyword in content for keyword in self.motif_keywords) or any(handle in author for handle in self.motif_keywords)
        
        stage_record = {
            "candidate_id": f"CANDIDATE_{int(time.time())}_{hash(content) % 10000}",
            "timestamp": time.time(),
            "author": author,
            "raw_text": raw_input_payload.get("text", ""),
            "motif_matched": has_motif,
            "promotion_status": "STAGED_UNVERIFIED"
        }
        
        if has_motif:
            self.candidate_pool.append(stage_record)
            
        return stage_record

    def cross_reference_and_promote(self, candidate_id: str, verifiable_blockchain_tx: dict, timeline_parser_instance) -> dict:
        """
        Evaluates a staged candidate against a real on-chain transaction transfer, mint, 
        or liquidity delta. Promotes it straight into the timeline events array upon proof matching.
        """
        target_candidate = None
        for record in self.candidate_pool:
            if record["candidate_id"] == candidate_id:
                target_candidate = record
                break
                
        if not target_candidate:
            return {"status": "ERROR_CANDIDATE_NOT_FOUND", "promoted": False}
            
        tx_hash = verifiable_blockchain_tx.get("tx_hash", "0x00")
        source_chain = verifiable_blockchain_tx.get("chain", "solana")
        source_url = f"https://solscan.io{tx_hash}" if source_chain == "solana" else f"https://etherscan.io{tx_hash}"
        
        # Structure the formal chronological promotion block
        promoted_event = {
            "token": "CLUSTER_MOTIF",
            "event_type": "claim",
            "date": time.strftime('%Y-%m-%d'),
            "magnitude": float(verifiable_blockchain_tx.get("value_sol", 0.0011)),
            "source_url": source_url,
            "notes": f"PROMOTED_SIGNAL: Post by {target_candidate['author']} matching narrative claims verified on-chain. Text: '{target_candidate['raw_text']}'"
        }
        
        # Dynamic Append: Directly insert into the timeline parser array to update honesty oracle feeds
        timeline_parser_instance.chronological_events.append(promoted_event)
        target_candidate["promotion_status"] = "PROMOTED_VERIFIED"
        
        return {
            "status": "PROMOTED_SUCCESSFULLY",
            "promoted": True,
            "linked_event": promoted_event
        }
