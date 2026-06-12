from fastapi import APIRouter

from memory.short_term import memory


router = APIRouter()


@router.get("/sessions")
def list_sessions():
    data = memory.list_threads()
    return {
        "sessions": [
            {
                "thread_id": thread_id,
                "message_count": len(messages),
                "last_message": messages[-1]["content"] if messages else "",
            }
            for thread_id, messages in data.items()
        ]
    }


@router.get("/sessions/{thread_id}")
def get_session(thread_id: str):
    return {
        "thread_id": thread_id,
        "messages": memory.get_thread(thread_id),
    }


@router.delete("/sessions/{thread_id}")
def delete_session(thread_id: str):
    memory.delete_thread(thread_id)
    return {
        "thread_id": thread_id,
        "status": "deleted",
    }

