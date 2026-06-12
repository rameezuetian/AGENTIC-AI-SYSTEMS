from memory.long_term import store

PERSONAL_PATTERNS = [
    "i prefer",
    "i like",
    "my deadline",
    "my favorite",
    "i work with",
    "i am learning",
    "i use"
]


def extract_memory(
    message: str,
    user_id: str
):

    for pattern in PERSONAL_PATTERNS:

        if pattern in message.lower():

            store.put(
                namespace=(
                    "users",
                    user_id
                ),
                key=str(
                    abs(hash(message))
                ),
                value={
                    "fact": message
                }
            )

            print(
                f"[MEMORY STORED] {message}"
            )

            return True

    return False