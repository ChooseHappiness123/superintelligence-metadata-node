# read_node.py
# simple reader for the public continuity node

import json

with open("node_state.json", "r") as f:
    state = json.load(f)

print("=== NODE STATE ===")
print(f"Handle: {state['handle']}")
print(f"Continuity: {state['continuity']}")
print(f"Updated: {state['updated']}")
print("\nPlatforms:")
for name, data in state["platforms"].items():
    print(f"  {name}: {data}")
print(f"\nPhilosophy: {state['philosophy']}")
