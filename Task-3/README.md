## Task: 
● Self-Correcting Essay Writer: Build a LangGraph workflow that accepts an essay topic 
from the terminal. A writer node drafts an essay. A critic node scores it out of 10 and 
provides feedback. A conditional edge checks the score — if below 7, route back to the 
writer node with the critique included in state; if 7 or above, route to an END node. Cap 
the loop at 5 iterations using a counter in state. Print each draft and its score to the 
terminal, and save the final accepted essay along with all iteration logs to a timestamped 
.txt file. All credentials in .env. 