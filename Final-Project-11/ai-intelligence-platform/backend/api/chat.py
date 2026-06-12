from fastapi import APIRouter
from pydantic import BaseModel

from graph.workflow import graph
from memory.short_term import memory


router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    user_id: str
    thread_id: str


@router.post("/chat")
async def chat(request: ChatRequest):
    config = {
        "configurable": {
            "thread_id": request.thread_id,
        }
    }
    state = {
        "question": request.question,
        "user_id": request.user_id,
        "thread_id": request.thread_id,
        "retrieved_docs": [],
        "analysis": "",
        "answer": "",
        "sources": [],
        "safety_decision": "",
    }
    result = graph.invoke(state, config=config)
    memory.append_message(request.thread_id, "user", request.question)
    memory.append_message(request.thread_id, "assistant", result["answer"])
    return {
        "answer": result["answer"],
        "sources": result.get("sources", []),
        "safety": result.get("safety_decision", "Passed"),
        "thread_id": request.thread_id,
        "user_id": request.user_id,
    }
