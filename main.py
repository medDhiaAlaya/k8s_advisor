from rich import print
from rich.panel import Panel
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

    if summary["crashloop_pods"]:
        print("\n[red]🔁 CrashLoopBackOff Pods:[/red]")
        for pod in summary["crashloop_pods"]:
            print(f"  - {pod}")
    if summary["pending_pods"]:
        print("\n[yellow]⏳ Pending Pods:[/yellow]")
        for pod in summary["pending_pods"]:
            print(f"  - {pod}")

def main():
    print("[cyan]Collecting cluster data...[/cyan]")
    summary = get_detailed_cluster_info()
    display_summary(summary)

    print("\n[cyan]Sending data to Gemini...[/cyan]")
    advice = analyze_cluster(summary)

    console.rule("🤖 Gemini AI Recommendations")
    print(advice)

    with open("recommendations.txt", "w") as f:
        f.write(advice)
    print("\n[green]✅ Recommendations saved to recommendations.txt[/green]")
