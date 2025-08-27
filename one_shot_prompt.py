import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env (expects GOOGLE_API_KEY)
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- One-shot Prompting ---
# We provide ONE example interaction (user + assistant) to guide the style/format.
# This helps the model better align with structured finance outputs.
INSTRUCTION = (
    "You are a smart personal finance assistant. "
    "When the user provides income, expenses, or financial goals, "
    "respond with clear explanations. "
    "If numeric calculations are involved, show the steps briefly. "
    "If JSON is requested, return valid JSON."
)

# --- One-shot Example ---
ONE_SHOT_EXAMPLE = """
User: Create a monthly budget for a $4000 income.
AI: {
  "income": 4000,
  "recommended_budget": {
    "housing": 1200,
    "food": 400,
    "savings": 800,
    "utilities": 300,
    "entertainment": 300,
    "miscellaneous": 1000
  },
  "advice": "You are saving 20% of your income — great job!"
}
"""

# --- Test Prompts (new unseen queries) ---
USER_PROMPTS = [
    "Create a monthly budget for a ₹60,000 income using the 50/30/20 rule.",
    "Suggest low-risk investment options in simple terms.",
    "How much must I save monthly to reach ₹20,00,000 in 5 years at 7% annual return?",
    "Give 5 practical ways to cut spending without changing my lifestyle too much.",
    "Explain emergency funds to a beginner."
]

# Load model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 0.4,
        "top_p": 0.9,
        "max_output_tokens": 1024,
        "stop_sequences": []
    }
)

def run_one_shot_prompting():
    """
    Demonstrates ONE-SHOT prompting:
    - We provide ONE reference example (user + assistant).
    - The model uses this as a guide for style, structure, and format.
    """
    for i, user_input in enumerate(USER_PROMPTS, 1):
        prompt = f"{INSTRUCTION}\n\nExample:\n{ONE_SHOT_EXAMPLE}\n\nUser: {user_input}\nAI:"
        resp = model.generate_content(prompt)
        print(f"\n--- One-shot Test {i}: {user_input} ---")
        print(resp.text)

if __name__ == "__main__":
    run_one_shot_prompting()
