import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def format_summary_to_prompt(summary: dict) -> str:
    prompt = (
        f"My Kubernetes cluster is running version {summary['cluster_version']} with {summary['node_count']} nodes.\n"
        f"There are {summary['pod_count']} total pods.\n"
        f"Pods in CrashLoopBackOff: {summary['crashloop_pods']}\n"
        f"Pending pods: {summary['pending_pods']}\n"
        f"Total container restarts: {summary['total_restarts']}\n"
        f"Nodes: {', '.join(summary['nodes'])}\n\n"
        "Based on this, please provide:\n"
        "1. Any issues or warnings you see.\n"
        "2. Suggestions to improve performance, reliability, or cost-efficiency.\n"
        "3. Any security advice.\n"
    )
    return prompt

def analyze_cluster(summary):
    prompt = format_summary_to_prompt(summary)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text
