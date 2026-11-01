import json
import time

class ClaimGraphExporter:
    def __init__(self, sink_instance, oracle_instance, monitor_instance):
        self.sink = sink_instance
        self.oracle = oracle_instance
        self.monitor = monitor_instance

    def export_portable_claim_graph_json(self) -> str:
        """
        Dumps the append-only PROMOTED store into a clean, third-party verifiable JSON structure.
        """
        promoted_records = self.sink.fetch_promoted_records_only()
        graph_nodes = []

        for record in promoted_records:
            url = record.get("source_url")
            
            # Find the corresponding state outputs matching the original source url link
            honesty_contribution = next((snap for snap in self.oracle.score_history_log if snap.get("triggering_source_url") == url), {})
            pressure_contribution = next((snap for snap in self.monitor.pressure_history_log if snap.get("triggering_source_url") == url), {})

            node = {
                "timestamp": record.get("timestamp"),
                "motif": record.get("motif"),
                "source_url": url,
                "onchain_match": record.get("onchain_match"),
                "honesty_delta": str(honesty_contribution.get("rolling_honesty_score_pct", 100.0)) + "%",
                "pressure_ratio_after": str(pressure_contribution.get("calculated_pressure_ratio", 0.0))
            }
            graph_nodes.append(node)

        export_payload = {
            "export_timestamp": time.time(),
            "graph_edges": graph_nodes
        }
        
        # Write out to an append-only timestamped file configuration path to avoid overwriting prior work
        filename = f"claim_graph_export_{int(time.time())}.json"
        with open(filename, "w") as f:
            json.dump(export_payload, f, indent=2)

        return json.dumps(export_payload, indent=2)
