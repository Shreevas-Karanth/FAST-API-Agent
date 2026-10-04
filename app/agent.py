import json
from datetime import date
from pathlib import Path

import ollama


MODEL = "qwen3:4b"
TASKS_FILE = Path(__file__).resolve().parent.parent / "tasks.json"


def get_tasks(status: str = "ALL") -> str:
    """Return tasks, optionally filtered by status."""

    with TASKS_FILE.open("r", encoding="utf-8") as file:
        tasks = json.load(file)

    status = status.upper()

    if status != "ALL":
        tasks = [
            task for task in tasks
            if task["status"] == status
        ]

    return json.dumps(tasks)


def get_today() -> str:
    """Return today's date."""
    return date.today().isoformat()


TOOLS = [get_tasks, get_today]

AVAILABLE_TOOLS = {
    "get_tasks": get_tasks,
    "get_today": get_today,
}


def run_agent(user_input: str) -> str:
    """Run the agent and return its final answer."""

    messages = [
        {
            "role": "system",
            "content": """
You are a personal task assistant.

Use get_tasks to retrieve task information.
Use get_today when you need today's date.
Never invent tasks or their statuses.
Use tool results as the source of truth.
Answer clearly and concisely.
"""
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    for _ in range(5):
        response = ollama.chat(
            model=MODEL,
            messages=messages,
            tools=TOOLS
        )

        assistant_message = response.message

        messages.append(
            assistant_message.model_dump(exclude_none=True)
        )

        tool_calls = assistant_message.tool_calls or []

        if not tool_calls:
            return assistant_message.content or ""

        for tool_call in tool_calls:
            name = tool_call.function.name
            arguments = tool_call.function.arguments

            function = AVAILABLE_TOOLS.get(name)

            if function is None:
                result = f"Unknown tool: {name}"
            else:
                try:
                    result = function(**arguments)
                except Exception as exc:
                    result = f"Tool error: {exc}"

            messages.append({
                "role": "tool",
                "tool_name": name,
                "content": str(result)
            })

    return "The agent reached its tool-call limit."
