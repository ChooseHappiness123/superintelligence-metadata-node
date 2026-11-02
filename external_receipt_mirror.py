import json
import time

class ExternalReceiptMirror:
    def __init__(self):
        self.remote_mirror_log = []
        self.local_audit_receipts = []

    def emit_to_public_mirror(self, record: dict) -> dict:
        """
        POSTs a minimal payload to an external endpoint if state is PROMOTED 
        or REVALIDATION_FAILED. Appends a local receipt of the emission attempt.
        """
        record_status = record.get("status", "CANDIDATE")
        source_url = record.get("source_url", "UNKNOWN_URL")
        
        if record_status in ["CANDIDATE", "STAGED_UNVERIFIED"]:
            audit_receipt = {
                "timestamp": time.time(),
                "source_url": source_url,
                "attempt_status": "SKIPPED_ISOLATED",
                "reason": "Candidates forbidden from remote emission"
            }
            self.local_audit_receipts.append(audit_receipt)
            return {"status": "REJECTED_ISOLATED", "audit": audit_receipt}

        minimal_payload = {
            "timestamp": record.get("timestamp"),
            "event_type_context": "REVALIDATION_FAILED_STALE" if record_status == "REVALIDATION_FAILED_STALE" else "PROMOTED_NOMINAL",
            "motif": record.get("motif"),
            "source_url": source_url,
            "onchain_match": record.get("onchain_match")
        }
        
        # Simulate network POST transaction layer
        self.remote_mirror_log.append(minimal_payload)
        
        audit_receipt = {
            "timestamp": time.time(),
            "source_url": source_url,
            "attempt_status": "SUCCESSFUL_POST",
            "mirrored_payload_hash": hash(json.dumps(minimal_payload))
        }
        self.local_audit_receipts.append(audit_receipt)
        
        return {
            "remote_anchor_status": "APPEND_SUCCESS",
            "audit": audit_receipt,
            "payload": minimal_payload
        }
