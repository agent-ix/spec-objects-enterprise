---
id: FR-004
title: "Give every enterprise object type a role-distinct declaration schema"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-enterprise/US-001"
    type: "implements"
  - target: "ix://agent-ix/filament-core-data/FR-031"
    type: "depends_on"
---
# FR-004: Give every enterprise object type a role-distinct declaration schema

## Description

The TypeSpec source SHALL declare one model per enterprise object type whose
emitted schema validates that type's declaration record
`{ fields?, relations?, clauses?, operations?, … }` with type-specific required
keys, forbidden keys, and item rules, so that no type is a placeholder, each
enterprise-architecture role refuses the records that violate its own rules,
and a metric definition is refused where a metric reading is authored.

## Inputs

- semantic-core 0.1.0 grammar models: `FieldDecl`, `TypeRef`, `RelationDecl`,
  `OperationDecl`, `ClauseRef`, `EdgeCategory`, `Identifier`, `SemanticId`,
  `KernelScalar`, `UnitSymbol`.
- The declaration record Quire assembles per artifact: `fields` from
  `## Properties`, `clauses` from `## Invariants`, `operations` from
  `## Operations` (quire-rs FR-070/FR-071), with any key absent when its
  section is absent.

## Outputs

- Seven object-type models, each emitted as `schemas/<Model>.json`, sealed
  (`unevaluatedProperties: {not: {}}`).
- Support models emitted as sibling files: the open marker schemas
  `IdentityField`, `TemporalField`, `TemporalTypeRef`, `MeasuredField`, and
  `MeasuredTypeRef` (used as `contains` predicates); the sealed declaration
  models `MeasureDecl`, `TargetDecl`, `ThresholdDecl`, `StageDecl`,
  `OutcomeDecl`, `AlternativeDecl`, `LifecycleDecl`, `OwnershipDecl`, and
  `ProvenanceDecl`; the enums `AggregationKind`, `Direction`, `Comparator`,
  `ThresholdLevel`, and `LifecycleState`; and one relation-verb enum per object
  type: `CapabilityVerb`, `BusinessFunctionVerb`, `ValueStreamVerb`,
  `DecisionVerb`, `ObjectiveVerb`, `PrincipleVerb`, `KpiVerb`.

## Behavior

Each model SHALL enforce its row of the following table. "Identity field"
means a `FieldDecl` with `identity: true`; "temporal field" a `FieldDecl` whose
`type.target` is `Timestamp`; "measured field" a `FieldDecl` whose `type.unit`
is present. All three readings are semantic-core 0.1.0 reader conventions (the
identity flag is set only by a bare `identity` keyword in a Constraints cell
and is absent, not `false`, otherwise; the kernel scalar is the bare token
`Timestamp`; the unit is the trailing ` [symbol]` of a `Type` cell on a
unit-allowed scalar), so a semantic-core release that renders `identity: false`,
namespaces kernel scalars, or moves the unit is a breaking change to these
schemas and SHALL be handled by a manifest version bump, not by widening a
rule. Where a row admits "≥ 1 identity field", two or more identity rows are
admitted: a composite key is a legitimate declaration and no rule forbids it.

