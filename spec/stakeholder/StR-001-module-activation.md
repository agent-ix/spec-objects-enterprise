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

This need is considered satisfied when:

- A Module activation against filament-core registers the contents this module
  declares.
- Agent CLI generators (minijinja-cli) can produce valid artifacts using the
  templates and schemas this module ships.

## Dependencies

- **Upstream**: filament-core-service [FR-035](ix://agent-ix/filament-core-service/FR-035) (Module Manifest Schema).
