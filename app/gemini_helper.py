import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1/models/{GEMINI_MODEL}:generateContent"

def ask_gemini(prompt: str) -> str:
    if not GEMINI_API_KEY:
        return "Gemini API key is missing. Set GEMINI_API_KEY in your .env file."

    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": GEMINI_API_KEY
    }
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Gemini API error: {response.status_code} {response.text}"
    except Exception as e:
        return f"Gemini request failed: {e}"

def start_chat():
    print("Welcome to the Gemini AI chatbot!")
    print("Ask anything, and type 'exit' to stop.")

    while True:
        user_input = input("You: ")  
        if user_input.lower() == 'exit':
            print("Goodbye! Exiting the chat.")
            break
        else:
            response = ask_gemini(user_input)
            print(f"Gemini: {response}")


if __name__ == "__main__":
    start_chat()