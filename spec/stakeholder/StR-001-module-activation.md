---
id: StR-001
title: "Tier-2 enterprise architecture"
type: StR
---
# StR-001: Tier-2 enterprise architecture

## Stakeholder Need

The Filament platform, spec authors, and agent CLI generators require that
enterprise architecture specifications shall yield extractable graph entities for
capabilities, business functions, value streams, decisions, objectives, principles,
and KPIs, so that tier-2 enterprise architecture can be authored and consumed as
first-class graph objects.

## Rationale

Enterprise architecture content today is unstructured prose that cannot be linked,
queried, or generated as a graph. Spec authors and agent generators need these
concepts modelled as activatable archetypes and object-types so that a Module
activation registers them in filament-core and downstream tooling can treat them as
extractable entities rather than free text.

## Validation Criteria


| ID | Criteria | Validation |
|----|----------|------------|
| StR-001-VC-1 | A Module activation against filament-core registers the contents this module declares. | Inspection |
| StR-001-VC-2 | Agent CLI generators (minijinja-cli) can produce valid artifacts using the templates and schemas this module ships. | Demonstration |
| StR-001-VC-3 | Every enterprise object type carries one typed structural contract that the downstream frontends (`agent-ix/quire-contract-ir#52`, `agent-ix/filament-core-data#36`) can consume read-only, so a capability and a KPI are distinguishable to a consumer without reading the prose, and a KPI definition is distinguishable from a reading of it. | Demonstration |

## Dependencies

- **Upstream**: filament-core-service [FR-035](ix://agent-ix/filament-core-service/FR-035) (Module Manifest Schema).
