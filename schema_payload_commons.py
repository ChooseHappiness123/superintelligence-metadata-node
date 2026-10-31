import json
import time

class SchemaPayloadCommons:
    def __init__(self):
        self.commons_registry = {}

    def capture_and_version_shape(self, emitter_origin: str, raw_incoming_json: str) -> dict:
        """
        PHASE_36_ZAGGING_ACTIVE: Extracts, timestamps, and indexes the raw JSON schemas 
        coming out of deBridge and Geoff endpoints to prevent narrative drift or gatekeeping.
        """
        timestamp_key = str(int(time.time()))
        
        try:
            parsed_structure = json.loads(raw_incoming_json) if isinstance(raw_incoming_json, str) else raw_incoming_json
            extracted_keys = list(parsed_structure.keys()) if isinstance(parsed_structure, dict) else []
        except Exception:
            extracted_keys = ["MALFORMED_STRUCTURE_RAW_RETAINED"]
            
        version_entry = {
            "timestamp": time.time(),
            "origin_endpoint": emitter_origin,
            "structural_shape_keys": extracted_keys,
            "schema_integrity": "STABLE"
        }
        
        if emitter_origin not in self.commons_registry:
            self.commons_registry[emitter_origin] = {}
            
        self.commons_registry[emitter_origin][timestamp_key] = version_entry
        return version_entry
