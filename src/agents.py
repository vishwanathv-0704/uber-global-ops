import os
import json
import requests

from src.tools import (
    get_airport_metrics,
    calculate_driver_incentive,
    trigger_surge_override
)

from src.rag_pipeline import retrieve_documents
from src.memory import ConversationMemory


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

OLLAMA_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "qwen3:8b"

MAX_ITERATIONS = 5


# ---------------------------------------------------------
# LLM Helper
# ---------------------------------------------------------

def call_llm(prompt):
    """
    Send a prompt to the local Ollama model.
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False,
            "think":False,
            "options":{
            "temperature":0.1,
            "num_predict":600
            }
        },
        timeout=300
    )

    response.raise_for_status()

    return response.json()["response"]


# ---------------------------------------------------------
# Operations Investigator Agent
# ---------------------------------------------------------

def operations_investigator(airport_code):
    """
    Investigate airport operational conditions.

    Uses operational telemetry tools to identify
    anomalies and contributing factors.
    """

    metrics = get_airport_metrics(airport_code)

    if metrics["status"] != "success":
        return metrics

    completion_rate = metrics["completion_rate"]

    # Day 3 operational threshold from the project scenario
    expected_threshold = 85.0

    if completion_rate < expected_threshold:
        status = "ANOMALY"
    else:
        status = "NORMAL"

    return {
        "agent": "operations_investigator",
        "status": "success",
        "airport_code": airport_code,
        "completion_rate": completion_rate,
        "expected_threshold": expected_threshold,
        "operational_status": status,
        "average_eta": metrics["average_eta"],
        "active_drivers": metrics["active_drivers"],
        "driver_cancellation_rate": metrics[
            "driver_cancellation_rate"
        ],
        "queue_size": metrics["queue_size"],
        "surge_multiplier": metrics["surge_multiplier"],
        "timestamp": metrics["timestamp"]
    }
    
    
    # ---------------------------------------------------------
# Resolution Agent
# ---------------------------------------------------------

def resolution_agent(operational_data, policy_data=None):
    """
    Evaluate an operational issue and generate
    possible resolution actions.
    """

    if not operational_data:
        return {
            "agent": "resolution_agent",
            "status": "error",
            "error": "Operational data is required"
        }

    if operational_data.get("status") != "success":
        return {
            "agent": "resolution_agent",
            "status": "error",
            "error": "Invalid operational data"
        }

    airport_code = operational_data["airport_code"]
    completion_rate = operational_data["completion_rate"]
    surge_multiplier = operational_data["surge_multiplier"]
    cancellation_rate = operational_data["driver_cancellation_rate"]
    queue_size = operational_data["queue_size"]
    average_eta = operational_data["average_eta"]

    recommendations = []

    # Identify severity
    if completion_rate < 70:
        severity = 3
    elif completion_rate < 80:
        severity = 2
    elif completion_rate < 85:
        severity = 1
    else:
        severity = 0

    # Generate possible interventions
    if severity > 0:

        if surge_multiplier < 1.5:
            recommendations.append({
                "action": "increase_surge",
                "target_multiplier": min(
                    surge_multiplier + 0.3,
                    1.5
                ),
                "reason": "Low completion rate and supply-demand imbalance"
            })

        if cancellation_rate > 10:
            recommendations.append({
                "action": "driver_incentive",
                "reason": "Elevated driver cancellation rate"
            })

        if queue_size > 100:
            recommendations.append({
                "action": "increase_driver_supply",
                "reason": "Large airport queue"
            })

        if average_eta > 15:
            recommendations.append({
                "action": "reduce_wait_time",
                "reason": "Elevated average ETA"
            })

    if severity == 0:
        recommendations.append({
            "action": "monitor",
            "reason": "Operational metrics are within expected range"
        })

    return {
        "agent": "resolution_agent",
        "status": "success",
        "airport_code": airport_code,
        "severity_level": severity,
        "recommendations": recommendations,
        "policy_review_required": len(recommendations) > 0,
        "policy_data": policy_data
    }
    
    
# ---------------------------------------------------------
# Policy Compliance Agent
# ---------------------------------------------------------
def policy_compliance_agent(airport_code, recommendations):
    """
    Validate all proposed actions against airport policy.

    Performs ONE RAG + LLM call for the complete set of
    recommendations instead of calling the LLM separately
    for every action.
    """

    if not recommendations:
        return {
            "agent": "policy_compliance",
            "status": "success",
            "airport_code": airport_code,
            "policy_checks": []
        }

    # Combine all recommendations into ONE policy question
    actions_text = "\n".join(
        f"{i + 1}. {rec.get('action', '')}: "
        f"{rec.get('reason', '')}"
        for i, rec in enumerate(recommendations)
    )

    query = f"""
You are a policy compliance agent for airport operations.

Airport: {airport_code}

Proposed operational actions:

{actions_text}

Retrieve the relevant airport policies and evaluate ALL
proposed actions against those policies.

For each action determine:
- whether it is allowed
- whether human approval is required
- relevant policy/source
- short explanation

Return a concise structured JSON object.
"""

    try:
        # ONE RAG retrieval
        policy_context = retrieve_documents(query)

        # ONE LLM call
        prompt = f"""
{query}

Retrieved policy information:
{policy_context}

Return JSON only in this format:

{{
    "airport_code": "{airport_code}",
    "checks": [
        {{
            "action": "action name",
            "allowed": true,
            "approval_required": true,
            "policy": "relevant policy",
            "reason": "short explanation"
        }}
    ]
}}
"""

        response = call_llm(prompt)

        # Parse JSON returned by Qwen
        result = json.loads(response)

        return {
            "agent": "policy_compliance",
            "status": "success",
            "airport_code": airport_code,
            "policy_checks": result.get("checks", [])
        }

    except Exception as e:
        return {
            "agent": "policy_compliance",
            "status": "error",
            "error": f"Policy analysis failed: {str(e)}"
        }

    
# ---------------------------------------------------------
# Orchestrator Agent
# ---------------------------------------------------------


def orchestrator(airport_code):
    """
    Coordinate the multi-agent operational workflow.

    Flow:
        Operations Investigator
                ↓
        Resolution Agent
                ↓
        Policy Compliance Agent
                ↓
        Final Recommendation
    """

    # Step 1: Investigate
    operational_data = operations_investigator(airport_code)

    if operational_data.get("status") != "success":
        return {
            "agent": "orchestrator",
            "status": "error",
            "error": operational_data.get(
                "error",
                "Operations investigation failed"
            )
        }

    # Step 2: Generate resolutions
    resolution_data = resolution_agent(operational_data)

    if resolution_data.get("status") != "success":
        return {
            "agent": "orchestrator",
            "status": "error",
            "error": resolution_data.get(
                "error",
                "Resolution analysis failed"
            )
        }

    recommendations = resolution_data.get(
        "recommendations",
        []
    )

    # Step 3: ONE policy check for ALL recommendations
    policy_result = policy_compliance_agent(
        airport_code,
        recommendations
    )

    # Step 4: Final result
    return {
        "agent": "orchestrator",
        "status": "success",
        "airport_code": airport_code,
        "operational_analysis": operational_data,
        "resolution_analysis": resolution_data,
        "policy_checks": policy_result
    }
