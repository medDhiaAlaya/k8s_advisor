import json
from ai.analysis import model

def suggest_cost_optimizations(summary: dict):
    prompt = f"""
You are a Kubernetes FinOps advisor. Based on the cluster summary, suggest cost-saving opportunities.

Output format:
[
  {{"area": "Resource/Component", "suggestion": "Optimization tip", "impact": "High/Medium/Low"}}
]

Cluster Summary:
{json.dumps(summary, indent=2)}
"""
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text.strip("```json\n").strip("```"))
    except json.JSONDecodeError:
        return [{"area": "ParsingError", "suggestion": response.text.strip(), "impact": "Unknown"}]
