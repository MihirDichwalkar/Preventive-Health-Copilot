# Preventive Health Copilot — Repo Template

This document contains the scaffolded repository files and ready-to-use code templates for the Preventive Health Copilot project. Copy each file into your project folder as shown in the *Repository structure* section.

---

## Repository structure

```
health-copilot/
├── notebooks/
│   └── preventive_health_copilot.py   # jupytext-style script (can convert to .ipynb)
├── src/
│   ├── __init__.py
│   ├── agent.py
│   ├── tools.py
│   ├── prompts.py
│   └── evaluation.py
├── slides/
│   └── slides_outline.md
├── requirements.txt
├── README.md
└── .gitignore
```

---

---

## File: requirements.txt

```text
# Core
langchain>=0.0.300
langchain-community
ollama
langgraph
jupyter
jupytext

# Utilities
python-dotenv
pytest
black
mypy

# Optional (if you add RAG later)
faiss-cpu
sentence-transformers

```

---

## File: .gitignore

```text
__pycache__/
.env
*.pyc
.ipynb_checkpoints/
*.egg-info/
.vscode/
.DS_Store

```

---

## File: README.md

````markdown
# Preventive Health Copilot

Open-source implementation of a Preventive Health Copilot using Ollama (Llama3.1), LangChain and LangGraph. This repository contains modular code, a demo notebook, evaluation utilities, and slide outlines for a 5-7 slide presentation.

## Structure
See the repository structure at the top-level of this document.

## Quickstart
1. Install Ollama and pull Llama 3.1:
   ```bash
   ollama pull llama3.1
````

2. Create Python environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run the demo notebook (Jupytext script provided):

   ```bash
   jupyter notebook notebooks/preventive_health_copilot.py
   ```

## Running tests

```bash
pytest -q
```

## Notes on production-readiness

* Keep the `src/` folder as your primary implementation. The notebook is a demonstration + evaluation harness.
* Add integration tests for tool-calling and agent behavior.

````

---

## File: src/__init__.py

```python
# Package marker for src
__all__ = ["agent", "tools", "prompts", "evaluation"]
````

---

## File: src/prompts.py

```python
"""Prompt templates used across iterations.

Separate file so prompts can be versioned and evaluated.
"""
from typing import Dict

BASELINE_PROMPT = """
You are a preventive health assistant.
Provide concise preventive health tips for the condition: {condition}.
Keep recommendations evidence-informed, actionable, and brief.
"""

REACT_PROMPT = """
You are a Preventive Health Copilot implementing the ReAct reasoning framework.

User query: {query}

Follow these steps explicitly:
1. Thought: think about the user's intent and constraints.
2. Action: decide whether to call a tool (get_health_tips or schedule_reminder).
3. Observation: include the tool output if a tool is called.
4. Answer: provide final actionable guidance and any scheduled reminders.

Respond using labeled sections: Thought, Action, Observation, Answer.
"""

PLAN_SOLVE_PROMPT = """
You are a Preventive Health Copilot using a Plan-and-Solve approach.

User query: {query}

1) Produce a short plan (2-4 steps).
2) Execute the steps, calling tools when helpful.
3) Summarize the final recommendations.

Return JSON with keys: plan (list), actions (list), result (string).
"""

PROMPT_LIBRARY: Dict[str, str] = {
    "baseline": BASELINE_PROMPT,
    "react": REACT_PROMPT,
    "plan_solve": PLAN_SOLVE_PROMPT,
}
```

---

## File: src/tools.py

```python
"""Tool implementations for the Preventive Health Copilot.

These are intentionally simple, deterministic, and mock interfaces so you
can focus on agent/tool orchestration and evaluation.

In production: replace scheduling mock with a calendar API wrapper and
replace static tips with a vetted knowledge base or RAG.
"""
from typing import List, Dict
import datetime


def _now_iso() -> str:
    return datetime.datetime.now().isoformat()


HEALTH_TIPS: Dict[str, List[str]] = {
    "stress": [
        "Practice 10 minutes of mindfulness meditation daily",
        "Take short movement breaks every 60 minutes",
        "Prioritize sleep: 7-9 hours per night",
    ],
    "diabetes": [
        "Choose high-fiber foods and whole grains",
        "Aim for 30 minutes of moderate activity most days",
        "Limit sugary drinks and refined carbs",
    ],
    "hypertension": [
        "Reduce sodium intake; aim for <2.3g sodium/day",
        "Engage in aerobic exercise 150 minutes/week",
        "Increase potassium-rich foods (bananas, spinach)",
    ],
}


def get_health_tips(condition: str) -> List[str]:
    """Return a list of preventive tips for a health condition.

    Args:
        condition: condition name (e.g., 'stress', 'diabetes')

    Returns:
        List of short action-oriented tips. Empty list if unknown.
    """
    if not condition:
        return []
    key = condition.strip().lower()
    return HEALTH_TIPS.get(key, [])


def schedule_reminder(time_iso: str, message: str) -> Dict[str, str]:
    """Mock scheduling function. Returns a dictionary describing the scheduled reminder.

    Args:
        time_iso: ISO-8601 time string for the reminder
        message: message text

    Returns:
        A dict with scheduled_at, message, and status.
    """
    # Simple validation
    try:
        _ = datetime.datetime.fromisoformat(time_iso)
    except Exception:
        scheduled_at = _now_iso()
        status = "scheduled_with_adjusted_time"
    else:
        scheduled_at = time_iso
        status = "scheduled"

    return {
        "scheduled_at": scheduled_at,
        "message": message,
        "status": status,
    }
```

---

## File: src/agent.py

