---
id: Plan-001
title: "spec-objects-enterprise — semantic module contract (issue #4)"
type: Plan
status: complete
relationships:
  - target: ix://agent-ix/spec-objects-enterprise/StR-001
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/US-001
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/FR-001
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/FR-002
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/FR-003
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/FR-004
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/FR-005
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/NFR-001
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/IT-001
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/IT-002
    type: references
---
# Implementation Plan: semantic module contract

## Requirements Summary

### Stakeholder Requirements
- [x] **StR-001**: Enterprise-architecture specifications yield extractable graph entities; every enterprise object carries one typed structural contract downstream frontends can read, and a KPI definition is distinguishable from a reading of it (VC-1..VC-3).

### User Stories
- [x] **US-001**: Declare every enterprise object type against the shared semantic-core grammar, so one declaration record per object validates identically in Quire, Quoin and the compiler.

### Functional Requirements
- [x] **FR-001**: The manifest conforms to filament-core-service FR-035 at revision `a77f31e` and activates idempotently; the registered `data_schema` is the reference object as posted.
- [x] **FR-002**: Emit one JSON Schema 2020-12 document per model from `typespec/main.tsp` with the official `@typespec/json-schema` emitter at a pinned toolchain; normalize `$id`/`$ref`; gate drift; package the schemas into the wheel and the npm tarball; version-embedded `$id` with an atomic bump procedure.
- [x] **FR-003**: `manifest.yaml` at version 0.2.0 carries the quoin FR-070 `semantic` block and a reference-form `data_schema` (path + digest) per exported object type, every 0.1.0 locator unchanged, and each type's `allowed_links` key set equal to its emitted relation-verb enum.
- [x] **FR-004**: One role-distinct model per enterprise object type — required, forbidden and item rules — with the KPI definition / measurement boundary expressed as schema rules, every grammar item by `$ref` to semantic-core 0.1.0, and no redeclaration.
- [x] **FR-005**: Every skeleton is an executable typed fixture in the quoin FR-071/FR-072 Markdown forms, with three `sysml` alternates and ten negative fixtures; the semantic suite fails rather than skips when the engine is absent.

### Non-Functional Requirements
- [x] **NFR-001**: Additive compatibility — the checked-in 0.1.0 skeleton set still validates at 0.2.0, every 0.1.0 locator definition is unchanged, and the required-heading and frontmatter yields are byte-identical.

### Integration Test Requirements
- [ ] **IT-001**: Activation roundtrip against a running filament-core-service at `a77f31e` or later.
- [ ] **IT-002**: `quoin module install path:<dir>` accepts the semantic contract and the prior module state is restored unconditionally.

## Dependency Graph

### Core dependency edges
- `FR-002 (toolchain half) -> FR-004`
  Reason: the models cannot be authored until `tsp compile` runs against `@agent-ix/semantic-core` 0.1.0 and the generator normalizes what it emits.
- `FR-004 -> FR-002 (emitted-set half)`
  Reason: FR-002-AC-1/AC-2/AC-3 assert the emitted file set, its `$id`s and its `$ref`s, none of which exist before FR-004 declares the models. FR-002 is split into an enablement half (generator, drift gate, packaging) that precedes FR-004 and an emitted-set half that follows it; FR-002 `depends_on` FR-004 in the frontmatter.
- `FR-004 -> FR-003`
  Reason: FR-003-AC-7 compares each type's `allowed_links` key set against the emitted relation-verb enum. The dependency review broke the apparent `FR-003 ↔ FR-004` cycle by naming the schema the authority; the manifest follows it.
- `FR-002 (emitted set) + FR-001 -> FR-003`
  Reason: the manifest references the emitted files by path and digest, and the 0.2.0 manifest must still be an FR-035-valid manifest.
- `FR-003 + FR-004 -> FR-005`
  Reason: a skeleton validates only once the archetype loads with its schema, and the negative fixtures pin refusals the FR-004 rules define.
- `FR-005 -> FR-003 (added locators)`
  Reason: the `required: false` locators the manifest gains exist to assert sections the skeletons introduce, so the section lands before its locator.
- `FR-003 + FR-005 -> NFR-001`
  Reason: the compatibility metrics compare 0.1.0 locators and skeletons against the finished 0.2.0 manifest and its loader behaviour.
- `FR-003 -> IT-002`
  Reason: the Quoin install exercises the finished `semantic` block and digests.
- `FR-003 -> FR-001 / IT-001 (re-verification)`
  Reason: the manifest changed, so activation must be re-verified against the pinned service revision.

### Shared dependencies
- **The generator** (`scripts/generate-schemas.mjs`) is the single writer of
  `spec_objects_enterprise/schemas/` and of `manifest.yaml`'s
  `data_schema.digest` values. It is needed by FR-002, FR-003, FR-004 and
  NFR-001; it is extracted as Task-001 and no other task writes those bytes.
