from dotenv import load_dotenv

load_dotenv()


async def retrieve_node(state):
    """
    Placeholder retrieval node.

    In a real RAG system:
    - Search vector DB
    - Retrieve documents
    - Add context to state
    """

    return {}


async def generate_node(state):
    """
    No LLM call here.

    The LLM call is executed through LangGraph
    streaming events so we can stream tokens.
    """

    return {}
