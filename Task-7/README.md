## Task:  
● Human-Approved Action Agent: Build a LangGraph agent that accepts a high-stakes 
task from the terminal (e.g. "Draft and send a project update email"). The agent has 
three nodes — a planner node that produces a structured action plan, a human approval 
node that interrupts and prints the plan asking Approve? (yes/edit/reject), and 
an executor node that carries out the approved plan. If the human types edit, capture 
their correction and use graph.update_state() to inject the revised plan before 
resuming. If reject, route to END. Log the original plan, human decision, any edits 
made, and the final execution result to a timestamped file. All credentials in .env.