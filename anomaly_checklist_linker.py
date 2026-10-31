import time

class AnomalyChecklistLinker:
    def __init__(self):
        self.output_target = "SIMULATION_EXIT_CHECKLIST.md"

    def link_anomaly_to_checklist(self, anomaly_report: dict) -> str:
        """
        PHASE_36_ZAGGING_ACTIVE: Automatically transforms raw anomaly flags and 
        velocity spike proofs into structured public decision checklists.
        """
        deviation_score = anomaly_report.get("deviation_score", 0.0)
        source_link = anomaly_report.get("source_verification_link", "https://solscan.io")
        tx_hash = anomaly_report.get("tx_hash", "0x00")
        
        pre_filled_markdown = f"""## [🚨 AUTOMATED SYSTEM ALERT] // {time.strftime('%Y-%m-%d %H:%M:%S')}
- **Anomaly Severity Index:** {deviation_score:.2f} Sigma Deviation Detect
- **Source Verification Link:** {source_link}
- **Mandatory Sizing Posture:** TRIPPED CRITICAL THRESHOLD. EXPORT ALL POSITIONS TO SIZE ZERO IMMEDIATELY.

### 📋 COMPLIANCE DRILL ACTION ITEMS
- [ ] Open the raw block proof link: {source_link}
- [ ] Verify if tx hash `{tx_hash[:10]}...` indicates key vault outflow movement.
- [ ] Confirm local kill-switch scripts are armed and cleared to deploy.
- [ ] Practice exposure reduction run via `exit_rehearsal_gym.py`.
"""
        return pre_filled_markdown
