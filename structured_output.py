import os
from dotenv import load_dotenv
import google.generativeai as genai
import json

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Structured Output Prompt ---
SYSTEM_PROMPT = """
You are a Smart Financial Advisor AI.

Rules:
1. Always return results in valid JSON format only (no extra text).
2. JSON must contain keys: "income", "recommended_budget", and "advice".
3. "recommended_budget" must break down income into categories.
4. Keep numbers realistic and ensure the JSON parses correctly.
"""

# Example user prompts
USER_PROMPTS = [
    "My income is ₹60,000. Create a budget using the 50/30/20 rule.",
    "I earn ₹1,00,000. Suggest a budget with 25% savings, 50% needs, 25% wants."
]

# Load model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 0.2,  # more deterministic for structured output
        "max_output_tokens": 512,
    }
)

def run_structured_output():
    """
    Demonstrates STRUCTURED OUTPUT:
    - Forces the model to output strict JSON.
    - Useful for app integration.
    """
    for i, user_input in enumerate(USER_PROMPTS, 1):
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_input}\nAI:"
        response = model.generate_content(full_prompt)
        print(f"\n--- Structured Output Test {i}: {user_input} ---")
        try:
            parsed = json.loads(response.text)  # ensure valid JSON
            print(json.dumps(parsed, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print("Invalid JSON returned by model:")
            print(response.text)

if __name__ == "__main__":
    run_structured_output()
