import os
import pandas as pd


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

METRICS_PATH = os.path.join(
    BASE_DIR,
    "data",
    "airport_metrics.csv"
)


# ---------------------------------------------------------
# Tool 1: Airport Metrics
# ---------------------------------------------------------

def get_airport_metrics(airport_code):
    """
    Retrieve the latest operational metrics for an airport.
    """

    if not airport_code:
        return {
            "status": "error",
            "error": "airport_code is required"
        }

    airport_code = airport_code.upper().strip()

    try:
        df = pd.read_csv(METRICS_PATH)

        # Validate airport
        valid_airports = {"SFO", "LAX", "JFK"}

        if airport_code not in valid_airports:
            return {
                "status": "error",
                "error": f"Invalid airport code: {airport_code}"
            }

        airport_data = df[
            df["airport_code"] == airport_code
        ]

        if airport_data.empty:
            return {
                "status": "error",
                "error": f"No operational data found for {airport_code}"
            }

        # Get latest telemetry
        latest = airport_data.sort_values(
            "timestamp",
            ascending=False
        ).iloc[0]

        return {
            "status": "success",
            "airport_code": airport_code,
            "completion_rate": float(latest["completion_rate"]),
            "average_eta": float(latest["average_eta"]),
            "active_drivers": int(latest["active_drivers"]),
            "driver_cancellation_rate": float(
                latest["driver_cancellation_rate"]
            ),
            "queue_size": int(latest["queue_size"]),
            "surge_multiplier": float(latest["surge_multiplier"]),
            "timestamp": str(latest["timestamp"])
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Tool execution failed: {str(e)}"
        }


# ---------------------------------------------------------
# Tool 2: Driver Incentive Calculator
# ---------------------------------------------------------

def calculate_driver_incentive(driver_count, severity_level):
    """
    Calculate a mock recommended driver incentive.

    severity_level:
        1 = Low
        2 = Medium
        3 = High
    """

    if driver_count is None:
        return {
            "status": "error",
            "error": "driver_count is required"
        }

    if severity_level is None:
        return {
            "status": "error",
            "error": "severity_level is required"
        }

    try:
        driver_count = int(driver_count)
        severity_level = int(severity_level)

    except (ValueError, TypeError):
        return {
            "status": "error",
            "error": "driver_count and severity_level must be numeric"
        }

    if driver_count <= 0:
        return {
            "status": "error",
            "error": "driver_count must be greater than 0"
        }

    if severity_level not in {1, 2, 3}:
        return {
            "status": "error",
            "error": "severity_level must be 1, 2, or 3"
        }

    incentive_by_severity = {
        1: 5.0,
        2: 10.0,
        3: 20.0
    }

    incentive = incentive_by_severity[severity_level]

    total_cost = driver_count * incentive

    return {
        "status": "success",
        "driver_count": driver_count,
        "severity_level": severity_level,
        "recommended_incentive": incentive,
        "estimated_total_cost": total_cost,
        "currency": "USD"
    }


# ---------------------------------------------------------
# Tool 3: Surge Override
# ---------------------------------------------------------

def trigger_surge_override(
    airport_code,
    new_multiplier,
    reason
):
    """
    Mock surge override execution.

    Actual approval and guardrails will be implemented
    later in Day 4.
    """

    if not airport_code:
        return {
            "status": "error",
            "error": "airport_code is required"
        }

    if new_multiplier is None:
        return {
            "status": "error",
            "error": "new_multiplier is required"
        }

    if not reason:
        return {
            "status": "error",
            "error": "reason is required"
        }

    airport_code = airport_code.upper().strip()

    if airport_code not in {"SFO", "LAX", "JFK"}:
        return {
            "status": "error",
            "error": f"Invalid airport code: {airport_code}"
        }

    try:
        new_multiplier = float(new_multiplier)

    except (ValueError, TypeError):
        return {
            "status": "error",
            "error": "new_multiplier must be numeric"
        }

    if new_multiplier <= 0:
        return {
            "status": "error",
            "error": "new_multiplier must be greater than 0"
        }

    # Day 2 = mock execution only.
    # Policy guardrails and human approval are Day 4.

    return {
        "status": "success",
        "action": "surge_override",
        "airport_code": airport_code,
        "new_multiplier": new_multiplier,
        "reason": reason,
        "execution": "mock_success"
    }


# ---------------------------------------------------------
# Simple Manual Tests
# ---------------------------------------------------------

# ---------------------------------------------------------
# Error Handling Tests
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("DAY 2 ERROR HANDLING TESTS")
    print("=" * 60)

    # -----------------------------------------------------
    # 1. Invalid Airport Code
    # -----------------------------------------------------

    print("\n1. INVALID AIRPORT CODE")

    result = get_airport_metrics("ABC")

    print(result)


    # -----------------------------------------------------
    # 2. Missing Parameter
    # -----------------------------------------------------

    print("\n2. MISSING PARAMETER")

    result = get_airport_metrics(None)

    print(result)


    # -----------------------------------------------------
    # 3. Invalid Surge Multiplier
    # -----------------------------------------------------

    print("\n3. INVALID SURGE MULTIPLIER")

    result = trigger_surge_override(
        "SFO",
        -1,
        "Testing invalid multiplier"
    )

    print(result)


    # -----------------------------------------------------
    # 4. Tool Execution Failure
    # -----------------------------------------------------

    print("\n4. TOOL EXECUTION FAILURE")

    original_path = METRICS_PATH

    try:

        # Temporarily point to a non-existent file
        globals()["METRICS_PATH"] = "invalid/path/airport_metrics.csv"

        result = get_airport_metrics("SFO")

        print(result)

    finally:

        # Restore original path
        globals()["METRICS_PATH"] = original_path


    # -----------------------------------------------------
    # 5. Unexpected Tool Response
    # -----------------------------------------------------

    print("\n5. UNEXPECTED TOOL RESPONSE")

    try:

        result = calculate_driver_incentive(
            "invalid",
            3
        )

        # Validate that the tool returned a structured response
        if not isinstance(result, dict):
            raise ValueError("Unexpected tool response format")

        if "status" not in result:
            raise ValueError("Unexpected tool response: missing status")

        print(result)

    except Exception as e:

        print({
            "status": "error",
            "error": f"Unexpected tool response: {str(e)}"
        })


    print("\n" + "=" * 60)
    print("ERROR HANDLING TESTS COMPLETED")
    print("=" * 60)

