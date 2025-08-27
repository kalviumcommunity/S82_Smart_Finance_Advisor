import os
from dotenv import load_dotenv
import google.generativeai as genai
import json

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Function Definitions ---
def calculate_budget(income: float, rule: str = "50/30/20") -> dict:
    """
    Simple budget calculator based on income and a rule.
    Supported: "50/30/20", "70/20/10"
    """
    if rule == "50/30/20":
        return {
            "needs": round(income * 0.5, 2),
            "wants": round(income * 0.3, 2),
            "savings": round(income * 0.2, 2)
        }
    elif rule == "70/20/10":
        return {
            "needs": round(income * 0.7, 2),
            "wants": round(income * 0.2, 2),
            "savings": round(income * 0.1, 2)
        }
    else:
        return {"error": "Unsupported rule"}

def analyze_expenses(expenses: dict) -> str:
    """
    Analyzes spending pattern.
    """
    total = sum(expenses.values())
    if total == 0:
        return "No expenses to analyze."
    
    insights = []
    for category, amount in expenses.items():
        perc = (amount / total) * 100
        if perc > 40:
            insights.append(f"You are overspending on {category} ({perc:.1f}%).")
    if not insights:
        insights.append("Your expenses look balanced.")
    return " ".join(insights)

# --- Gemini Setup ---
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={"temperature": 0.3, "max_output_tokens": 512}
)

# --- Simulated Function Calling Logic ---
def run_function_calling():
    """
    Demonstrates FUNCTION CALLING:
    - Model suggests a function call (simulated).
    - Python executes the function and returns the result.
    """

    test_queries = [
        {"query": "I earn ₹60,000. Create a budget using the 50/30/20 rule."},
        {"query": "I spend 15,000 on rent, 10,000 on food, and 20,000 on shopping. Analyze my expenses."}
    ]

    for i, q in enumerate(test_queries, 1):
        print(f"\n--- Function Calling Test {i}: {q['query']} ---")

        # Step 1: Ask model what to do
        full_prompt = f"""
        You are a financial assistant. 
        Decide which function to call based on the query:
        1. calculate_budget(income, rule)
        2. analyze_expenses(expenses)
        Respond ONLY in JSON with fields: "function", "arguments".
        """
        response = model.generate_content(q["query"] + "\n\nAI:")
        
        try:
            call = json.loads(response.text)
            print("Model suggested function call:", call)

            # Step 2: Execute the suggested function
            if call["function"] == "calculate_budget":
                result = calculate_budget(**call["arguments"])
            elif call["function"] == "analyze_expenses":
                result = analyze_expenses(call["arguments"])
            else:
                result = {"error": "Unknown function"}

            # Step 3: Return result
            print("Function result:", result)

        except Exception as e:
            print("Error parsing function call:", response.text, e)

if __name__ == "__main__":
    run_function_calling()
