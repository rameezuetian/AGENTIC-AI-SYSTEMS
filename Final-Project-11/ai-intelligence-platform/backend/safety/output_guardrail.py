def check_output(
    answer: str,
    sources: list
):

    if not sources:

        return (
            "[WARNING] Response may not be grounded in source documents.\n\n"
            + answer,
            "Flagged"
        )

    return (
        answer,
        "Passed"
    )