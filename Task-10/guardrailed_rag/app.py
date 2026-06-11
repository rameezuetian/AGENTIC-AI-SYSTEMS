from graph.workflow import config, graph
from utils.logger import save_session


def main() -> None:
    while True:
        question = input("\nQuestion: ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        result = graph.invoke({"question": question}, config=config)

        print("\nAnswer:\n")
        print(result["answer"])
        save_session(result)


if __name__ == "__main__":
    main()
