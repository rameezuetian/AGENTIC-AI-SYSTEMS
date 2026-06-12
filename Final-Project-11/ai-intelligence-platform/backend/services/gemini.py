from langchain_google_genai import ChatGoogleGenerativeAI
from config import settings

def get_llm():
    key = settings.google_api_key
    if not key or key == "YOUR_GOOGLE_API_KEY":
        return None
    try:
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=key,
            temperature=0.3
        )
    except Exception as e:
        print(f"Error initializing ChatGoogleGenerativeAI: {e}")
        return None
