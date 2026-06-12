from memory.long_term import store
from safety.output_guardrail import check_output
from services.gemini import get_llm


def writer_agent(state: dict) -> dict:
    memories = store.search(namespace=("users", state["user_id"]))
    memory_text = ", ".join(memory.value["fact"] for memory in memories)
    analysis = state.get("analysis", "")
    question = state["question"]
    sources = state.get("sources", [])

    llm = get_llm()
    if llm:
        try:
            system_prompt = (
                "You are an expert technical writer. Synthesize a polished final answer to the user's question "
                "based on the provided Data Analyst's analysis and documents.\n"
                "Strictly adhere to the user's preferences if any are stored in their memory (e.g. format preference, tone, length).\n\n"
                f"User Memory (Stored Preferences/Facts): {memory_text if memory_text else 'None'}\n"
                f"Data Analyst Synthesis: {analysis}\n"
                f"User Question: {question}\n\n"
                "Respond in clear, professional, well-formatted markdown. If documents were used, ground your response in them. "
                "If no documents match, formulate a helpful response and suggest uploading files for context."
            )
            response = llm.invoke(system_prompt)
            answer = response.content
            # Run output guardrail
            answer, decision = check_output(answer, sources)
            return {
                "answer": answer,
                "safety_decision": decision,
            }
        except Exception as e:
            print(f"Writer agent LLM error, falling back: {e}")

    # Fallback heuristic generator
    if state.get("retrieved_docs"):
        answer = (
            "Here is a grounded response based on your uploaded knowledge base (Local Heuristic Fallback).\n\n"
            f"{analysis}\n\n"
            f"Question: {question}\n"
            "Summary: The uploaded material above matches your query."
        )
    else:
        answer = (
            "I could not find matching uploaded documents, so this is a general guidance response.\n\n"
            f"Question: {question}\n"
            "Suggestion: Upload a relevant file to get a more grounded answer."
        )

    if memory_text:
        answer += f"\n\n[System Alert: running in Local Fallback mode due to missing GOOGLE_API_KEY]\nRemembered preferences or facts: {memory_text}"
    else:
        answer += f"\n\n[System Alert: running in Local Fallback mode due to missing GOOGLE_API_KEY]"

    answer, decision = check_output(answer, sources)
    return {
        "answer": answer,
        "safety_decision": decision,
    }

