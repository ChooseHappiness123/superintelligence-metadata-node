#!/usr/bin/env bash
# ==============================================================================
# PHASE_36_ZAGGING_ACTIVE: OPEN VERIFICATION NODE ONE-COMMAND BOOTSTRAPPER
# ==============================================================================
set -euo pipefail

echo "🌌 INITIALIZING SOVEREIGN OPEN VERIFICATION SYSTEM LAYER..."

# Verify docker configuration footprint dependencies
if ! command -v docker &> /dev/null; then
    echo "❌ ERROR: Docker engine dependency missing. Install docker before spinning up node."
    exit 1
fi

echo "🔄 SPINNING UP CONTAINER INTEGRATION NETWORK..."
docker compose up -d --build

echo "⏳ VERIFYING LOCAL COMPILATION RUNTIME INTEGRITY..."
docker compose exec -T phase_35_simulation_mirror python /app/test_phase_35_pipeline.py

echo "🟢 SUCCESS: OPEN LOCAL VERIFICATION NODE NOMINAL AND COUPLED TO PUBLIC RPC DATA INDICES."
echo "📡 Truth dashboard endpoint active. Access SIMULATION_EXIT_CHECKLIST.md locally."
