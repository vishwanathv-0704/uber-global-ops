import json
from datetime import datetime


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

VALID_AIRPORTS = {"SFO", "LAX", "JFK"}

MAX_SURGE = {
    "SFO": 1.5,
    "LAX": 1.6,
    "JFK": 1.6
}


# ---------------------------------------------------------
# Input Guardrails
# ---------------------------------------------------------

def validate_input(
    airport_code=None,
    surge_multiplier=None,
    driver_count=None,
    incentive_amount=None,
    severity_level=None
):
    """
    Validate operational action inputs.
    """

    errors = []

    if airport_code is not None:
        airport_code = airport_code.upper().strip()

        if airport_code not in VALID_AIRPORTS:
            errors.append(
                f"Invalid airport code: {airport_code}"
            )

    if surge_multiplier is not None:
        try:
            surge_multiplier = float(surge_multiplier)

            if surge_multiplier <= 0:
                errors.append(
                    "Surge multiplier must be greater than 0"
                )

            if surge_multiplier > 2.0:
                errors.append(
                    "Surge multiplier exceeds safety limit"
                )

        except (ValueError, TypeError):
            errors.append(
                "Surge multiplier must be numeric"
            )

    if driver_count is not None:
        try:
            driver_count = int(driver_count)

            if driver_count <= 0:
                errors.append(
                    "Driver count must be greater than 0"
                )

        except (ValueError, TypeError):
            errors.append(
                "Driver count must be numeric"
            )

    if incentive_amount is not None:
        try:
            incentive_amount = float(incentive_amount)

            if incentive_amount < 0:
                errors.append(
                    "Incentive amount cannot be negative"
                )

        except (ValueError, TypeError):
            errors.append(
                "Incentive amount must be numeric"
            )

    if severity_level is not None:
        try:
            severity_level = int(severity_level)

            if severity_level not in {1, 2, 3}:
                errors.append(
                    "Severity level must be 1, 2, or 3"
                )

        except (ValueError, TypeError):
            errors.append(
                "Severity level must be numeric"
            )

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


# ---------------------------------------------------------
# Risk Classification
# ---------------------------------------------------------

def classify_risk(action, target_multiplier=None):
    """
    Classify operational actions by risk.

    Project assumptions from Day 4 SOP:
    - Read metrics -> Low
    - Search policy -> Low
    - Calculate incentive -> Medium
    - Increase surge < 1.3x -> Medium
    - Increase surge >= 1.3x -> High
    - Incentive above threshold -> High
    """

    if action in {
        "read_metrics",
        "get_airport_metrics",
        "search_policy"
    }:
        return {
            "risk_level": "LOW",
            "approval_required": False
        }

    if action == "calculate_incentive":
        return {
            "risk_level": "MEDIUM",
            "approval_required": False
        }

    if action == "increase_surge":

        if target_multiplier is None:
            return {
                "risk_level": "HIGH",
                "approval_required": True
            }

        target_multiplier = float(target_multiplier)

        if target_multiplier < 1.3:
            return {
                "risk_level": "MEDIUM",
                "approval_required": True
            }

        return {
            "risk_level": "HIGH",
            "approval_required": True
        }

    if action == "driver_incentive":
        return {
            "risk_level": "HIGH",
            "approval_required": True
        }

    return {
        "risk_level": "HIGH",
        "approval_required": True
    }


# ---------------------------------------------------------
# Policy Guardrail
# ---------------------------------------------------------

def validate_policy(
    airport_code,
    action,
    target_multiplier=None,
    policy_max=None
):
    """
    Ensure proposed action does not violate policy.
    """

    airport_code = airport_code.upper().strip()

    if airport_code not in VALID_AIRPORTS:
        return {
            "allowed": False,
            "reason": "Invalid airport code"
        }

    if action == "increase_surge":

        if target_multiplier is None:
            return {
                "allowed": False,
                "reason": "Target surge multiplier is required"
            }

        target_multiplier = float(target_multiplier)

        maximum = policy_max or MAX_SURGE[airport_code]

        if target_multiplier > maximum:
            return {
                "allowed": False,
                "reason": (
                    f"Policy violation: maximum permitted "
                    f"surge at {airport_code} is {maximum}x"
                )
            }

    return {
        "allowed": True,
        "reason": "Action complies with configured policy limits"
    }


