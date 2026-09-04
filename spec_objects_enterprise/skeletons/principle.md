---
id: PRIN-001
title: "PromiseFromLiveCapacity"
type: principle
object: principle
---
<!-- principle authoring skeleton (spec-objects-enterprise). Contract (manifest
     body_extraction asserts):
     - Frontmatter MUST carry id, title, type: principle, object: principle.
     - "Rationale" (H2, required): the justification and its implications
       (no TODO/TBD/placeholder text).
     - "Invariants" (H2): at least one clause — Principle.json requires
       `clauses`.
     A principle declares a rule, not data and not behaviour: Principle.json
     forbids `fields` and `operations`, so this skeleton carries no
     "Properties" section. -->
# [PRIN-001] PromiseFromLiveCapacity

Every delivery promise shown to a customer must be computed from live
fulfillment-network capacity — current inventory positions, warehouse cut-off
times and carrier pickup schedules — never from a static service-level table.

## Rationale

Missed delivery promises are the single largest driver of fulfillment-related
support contacts and refund concessions, and static promise tables drift from
reality every peak season. Computing promises from live network state keeps the
storefront honest at the moment of checkout: when a fulfillment center falls
behind, promises lengthen automatically instead of being broken silently. The
implication is that every system in the OrderToDelivery value stream must
publish its capacity and cut-off signals to the promise engine, and any new
fulfillment integration is not production-ready until it does.

## Invariants

The rules the PromiseFromLiveCapacity declaration governs by.

### PromiseIsComputedFromLiveCapacity

```ocl
context PromiseFromLiveCapacity
inv PromiseIsComputedFromLiveCapacity:
  DeliveryPromise.allInstances()->forAll(p | p.source = CapacitySignal)
```

### NoStaticServiceLevelTable

```ocl
context PromiseFromLiveCapacity
inv NoStaticServiceLevelTable:
  DeliveryPromise.allInstances()->forAll(p | p.source <> StaticTable)
```
