from rich import print
from rich.console import Console
from rich.table import Table
from k8s_collector import get_detailed_cluster_info
from gemini_client import analyze_cluster

console = Console()

def display_summary(summary):
    table = Table(title="📊 Kubernetes Cluster Summary", show_header=False)
    table.add_row("🔧 Version", summary["cluster_version"])
    table.add_row("🖥️  Node Count", str(summary["node_count"]))
    table.add_row("📦 Total Pods", str(summary["pod_count"]))
    table.add_row("🚨 Total Restarts", str(summary["total_restarts"]))
    console.print(table)

    for node in summary.get("nodes", []):
        node_table = Table(title=f"🖥️ Node: [bold blue]{node['name']}[/bold blue]")
        node_table.add_column("Info", style="cyan", no_wrap=True)
        node_table.add_column("Value", style="magenta")

        node_table.add_row("Pod Count", str(node["pod_count"]))
        node_table.add_row("Restart Count", str(node["restart_count"]))
        node_table.add_row("Pods", ", ".join(node["pods"]) if node["pods"] else "-")
        console.print(node_table)

    if summary["crashloop_pods"]:
        print("\n[red]🔁 CrashLoopBackOff Pods:[/red]")
        for pod in summary["crashloop_pods"]:
            print(f"  - {pod}")
    if summary["pending_pods"]:
        print("\n[yellow]⏳ Pending Pods:[/yellow]")
        for pod in summary["pending_pods"]:
            print(f"  - {pod}")


def display_gemini_recommendations(recommendations):
    table = Table(title="🤖 Gemini AI Recommendations")
    table.add_column("Issue", style="bold red", width=30)
    table.add_column("Recommendation", style="green")

    for item in recommendations:
        issue = item.get("issue", "N/A")
        recommendation = item.get("recommendation", "N/A")
        table.add_row(issue, recommendation)

    console.print(table)

def main():
    try:
        print("[cyan]🚀 Starting Kubernetes AI Advisor CLI...[/cyan]")
        print("\n[cyan]🔍 Collecting cluster data...[/cyan]")
        summary = get_detailed_cluster_info()
        display_summary(summary)

        print("\n[cyan]🧠 Asking Gemini for analysis...[/cyan]")
        recommendations = analyze_cluster(summary)
        display_gemini_recommendations(recommendations)

        with open("recommendations.txt", "w") as f:
            import json
            json.dump(recommendations, f, indent=2)

        print("\n[green]✅ Recommendations saved to recommendations.txt[/green]")

    except Exception as e:
        print(f"[red]❌ Error: {e}[/red]")

if __name__ == "__main__":
    main()
