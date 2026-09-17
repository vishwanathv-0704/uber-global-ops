# JFK Airport Operations Policy

## Policy ID
JFK-OPS-001

## Airport
JFK – John F. Kennedy International Airport

## Purpose
Define operational monitoring and investigation procedures for JFK airport.

## Operational Thresholds

| Metric | Expected Threshold | Alert Condition |
|---|---|---|
| Completion Rate | >83% | <83% |
| Average ETA | <17 minutes | >17 minutes |
| Driver Cancellation Rate | <16% | >16% |
| Queue Size | <160 drivers | >160 drivers |

## Operational Anomaly

An anomaly exists when one or more monitored metrics breach their defined threshold.

Multiple simultaneous threshold breaches should be treated as a higher-priority operational issue.

## Investigation Procedure

When an anomaly occurs:

1. Retrieve current JFK telemetry.
2. Identify degraded metrics.
3. Examine supply and demand conditions.
4. Retrieve relevant JFK policies.
5. Generate possible interventions.
6. Validate interventions against policy.
7. Obtain approval where required.
8. Monitor the result.

## Supply Issues

Potential causes of degraded completion rate include:

- Driver shortages
- High cancellation rates
- Large airport queue
- Increased pickup ETA
- High request volume

## Pickup Operations

Drivers must use designated JFK pickup areas.

Operations should monitor pickup congestion when average ETA increases significantly.

## Monitoring
Metrics should be reviewed before and after operational interventions.

## Audit Requirements

The investigation record should include airport, timestamp, metrics, anomaly, contributing factors, recommendation, approval status, and final action.

