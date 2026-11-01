#!/usr/bin/env bash
# ==============================================================================
# PHASE_36_ZAGGING_ACTIVE: FORKABLE NODE SETUP & CLAIM-GRAPH INTERROGATION LAYER
# ==============================================================================
set -euo pipefail

RUN_DELTA_SUMMARY=false
RUN_GRAPH_EXPORT=false

if [[ $# -gt 0 && "$1" == "--delta" ]]; then
    RUN_DELTA_SUMMARY=true
elif [[ $# -gt 0 && "$1" == "--graph" ]]; then
    RUN_GRAPH_EXPORT=true
fi

if [ "$RUN_GRAPH_EXPORT" = true ]; then
    echo "📊 RE-VERIFICATION ACCESS TERMINAL: EXPORTING PORTABLE DECOUPLED MESH..."
    python3 -c "
from receipt_event_sink import ReceiptEventSink
from honesty_oracle import HonestyOracle
from emergency_kill_switch import EmergencyKillSwitch
from liquidity_pressure_monitor import LiquidityPressureMonitor
from claim_graph_exporter import ClaimGraphExporter

sink = ReceiptEventSink()
kill_switch = EmergencyKillSwitch()
monitor = LiquidityPressureMonitor(kill_switch)
oracle = HonestyOracle()
exporter = ClaimGraphExporter(sink, oracle, monitor)

# Seed sample data for state verification checks
candidate = sink.append_candidate_event('0.0011 SOL sequence active via @gymcore.', 'https://solscan.io')
sink.try_promote('https://solscan.io', 'sample_hash')
candidate['magnitude'] = 0.0011

monitor.evaluate_pool_pressure({'current_pool_depth_usd': 600000.0}, {'cumulative_24h_outflow_usd': 60000.0}, candidate)
oracle.calculate_rolling_honesty_delta({'status': 'CLEAR'}, {'kill_switch_triggered': True}, [candidate])

print(exporter.export_portable_claim_graph_json())
"
    exit 0
fi

if [ "$RUN_DELTA_SUMMARY" = true ]; then
    echo "🔍 LIVE FORENSIC INTERROGATION: COMPUTING TRUE REPO CONVERGENCE DELTA..."
    echo "=============================================================================="
    python3 -c "
from historical_phase_ledger import HistoricalPhaseLedger
from ecosystem_timeline_parser import EcosystemTimelineParser
from live_public_ingester import LivePublicIngester
from emergency_kill_switch import EmergencyKillSwitch
from liquidity_pressure_monitor import LiquidityPressureMonitor

ingester = LivePublicIngester()
kill_switch = EmergencyKillSwitch()
pressure_monitor = LiquidityPressureMonitor(kill_switch)
ledger = HistoricalPhaseLedger()
parser = EcosystemTimelineParser()

eth_metrics = ingester.fetch_latest_ethereum_block_metrics()
timeline_report = parser.parse_sequence_and_check_traps(ledger)
delta_report = ledger.generate_delta_report()

print(f'🌐 [LIVE_RPC_NODE] CORE INFRASTRUCTURE CONNECTED: {eth_metrics[\"rpc_status\"]}')
print(f'📡 [DATA_CENTER]  TOTAL REGISTRY ENTRIES CAPTURED : {delta_report[\"total_phases_catalogued\"]}')
print(f'📈 [TIMELINE_LOOP] CHRONO SEQUENCE TRAP STATUS   : {timeline_report[\"status\"]}')
print('==============================================================================')
"
    exit 0
fi

echo "🌌 INITIALIZING SOVEREIGN OPEN VERIFICATION SYSTEM LAYER..."
docker compose up -d --build
docker compose exec -T phase_36_open_verification_node python3 test_phase_35_pipeline.py
echo "🟢 SUCCESS: OPEN LOCAL VERIFICATION NODE NOMINAL."
