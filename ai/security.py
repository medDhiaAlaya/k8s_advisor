import json
from ai.analysis import model

def check_security_practices(summary: dict):
    prompt = f"""
You're a Kubernetes security auditor. Based on the following cluster summary, check for security risks and suggest best practices.

Output format:
[
  {{"risk": "What is wrong", "recommendation": "What to do"}}
]

Cluster Summary:
{json.dumps(summary, indent=2)}
"""
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text.strip("```json\n").strip("```"))
    except json.JSONDecodeError:
        return [{"risk": "ParsingError", "recommendation": response.text.strip()}]
