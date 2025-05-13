import json
from ai.analysis import model

def suggest_auto_healing(summary: dict):
    prompt = f"""
As a Kubernetes reliability expert, review the following cluster summary and suggest possible auto-healing strategies.

Output format:
[
  {{"trigger": "Issue condition", "action": "Auto-healing action to take", "tool": "K8s/Argo/CD/Script"}}
]

Cluster Summary:
{json.dumps(summary, indent=2)}
"""
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text.strip("```json\n").strip("```"))
    except json.JSONDecodeError:
        return [{"trigger": "ParsingError", "action": response.text.strip(), "tool": "N/A"}]
