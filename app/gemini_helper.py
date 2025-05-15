import requests
from app.utils.config import settings
from app.utils.whatsapp_helper import send_whatsapp_message

GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1/models/{settings.GEMINI_MODEL}:generateContent"

def ask_gemini(user_prompt: str) -> str:
    headers = {"Content-Type": "application/json"}
    params = {"key": settings.GEMINI_API_KEY}
    data = {
        "contents": [{"parts": [{"text": user_prompt}]}]
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        return f"Gemini API error: {response.status_code} {response.text}"
    except Exception as e:
        return f"Gemini request failed: {e}"

def start_chat():
    print("🤖 Welcome to the Gemini AI WhatsApp Bot!")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            break
        gemini_reply = ask_gemini(user_input)
        print(f"Gemini: {gemini_reply}")
        try:
            sid = send_whatsapp_message("whatsapp:+491626817993", gemini_reply)
            print(f"✅ WhatsApp message sent! SID: {sid}")
        except Exception as e:
            print(f"❌ Failed to send WhatsApp message: {e}")

if __name__ == "__main__":
    start_chat()