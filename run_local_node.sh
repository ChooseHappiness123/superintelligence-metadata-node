```bash
#!/usr/bin/env bash
# ==============================================================================
# PHASE_36_ZAGGING_ACTIVE: FORKABLE NODE SETUP & DELTA INTERROGATION LAYER
# ==============================================================================
set -euo pipefail

# Ensure environment reads from the exact same central data objects
RUN_DELTA_SUMMARY=false

if [[ \$# -gt 0 && "\$1" == "--delta" ]]; then
    RUN_DELTA_SUMMARY=true
fi

if [ "\$RUN_DELTA_SUMMARY" = true ]; then
    echo "🔍 FORENSIC LAYER INTERROGATION: COMPUTING INTER-MODULE DELTA REPORT..."
    echo "=============================================================================="
    python3 -c "
from historical_phase_ledger import HistoricalPhaseLedger
from ecosystem_timeline_parser import EcosystemTimelineParser
import json

ledger = HistoricalPhaseLedger()
parser = EcosystemTimelineParser()

parser.parse_sequence_and_check_traps(ledger)
report = ledger.generate_delta_report()

print(f'📡 [DATA_CENTER] TOTAL REGISTRY ENTRIES CAPTURED: {report[\"total_phases_catalogued\"]}')
print(f'⚠️  [CRITICAL_ALERTS] AUDITED THRESHOLD BREACHES: {report[\"critical_divergences_found\"]}')
print(f'📊 [HONESTY_INDEX] SYSTEM CONVERGENCE RATIO    : {report[\"system_honesty_score\"]:.1f}%')
print('==============================================================================')
"
    exit 0
fi

echo "🌌 INITIALIZING SOVEREIGN OPEN VERIFICATION SYSTEM LAYER..."
if ! command -v docker &> /dev/null; then
    echo "❌ ERROR: Docker engine dependency missing."
    exit 1
fi

docker compose up -d --build
echo "⏳ VERIFYING LOCAL COMPILATION RUNTIME INTEGRITY..."
docker compose exec -T phase_35_simulation_mirror python /app/test_phase_35_pipeline.py
echo "🟢 SUCCESS: OPEN FORKABLE LOCAL NODE RUNNING NOMINAL."
```

---
