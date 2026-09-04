---
id: Task-005
title: "FR-005 — executable skeletons, sysml alternates and negative fixtures"
type: Task
status: todo
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-enterprise/Task-004
    type: depends_on
  - target: ix://agent-ix/spec-objects-enterprise/Task-011
    type: depends_on
  - target: ix://agent-ix/spec-objects-enterprise/FR-005
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/TC-050
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-051
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-052
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-053
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-054
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-056
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-057
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-058
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-059
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-064
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-065
    type: verifies
---
# Task-005: FR-005 — executable skeletons, sysml alternates and negative fixtures

## Scope

Rewrite the seven skeletons as executable typed fixtures, add three
alternate-form skeletons, and add the ten negative fixtures that pin what the
schemas and the engine refuse.

## Subtasks

- [ ] **Typed `## Properties`** with the header exactly `Field | Type | Multiplicity | Constraints` on `capability`, `business_function`, `value_stream`, `decision`, `objective`, `kpi`. `principle` carries none — `Principle.json` forbids `fields`.
- [ ] **`## Invariants`** on all seven, one `### <clauseId>` per clause, each owning exactly one ```` ```ocl ```` fence. The fence text is carried verbatim and never evaluated.
- [ ] **`## Operations`** on `business_function` only; every other type forbids `operations`.
- [ ] **Keep every required 0.1.0 H2**: `## Sub-capabilities`, `## Description`, `## Stages`, `## Decision`, `## Rationale`, and the `objective`/`kpi` frontmatter `metric`, `target`, `threshold`, `deadline` fields.
- [ ] **Frontmatter `object:`** equal to `type:` on every skeleton, or the semantic layer never runs.
- [ ] **`Identifier` titles**, unique across the skeletons and outside the `KernelScalar` names, so a `Type` cell can name another skeleton.
- [ ] **KPI fixture**: at least one measured field (`Type` cell with a trailing ` [unit]`), including one dimensionless row carrying `[1]`; no identity row; no `Timestamp` row.
- [ ] **Objective fixture**: an identity row and a `Timestamp` row (the horizon).
- [ ] **Three `sysml` alternates**: `capability.sysml.md`, `objective.sysml.md`, `kpi.sysml.md`, declaring exactly the same fields as their table skeletons under the same `id` and `title`.
- [ ] **Ten negative fixtures** under `tests/fixtures/negative/`, each with a frontmatter `expect:` code: KPI with a `Timestamp` row; KPI with an identity row; KPI with no unit; objective with no `Timestamp` row; principle with a `## Properties` table; capability with no identity row; business function whose `## Operations` declares none (all `semantic.record-invalid`); both Properties forms in one artifact (`semantic.properties-both-forms`); an operation whose `Post:` names an undeclared clause (`semantic.dangling-clause-ref`); a `Type` token that is not an `Identifier` (`semantic.invalid-type-token`).

## Deliverables

- `spec_objects_enterprise/skeletons/` — 7 skeletons + 3 alternates
- `tests/fixtures/negative/` — 10 fixtures
- `tests/test_skeletons_semantic.py` covering TC-050..TC-054, TC-056..TC-059, TC-064, TC-065

## Notes

- One artifact carries one Properties form. The alternate is a separate file,
  never a second block (FR-005-CON-2), and TC-057 pins the refusal.
- No skeleton may score or rate an organizational unit or a person
  (FR-005-CON-3, TC-065). A capability skeleton describing "maturity" is the
  shape to avoid.
- TC-058 is an inspection over the branch diff: no corpus repository and no
  vendored quoin/quire fixture is touched.
- The engine was probed before authoring: `Decimal(5,2) [%]`, `Duration [d]`
  and `Integer [1]` all extract `type.unit`, and the table and fence forms
  produce identical `FieldDecl[]`. A bare `Decimal` is an error — every decimal
  row needs `(precision,scale)`.
