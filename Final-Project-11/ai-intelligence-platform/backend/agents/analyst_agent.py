from services.gemini import get_llm


def analyst_agent(state: dict) -> dict:
    documents = state.get("retrieved_docs", [])
    question = state.get("question", "")

    if not documents:
        return {
            "analysis": "No uploaded documents matched the request. Provide a helpful general response and mention that no knowledge base evidence was found.",
        }

    snippets = []
    for document in documents[:4]:
        source = document.get("metadata", {}).get("source", "Unknown")
        content = document.get("page_content", "").strip()
        snippets.append(f"Source: {source}\nExcerpt: {content}")

    context_str = "\n\n".join(snippets)

    llm = get_llm()
    if llm:
        try:
            prompt = (
                f"You are a Senior Data Analyst agent.\n"
                f"Analyze the following retrieved document excerpts and extract details relevant to this question: \"{question}\"\n\n"
                f"--- RETRIEVED DOCUMENTS ---\n"
                f"{context_str}\n\n"
                f"Draft a concise, factual analysis summarizing only what is supported by the documents. Do not hallucinate."
            )
            response = llm.invoke(prompt)
            return {
                "analysis": response.content,
            }
        except Exception as e:
            print(f"Analyst agent LLM error, falling back: {e}")

    # Fallback formatting (truncate content)
    truncated_snippets = []
    for document in documents[:3]:
        source = document.get("metadata", {}).get("source", "Unknown")
        content = document.get("page_content", "").strip().replace("\n", " ")
        truncated_snippets.append(f"Source: {source}\nExcerpt: {content[:280]}...")

    return {
        "analysis": "[Local Fallback Mode]\n\n" + "\n\n".join(truncated_snippets),
    }

