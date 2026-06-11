import re
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI


from prompts.writer_prompt import WRITER_PROMPT
from prompts.critic_prompt import CRITIC_PROMPT


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview", 
    temperature=0.7
)

def writer_node(state):

    prompt = WRITER_PROMPT.format(
        topic=state["topic"],
        feedback=state["feedback"]
    )

    response = llm.invoke(prompt)

    essay = response.content

    iteration = state["iteration"] + 1

    print("\n" + "=" * 60)
    print(f"ITERATION {iteration}")
    print("=" * 60)

    print("\nESSAY DRAFT:\n")
    print(essay)

    return {
        "essay": essay,
        "iteration": iteration,
        "logs": [
            f"\n{'='*60}\n"
            f"ITERATION {iteration}\n"
            f"{'='*60}\n\n"
            f"ESSAY:\n{essay}\n"
        ]
    }
    
    
def critic_node(state):

    prompt = CRITIC_PROMPT.format(
        essay=state["essay"]
    )

    response = llm.invoke(prompt)

    critique = response.content

    score_match = re.search(
        r"SCORE:\s*(\d+)",
        critique
    )

    if score_match:
        score = int(
            score_match.group(1)
        )
    else:
        score = 0

    feedback = ""

    if "FEEDBACK:" in critique:

        feedback = critique.split(
            "FEEDBACK:"
        )[1].strip()

    print("\nSCORE:", score)

    print("\nFEEDBACK:\n")
    print(feedback)

    return {

        "score": score,

        "feedback": feedback,

        "logs": [
            f"\nSCORE: {score}\n\n"
            f"FEEDBACK:\n{feedback}\n"
        ]
    }