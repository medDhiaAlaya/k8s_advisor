# Standard imports
from rich import print
from rich.console import Console
from rich.table import Table
from k8s_collector import get_detailed_cluster_info

# AI modules
from ai.analysis import analyze_cluster
from ai.monitoring import generate_alerting_rules
from ai.autohealing import suggest_auto_healing
from ai.cost import suggest_cost_optimizations
from ai.security import check_security_practices

# Utils
from utils import display_banner

import json

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

def display_recommendations(title, data, key1, key2, color1="bold red", color2="green"):
    table = Table(title=title)
    table.add_column(key1.capitalize(), style=color1, width=30)
    table.add_column(key2.capitalize(), style=color2)
    for item in data:
        table.add_row(item.get(key1, "N/A"), item.get(key2, "N/A"))
    console.print(table)

def main():
    try:
        display_banner()

        print("[cyan]🚀 Starting Kubernetes AI Advisor CLI...[/cyan]")
        print("\n[cyan]🔍 Collecting cluster data...[/cyan]")
        summary = get_detailed_cluster_info()
        display_summary(summary)

        print("\n[cyan]🧠 Asking Gemini for cluster analysis...[/cyan]")
        recommendations = analyze_cluster(summary)
        display_recommendations("🤖 Gemini AI Recommendations", recommendations, "issue", "recommendation")

        print("\n[cyan]📡 Generating monitoring alerts...[/cyan]")
        alerts = generate_alerting_rules(summary)
        display_recommendations("📈 Monitoring Alerts", alerts, "alert_name", "description")

        print("\n[cyan]🔄 Suggesting auto-healing actions...[/cyan]")
        healing = suggest_auto_healing(summary)
        display_recommendations("🛠️ Auto-Healing Suggestions", healing, "trigger", "action")

        print("\n[cyan]💰 Looking for cost optimizations...[/cyan]")
        cost = suggest_cost_optimizations(summary)
        display_recommendations("💸 Cost Optimization Tips", cost, "area", "suggestion")

        print("\n[cyan]🔐 Performing security audit...[/cyan]")
        security = check_security_practices(summary)
        display_recommendations("🔒 Security Best Practices", security, "risk", "recommendation")

        # Save all results
        with open("recommendations.txt", "w") as f:
            json.dump(recommendations, f, indent=2)
        with open("alerts.txt", "w") as f:
            json.dump(alerts, f, indent=2)
        with open("healing.txt", "w") as f:
            json.dump(healing, f, indent=2)
        with open("cost.txt", "w") as f:
            json.dump(cost, f, indent=2)
        with open("security.txt", "w") as f:
            json.dump(security, f, indent=2)

        print("\n[green]✅ All results saved to disk.[/green]")

    except Exception as e:
        print(f"[red]❌ Error: {e}[/red]")

if __name__ == "__main__":
    main()