- **The Quire test harness** (module registry construction, `validate_document`,
  `extract_semantic`, the schema registry that resolves every `$ref` locally,
  the hard-fail-on-missing-engine rule) is needed by FR-003, FR-004, FR-005 and
  NFR-001; it is extracted as Task-007.
- **The 0.1.0 baseline** (a checked-in copy of the 0.1.0 `body_extraction` and
  of all seven 0.1.0 skeletons) is needed by FR-003-AC-3 and by every NFR-001
  metric; it is captured in Task-007 before the manifest changes, because after
  the change the pre-image no longer exists in the working tree.

## Execution Tracks

### Track A — critical path (serial)
Task-001 → Task-002 → Task-003 → Task-004 → Task-005 → Task-006

### Track B — parallel with Track A
Task-007 (test environment and 0.1.0 baseline) runs first and alongside
Task-001; nothing on Track A may capture the baseline after Task-004 edits the
manifest.

### Track C — after the critical path
Task-008 (NFR-001), Task-009 (IT-002), Task-010 (FR-001 re-verification and
trace tags).

### Gate
Task-011 — `Kpi`, `Objective` and `Principle` end to end, run as soon as
Task-002 and Task-003 land and before Task-005 authors the remaining
skeletons.

## Quality Gates

1. **Emitter gate (Task-011, after Task-003).** `Kpi.json`, `Objective.json`
   and `Principle.json` must survive a real 2020-12 validator with the record
   sealed, both `@extension("allOf", …)` `contains` clauses intact on `Kpi`,
   and the temporal rule intact on `Objective`. This is the risk register's top
   technical hazard: no other module in the programme emits two `allOf`
   `contains` clauses over one array. If the emitter refuses the second clause,
   stop and re-derive the expression before writing the other four models.
2. **No vacuous skip (Task-007).** With the Quire wheel absent, the semantic
   tests must FAIL with a message naming `extract_semantic`, `make dev-quire`
   and `agent-ix/quire-rs#392`. A skip is a defect in this plan, not a state.
3. **Drift gate (Task-001).** `make lint` runs `make schemas-check`; a
   `typespec/` edit that was never regenerated fails before push.
4. **Baseline-before-change (Task-007).** The 0.1.0 locator and skeleton
   baseline is committed before Task-004 touches `manifest.yaml`.
5. **Trace-tag gate (Task-010).** Every test carries a `@pytest.mark.trace`
   the engine's `pytest-trace-marker` form matches, no marker is wrapped by
   `black` onto a line the form cannot read, and no bare TC id appears in a
   comment or a container docstring where it would bind the next symbol.

## Test Plan

| TC | Task | Kind |
|---|---|---|
| TC-001 | Task-010 | Manifest validates against the vendored FR-035 schema |
| TC-002..TC-004 | Task-010 | Activation rows, `🚧` — needs a running filament-core |
| TC-005, TC-006 | Task-010 | Demonstration / Manual rows, `🚧` |
| TC-010..TC-012 | Task-003 | Emitted set, `$schema`/`$id`, `$ref` resolution |
| TC-013, TC-014, TC-016..TC-019 | Task-001 | Drift gate, version disagreement, determinism, packaging inspection, lockfile origin |
| TC-015, TC-071..TC-074 | Task-003 | Wheel and npm tarball contents, atomic bump, stale-file check, no hard-coded version |
| TC-020..TC-026, TC-028 | Task-004 | `semantic` block, digests, baseline locators, registry load, refusals, verb-enum equality |
| TC-027, TC-070 | Task-009 | Quoin install roundtrip, `🚧` — needs a Quoin built from main |
| TC-030..TC-043 | Task-002 | The seven schemas' required, forbidden and item rules |
| TC-050..TC-057, TC-059, TC-064 | Task-005 | Skeletons, alternates, negatives, availability, KPI/objective field markers |
| TC-055 | Task-006 | H2 sets asserted by the manifest |
| TC-058, TC-065 | Task-005 | Inspection rows: no corpus edit, no scoring in a skeleton |
| TC-060..TC-063 | Task-008 | NFR-001 metrics against the 0.1.0 baseline |
| TC-075 | Task-010 | StR-001-VC-3 demonstration |

## Notes

- The plan implements the specification as reviewed. Four findings from the
  review round changed the design before planning and are carried into the
  tasks: the UCUM unity symbol for dimensionless measures, uniqueness keys on
  the named declaration arrays, acyclic `decomposes`/`supersedes`, and inert
  clause text.
- Nothing in this plan waits on an open upstream issue. `quire-rs#392`,
  `#221`, `#394`, `#391` and `filament-core-service#23` are discharged by
  out-of-scope entries and expected failures, not by blocked tasks.
