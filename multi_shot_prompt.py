import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env (expects GOOGLE_API_KEY)
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Multi-shot Prompting ---
# We provide MULTIPLE examples (user + assistant pairs).
# This strongly guides the model toward consistent formatting and reasoning.

INSTRUCTION = (
    "You are a smart personal finance assistant. "
    "When the user provides income, expenses, or financial goals, "
    "respond with clear explanations. "
    "If numeric calculations are involved, show the steps briefly. "
    "If JSON is requested, return valid JSON."
)

# --- Multi-shot Examples ---
MULTI_SHOT_EXAMPLES = """
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

User: How much should I save monthly to reach $50,000 in 10 years at 5% annual return?
AI: To calculate:
1. Future Value (FV) = 50,000
2. Rate of return (r) = 5% ÷ 12 = 0.004167
3. Time (n) = 10 × 12 = 120 months
4. Use FV formula for monthly savings:
   PMT = FV × r / ((1 + r)^n – 1)
   PMT ≈ 322.09
So, you should save about **$322 per month**.

User: Suggest safe, low-risk investment options.
AI: Some common low-risk options include:
- High-yield savings accounts
- Government bonds (e.g., Treasury Bills)
- Certificates of Deposit (CDs)
- Index funds with conservative allocation
These protect your principal and grow steadily, though slower than high-risk investments.
"""

# --- Test Prompts (new unseen queries) ---
USER_PROMPTS = [
    "Create a monthly budget for a ₹60,000 income using the 50/30/20 rule.",
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

def run_multi_shot_prompting():
    """
    Demonstrates MULTI-SHOT prompting:
    - Provide multiple user+assistant examples.
    - Model mimics the structure and reasoning shown in examples.
    """
    for i, user_input in enumerate(USER_PROMPTS, 1):
        prompt = f"{INSTRUCTION}\n\nExamples:\n{MULTI_SHOT_EXAMPLES}\n\nUser: {user_input}\nAI:"
        resp = model.generate_content(prompt)
        print(f"\n--- Multi-shot Test {i}: {user_input} ---")
        print(resp.text)

if __name__ == "__main__":
    run_multi_shot_prompting()
