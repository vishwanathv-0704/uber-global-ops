# LAX Airport Pricing Policy

## Policy ID
LAX-PRICING-001

## Airport
LAX – Los Angeles International Airport

## Purpose
Define pricing and surge rules for LAX airport operations.

## Surge Multiplier Rules

| Surge Range | Status | Approval |
|---|---|---|
| 1.0x – 1.1x | Permitted | No approval required |
| >1.1x – 1.4x | Permitted | Operations Manager approval required |
| >1.4x | Not permitted | Cannot be executed |

## Maximum Surge

The maximum permitted surge multiplier at LAX is **1.4x**.

The system must never execute a surge multiplier above 1.4x.

## Conditions for Increasing Surge

A surge increase may be considered when:

- Completion rate falls below 87%.
- Request volume exceeds available driver supply.
- Queue size exceeds the operational threshold.
- Average ETA exceeds the operational threshold.

Current operational telemetry must be reviewed before recommending an increase.

## Approval Requirements

Any increase above 1.1x requires Operations Manager approval.

An increase to 1.4x is considered a high-impact action and requires explicit human approval.

## Prohibited Actions

The following are prohibited:

- Increasing surge above 1.4x.
- Executing an unapproved increase above 1.1x.
- Bypassing the approval process.
- Increasing surge without reviewing current operational conditions.

## Audit Requirements

Every surge override must record:

- Airport code
- Previous multiplier
- New multiplier
- Reason
- Approving authority
- Timestamp

## Policy Summary

LAX permits surge up to **1.4x**.

Surge above **1.1x requires Operations Manager approval**.

Surge above **1.4x is prohibited**.
