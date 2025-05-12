from kubernetes import client, config

def get_detailed_cluster_info():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    version_info = client.VersionApi().get_code()

    pods = v1.list_pod_for_all_namespaces().items
    crashloop_pods = []
    pending_pods = []
    total_restarts = 0

    for pod in pods:
        for container_status in pod.status.container_statuses or []:
            restarts = int(container_status.restart_count)
            total_restarts += restarts
            if container_status.state and container_status.state.waiting and \
                    container_status.state.waiting.reason == "CrashLoopBackOff":
                crashloop_pods.append(pod.metadata.name)
        if pod.status.phase == "Pending":
            pending_pods.append(pod.metadata.name)

    nodes_summary = []
    for node in v1.list_node().items:
        node_name = node.metadata.name
        pods_on_node = [pod for pod in pods if pod.spec.node_name == node_name]
        restart_count = sum(
            int(cs.restart_count) for pod in pods_on_node
            for cs in pod.status.container_statuses or []
        )
        nodes_summary.append({
            "name": node_name,
            "pod_count": len(pods_on_node),
            "restart_count": restart_count,
            "pods": [pod.metadata.name for pod in pods_on_node]
        })

    return {
        "cluster_version": version_info.git_version,
        "node_count": len(nodes_summary),
        "pod_count": len(pods),
        "total_restarts": total_restarts,
        "crashloop_pods": crashloop_pods,
        "pending_pods": pending_pods,
        "nodes": nodes_summary
    }
