import json
import requests

from src.tools import (
    get_airport_metrics,
    calculate_driver_incentive,
    trigger_surge_override
)


OLLAMA_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "qwen3:8b"


# ---------------------------------------------------------
# Tool Definitions
# ---------------------------------------------------------

TOOLS = {
    "get_airport_metrics": get_airport_metrics,
    "calculate_driver_incentive": calculate_driver_incentive,
    "trigger_surge_override": trigger_surge_override
}


# ---------------------------------------------------------
# Ask LLM which tool to use
# ---------------------------------------------------------

def choose_tool(user_query):

    prompt = f"""
You are an airport operations assistant.

You have access to these tools:

1. get_airport_metrics
   Parameters:
   - airport_code

2. calculate_driver_incentive
   Parameters:
   - driver_count
   - severity_level

3. trigger_surge_override
   Parameters:
   - airport_code
   - new_multiplier
   - reason

Determine whether the user's request requires a tool.

Return ONLY valid JSON.

If a tool is required:
{{
    "tool": "tool_name",
    "arguments": {{
        "parameter": "value"
    }}
}}

If no tool is required:
{{
    "tool": null,
    "arguments": {{}}
}}

User request:
{user_query}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    result = response.json()["response"].strip()

    # Remove possible markdown fences
    result = result.replace("```json", "").replace("```", "").strip()

    return json.loads(result)


# ---------------------------------------------------------
# Execute Selected Tool
# ---------------------------------------------------------

def execute_tool(tool_name, arguments):

    if tool_name not in TOOLS:
        return {
            "status": "error",
            "error": f"Unknown tool: {tool_name}"
        }

    try:

        tool_function = TOOLS[tool_name]

        result = tool_function(**arguments)

        return result

    except Exception as e:

        return {
            "status": "error",
            "error": str(e)
        }


# ---------------------------------------------------------
# Complete Tool-Calling Workflow
# ---------------------------------------------------------

def run_tool_workflow(user_query):

    print("\nUSER:")
    print(user_query)

    decision = choose_tool(user_query)

    print("\nLLM TOOL DECISION:")
    print(decision)

    tool_name = decision.get("tool")
    arguments = decision.get("arguments", {})

    if tool_name is None:

        return {
            "status": "success",
            "message": "No operational tool required."
        }

    print("\nEXECUTING TOOL:")
    print(tool_name)

    result = execute_tool(
        tool_name,
        arguments
    )

    print("\nTOOL RESULT:")
    print(result)

    return result


# ---------------------------------------------------------
# Test
# ---------------------------------------------------------

if __name__ == "__main__":

    run_tool_workflow(
        "What's happening at SFO?"
    )
