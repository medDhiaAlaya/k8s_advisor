import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_cluster(summary):
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"Here is my Kubernetes cluster info: {summary}. Give me advice to optimize performance, stability, and security."
    response = model.generate_content(prompt)
    return response.text
