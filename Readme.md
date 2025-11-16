# 🩺 Preventive Health Copilot: An Open-Source LLM Agent

**An Open-Source ReAct LLM Agent for Personalized Preventive Health Guidance**

This project implements an intelligent, prompt-driven **Preventive Health Copilot** using an open-source Large Language Model (LLM) agent. The Copilot is designed to demonstrate **multi-step reasoning (ReAct)**, **high-quality prompt engineering**, and **robust tool/function calling** for generating personalized health tips and scheduling mock reminders.

## 🎯 Project Objectives

1.  **Framework:** Design a LangChain/LangGraph ReAct agent architecture.
2.  **LLM Model:** Utilize an open-source LLM, specifically **Llama 3.1 (8B)**, running locally via **Ollama**.
3.  **Reasoning:** Implement a multi-step planning (ReAct) mechanism to intelligently process user health goals.
4.  **Tooling:** Integrate custom tools for:
    * Retrieving **diet and lifestyle tips** for common conditions (e.g., stress, hypertension).
    * **Mock scheduling** personalized preventive reminders (e.g., "Go for a walk at 18:30").
5.  **Evaluation:** Conduct a qualitative and quantitative evaluation of different prompt iterations, culminating in a **"Production-Ready" structured prompt**.

***

## 🚀 Key Features
### 🧠 ReAct Agent (Reason + Act)

* Multi-step reasoning using LangGraph’s ReAct architecture.
* Tools invoked through explicit function calls.

### 🛠️ Custom Tools

Defined in `src/tools.py`:

* `get_health_tips(condition)` – Returns diet & lifestyle tips for common conditions.
* `schedule_preventive_reminder(time, message)` – Schedules a mock reminder event.

### 💬 Production-Grade Prompt Engineering

* Four iterative prompt versions demonstrating reasoning improvements.
* Final prompt includes few-shot examples, argument validation, and strict schema enforcement.

### 📊 Quantitative Prompt Evaluation

Scored using a Judge LLM `(gemini-2.5-flash)` across relevance, accuracy, and adherence.

### 🧱 Open-Source Model Deployment

Runs fully locally using **Ollama + Llama 3.1 (8B)**.

***

## ⚙️ System Architecture & Workflow

The Copilot is built as a **ReAct Agent** using **LangGraph**. The agent follows these steps:

1.  **User Query:** Receives a natural language request (e.g., "Give me tips for better sleep and schedule a water break").
2.  **Agent Reasoning:** The Llama 3.1 agent, guided by the structured "Production-Ready" prompt, uses the ReAct pattern to **Think** (plan), **Act** (call a tool), and **Observe** (get tool output).
3.  **Tool Execution:** The agent calls the necessary functions defined in `src/tools.py` (e.g., `get_health_tips`, `schedule_reminder`).
4.  **Structured Output:** The agent generates a final, machine-readable JSON response summarizing the recommendations and scheduled actions for easy downstream integration.

***

## 🧪 Prompt Strategy, Evaluation & Outcomes

The core of this project was demonstrating that **iterative prompt engineering** is crucial for achieving reliable tool-use and structured output, especially with smaller, open-source models.

### Prompt Iterations

The development utilized multiple prompt versions, with the focus on moving from a simple baseline to a robust, tool-capable agent:

| Prompt Version | Description | Key Feature |
| :--- | :--- | :--- |
| **Prompt 1 & 2** | Baseline & Improved Reasoning | Focus on generating coherent text responses and basic instruction following. |
| **Prompt 3** | Function-Calling Integrated | First version to **reliably use tools** and return parsable output (ReAct implementation). |
| **Prompt 4 (Production-Ready)** | **Final Prompt** | Added explicit instructional examples (few-shot), argument validation rules, and strict enforcement of the exact function signatures required for application integration. |

### Evaluation Metrics & Scores

A custom Judge LLM (gemini-2.5-flash) was used to quantitatively score  all the prompt's performance across 5 evaluation queries.
The Evaluation rubrics is as follows:

 1. **Query Relevance**  How well the agent understood and addressed the user's primary health goal. 
 2. **Response Accuracy**  The factual correctness and helpfulness of the health tips provided. 
 3. **Prompt Adherence** The agent's ability to perfectly match the strict, complex output format defined in the prompt. 
 4. **Overall Score**  A weighted average assessing the total utility and quality of the response. 


#### Evaluation Summary Table

| Prompt Strategy               | Query Relevance (1-5) | Prompt Adherence (1-5) | Response Accuracy (1-5) | Overall Score (1-5) |
|-------------------------------|-----------------------|------------------------|-------------------------|---------------------|
| Baseline Prompt               | 2.8                   | 1.8                    | 2.0                     | 2.2                 |
| Improved Reasoning Prompt     | 3.6                   | 1.2                    | 2.6                     | 2.4                 |
| Structured ReAct Prompt       | 3.2                   | 1.0                    | 2.8                     | 2.2                 |
| Production-Ready ReAct Prompt | 4.4                   | 1.6                    | 2.6                     | 3.0                 |


### Key Outcomes and Trade-offs

* **Success:** The **Production-Ready** prompt achieved the highest **`Overall Score` (3.0)** and the best **`Query Relevance` (4.4)**, demonstrating its superior ability to address the user's problem and execute the multi-step plan.
* **Trade-off:** The agent scored lowest on **Prompt Adherence (1.6)** because smaller open-source models often struggle with strict output formats. While formatting was inconsistent, the high relevance score shows the model still performed strong reasoning and tool use.

***

## 💻 Setup and Execution

### 1. Prerequisites

You must have **Ollama** installed and running to serve the `llama3.1` model locally.

1.  **Install Ollama:** Follow the instructions on the [Ollama website](https://ollama.com/download).
2.  **Download Llama 3.1:** Run the following command in your terminal:
    ```bash
    ollama pull llama3.1
    ```

### 2. Project Installation

1.  **Clone the Repository:**
    ```bash
    git clone [repo-link]
    cd preventive-health-copilot
    ```
2.  **Create and Activate Virtual Environment:** (Recommended)
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
### 3. 📁 Project Structure

    
        preventive-health-copilot
        ├── 00_preventive_health_copilot.ipynb
        ├── requirements.txt
        ├── src/
        │   └── tools.py
        └── README.md
    

### 4. Running the Copilot

The entire development, iteration, and evaluation process is contained within the Jupyter Notebook.

* **Main Notebook:** `00_preventive_health_copilot.ipynb`
* **Tools:** Custom tool functions are defined in: `src/tools.py`

To run the project, ensure Ollama is serving `llama3.1` on `http://localhost:11434/v1`, and then open and run the cells in the Jupyter Notebook:

