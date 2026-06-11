from memory.store import store


def show_memories(user_id: str):

    memories = store.search(
        namespace=("users", user_id)
    )

    print("\n===== STORED MEMORIES =====\n")

    if not memories:
        print("No memories found.")
        return

    for item in memories:
        print("-", item.value["fact"])
