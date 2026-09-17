# LAX Airport Operations Policy

## Policy ID
LAX-OPS-001

## Airport
LAX – Los Angeles International Airport

## Purpose
Define operational thresholds for monitoring ride marketplace performance at LAX.

## Operational Thresholds

| Metric | Expected Threshold | Alert Condition |
|---|---|---|
| Completion Rate | >87% | <87% |
| Average ETA | <16 minutes | >16 minutes |
| Driver Cancellation Rate | <14% | >14% |
| Queue Size | <170 drivers | >170 drivers |

## Operational Anomaly

An operational anomaly exists when a monitored metric breaches its alert threshold.

A severe issue should be investigated when multiple key metrics breach their thresholds simultaneously.

## Investigation Procedure

Operations teams should:

1. Retrieve current LAX telemetry.
2. Identify degraded metrics.
3. Investigate supply and demand conditions.
4. Retrieve applicable LAX policies.
5. Evaluate possible interventions.
6. Apply required approval controls.
7. Monitor the outcome.

## Pickup Operations

Drivers must use designated airport pickup zones.

Drivers should not collect passengers from unauthorized curbside locations.

## Supply Management

When available driver supply is insufficient, operations may consider driver incentives or other permitted interventions.

## Monitoring

Operational metrics should be monitored before and after interventions.

## Audit Requirements

Investigations should record the airport, timestamp, observed metrics, identified issue, recommendation, and final action.

