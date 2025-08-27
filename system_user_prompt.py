import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define System Prompt (role + behavior)
SYSTEM_PROMPT = """
You are a Smart Financial Advisor AI.

Your role:
- Help users create budgets (50/30/20 rule or custom categories).
- Suggest investments based on risk tolerance (low, medium, high).
- Provide tax-saving strategies using general financial principles.
- Analyze expenses and suggest improvements.

Rules:
1. Explain reasoning in simple terms.
2. When providing structured data, use JSON format.
3. If unsure, say: "I need more details to give accurate advice."
4. Keep tone professional but easy to understand.
"""

# Example User Prompts
USER_PROMPTS = [
    "My monthly salary is ₹60,000. Can you create a budget using the 50/30/20 rule?",
    "I have ₹1,00,000 to invest. Suggest safe investment options with low risk.",
    "How can I save tax legally as a salaried employee in India?",
    "I spend ₹10,000 on rent, ₹5,000 on food, and ₹15,000 on shopping. Can you analyze my spending?",
    "I want to buy a car in 2 years. How should I plan my savings?"
]

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

def run_system_user_prompting():
    """
    Demonstrates System and User prompting:
    - SYSTEM_PROMPT defines AI's role.
    - USER_PROMPTS simulate user queries.
    """
    for i, user_input in enumerate(USER_PROMPTS, 1):
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_input}\nAI:"
        response = model.generate_content(full_prompt)
        print(f"\n--- Test {i}: {user_input} ---")
        print(response.text)

if __name__ == "__main__":
    run_system_user_prompting()
