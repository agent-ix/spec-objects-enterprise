---
id: CAP-001
title: "OrderFulfillment"
type: capability
object: capability
---
<!-- capability authoring skeleton, alternate Properties form. Declares exactly
     the same fields as capability.md, authored as one ```sysml``` fence instead
     of the typed table (FR-005-AC-2). One artifact carries one form; the
     alternate is a separate file, never a second block in the same artifact. -->
# [CAP-001] OrderFulfillment

The Order Fulfillment capability is the organization's ability to take a placed
customer order and deliver the right goods to the right address within the
promised window.

## Properties

```sysml
attribute capability_id : UUID[1..1] { identity }
attribute name : String[1..1] { minLength: 1, maxLength: 120 }
attribute scope_statement : String[1..1] { minLength: 1 }
ref item realizing_function : SupplyChainManagement[0..*]
ref item governing_principle : PromiseFromLiveCapacity[0..*]
```

## Sub-capabilities

- **Order Orchestration** — sequences payment capture, inventory reservation
  and shipment creation across regional fulfillment centers.
- **Warehouse Operations** — pick, pack and ship execution inside each
  fulfillment center.
- **Carrier Management** — rate shopping, label generation and delivery-promise
  calculation across contracted carriers.
- **Returns Processing** — RMA intake, inbound inspection and
  restock-or-refurbish disposition.

## Invariants

The clauses the OrderFulfillment declaration enforces.

### EveryChildIsRealizedByAFunction

```ocl
context OrderFulfillment
inv EveryChildIsRealizedByAFunction:
  self.realizing_function->notEmpty()
```

### ScopeIsStated

```ocl
context OrderFulfillment
inv ScopeIsStated:
  self.scope_statement->notEmpty()
```
