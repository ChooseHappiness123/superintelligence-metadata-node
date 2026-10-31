import time
from position_reduction_tester import PositionReductionTester

class ExitRehearsalGym:
    def __init__(self):
        self.reduction_tester = PositionReductionTester()
        self.rehearsal_history_count = 0

    def execute_exit_rehearsal(self, participant_handle: str, sim_position: dict, live_market: dict) -> dict:
        """
        PHASE_36_ZAGGING_ACTIVE: Scheduled dry-run environment allowing community participants 
        to practice reducing exposure to zero under actual live liquidity depth variables.
        """
        self.rehearsal_history_count += 1
        
        # Pull route quotes and slippage calculations directly from our reduction engine
        exit_metrics = self.reduction_tester.simulate_exit_route(sim_position, live_market)
        
        rehearsal_session_report = {
            "rehearsal_id": f"GYM_SESSION_{int(time.time())}_{self.rehearsal_history_count}",
            "participant_identity_hash": hash(participant_handle),
            "rehearsal_timestamp": time.time(),
            "simulated_metrics": {
                "asset": exit_metrics.get("target_asset"),
                "size_to_zero_target": exit_metrics.get("size_to_zero_target"),
                "estimated_slippage_pct": exit_metrics.get("implied_slippage_pct"),
                "expected_execution_time_seconds": exit_metrics.get("estimated_time_to_exit_seconds"),
                "exit_pathway_clearance": exit_metrics.get("recommended_action")
            },
            "educational_note": "PRACTICE EXIT COMPLETE. THIS IS A DRY-RUN DRILL. NO REAL PORTFOLIO MUTATION OCCURRED."
        }
        
        return rehearsal_session_report
