## Task: 
● Live Streaming RAG Terminal: Extend the Day 4 persistent chatbot to support full 
token-level streaming. Use astream_events() to intercept on_chat_model_stream 
events and print each token to the terminal as it arrives — character by character, with 
no newline until the full response completes. Also stream node-level progress updates 
(e.g. [Retrieving...], [Generating...]) by printing node names as the graph 
transitions between them using "updates" mode alongside token streaming. Log the 
complete final responses (not individual tokens) to a timestamped session file. All 
credentials in .env. 