```python
"""Agent wrapper that creates a LangChain agent wired to Ollama.

This module exposes create_agent() and helper functions. Keep logic minimal
so it is easy to unit test.
"""
from typing import Any, List
import logging

from langchain_community.llms import Ollama
from langchain.agents import initialize_agent, AgentType

from .tools import get_health_tips, schedule_reminder
from .prompts import REACT_PROMPT

logger = logging.getLogger(__name__)


def _llm_instance(model_name: str = "llama3.1") -> Ollama:
    """Create and return an Ollama LLM wrapper.

    Args:
        model_name: name of the Ollama model to use.

    Returns:
        Ollama LLM instance
    """
    return Ollama(model=model_name)


def create_agent(model_name: str = "llama3.1", verbose: bool = False):
    """Initialize a LangChain zero-shot ReAct agent with our tools.

    Args:
        model_name: Ollama model name
        verbose: whether to turn on verbose logging for the agent

    Returns:
        LangChain agent object
    """
    llm = _llm_instance(model_name)

    # LangChain expects tools decorated or simple callables; here we pass
    # small wrapper functions to keep separation of concerns.
    tools = [
        # Each tool should be a callable that accepts a string and returns string/dict
    ]

    # We'll create small thin wrappers so the agent can call them with text args.
    from langchain.tools import Tool


    def _tips_tool(text: str) -> str:
        tips = get_health_tips(text)
        if not tips:
            return f"No tips found for '{text}'."
        return "\n".join([f"- {t}" for t in tips])


    def _reminder_tool(text: str) -> str:
        # Expect `time_iso || message` simple format or natural language
        # For demo, try to split on '||'
        if "||" in text:
            time_iso, message = [p.strip() for p in text.split("||", 1)]
        else:
            # fallback: schedule at now + 1 minute (mock)
            import datetime

            time_iso = (datetime.datetime.now() + datetime.timedelta(minutes=1)).isoformat()
            message = text
        scheduled = schedule_reminder(time_iso, message)
        return str(scheduled)


    tools.append(Tool(name="get_health_tips", func=_tips_tool, description="Get preventive health tips for a condition"))
    tools.append(Tool(name="schedule_reminder", func=_reminder_tool, description="Schedule a reminder using 'time_iso || message'"))

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=verbose,
    )

    logger.info("Agent created with model=%s", model_name)
    return agent


if __name__ == "__main__":
    # Simple manual test
    a = create_agent(verbose=True)
    print(a.run("I have high blood pressure — give me 3 tips and schedule a reminder to walk at 18:30:00+00:00 || Walk 30 minutes"))
```

---

## File: src/evaluation.py

```python
"""Evaluation helpers for the Preventive Health Copilot.

Provides simple quantitative and qualitative metrics to compare prompt
iterations and agent performance.
"""
from typing import Dict, Any


def reasoning_quality_score(response: str) -> int:
    """Simple heuristic scoring for reasoning quality.

    Score 0-3: +1 for explicit chain-of-thought markers (Thought/Plan),
    +1 for a clear final recommendation, +1 for citing tool output or reasoning.
    """
    score = 0
    lc = response.lower()
    if "thought" in lc or "plan" in lc:
        score += 1
    if "answer" in lc or "recommend" in lc or "recommendation" in lc:
        score += 1
    if "observation" in lc or "tool" in lc or "reminder" in lc:
        score += 1
    return score


def evaluate_response(query: str, response: str) -> Dict[str, Any]:
    """Aggregate evaluation result for a single query/response pair.

    Returns a dict with scoring and short notes for manual review.
    """
    return {
        "query": query,
        "response_snippet": response[:300],
        "reasoning_score": reasoning_quality_score(response),
        "length_words": len(response.split()),
    }
```

---

## File: notebooks/preventive_health_copilot.py

```python
# %%
# Jupytext-style demo script: open in Jupyter or convert to .ipynb

# Install note: run `pip install -r ../requirements.txt` from the repo root.

# %%
from src.agent import create_agent
from src.prompts import BASELINE_PROMPT, REACT_PROMPT, PLAN_SOLVE_PROMPT
from src.tools import get_health_tips, schedule_reminder
from src.evaluation import evaluate_response

# %%
# Create agent
agent = create_agent(verbose=True)

# %%
# Baseline prompt demo
query = "stress"
print("--- Baseline Manual Call ---")
print(BASELINE_PROMPT.format(condition=query))

# %%
print("--- Tool Direct Call Example ---")
print(get_health_tips("stress"))

# %%
# Agent demo: tool-calling
user_query = "I'm worried about diabetes risk. Give me 3 tips and set a daily reminder at 08:00:00+00:00 || Morning glucose-friendly breakfast"
print(agent.run(user_query))

# %%
# Evaluation demo
resp = agent.run("I want tips for hypertension")
eval = evaluate_response("I want tips for hypertension", resp)
print(eval)
```

---

## File: slides/slides_outline.md

```markdown
# Slides Outline: Preventive Health Copilot

1. Title + Objective
2. Architecture Diagram (Ollama -> LangChain Agent -> Tools -> Notebook UI)
3. Prompt Design Iterations (baseline -> ReAct -> Plan-Solve)
4. Tools & Integration (get_health_tips, schedule_reminder)
5. Evaluation & Results
6. Trade-offs, Limitations
7. Future work & Deployment
```

---

# Instructions / Next steps

1. Copy files into your project directory.
2. Initialize git and create meaningful commits for each development step.
3. Run the demo script in `notebooks/` with Jupyter or convert to `.ipynb` using Jupytext.

If you'd like, I can:

* generate a downloadable zip of the repo scaffold (ask me to produce it),
* produce a proper `.ipynb` file instead of the Jupytext `.py` script,
* or create a PowerPoint file for the slide deck.

Tell me which of those you'd like next.
