---
id: DEC-001
title: "AdoptEventDrivenOrchestration"
type: decision
object: decision
---
<!-- decision authoring skeleton (spec-objects-enterprise). Contract (manifest
     body_extraction asserts):
     - Frontmatter MUST carry id, title, type: decision, object: decision.
     - "Properties" (H2, optional for the schema): typed rows describing the
       decision record itself.
     - "Decision" (H2, required): the decision taken, its scope and the
       alternatives it supersedes (no TODO/TBD/placeholder text).
     - "Invariants" (H2): at least one clause — Decision.json requires
       `clauses`, because the commitment taken is an asserted clause and not
       prose.
     A decision performs nothing: Decision.json forbids `operations`. -->
# [DEC-001] AdoptEventDrivenOrchestration

## Properties

| Field | Type | Multiplicity | Constraints |
|---|---|---|---|
| decision_id | UUID | 1..1 | identity |
| status | String | 1..1 | enumValues: proposed\|accepted\|superseded |
| constrained_capability | OrderFulfillment | 0..* unique | |

## Decision

The Fulfillment Platform group will orchestrate order fulfillment through an
event-driven saga over the order event bus, replacing the synchronous
point-to-point calls between checkout, inventory and the warehouse management
system. Each fulfillment step publishes a completion event and registers a
compensating action, so a failed shipment creation releases its inventory
reservation automatically instead of requiring the nightly reconciliation job.
The decision applies to all regional fulfillment centers; the legacy
synchronous path is retired once the final region migrates. The alternative of
scaling the existing orchestrator with retries was rejected because it could
not meet the peak-season throughput target without over-provisioning the
warehouse management system.

## Invariants

The commitments the AdoptEventDrivenOrchestration declaration asserts.

### EveryStepRegistersACompensation

```ocl
context AdoptEventDrivenOrchestration
inv EveryStepRegistersACompensation:
  self.status <> 'superseded' implies self.constrained_capability->notEmpty()
```

### NoSynchronousPathSurvivesMigration

```ocl
context AdoptEventDrivenOrchestration
inv NoSynchronousPathSurvivesMigration:
  self.status = 'accepted' implies self.decision_id->notEmpty()
```
