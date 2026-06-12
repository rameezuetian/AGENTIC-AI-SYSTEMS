from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from memory.short_term import memory
from services.streaming import stream_graph


router = APIRouter()


class StreamRequest(BaseModel):
    question: str
    user_id: str
    thread_id: str


@router.post("/chat/stream")
async def chat_stream(request: StreamRequest):
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
    config = {
        "configurable": {
            "thread_id": request.thread_id,
        }
    }

    async def event_stream():
        final_state = dict(state)
        async for chunk, event_state in stream_graph(state, config):
            if event_state:
                final_state = event_state
            yield chunk

        answer = final_state.get("answer", "")
        if answer:
            memory.append_message(request.thread_id, "user", request.question)
            memory.append_message(request.thread_id, "assistant", answer)

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
    )
