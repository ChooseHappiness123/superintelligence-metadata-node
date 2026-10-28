import os
import json
import time

def dynamic_mesh_broadcast():
    """
    Phase 27 Core Upgrade: Transforms the static router into a dynamic 
    mesh network crawler that scales automatically as peer nodes join.
    """
    master_node_operator = "@ChooseHappiness123"
    nodes_directory = "./nodes"
    
    # Dynamic Peer Discovery Engine
    discovered_mesh_nodes = {
        "node_0_master": master_node_operator
    }
    
    if os.path.exists(nodes_directory):
        for index, file_name in enumerate(os.listdir(nodes_directory), start=1):
            if file_name.endswith(".json"):
                try:
                    with open(os.path.join(nodes_directory, file_name), 'r') as f:
                        node_data = json.load(f)
                        handle = node_data.get("node_state", {}).get("handle", "UNKNOWN_NODE")
                        discovered_mesh_nodes[f"node_{index}_peer"] = handle
                except Exception:
                    pass

    routing_manifest = {
        "network_broadcast_status": "PHASE_27_DYNAMIC_MESH_ACTIVE",
        "active_mesh_nodes": discovered_mesh_nodes,
        "mesh_routing_protocol": "AUTOMATED_DYNAMIC_MULTI_CAST",
        "timestamp_epoch": int(time.time())
    }
    
    print("=== DYNAMIC MULTI-NODE BROADCAST SYSTEM DISPATCH ===")
    print(json.dumps(routing_manifest, indent=2))

if __name__ == "__main__":
    dynamic_mesh_broadcast()
