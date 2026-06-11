from graph.workflow import graph

from utils.logger import (
    save_log
)


def main():

    config = {
        "configurable": {
            "thread_id":
            "approval_flow"
        }
    }

    task = input(
        "\nEnter High-Stakes Task:\n"
    )

    graph.invoke(
        {
            "task": task,
            "plan": "",
            "decision": "",
            "execution_result": "",
            "edited_plan": ""
        },
        config=config
    )

    state = graph.get_state(
        config
    )

    plan = state.values["plan"]

    print(
        "\nGenerated Plan:\n"
    )

    print(plan)

    decision = input(
        "\nApprove? "
        "(yes/edit/reject): "
    )

    if decision == "reject":

        graph.update_state(
            config,
            {
                "decision":
                "reject"
            }
        )

        print(
            "\nPlan Rejected."
        )

        return

    if decision == "edit":

        edited = input(
            "\nEnter Revised Plan:\n"
        )

        graph.update_state(
            config,
            {
                "plan": edited,
                "edited_plan": edited,
                "decision": "edit"
            }
        )

    if decision == "yes":

        graph.update_state(
            config,
            {
                "decision":
                "approved"
            }
        )

    final_result = graph.invoke(
        None,
        config=config
    )

    print(
        "\nExecution Result:\n"
    )

    print(
        final_result[
            "execution_result"
        ]
    )

    log_file = save_log(
        final_result
    )

    print(
        f"\nSaved To: {log_file}"
    )


if __name__ == "__main__":
    main()