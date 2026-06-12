## Task:  
● Guardrailed Observability-Ready RAG Agent: Take the RAG pipeline from the 
provided course syllabus (load, chunk, embed, persist, retrieve, generate) and wrap it 
with a complete safety and observability layer using LangGraph. Add an input guardrail 
node that blocks prompt injections and off-topic queries (anything unrelated to the 
loaded documents), routing blocked requests to a polite rejection node. Add an output 
guardrail node that scans the LLM's response for hallucination signals (answer not 
grounded in retrieved chunks) and flags them with a warning prefix. Enable full 
LangSmith tracing with a descriptive run_name per session. Generate a local 
timestamped session report listing every question asked, the guardrail decision 
(pass/block/flag), the final answer, and all cited sources. All credentials in .env. 