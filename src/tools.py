from langchain_core.tools import tool
from datetime import datetime, date

# ============================
#   TOOL: HEALTH TIPS
# ============================


@tool
def get_health_tips(condition: str) -> str:
    """Return preventive health tips for a given health condition.

    Input:
        condition (str): A short condition name such as 
                         "stress", "diabetes", or "hypertension".
                         Case-insensitive.

    Output:
        A formatted bullet list of preventive tips.
        If the condition is unknown, returns a message like:
        "No tips found for: <condition>"

    This tool should be called ONLY when the user is explicitly asking 
    for preventive advice tied to a specific condition name."""


    condition = condition.lower().strip()
    tips = {
        "stress": [
            "Take deep breathing breaks",
            "Walk 15 minutes outdoors",
            "Sleep 7–9 hours"
        ],
        "diabetes": [
            "Reduce refined carbs",
            "Increase fiber in each meal",
            "Walk after meals"
        ],
        "hypertension": [
            "Lower sodium intake",
            "Do 150 min aerobic activity weekly",
            "Increase potassium-rich foods"
        ],
    }.get(condition, [])

    if not tips:
        return f"No tips found for: {condition}"

    return "\n".join(f"- {t}" for t in tips)


# ============================
#   TOOL: SCHEDULE REMINDER
# ============================

@tool
def schedule_preventive_reminder(input: str) -> str:
    """
     Schedule a preventive health reminder at a specific datetime.

    Expected input format:
        "ISO_DATETIME || reminder message"

    Example:
        "2025-01-01T08:00:00 || Morning walk"

    The datetime MUST follow ISO 8601 format:
        YYYY-MM-DDTHH:MM:SS

    The tool validates the datetime and returns:
        "Reminder scheduled at <ISO_DATETIME> with message: '<message>'"

    Use this tool when the user wants something scheduled at a 
    specific time rather than relative durations (e.g., “in 2 hours”).
    """
    if "||" not in input:
        return "Invalid format. Use 'ISO_TIME || message'."

    time_iso, message = [x.strip() for x in input.split("||", 1)]

    try:
        datetime.fromisoformat(time_iso)
    except Exception:
        return "Invalid ISO time format."

    return f"Reminder scheduled at {time_iso} with message: '{message}'"

 