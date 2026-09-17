# SFO Airport Pricing Policy

## Policy ID
SFO-PRICING-001

## Airport
SFO – San Francisco International Airport

## Purpose
Define pricing and surge rules for rides originating from SFO airport during periods of demand and supply imbalance.

## Scope
This policy applies to airport-originating ride requests handled by the Airport Operations team.

## Surge Multiplier Rules

| Surge Range | Status | Approval |
|---|---|---|
| 1.0x – 1.2x | Permitted | No approval required |
| >1.2x – 1.5x | Permitted | Operations Manager approval required |
| >1.5x | Not permitted | Cannot be executed |

## Maximum Surge
The maximum permitted surge multiplier at SFO is **1.5x**.

The system must never execute a surge multiplier above 1.5x.

## Conditions for Increasing Surge

An increase in surge may be considered when one or more of the following conditions are observed:

- Completion rate falls below 85%.
- Request volume significantly exceeds available driver supply.
- Airport queue size increases substantially.
- Average pickup ETA exceeds the operational target.

Operational telemetry must be reviewed before recommending a surge increase.

## Approval Requirements

Any increase above 1.2x requires Operations Manager approval before execution.

An increase to 1.5x is classified as a high-impact operational action and requires explicit human approval.

## Prohibited Actions

The following actions are prohibited:

- Setting surge above 1.5x.
- Executing an unapproved surge increase above 1.2x.
- Bypassing the approval process through automated execution.
- Increasing surge without reviewing current operational conditions.

## Exceptions

No exception may override the maximum surge limit of 1.5x.

## Audit Requirements

Every approved surge override must record:

- Airport code
- Previous surge multiplier
- New surge multiplier
- Reason for change
- Approving authority
- Timestamp

## Policy Summary

SFO allows surge up to **1.5x**.  
Surge above **1.2x requires Operations Manager approval**.  
Surge above **1.5x is prohibited**.
