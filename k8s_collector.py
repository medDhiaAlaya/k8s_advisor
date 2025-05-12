from kubernetes import client, config

def get_detailed_cluster_info():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    version_api = client.VersionApi()
    
    # General info
    version = version_api.get_code()
    nodes = v1.list_node().items
    pods = v1.list_pod_for_all_namespaces().items

    crashloop_pods = []
    pending_pods = []
    total_restarts = 0

    for pod in pods:
        for cs in (pod.status.container_statuses or []):
            if cs.restart_count:
                total_restarts += cs.restart_count
            if cs.state and cs.state.waiting:
                if cs.state.waiting.reason == "CrashLoopBackOff":
                    crashloop_pods.append(pod.metadata.name)
                elif pod.status.phase == "Pending":
                    pending_pods.append(pod.metadata.name)

    return {
        "cluster_version": f"{version.major}.{version.minor}",
        "node_count": len(nodes),
        "pod_count": len(pods),
        "crashloop_pods": crashloop_pods,
        "pending_pods": pending_pods,
        "total_restarts": total_restarts,
        "nodes": [node.metadata.name for node in nodes]
    }


# for testing purposes
# def get_cluster_summary():
#     # Fake data for testing purposes
#     summary = {
#         "node_count": 3,
#         "nodes": ["node-1", "node-2", "node-3"],
#         "pod_count": 10,
#         "crashloop_pods": ["pod-1", "pod-3"]
#     }
#     return summary
