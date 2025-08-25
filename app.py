# app.py
from dotenv import load_dotenv
load_dotenv()  # this reads .env and sets GOOGLE_API_KEY

import os
import google.generativeai as genai
from prompts import SYSTEM_PROMPT, USER_PROMPTS

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load model (use flash for free/fast, pro for better quality)
model = genai.GenerativeModel("gemini-1.5-flash")

def ask_ai(user_input):
    # Merge system and user prompts
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_input}\nAI:"
    
    response = model.generate_content(full_prompt)
    return response.text

if __name__ == "__main__":
    for i, prompt in enumerate(USER_PROMPTS, 1):
        print(f"\n--- Test {i}: {prompt} ---")
        answer = ask_ai(prompt)
        print(answer)
