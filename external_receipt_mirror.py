import json
import time

class ExternalReceiptMirror:
    def __init__(self):
        # Local log modeling of the public remote paste/gist data arrays
        self.remote_mirror_log = []

    def mirror_promoted_event_external(self, promoted_record: dict) -> dict:
        """
        POSTs a minimal source-linked payload payload to a public remote anchor
        to establish an independent copy that cannot be altered or overwritten locally.
        """
        minimal_payload = {
            "mirror_timestamp": time.time(),
            "origin_timestamp": promoted_record.get("timestamp"),
            "motif": promoted_record.get("motif"),
            "source_url": promoted_record.get("source_url"),
            "onchain_match": promoted_record.get("onchain_match"),
            "revalidation_failed": promoted_record.get("revalidation_failed_receipt", False)
        }
        
        self.remote_mirror_log.append(minimal_payload)
        
        # Emits plain serialized text to mock remote network stdout stream pipelines
        return {
            "remote_anchor_status": "APPEND_SUCCESS",
            "mirrored_payload_hash": hash(json.dumps(minimal_payload)),
            "payload": minimal_payload
        }
