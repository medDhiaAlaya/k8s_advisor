import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

def analyze_cluster(summary: dict):
    prompt = f"""
You are a Kubernetes expert AI. Based on the following cluster summary, return a concise list of problems and recommendations in this JSON format:

[
  {{"issue": "Short description", "recommendation": "Actionable advice"}}
]

Cluster Summary:
{json.dumps(summary, indent=2)}

Only return valid JSON.
"""
    response = model.generate_content(prompt)
    content = response.text.strip()

    if content.startswith("```json") and content.endswith("```"):
        content = content[7:-3].strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return [{"issue": "Unable to parse Gemini response", "recommendation": content}]
