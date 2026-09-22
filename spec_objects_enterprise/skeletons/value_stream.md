---
id: VS-001
title: "OrderToDelivery"
type: value_stream
object: value_stream
---
<!-- value_stream authoring skeleton (spec-objects-enterprise). Contract
     (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: value_stream,
       object: value_stream.
     - "Properties" (H2): typed rows with one `identity` row.
     - "Stages" (H2, required): the stages in order with the value each adds
       (no TODO/TBD/placeholder text).
     - "Invariants" (H2): at least one clause — ValueStream.json requires
       `clauses`, because a value stream exists to make an end-to-end guarantee.
     A value stream performs nothing of its own: ValueStream.json forbids
     `operations`; the business functions inside it carry those. -->
# [VS-001] OrderToDelivery

The Order to Delivery value stream traces a customer order from checkout
confirmation to doorstep delivery. Its triggering stakeholder is the storefront
customer; the value received is the ordered goods arriving within the promised
delivery window.

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| stream_id | UUID | 1..1 | identity |
| triggering_stakeholder | String | 1..1 | minLength: 1 |
| value_received | String | 1..1 | minLength: 1 |
| stage_count | Integer | 1..1 | min: 2 |
| contained_function | SupplyChainManagement | 0..* unique | |

## Stages

1. **Order Capture** — checkout confirms payment authorization and records the
   delivery promise shown to the customer.
2. **Fulfillment Planning** — the order is sourced to a fulfillment center and
   inventory is hard-reserved against the promise date.
3. **Pick and Pack** — warehouse staff pick the items, pack them and apply the
   carrier label produced by rate shopping.
4. **Carrier Handoff** — packages are manifested and tendered to the selected
   carrier at the scheduled pickup.
5. **In-Transit Tracking** — carrier scans update the customer-facing tracking
   page and feed the delivery-promise model.
6. **Delivery Confirmation** — proof of delivery closes the order and starts
   the returns-eligibility clock.

## Invariants

The end-to-end guarantees the OrderToDelivery declaration makes.

### StageOrderIsContiguous

```ocl
context OrderToDelivery
inv StageOrderIsContiguous:
  self.stage_count >= 2
```

### ValueReachesTheTriggeringStakeholder

```ocl
context OrderToDelivery
inv ValueReachesTheTriggeringStakeholder:
  self.value_received->notEmpty() and self.triggering_stakeholder->notEmpty()
```
