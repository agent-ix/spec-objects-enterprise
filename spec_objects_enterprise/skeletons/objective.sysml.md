---
id: OBJ-001
title: "HalveOrderToShipTime"
type: objective
object: objective
metric: "Median order-to-ship time across all fulfillment centers (hours)"
target: "12 hours or less"
deadline: "2026-12-31"
---
<!-- objective authoring skeleton, alternate Properties form. Declares exactly
     the same fields as objective.md, authored as one ```sysml``` fence instead
     of the typed table (FR-005-AC-2). -->
# [OBJ-001] HalveOrderToShipTime

This objective commits the Fulfillment Platform group to bringing the median
order-to-ship time down to 12 hours or less across all fulfillment centers by
the end of 2026.

## Properties

```sysml
attribute objective_id : UUID[1..1] { identity }
attribute horizon : Timestamp[1..1]
attribute baseline_hours : Integer [h][1..1] { min: 0 }
attribute target_hours : Integer [h][1..1] { min: 0 }
ref item measured_by : OnTimeDeliveryRate[0..* unique]
```

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
