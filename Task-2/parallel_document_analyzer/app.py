from graph.workflow import graph

from utils.logger import save_report


def main():

    initial_state = {

        "document": "",

        "summary": "",

        "topics": "",

        "sentiment": "",

        "report": "",

        "trace": []
    }

    result = graph.invoke(
        initial_state
    )

    print(
        "\n" +
        "=" * 50
    )

    print(
        "DOCUMENT ANALYSIS REPORT"
    )

    print(
        "=" * 50
    )

    print(
        result["report"]
    )

    log_file = save_report(
        result["trace"],
        result["report"]
    )

    print(
        f"\nLog saved to: {log_file}"
    )


if __name__ == "__main__":
    main()