# ---------------------------------------------------------
# Human Approval
# ---------------------------------------------------------

def require_human_approval(risk_level, approval_required):
    """
    Determine whether human approval is required.
    """

    if risk_level == "HIGH" or approval_required:
        return {
            "required": True,
            "status": "PENDING"
        }

    return {
        "required": False,
        "status": "NOT_REQUIRED"
    }


# ---------------------------------------------------------
# Output Validation
# ---------------------------------------------------------

def validate_output(result):
    """
    Validate structured agent output before execution.
    """

    if not isinstance(result, dict):
        return {
            "valid": False,
            "error": "Agent output must be a dictionary"
        }

    required_fields = {
        "action",
        "risk_level",
        "approval_required"
    }

    missing = required_fields - set(result.keys())

    if missing:
        return {
            "valid": False,
            "error": f"Missing output fields: {list(missing)}"
        }

    return {
        "valid": True,
        "error": None
    }


# ---------------------------------------------------------
# Complete Guardrail Check
# ---------------------------------------------------------

def apply_guardrails(
    airport_code,
    action,
    target_multiplier=None,
    policy_max=None
):
    """
    Run the complete Day 4 guardrail pipeline.
    """

    # 1. Input validation
    input_check = validate_input(
        airport_code=airport_code,
        surge_multiplier=target_multiplier
    )

    if not input_check["valid"]:
        return {
            "status": "BLOCKED",
            "reason": "Input validation failed",
            "input_validation": input_check
        }

    # 2. Risk classification
    risk = classify_risk(
        action,
        target_multiplier
    )

    # 3. Policy validation
    policy = validate_policy(
        airport_code,
        action,
        target_multiplier,
        policy_max
    )

    if not policy["allowed"]:
        return {
            "status": "BLOCKED",
            "reason": policy["reason"],
            "risk": risk,
            "policy": policy
        }

    # 4. Human approval
    approval = require_human_approval(
        risk["risk_level"],
        risk["approval_required"]
    )

    return {
        "status": "APPROVAL_REQUIRED"
        if approval["required"]
        else "ALLOWED",
        "airport_code": airport_code,
        "action": action,
        "risk": risk,
        "policy": policy,
        "approval": approval
    }


# ---------------------------------------------------------
# Audit Trail
# ---------------------------------------------------------

def create_audit_record(
    user_request,
    agents_invoked,
    tools_called,
    retrieved_policies,
    recommendation,
    risk_level,
    approval_decision,
    final_action,
    execution_result
):
    """
    Create structured audit record.
    """

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "user_request": user_request,
        "agents_invoked": agents_invoked,
        "tools_called": tools_called,
        "retrieved_policies": retrieved_policies,
        "recommendation": recommendation,
        "risk_level": risk_level,
        "approval_decision": approval_decision,
        "final_action": final_action,
        "execution_result": execution_result
    }


# ---------------------------------------------------------
# Manual Tests
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("DAY 4 GUARDRAILS TEST")
    print("=" * 60)

    print("\n1. Valid input")
    print(
        validate_input(
            airport_code="SFO",
            surge_multiplier=1.5
        )
    )

    print("\n2. Invalid airport")
    print(
        validate_input(
            airport_code="UNKNOWN"
        )
    )

    print("\n3. Policy violation")
    print(
        apply_guardrails(
            airport_code="SFO",
            action="increase_surge",
            target_multiplier=2.0
        )
    )

    print("\n4. High-risk valid action")
    print(
        apply_guardrails(
            airport_code="SFO",
            action="increase_surge",
            target_multiplier=1.5
        )
    )

