## Task:  
● Multi-Agent Research & Report System: Build a supervisor-pattern multi-agent system 
with one supervisor agent and three specialised worker agents — a Web Researcher 
(searches and retrieves facts), a Data Analyst (processes any structured data or 
numbers from the research), and a Report Writer (composes the final output). Accept a 
broad research topic from the terminal. The supervisor breaks the topic into subtasks 
and routes each to the appropriate worker using Command(goto=...). Workers return 
their output to the supervisor which assembles the final report. Print each agent's name 
and output as it executes. Save the final compiled report and the full delegation trace to 
a timestamped .txt file. All credentials in .env. 