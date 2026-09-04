---
id: BF-001
title: "SupplyChainManagement"
type: business_function
object: business_function
---
<!-- business_function authoring skeleton (spec-objects-enterprise). Contract
     (manifest body_extraction asserts):
     - Frontmatter MUST carry id, title, type: business_function,
       object: business_function.
     - "Properties" (H2): typed rows, header exactly
       `Field | Type | Multiplicity | Constraints`, with one `identity` row.
     - "Description" (H2, required): what the function does, who performs it
       and which capabilities it supports (no TODO/TBD/placeholder text).
     - "Operations" (H2): one `### <name>` per operation, an optional
       `| Param | Type | Multiplicity | Constraints |` table, a `Returns:` line
       where the operation returns a value, and optional `Pre:`/`Post:` lines
       naming clause ids declared in this artifact.
     - "Invariants" (H2): one `### <clauseId>` per clause with one ```ocl```
       fence.
     A function is defined by what it performs: BusinessFunction.json requires
     at least one operation. -->
# [BF-001] SupplyChainManagement

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| function_id | UUID | 1..1 | identity |
| name | String | 1..1 | minLength: 1, maxLength: 120 |
| planning_cycle | Duration [d] | 1..1 | |
| supported_capability | OrderFulfillment | 0..* | |

## Description

Supply Chain Management is the organizational function responsible for keeping
sellable inventory available at the lowest landed cost. The function is staffed
by the Planning and Procurement teams and reports to the COO. It owns demand
forecasting, replenishment purchasing, supplier scorecards and inbound
logistics scheduling, and it supplies the inventory positions that the
OrderFulfillment capability reserves against. Its primary cadences are a weekly
S&OP review and a daily replenishment run per fulfillment center.

## Operations

The operations the SupplyChainManagement declaration exposes. Each operation
owns one `### <name>` heading with an optional parameter table, a `Returns:`
line where it returns a value, and `Pre:`/`Post:` lines where it names clauses
declared in this artifact.

### forecast_demand

Produce the demand forecast for one fulfillment center over the planning
horizon, from shipment history and the open promise book.

| Param | Type | Multiplicity | Constraints |
|---|---|---|---|
| center_id | UUID | 1..1 | |
| horizon | Duration [d] | 1..1 | |

Returns: JsonObject[1..1]

Pre: PlanningCycleIsPositive

### replenish

Raise replenishment purchase orders for every SKU whose projected position
falls below its safety stock inside the planning cycle.

| Param | Type | Multiplicity | Constraints |
|---|---|---|---|
| center_id | UUID | 1..1 | |

Returns: Integer[1..1]

Post: EveryFunctionSupportsACapability

### score_supplier

Recompute a supplier's on-time-in-full performance for the trailing quarter and
publish it to the sourcing rules.

| Param | Type | Multiplicity | Constraints |
|---|---|---|---|
| supplier_id | UUID | 1..1 | |

Returns: Decimal(5,2)[1..1]

## Invariants

The clauses the SupplyChainManagement declaration enforces.

### PlanningCycleIsPositive

```ocl
context SupplyChainManagement
inv PlanningCycleIsPositive:
  self.planning_cycle > 0
```

### EveryFunctionSupportsACapability

```ocl
context SupplyChainManagement
inv EveryFunctionSupportsACapability:
  self.supported_capability->notEmpty()
```
