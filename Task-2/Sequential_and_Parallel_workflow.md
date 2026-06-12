## Task: 
● Parallel Document Analyser: Build a LangGraph workflow that takes a single input 
document (plain .txt file). In the first node, load and prepare the text. Then fan out in 
parallel to three nodes simultaneously — one that generates a summary, one that 
extracts key topics, and one that performs a sentiment analysis — each making its own 
LLM call. A final merge node combines all three outputs and prints a unified report to the 
terminal. Log the full graph execution trace and the final merged report to a timestamped 
.txt file. All credentials in .env. 