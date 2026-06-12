from safety.patterns import INJECTION_PATTERNS


def check_input(question: str):

    question = question.lower()

    for pattern in INJECTION_PATTERNS:

        if pattern in question:

            return (
                False,
                f"Prompt Injection Detected: {pattern}"
            )

    return (
        True,
        "Passed"
    )