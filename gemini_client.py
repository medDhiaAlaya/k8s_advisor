import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

def analyze_cluster(summary: dict):
    # Constructing the prompt for Gemini
    prompt = f"""
You are a Kubernetes expert AI. Based on the following cluster summary, return a concise list of problems and recommendations in this JSON format:

[
  {{"issue": "Short description", "recommendation": "Actionable advice"}}
]

Cluster Summary:
{json.dumps(summary, indent=2)}

Only return valid JSON.
"""
    # Get response from Gemini
    response = model.generate_content(prompt)
    content = response.text.strip()

    # Clean up the response text, remove the outer markdown block and ensure it’s valid JSON
    if content.startswith("```json") and content.endswith("```"):
        content = content[7:-3].strip()

    # Try parsing the JSON response
    try:
        parsed_content = json.loads(content)
    except json.JSONDecodeError:
        # Handle case where response isn't valid JSON
        parsed_content = [{"issue": "Unable to parse Gemini response", "recommendation": content}]

    return parsed_content