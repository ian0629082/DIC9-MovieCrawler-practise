import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("Missing GEMINI_API_KEY. Please set it in .env first.")

genai.configure(api_key=api_key)

models_to_test = [
    "gemini-2.0-flash",
    "gemini-2.5-flash",
    "gemini-3.5-flash",
    "gemini-flash-latest",
    "gemini-pro-latest",
    "gemma-4-26b-a4b-it"
]

for m_name in models_to_test:
    try:
        print(f"Testing {m_name}...")
        model = genai.GenerativeModel(m_name)
        resp = model.generate_content("Hi", safety_settings=[])
        print(f"  Success: {resp.text.strip()}")
    except Exception as e:
        print(f"  Failed for {m_name}: {e}")
