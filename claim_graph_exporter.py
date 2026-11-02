import json
import time
import os

class ClaimGraphExporter:
    def __init__(self, sink_instance, oracle_instance, monitor_instance):
        self.sink = sink_instance
        self.oracle = oracle_instance
        self.monitor = monitor_instance

    def export_portable_claim_graph_json(self) -> str:
        """
        Extracts only records where status == 'PROMOTED', mapping the original 
        source links side-by-side with resulting honesty and pressure shifts.
        """
        promoted_records = self.sink.fetch_promoted_records_only()
        graph_nodes = []

        for record in promoted_records:
            url = record.get("source_url")
            
            # Match snapshots using the unique source_url index point
            honesty_contribution = next((snap for snap in self.oracle.score_history_log if snap.get("triggering_source_url") == url), {})
            pressure_contribution = next((snap for snap in self.monitor.pressure_history_log if snap.get("triggering_source_url") == url), {})

            node = {
                "timestamp": record.get("timestamp"),
                "motif": record.get("motif"),
                "source_url": url,
                "onchain_match": record.get("onchain_match"),
                "resulting_honesty_delta": str(honesty_contribution.get("rolling_honesty_score_pct", 100.0)) + "%",
                "resulting_pressure_ratio": str(pressure_contribution.get("calculated_pressure_ratio", 0.0))
            }
            graph_nodes.append(node)

        export_payload = {
            "export_timestamp": time.time(),
            "graph_edges": graph_nodes
        }
        
        # Append-only file writing using a unique unix millisecond anchor to prevent overwriting history
        unique_file_id = int(time.time() * 1000)
        filename = f"claim_graph_export_{unique_file_id}.json"
        
        with open(filename, "w") as f:
            json.dump(export_payload, f, indent=2)

        return json.dumps(export_payload, indent=2)
