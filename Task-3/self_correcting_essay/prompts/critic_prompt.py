CRITIC_PROMPT = """
You are a strict essay critic.

Evaluate the essay below.

Essay:
{essay}

Instructions:
1. Give a score between 1 and 10.
2. Evaluate:
   - Clarity
   - Structure
   - Grammar
   - Depth
   - Conclusion

Return ONLY in this format:

SCORE: <number>

FEEDBACK:
<your feedback>
"""