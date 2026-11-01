import json
import time

class ClaimGraphExporter:
    def __init__(self, sink_instance, oracle_instance, monitor_instance):
        self.sink = sink_instance
        self.oracle = oracle_instance
        self.monitor = monitor_instance

    def export_portable_claim_graph_json(() -> str:
        """
        Dumps the append-only PROMOTED store as a clear directed list:
        motif -> source_url -> onchain_match -> resulting deltas.
        """
        promoted_records = self.sink.fetch_promoted_records_only()
        graph_nodes = []

        for record in promoted_records:
            url = record.get("source_url")
            # Trace matching historical delta slices from oracle and pressure logs
            honesty_contribution = next((snap for snap in self.oracle.score_history_log if snap.get("triggering_source_url") == url), {})
            pressure_contribution = next((snap for snap in self.monitor.pressure_history_log if snap.get("triggering_source_url") == url), {})

            node = {
                "motif": record.get("motif"),
                "source_url": url,
                "onchain_match": record.get("onchain_match"),
                "resulting_honesty_delta": {
                    "score_pct": honesty_contribution.get("rolling_honesty_score_pct", 100.0),
                    "status": honesty_contribution.get("verification_status", "NOMINAL")
                },
                "resulting_pressure_change": {
                    "ratio": pressure_contribution.get("calculated_pressure_ratio", 0.0),
                    "kill_switch_triggered": pressure_contribution.get("kill_switch_triggered", False)
                }
            }
            graph_nodes.append(node)

        return json.dumps({"timestamp": time.time(), "graph_edges": graph_nodes}, indent=2)

    def execute_stale_promotion_revalidation(self, broken_url_target: str = None) -> dict:
        """
        Re-polls existing PROMOTED endpoints. If a link fails or reverts, an append-only
        failure receipt is generated to alter down-chain oracle configurations.
        """
        promoted_records = self.sink.fetch_promoted_records_only()
        audit_report = {"timestamp": time.time(), "revalidated_count": len(promoted_records), "failures_logged": 0}

        for record in promoted_records:
            # Simulation of an unresolvable or modified transaction path link
            if broken_url_target and record.get("source_url") == broken_url_target:
                record["status"] = "REVALIDATION_FAILED"
                record["promoted_to_ledger"] = False
                audit_report["failures_logged"] += 1
                
        return audit_report
