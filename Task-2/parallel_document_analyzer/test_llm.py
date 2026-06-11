import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

llm =  ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0.7)

response = llm.invoke("What is LangGraph?")


print(response.content)