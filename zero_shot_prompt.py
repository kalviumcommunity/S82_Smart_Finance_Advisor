import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env (expects GOOGLE_API_KEY)
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Zero-shot Prompting ---
# No examples are provided. We rely on the model's pretrained knowledge.
# (We also avoid a long system prompt; just a short instruction header.)
INSTRUCTION = (
    "You are a helpful assistant. Answer clearly and concisely. "
    "If numeric calculations are needed, show the steps briefly. "
    "If the user asks for structured data, return valid JSON."
)

# Test prompts for the Smart Financial Advisor context (no examples given)
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
    # Keep outputs tight & repeatable enough for demos
    generation_config={
        "temperature": 0.4,
        "top_p": 0.9,
        "max_output_tokens": 1024,
        # Helpful when asking for JSON in zero-shot
        "stop_sequences": []
    }
)

def run_zero_shot_prompting():
    """
    Demonstrates ZERO-SHOT prompting:
    - We do NOT provide examples.
    - A minimal instruction header ensures clarity and JSON when asked.
    """
    for i, user_input in enumerate(USER_PROMPTS, 1):
        prompt = f"{INSTRUCTION}\n\nUser: {user_input}\nAI:"
        resp = model.generate_content(prompt)
        print(f"\n--- Zero-shot Test {i}: {user_input} ---")
        print(resp.text)

if __name__ == "__main__":
    run_zero_shot_prompting()
