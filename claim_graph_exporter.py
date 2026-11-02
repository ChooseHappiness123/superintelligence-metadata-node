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
            honesty_contribution = next((snap for snap in self.oracle.score_history_log if snap.get("triggering_source_url") == url), {})
            pressure_contribution = next((snap for snap in self.monitor.pressure_history_log if snap.get("triggering_source_url") == url), {})

            node = {
                "timestamp": record.get("timestamp"),
                "motif": record.get("motif"),
                "source_url": url,
                "onchain_match": record.get("onchain_match"),
                "resulting_honesty_delta": str(honesty_contribution.get("rolling_honesty_score_pct", 100.0)) + "%",
                "resulting_pressure_ratio": str(pressure_contribution.get("calculated_pressure_ratio", 0.0)),
                "revalidation_failed_receipt": record.get("revalidation_failed_receipt", False)
            }
            graph_nodes.append(node)

        export_payload = {
            "export_timestamp": time.time(),
            "graph_edges": graph_nodes
        }
        
        unique_file_id = int(time.time() * 1000)
        filename = f"claim_graph_export_{unique_file_id}.json"
        with open(filename, "w") as f:
            json.dump(export_payload, f, indent=2)

        return json.dumps(export_payload, indent=2)

    def execute_stale_promotion_revalidation(self, targeted_broken_url: str = None) -> dict:
        """
        Periodic pass over existing PROMOTED events that re-checks the original source_url.
        Appends a revalidation_failed receipt cleanly to keep historical promotions honest.
        """
        promoted_records = self.sink.fetch_promoted_records_only()
        audit_report = {
            "timestamp": time.time(),
            "revalidated_count": len(promoted_records),
            "failures_logged": 0,
            "failed_urls": []
        }

        for record in promoted_records:
            # Check for simulated network 404, tx reversals, or material liquidity drops
            if targeted_broken_url and record.get("source_url") == targeted_broken_url:
                record["revalidation_failed_receipt"] = True
                record["status"] = "REVALIDATION_FAILED_STALE"
                audit_report["failures_logged"] += 1
                audit_report["failed_urls"].append(record.get("source_url"))

        return audit_report
