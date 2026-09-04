---
id: US-001
title: "Declare enterprise object types against semantic-core"
type: US
relationships:
  - target: "ix://agent-ix/spec-objects-enterprise/StR-001"
    type: "traces_to"
---
# US-001: Declare enterprise object types against semantic-core

## Story

**As a** maintainer of the enterprise-architecture object module
**I want** every enterprise object type (capability, business function, value stream, decision, objective, principle, KPI) to carry a real structural contract expressed in the shared semantic-core grammar
**So that** spec authors write one typed `## Properties` table per object, reviewers and generators read one declaration record per object, a KPI definition can never be read as a measured value, and the same record validates identically in Quire, Quoin, and the compiler.

The story is stated from the maintainer's perspective and does not prescribe
the emitter, the file layout, or the extraction engine.

## Context

Today every object type in `manifest.yaml` carries `data_schema: {type: object}`,
which types nothing: a capability and a KPI are indistinguishable to a consumer,
`## Properties` does not exist, and the measurable types express their measure as
two free-text frontmatter strings (`metric`, `target`) that a consumer cannot tell
apart from an observed reading. The semantic-core grammar
(`agent-ix/filament-core-data#35`) and the semantic-module contract
(`agent-ix/quoin#293`, `agent-ix/quire-rs#388`) now exist and are merged, and the
sibling module `agent-ix/spec-objects-business#4` has already migrated; this
module is the enterprise-architecture fixture source for the downstream frontends
(`agent-ix/quire-contract-ir#52`, `agent-ix/filament-core-data#36`).

## Acceptance Examples (Illustrative)

These examples clarify the maintainer's expectations. They are illustrative
only, not test cases and not verification criteria.

### US-001-EX-1: A capability skeleton extracts to typed fields

- **Given** the `capability` skeleton with a `| Field | Type | Multiplicity | Constraints |` table
- **When** Quire extracts it under this module
- **Then** the record carries one `FieldDecl` per row, the identity row is flagged, and the record validates against the shipped `Capability.json`

### US-001-EX-2: A KPI that reads like an observation is refused

- **Given** a KPI artifact whose table carries an `observed_at : Timestamp` row and an identity row
- **When** Quire validates it
- **Then** validation fails naming the KPI schema, because a KPI declares a measure definition and never an observation of it

### US-001-EX-3: An objective names a KPI rather than restating one

- **Given** an objective declaration whose `targets` entry names `ix://agent-ix/spec-objects-enterprise/type/OnTimeDeliveryRate`
- **When** a consumer reads the record
- **Then** the objective's bound is visibly a declared target against a named measure definition, not a measurement

## Options (Exploratory)

Approaches discussed: hand-authoring one JSON Schema per type; generating the
schemas from a TypeSpec package that imports `@agent-ix/semantic-core`;
deriving the schemas from the skeletons. Only the TypeSpec route keeps one
source for the grammar and its vocabulary; it is the route the authoring
contract on the ticket already names, and the route the business module took.

## Constraints (Contextual)

No corpus repository may be edited; existing `body_extraction` locators stay as
they are so current artifacts keep extracting; no management score and no trust
score is introduced; role vocabulary changes wait on evidence from the corpus
review. The change is advisory until corpus promotion. This context is not
binding here and is refined in the functional and non-functional requirements.

## Dependencies (Contextual)

Upstream: semantic-core 0.1.0 on npm.ix, the module-manifest schema with the
`semantic` block, Quire 0.46.0 with `extract_semantic`. Downstream: the
frontends that read this module's skeletons as fixtures.

## Priority and Risk (Informative)

P1 on the Track A programme. The risk if unmet is that enterprise-architecture
content stays free prose, that a metric definition and a metric reading remain
indistinguishable to a consumer, and that the downstream frontends have no
enterprise fixture.

## Notes (Informative)

Open question captured for later analysis: which sections beyond
`## Properties`, `## Invariants`, and `## Operations` the extraction engine
should read (`## Stages`, `## Sub-capabilities`, thresholds, targets). The
schemas declare those keys; extraction of them is an engine concern.

## Traceability (Informative)

Traces to [StR-001](../stakeholder/StR-001-module-activation.md); implemented
by [FR-002](../functional/FR-002-emitted-json-schemas.md),
[FR-003](../functional/FR-003-semantic-manifest-contract.md),
[FR-004](../functional/FR-004-role-schemas.md), and
[FR-005](../functional/FR-005-executable-skeletons.md).
