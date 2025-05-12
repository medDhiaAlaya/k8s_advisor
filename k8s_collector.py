from kubernetes import client, config

# def get_cluster_summary():
#     config.load_kube_config()
#     v1 = client.CoreV1Api()
#     nodes = v1.list_node()
#     pods = v1.list_pod_for_all_namespaces()
    
#     summary = {
#         "node_count": len(nodes.items),
#         "nodes": [node.metadata.name for node in nodes.items],
#         "pod_count": len(pods.items),
#         "crashloop_pods": [
#             pod.metadata.name for pod in pods.items
#             if pod.status.container_statuses and
#                any(cs.state.waiting and cs.state.waiting.reason == "CrashLoopBackOff"
#                    for cs in pod.status.container_statuses)
#         ]
#     }
#     return summary

# for testing purposes
def get_cluster_summary():
    # Fake data for testing purposes
    summary = {
        "node_count": 3,
        "nodes": ["node-1", "node-2", "node-3"],
        "pod_count": 10,
        "crashloop_pods": ["pod-1", "pod-3"]
    }
    return summary
