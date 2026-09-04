---
id: Task-002
title: "FR-004 — the seven role-distinct models and the support models"
type: Task
status: todo
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-enterprise/Task-001
    type: depends_on
  - target: ix://agent-ix/spec-objects-enterprise/FR-004
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/US-001
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/TC-030
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-031
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-032
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-033
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-034
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-035
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-036
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-037
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-038
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-039
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-040
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-041
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-042
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-043
    type: verifies
---
# Task-002: FR-004 — the seven role-distinct models and the support models

## Scope

Declare in `typespec/main.tsp` one model per enterprise object type whose
emitted schema validates that type's declaration record, plus the support
models the item rules and the optional keys need. No type may remain a
placeholder, and the KPI definition / measurement boundary is expressed here or
nowhere.

## Subtasks

- [ ] **Spike first: `Kpi` and `Objective`.** Author these two models before the other five and run Task-011's gate on them. They are the only place in the programme where two `@extension("allOf", …)` `contains` clauses sit over one array; if the emitter refuses the second, the identity rule needs a different expression and the remaining models must not be written against a shape that cannot compile.
- [ ] **Seven object-type models.** `Capability`, `BusinessFunction`, `ValueStream`, `Decision`, `Objective`, `Principle`, `Kpi` — each sealed with `unevaluatedProperties: {not: {}}` and each carrying the required, optional and forbidden keys of the FR-004 table.
- [ ] **Marker support models.** `IdentityField`, `TemporalField`, `TemporalTypeRef`, `MeasuredField`, `MeasuredTypeRef` — open models used only as `contains` predicates.
- [ ] **Declaration support models.** `MeasureDecl`, `TargetDecl`, `ThresholdDecl`, `StageDecl`, `OutcomeDecl`, `AlternativeDecl`, `LifecycleDecl`, `OwnershipDecl`, `ProvenanceDecl` — sealed.
- [ ] **Closed enums.** `AggregationKind`, `Direction`, `Comparator`, `ThresholdLevel`, `LifecycleState`.
- [ ] **Relation-verb enums**, one per type: `CapabilityVerb`, `BusinessFunctionVerb`, `ValueStreamVerb`, `DecisionVerb`, `ObjectiveVerb`, `PrincipleVerb`, `KpiVerb`, each equal to that type's manifest `allowed_links` key set.
- [ ] **Item rules through official decorators.** `@contains(IdentityField)` for "≥ 1 identity field"; `@contains(IdentityField) @minContains(0) @maxContains(0)` for "0 identity fields"; the temporal and measured rules as `@extension("allOf", …)` clauses referencing `TemporalField.json` and `MeasuredField.json`.
- [ ] **Verb narrowing over the `$ref`.** Narrow `relations[].verb` with an `@extension("allOf", …)` clause; do not redeclare `RelationDecl` (FR-004-CON-1).
- [ ] **Forward compatibility.** Every key the current extractor does not populate is optional, so today's records validate and a future extractor fills them without a schema change.
- [ ] **Record fixtures.** Positive and negative JSON records per type, validated against the emitted files with a real 2020-12 validator and a registry that resolves every `$ref` locally.

## Deliverables

- `typespec/main.tsp` with 7 object-type models, 14 support models and 12 enums
- `tests/test_role_schemas.py` covering TC-030..TC-043

## Notes

- The KPI rules are the ticket's headline acceptance criterion. A dimensionless
  measure declares the UCUM unity symbol `1`; do not drop the measured-field
  rule to admit counts and ratios, and do not admit a `Timestamp` field to
  admit an "as of" declaration — that is the observation the rule exists to
  refuse.
- `Objective` must not admit `measure` and `Kpi` must not admit `targets`. Both
  are enforced by the seal; assert them explicitly anyway (TC-042), because a
  seal is easy to widen by accident.
- Criteria over unpopulated keys (`relations`, `scope`, `outcomes`, `inputs`,
  `outputs`, `stages`, `alternatives`, `targets`, `measure`, `thresholds`,
  `owner`, `lifecycle`, `provenance`) are verified with hand-built records, and
  each such test must say so in its docstring: they are schema evidence, not
  extraction evidence.
- Uniqueness by `name` within `stages`/`outcomes`/`alternatives`, acyclic
  `decomposes`/`supersedes`, a principle not governing itself, and
  `TargetDecl.measure` naming a `kpi` are reader rules the schema cannot
  express. State them; do not claim them as refusals and do not write a test
  that asserts one as one.
- `OwnershipDecl` carries no role name, no score and no rating (FR-004-CON-3).
  The organizational role vocabulary is corpus-review evidence this ticket does
  not have.
- Unblocks: Task-011 (the gate), Task-003 (the emitted set), Task-004 (the verb
  enums the manifest is compared against), Task-005 (what the negatives pin).