| Object type | Model | Required keys | Optional keys | Item rules |
|---|---|---|---|---|
| capability | `Capability` | `fields` | `relations`, `clauses`, `scope: string`, `outcomes: OutcomeDecl[]`, `owner: OwnershipDecl`, `lifecycle: LifecycleDecl`, `provenance: ProvenanceDecl` | `fields` has ≥ 1 item and ≥ 1 identity field; `operations` forbidden — a capability is an ability the organization holds, not an interface it exposes |
| business_function | `BusinessFunction` | `fields`, `operations` | `relations`, `clauses`, `scope: string`, `inputs: SemanticId[]`, `outputs: SemanticId[]`, `owner`, `lifecycle`, `provenance` | `fields` has ≥ 1 item and ≥ 1 identity field; `operations` has ≥ 1 item — a function is defined by what it performs |
| value_stream | `ValueStream` | `fields`, `clauses` | `relations`, `scope: string`, `stages: StageDecl[]`, `owner`, `lifecycle`, `provenance` | `fields` has ≥ 1 item and ≥ 1 identity field; `clauses` has ≥ 1 item — a value stream declares the end-to-end guarantee it makes to the triggering stakeholder; `operations` forbidden |
| decision | `Decision` | `clauses` | `fields`, `relations`, `alternatives: AlternativeDecl[]`, `owner`, `lifecycle`, `provenance` | `clauses` has ≥ 1 item — the decision taken is an asserted clause, not prose; `operations` forbidden |
| objective | `Objective` | `fields`, `clauses` | `relations`, `targets: TargetDecl[]`, `owner`, `lifecycle`, `provenance` | `fields` has ≥ 1 item, ≥ 1 identity field, and ≥ 1 temporal field — an objective is time-bound; `clauses` has ≥ 1 item; `operations` forbidden |
| principle | `Principle` | `clauses` | `relations`, `owner`, `lifecycle`, `provenance` | `clauses` has ≥ 1 item; `fields` and `operations` forbidden — a principle declares a rule, not data and not behaviour |
| kpi | `Kpi` | `fields` | `relations`, `clauses`, `measure: MeasureDecl`, `thresholds: ThresholdDecl[]`, `owner`, `lifecycle`, `provenance` | `fields` has ≥ 1 item, ≥ 1 measured field, 0 identity fields, and 0 temporal fields; `operations` forbidden |

