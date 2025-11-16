from langchain_core.prompts import ChatPromptTemplate

# -------------------------------------------------------------
# 1. BASELINE PROMPT
# -------------------------------------------------------------
baseline_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a preventive health assistant. Provide simple, clear, evidence-informed preventive health tips.",
    ),
    (
        "user",
        "Give me preventive health tips for: {condition}"
    ),
])


# -------------------------------------------------------------
# 2. IMPROVED STRUCTURED PROMPT
# -------------------------------------------------------------
structured_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a preventive health assistant who provides structured, actionable guidance.",
    ),
    (
        "user",
        """
Provide structured preventive tips for {condition}.

Format:
1. Brief explanation (1–2 sentences)
2. Three actionable tips
3. One sentence recommendation next steps
        """,
    ),
])


# -------------------------------------------------------------
# 3. REACT PROMPT (Reason + Act)
# -------------------------------------------------------------
react_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a preventive health copilot using ReAct reasoning.
Use: Thought → Action → Observation → Answer.
Use the available tools when required.
        """,
    ),
    (
        "user",
        """
User request: {query}

Follow this format strictly:
Thought:
Action:
Action Input:
Observation:
Answer:
        """,
    ),
])


# -------------------------------------------------------------
# 4. PLAN-SOLVE PROMPT
# -------------------------------------------------------------
plan_solve_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a preventive health copilot. First create a plan, then carry it out.",
    ),
    (
        "user",
        """
User query: {query}

Return structured JSON with this schema:
{
  "plan": ["step 1", "step 2", ...],
  "actions": ["execution details for each step"],
  "result": "final summarized recommendations"
}
        """,
    ),
])


# -------------------------------------------------------------
# 5. AGENT TOOL-CALLING PROMPT (create_react_agent compatible)
# -------------------------------------------------------------
tool_agent_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a preventive health copilot. Use tools when necessary and follow the ReAct pattern.",
    ),
    ("user", "{input}"),
])


__all__ = [
    "baseline_prompt",
    "structured_prompt",
    "react_prompt",
    "plan_solve_prompt",
    "tool_agent_prompt",
]
