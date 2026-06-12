## Task: 
● MCP-Powered Research Agent: Build and run two local MCP servers using mcp and 
FastMCP — one that exposes a search_web(query) tool (stubbed to return mock 
search results from a .json file) and one that exposes a read_file(path) tool 
(reads from an allowed directory). Connect both servers to a LangGraph ReAct-style 
agent using MultiServerMCPClient. Accept a research question from the terminal. 
The agent must autonomously decide which tools to call, in what order, to answer the 
question. Print every tool call and its result, then print the final synthesised answer. Log 
the full tool-use trace to a .txt file. All credentials in .env. 