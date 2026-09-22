---
id: KPI-001
title: "OnTimeDeliveryRate"
type: kpi
object: kpi
metric: "Orders delivered within the promised window (% of delivered orders)"
target: "97% or higher, measured weekly"
threshold: "Alert below 95% for two consecutive weeks"
---
<!-- kpi authoring skeleton, alternate Properties form. Declares exactly the
     same fields as kpi.md, authored as one ```sysml``` fence instead of the
     typed table (FR-005-AC-2). The unit travels with the type in both forms,
     which is what makes the measure-definition rule expressible either way. -->
# [KPI-001] OnTimeDeliveryRate

On-time delivery rate measures the share of delivered orders whose proof of
delivery falls within the delivery window promised at checkout.

## Properties

```sysml
attribute delivered_within_promise : Decimal(5,2) [%][1..1] { min: 0, max: 100 }
attribute delivered_order_count : Integer [1][1..1] { min: 0 }
attribute evaluation_window : Duration [d][1..1]
ref item measured_capability : OrderFulfillment[0..* unique]
```

## Invariants

The rules the OnTimeDeliveryRate definition carries.

### RateIsAProportion

```ocl
context OnTimeDeliveryRate
inv RateIsAProportion:
  self.delivered_within_promise >= 0 and self.delivered_within_promise <= 100
```

### WindowIsPositive

```ocl
context OnTimeDeliveryRate
inv WindowIsPositive:
  self.evaluation_window > 0
```
