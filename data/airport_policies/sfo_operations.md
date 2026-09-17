# SFO Airport Operations Policy

## Policy ID
SFO-OPS-001

## Airport
SFO – San Francisco International Airport

## Purpose
Define operational thresholds and procedures for monitoring ride marketplace performance at SFO.

## Scope
This policy applies to airport-originating ride operations monitored by the Airport Operations team.

## Operational Thresholds

| Metric | Expected Threshold | Alert Condition |
|---|---|---|
| Completion Rate | >85% | <85% |
| Average ETA | <15 minutes | >15 minutes |
| Driver Cancellation Rate | <15% | >15% |
| Queue Size | <150 drivers | >150 drivers |

## Anomaly Detection

An airport should be considered operationally degraded when one or more key metrics breach their alert threshold.

A severe operational issue should be considered when multiple metrics breach their thresholds simultaneously.

## Investigation Procedure

When an anomaly is detected:

1. Retrieve current airport telemetry.
2. Identify which metrics are outside their thresholds.
3. Investigate potential contributing factors.
4. Retrieve applicable airport policies.
5. Determine possible interventions.
6. Obtain approval when required.
7. Monitor the airport after intervention.

## Common Contributing Factors

Potential contributors to low completion rates include:

- High driver cancellation rate.
- Large driver queue.
- High average pickup ETA.
- Demand exceeding available supply.

## Queue Management

Drivers must remain in the designated airport queue system while waiting for eligible airport requests.

Drivers should not bypass the queue unless explicitly permitted by airport operations policy.

## Monitoring

Operational metrics should be reviewed before and after any major intervention.

## Audit Requirements

Operational investigations should record:

- Airport code
- Timestamp
- Metrics observed
- Detected anomaly
- Contributing factors
- Recommended action
- Final decision
