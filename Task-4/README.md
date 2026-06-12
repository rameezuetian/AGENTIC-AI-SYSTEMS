## Task: 
● Persistent Multi-Turn Chatbot: Build a LangGraph chatbot with SqliteSaver as the 
checkpointer, backed by a local chat_history.db file. On startup, prompt the user for 
a thread_id — a returning user enters their existing ID to resume their session, a new 
user picks a new one. Each user message is added to state and passed to an LLM node 
that always has access to the full conversation history. Print conversation history on 
session start. Add a /history command to display all past messages for the current 
thread, and a /threads command to list all active thread IDs stored in the database. All 
credentials in .env. 