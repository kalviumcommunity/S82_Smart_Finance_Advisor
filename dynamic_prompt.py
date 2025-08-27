import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env (expects GOOGLE_API_KEY)
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Dynamic Prompting ---
# The system instruction remains the same, but examples/context
# are inserted dynamically based on the query.

BASE_INSTRUCTION = (
    "You are a smart personal finance assistant. "
    "When the user provides income, expenses, or financial goals, "
    "respond with clear explanations. "
    "If numeric calculations are involved, show the steps briefly. "
    "If JSON is requested, return valid JSON."
)

# Context bank (like a mini knowledge base)
CONTEXT_SNIPPETS = {
    "budget": """Example:
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
}""",

    "investment": """Example:
User: Suggest safe, low-risk investment options.
AI: Some common low-risk options include:
- High-yield savings accounts
- Government bonds (e.g., Treasury Bills)
- Certificates of Deposit (CDs)
- Index funds with conservative allocation
""",

    "retirement": """Example:
User: How much should I save monthly to reach $50,000 in 10 years at 5% annual return?
AI: To calculate:
1. Future Value (FV) = 50,000
2. Rate of return (r) = 5% ÷ 12 = 0.004167
3. Time (n) = 10 × 12 = 120 months
4. Formula: PMT = FV × r / ((1 + r)^n – 1)
   PMT ≈ 322.09
So, you should save about **$322 per month**.
"""
}

# --- Test Prompts ---
USER_PROMPTS = [
    "Create a monthly budget for a ₹60,000 income using the 50/30/20 rule.",
    "Suggest low-risk investment options in simple terms.",
    "How much must I save monthly to reach ₹20,00,000 in 5 years at 7% annual return?",
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

def select_dynamic_context(user_input: str) -> str:
    """
    Chooses the most relevant example snippet dynamically.
    (Here we just keyword match, but in practice you could use embeddings/RAG.)
    """
    text = user_input.lower()
    if "budget" in text or "income" in text:
        return CONTEXT_SNIPPETS["budget"]
    elif "invest" in text or "low-risk" in text:
        return CONTEXT_SNIPPETS["investment"]
    elif "retire" in text or "save monthly" in text:
        return CONTEXT_SNIPPETS["retirement"]
    else:
        return ""  # fallback: no example provided

def run_dynamic_prompting():
    """
    Demonstrates DYNAMIC prompting:
    - Picks context/example snippets at runtime.
    - Creates a tailored prompt for each user query.
    """
    for i, user_input in enumerate(USER_PROMPTS, 1):
        dynamic_context = select_dynamic_context(user_input)
        prompt = f"{BASE_INSTRUCTION}\n\n{dynamic_context}\n\nUser: {user_input}\nAI:"
        resp = model.generate_content(prompt)
        print(f"\n--- Dynamic Test {i}: {user_input} ---")
        print(resp.text)

if __name__ == "__main__":
    run_dynamic_prompting()
