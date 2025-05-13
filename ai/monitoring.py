import json
from ai.analysis import model

def generate_alerting_rules(summary: dict):
    prompt = f"""
You're a Kubernetes monitoring expert. Based on the cluster summary below, generate a list of Prometheus or Kubernetes alerting rules for issues like high restarts, pod failures, or pending pods.

Output format:
[
  {{"alert_name": "AlertName", "expression": "PromQL or K8s condition", "description": "What it detects"}}
]

Cluster Summary:
{json.dumps(summary, indent=2)}
"""
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text.strip("```json\n").strip("```"))
    except json.JSONDecodeError:
        return [{"alert_name": "ParsingError", "expression": "-", "description": response.text.strip()}]
