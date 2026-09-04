---
id: OBJ-001
title: "HalveOrderToShipTime"
type: objective
object: objective
metric: "Median order-to-ship time across all fulfillment centers (hours)"
target: "12 hours or less"
deadline: "2026-12-31"
---
<!-- objective authoring skeleton (spec-objects-enterprise). Contract (manifest
     body_extraction asserts):
     - Frontmatter MUST carry id, title, type: objective, object: objective,
       plus the prose fields `metric` and `target`; `deadline` is optional but
       strongly recommended. Those three strings are the 0.1.0 human-facing
       form and are kept unchanged; the typed record below is the authority.
     - "Properties" (H2): typed rows carrying one `identity` row and one
       `Timestamp` row — an objective is time-bound, and Objective.json
       requires that horizon.
     - "Invariants" (H2): at least one clause — Objective.json requires
       `clauses`.
     An objective references a measure definition (a `kpi`) through its
     `targets`; it never declares one, and Objective.json admits no `measure`.
     It also performs nothing: `operations` is forbidden. -->
# [OBJ-001] HalveOrderToShipTime

Customers who receive a same-day ship confirmation reorder at twice the rate of
those who wait more than a day, yet our median order-to-ship time sits at 24
hours. This objective commits the Fulfillment Platform group to bringing the
median down to 12 hours or less across all fulfillment centers by the end of
2026, primarily by moving to event-driven orchestration and adding a second
daily carrier pickup at the two highest-volume centers.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| objective_id | UUID | 1..1 | identity |
| horizon | Timestamp | 1..1 | |
| baseline_hours | Integer [h] | 1..1 | min: 0 |
| target_hours | Integer [h] | 1..1 | min: 0 |
| measured_by | OnTimeDeliveryRate | 0..* | |

## Invariants

The commitments the HalveOrderToShipTime declaration asserts.

### TargetImprovesOnBaseline

```ocl
context HalveOrderToShipTime
inv TargetImprovesOnBaseline:
  self.target_hours < self.baseline_hours
```

### HorizonIsDeclared

```ocl
context HalveOrderToShipTime
inv HorizonIsDeclared:
  self.horizon->notEmpty()
```
