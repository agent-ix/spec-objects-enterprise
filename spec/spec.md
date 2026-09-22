---
type: master-requirements
name: spec-objects-enterprise
org: agent-ix
component_type: filament-module
implementation_language: python
tags:
  - filament
  - spec-objects
  - enterprise
depends_on: []
standards_alignment:
  - iso-iec-ieee-29148
relationships:
  - target: "ix://agent-ix/filament-core-service/FR-035"
    type: "depends_on"
    cardinality: "1:1"
  - target: "ix://agent-ix/filament-core-data/FR-031"
    type: "depends_on"
    cardinality: "1:1"
  - target: "ix://agent-ix/quoin/FR-070"
    type: "depends_on"
    cardinality: "1:1"
  - target: "ix://agent-ix/quire-rs/FR-069"
    type: "depends_on"
    cardinality: "1:1"
security_critical: false
---
# Master Requirements Specification

## Purpose

This document specifies the requirements for the `spec-objects-enterprise`
Filament Module. Enterprise architecture specs need extractable graph entities
for capabilities, business functions, value streams, decisions, objectives,
principles, and KPIs; this module contributes the tier-2 ObjectTypes, templates,
and schemas that make those entities extractable, so that implementers,
reviewers, and downstream consumers share one authoritative definition of what
the module delivers.

## Scope

### In Scope

- The seven tier-2 ObjectTypes this module contributes for enterprise
  architecture modeling: capability, business_function, value_stream, decision,
  objective, principle, and kpi.
- The Module manifest (`spec_objects_enterprise/manifest.yaml`) and its
  activation against filament-core-service.
- The semantic-module contract (issue #4): a TypeSpec source importing
  `@agent-ix/semantic-core` 0.3.0, the emitted JSON Schema per declared model
  shipped under `spec_objects_enterprise/schemas/`, the manifest `semantic`
  block with reference-form `data_schema`, and the skeletons rewritten as
  executable typed fixtures with negative counterparts.
- The definition / measurement boundary: a KPI declaration is a measure
  definition, and the schema refuses a record shaped like an observation of it.
- The advisory posture the ticket's merge gate requires: the module ships at
  `compatibility_posture: additive` with `legacy_forms: warning`, so no
  existing artifact becomes an error and the contract is advisory until
  corpus promotion (`agent-ix/quoin#291`) turns it into a gate.

### Out of Scope

- The activation and registry behaviour owned by filament-core-service,
  referenced here only by relationship to FR-035.
- Deployment topology and infrastructure, which live in the operating
  environment rather than this specification.
- Measurement, observation, and time-series storage of a KPI: this module types
  the *definition* only. The verification and measurement semantic types the
  ticket's Dependencies name are not declared here, and no key naming a
  measured value, sample, score, or rating is introduced (FR-004-CON-3).
- Any organizational role vocabulary beyond `OwnershipDecl`'s `owner` and
  `steward` references: the ticket's safety gate makes a role change conditional
  on evidence from the corpus review, which this module does not perform.
- Generated-language fixtures (Rust, TypeScript, Python) for the enterprise
  types: produced by the TypeSpec frontend and compiler core
  (`agent-ix/filament-core-data#21`, `#22`, `#23`) and published only behind the
  promotion gate (`agent-ix/quoin#290`); the semantic-core language packages are
  `agent-ix/filament-core-data#11`. None is produced or faked here.
- Extraction of the declared-but-not-yet-extracted keys (`relations`, `scope`,
  `outcomes`, `inputs`, `outputs`, `stages`, `alternatives`, `targets`,
  `measure`, `thresholds`, `owner`, `lifecycle`, `provenance`) from Markdown:
  the mapping is owned by `agent-ix/quoin#335` (FR-071/FR-072 define
  `Properties`, `Invariants`, and `Operations` only) and the extractor by
  `agent-ix/quire-rs` once the mapping is published; the schemas declare the
  keys as optional so the engine can fill them without a schema change.
- Naming what a module load refused: `agent-ix/quire-rs#221` (an unknown
  manifest key empties the model silently) and `agent-ix/quire-rs#394` (a
  `data_schema` digest mismatch drops the object type with no diagnostic).
  FR-003-AC-6's "naming the key or the path" half is blocked on them and is
  carried as an explicit expected failure.
- Record validation of a legacy-form artifact that declares `object:`:
  `agent-ix/quire-rs#391` (the engine validates an `unavailable` record as
  `{}`, so a legacy form errors even under `legacy_forms: warning`).
  NFR-001-AC-2 itself holds — no 0.1.0 artifact carries `object:` — and the
  defect is carried as an explicit expected failure beside it rather than
  worked around by relaxing a schema.
- Resolving a reference-form `data_schema` into a stored snapshot at
  activation: `agent-ix/filament-core-service#23`. Until it lands the service
  stores the reference verbatim, which is what FR-001-AC-4 and IT-001-SC-03
  assert.
- Editing any corpus repository or vendored fixture; the legacy-form sweep and
  corpus promotion (`agent-ix/quoin#291`).
- Application database schema generation: none is produced by these schemas.

## System Overview

### System Description

`spec-objects-enterprise` is a Python package that publishes a Filament Module
manifest declaring seven tier-2 ObjectTypes for enterprise architecture
modeling. The manifest is activated against `filament-core-service` over its
HTTP API, which registers the declared archetypes, object types, grammars, and
artifact types.

### Intended Users

The Filament platform (which activates and serves the contributed ObjectTypes),
spec authors (who model enterprise architecture using them), and agent CLI
generators such as `minijinja-cli` (which produce artifacts from the shipped
templates and schemas).

## Requirements Architecture

The requirement classes that make up this specification trace from the
stakeholder need for extractable enterprise-architecture graph entities
(`stakeholder/`) through the maintainer's story of declaring those types
against semantic-core (`usecase/`) to the functional requirements
(`functional/`): FR-001 activates the manifest against `filament-core`; FR-002
emits the schemas; FR-003 declares the semantic contract in the manifest;
FR-004 fixes each type's role-distinct schema and the definition / measurement
boundary; FR-005 makes the skeletons executable fixtures. NFR-001 bounds the
change to additive compatibility. Integration tests in `integration/` verify
the activation and Quoin-install boundaries; the third external boundary, the
Quire engine (loader, extraction, record surface), has no IT artifact of its
own — the FR-003 and FR-005 test harness is this module's Quire contract test,
and the wheel version is pinned once in FR-005 Inputs. The Test Matrix in
`tests.md` records every criterion's test case.

## References

- ISO/IEC/IEEE 29148 — Requirements engineering.
- This module's source repository and `manifest.yaml`.
- filament-core-service [FR-035](ix://agent-ix/filament-core-service/FR-035)
  (Module Manifest Schema), the upstream contract this module's manifest
  conforms to.
- `agent-ix/filament-core-data` FR-031..FR-034 (semantic-core grammar, scalars,
  JSON Schema projection, lowering) and ADR-0005 (TypeSpec source).
- `agent-ix/quoin` FR-070..FR-075 (semantic-module contract, mappings,
  `data_schema` by digest, legacy forms, package manifests).
- `agent-ix/quire-rs` FR-069..FR-072 (contract at load, typed Properties,
  clauses and operations, extraction surface).
- `agent-ix/spec-objects-business` issue #4, the sibling module whose migration
  this one follows.
