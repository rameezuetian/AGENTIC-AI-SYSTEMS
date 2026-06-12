from fastapi import APIRouter

from memory.long_term import store


router = APIRouter()


@router.get("/memories/{user_id}")
def get_memories(user_id: str):
    memories = store.search(namespace=("users", user_id))
    return {
        "memories": [{"key": memory.key, "fact": memory.value["fact"]} for memory in memories],
    }


@router.delete("/memories/{user_id}/{key}")
def delete_memory(user_id: str, key: str):
    store.delete(namespace=("users", user_id), key=key)
    return {
        "status": "deleted",
        "key": key,
    }