- A dimensionless measure SHALL declare the UCUM unity symbol `1` as its unit, so a count or a ratio satisfies the "≥ 1 measured field" rule without a dimensional unit.
- The item rules of this requirement SHALL apply to an assembled declaration record only. An artifact that declares no frontmatter `object:` assembles no record, so no item rule reaches it; that is the mechanism NFR-001 measures, not an exemption granted here.
- The `Kpi` item rules SHALL be the schema expression of the definition / measurement boundary: a KPI declaration names what is measured and in which unit (≥ 1 measured field) and carries neither the identity of a reading (0 identity fields) nor the instant of one (0 temporal fields), so a record shaped like an observation is refused by `Kpi.json` rather than accepted as a definition.
- No object-type model SHALL declare a key naming a measured value, a sample, an observation, a score, or a rating.
- Each object-type model SHALL seal its record with `unevaluatedProperties: {not: {}}`, so such a key is refused rather than merely undeclared.
- `Objective` SHALL NOT admit `measure`, because an objective references a measure definition through `targets[].measure` and never defines one.
- `Kpi` SHALL NOT admit `targets`, because a KPI defines a measure and never carries the goal set against it.
- `MeasureDecl` SHALL be `{ name: Identifier, unit: UnitSymbol, aggregation: AggregationKind, direction: Direction, window?: string, doc?: string }` with `AggregationKind` the closed set `sum`, `average`, `median`, `percentile`, `ratio`, `count`, `max`, `min` and `Direction` the closed set `higher_is_better`, `lower_is_better`, `target_band`.
- `TargetDecl` SHALL be `{ measure: SemanticId, comparator: Comparator, bound: string, by?: string, doc?: string }`, where `measure` names a KPI declaration and `bound` is the declared limit, never an observed reading, with `Comparator` the closed set `at_least`, `at_most`, `equals`, `within`.
- `ThresholdDecl` SHALL be `{ level: ThresholdLevel, comparator: Comparator, bound: string, doc?: string }` with `ThresholdLevel` the closed set `alert`, `warning`, `breach`.
- `StageDecl` SHALL be `{ name: Identifier, order: integer ≥ 1, value: string, inputs?: SemanticId[], outputs?: SemanticId[], doc?: string }`.
- `OutcomeDecl` SHALL be `{ name: Identifier, doc: string }` and `AlternativeDecl` `{ name: Identifier, doc: string, rejected_because: string }`.
- `LifecycleDecl` SHALL be `{ state: LifecycleState, since?: string, superseded_by?: SemanticId }` with `LifecycleState` the closed set `proposed`, `accepted`, `active`, `deprecated`, `retired`.
- `OwnershipDecl` SHALL be `{ owner: SemanticId, steward?: SemanticId }`.
- `OwnershipDecl` SHALL declare no role name, no score, and no rating, because the organizational role vocabulary is corpus-review evidence this requirement does not anticipate.
- `ProvenanceDecl` SHALL be `{ source: SemanticId, method?: string, recorded_in?: SemanticId }`.
- The TypeSpec source SHALL narrow each object type's `relations[].verb` to that type's relation-verb enum, whose members equal the type's manifest `allowed_links` keys (FR-003-AC-7): `CapabilityVerb` = `decomposes`, `realizes`, `depends_on`, `references`; `BusinessFunctionVerb` = `supports`, `realizes`, `references`; `ValueStreamVerb` = `contains`; `DecisionVerb` = `references`, `supersedes`, `constrains`; `ObjectiveVerb` = `supports`, `references`; `PrincipleVerb` = `governs`; `KpiVerb` = `measures`.
- Each model SHALL validate every `fields`, `params`, `clauses`, `operations`, and `relations` item by `$ref` to the semantic-core 0.1.0 model, never by a copied definition.
- The TypeSpec source SHALL apply the verb narrowing over that `$ref` without redeclaring `RelationDecl`.
- The TypeSpec source SHALL express the item rules through the official emitter's decorators over open marker models: `@contains(IdentityField)` for "≥ 1 identity field", `@contains(IdentityField) @minContains(0) @maxContains(0)` for "0 identity fields", and, because JSON Schema admits one `contains` per array, the temporal and measured rules as `@extension("allOf", …)` clauses whose `contains` references `TemporalField.json` and `MeasuredField.json`; the generator normalizes those relative `$ref`s per FR-002.
- Every cross-reference a declaration makes (`type.target`, `RelationDecl.target`, `inputs`, `outputs`, `TargetDecl.measure`, `StageDecl.inputs`/`outputs`, `LifecycleDecl.superseded_by`, `OwnershipDecl.owner`/`steward`, `ProvenanceDecl.source`/`recorded_in`) SHALL be a `SemanticId` or `KernelScalar` per semantic-core, so a bare token is rejected by the schema; resolution against the bundle, and the placeholder `ix://<org>/<repo>/unresolved/<Token>` with its `semantic.unresolved-type` finding, exist today for `type.target` only (quire-rs FR-070) and for the other keys once `agent-ix/quoin#335` publishes their mapping.
- Each schema SHALL describe the declared shape only, never a runtime occurrence (a measured reading, a dated review, a scored assessment).
- Where a key is declared but the current extractor does not populate it (`relations`, `scope`, `outcomes`, `inputs`, `outputs`, `stages`, `alternatives`, `targets`, `measure`, `thresholds`, `owner`, `lifecycle`, `provenance`), the key SHALL be optional, so a record produced by today's extractor validates and a future extractor can fill it without a schema change.
- The test suite SHALL verify every criterion over a key the extractor does not populate against a hand-built JSON record rather than an extracted one, naming that limitation in the test itself, so that no row claims extraction evidence it does not have; the extraction path for those keys is `agent-ix/quoin#335` (mapping) and its quire-rs successor.
- Every item of a `stages`, `outcomes`, or `alternatives` array SHALL be unique by `name` within that array, which is the uniqueness key those declarations carry; `fields`, `operations`, and `params` inherit uniqueness by `name` from the semantic-core reader rules.
- A `relations` entry whose `verb` is `decomposes` or `supersedes` SHALL NOT name the declaring artifact.
- The `decomposes` graph and the `supersedes` graph SHALL each be acyclic.
- A `principle` SHALL NOT `govern` itself, even though its `allowed_links` target is the wildcard `*`.
- A `StageDecl.order` SHALL be unique and contiguous from 1 within one `stages` array.
- A `TargetDecl.measure` SHALL name a `kpi` declaration of the same bundle.
- JSON Schema cannot express the uniqueness, acyclicity, self-reference, ordering, or target-kind rules stated above, so each is a reader rule stated here for the extractor that first populates `relations`, `stages`, `outcomes`, `alternatives`, and `targets`; none is claimed as a schema refusal, and no test asserts one as one.

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-004-CON-1 | No model SHALL redeclare a semantic-core model or scalar; the module namespace contributes archetype shapes only (semantic-core NFR-014 kernel discipline). | Architecture | Test |
| FR-004-CON-2 | The empty record `{}` SHALL fail every one of the seven types, because every type's required set is non-empty. | Integrity | Test |
| FR-004-CON-3 | No model SHALL introduce a management score, a maturity score, a trust score, or any other rating of an organizational unit or person. | Boundary | Test |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-004-AC-1 | Each of the seven shipped object-type schemas differs from every other in at least one required key, forbidden key, or item rule listed in the table; a schema with only `type: object` is absent. | Test |
| FR-004-AC-2 | A capability record with one identity field validates against `Capability.json`; the same record with the identity flag removed fails; a record with no `fields` fails; a record carrying `operations` fails. | Test |
| FR-004-AC-3 | A business-function record with an identity field and one operation validates; the same record with an empty `operations` array fails; a record with no `operations` key fails. | Test |
| FR-004-AC-4 | A value-stream record with an identity field and one clause validates, with `stages` accepted when present; the same record without `clauses` fails; a stage whose `order` is 0 fails. | Test |
| FR-004-AC-5 | A KPI record whose fields carry a unit and no identity and no `Timestamp` validates against `Kpi.json`; the same record with an identity field fails; with a `Timestamp` field fails; with no unit-bearing field fails; with `operations` fails. | Test |
| FR-004-AC-6 | An objective record with an identity field, a `Timestamp` field and one clause validates, with `targets` accepted when present; the same record without a `Timestamp` field fails; a `targets` entry whose `measure` is a bare token rather than a `SemanticId` fails. | Test |
| FR-004-AC-7 | A principle record with one clause validates; the same record carrying `fields` fails; carrying `operations` fails; with an empty `clauses` array fails. | Test |
| FR-004-AC-8 | A decision record with one clause validates, with `alternatives` accepted when present; the same record without `clauses` fails; an alternative missing `rejected_because` fails. | Test |
| FR-004-AC-9 | The empty record `{}` fails against all seven object-type schemas, each naming its own missing required key. | Test |
| FR-004-AC-10 | A `type.target` of `ix://agent-ix/spec-objects-enterprise/unresolved/Mystery` is accepted by the schema (it is a `SemanticId`) and reported by the extractor as `semantic.unresolved-type`; a bare `Mystery` string is rejected by the schema. | Test |
| FR-004-AC-11 | No module schema redeclares a semantic-core model; every grammar item is a `$ref` to semantic-core, including the `relations` items under the verb narrowing. | Test |
| FR-004-AC-12 | For each of the seven types, a `relations` entry whose `verb` is outside that type's verb enum fails, and one inside it validates. | Test |
| FR-004-AC-13 | `Objective.json` refuses a record carrying `measure`, and `Kpi.json` refuses a record carrying `targets`. | Test |
| FR-004-AC-14 | No shipped schema declares a property whose name matches `score`, `rating`, `maturity`, `observed`, `sample`, `reading`, or `measurement`, and every such key is refused by the seal on each of the seven object-type schemas. | Test |

## Dependencies

- **Upstream**: semantic-core FR-031 (`ix://agent-ix/filament-core-data/FR-031`)
- **Build**: [FR-002](./FR-002-emitted-json-schemas.md) emits these models
- **Downstream**: [FR-005](./FR-005-executable-skeletons.md); `agent-ix/quire-contract-ir#52` and `agent-ix/filament-core-data#36` read these schemas as fixtures
