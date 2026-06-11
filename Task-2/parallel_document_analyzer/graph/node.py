import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from prompts.summary_prompts import     SUMMARY_PROMPT
from prompts.sentiment_prompts import SENTIMENT_PROMPT
from prompts.topic_prompts import TOPIC_PROMPT


load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0.7)



def load_document(state):
    with open('data/document.txt', 'r', encoding='utf-8') as file:
        document = file.read()
        return {
            "document":document,
            "trace": ["Document loaded successfully."]
        }
        
        
def summarize_document(state):
    prompt = SUMMARY_PROMPT.format(document=state['document'])
    response = llm.invoke(prompt)
    return {
        "summary": response.content,
        "trace": ["Document summarized successfully."]
    }
    
    
def extract_topics(state):
    prompt = TOPIC_PROMPT.format(document=state['document'])
    response = llm.invoke(prompt)
    return {
        "topics": response.content,
        "trace": ["Topics extracted successfully."]
    }
    

def analyze_sentiment(state):
    prompt = SENTIMENT_PROMPT.format(document=state['document'])
    response = llm.invoke(prompt)
    return {
        "sentiment": response.content,
        "trace": ["Sentiment analyzed successfully."]
    }
    
def merge_results(state):

    report = f"""
==============================
DOCUMENT ANALYSIS REPORT
==============================

SUMMARY
--------
{state['summary']}

TOPICS
-------
{state['topics']}

SENTIMENT
---------
{state['sentiment']}
"""

    return {
        "report": report,
        "trace": [
            "Results Merged"
        ]
    }