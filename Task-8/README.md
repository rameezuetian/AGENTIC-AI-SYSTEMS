## Task:  
● Dual-Memory Personal Assistant: Build a LangGraph assistant that maintains both 
memory types simultaneously. Short-term memory: use SqliteSaver with message 
trimming — keep only the last 10 messages in active state, summarising older 
messages into a single summary node that prepends context. Long-term memory: use 
InMemoryStore with a user_id namespace — whenever the user states a personal 
fact (e.g. "I prefer Python", "My deadline is Friday"), a memory extraction node detects 
and stores it via store.put(). On every new session start, retrieve all stored long-term 
memories with store.search() and inject them into the system prompt. Add a 
/memories command to print all stored long-term facts. All credentials in .env. 