---
id: Task-004
title: "FR-003 — manifest 0.2.0, the semantic block and reference-form data_schema"
type: Task
status: todo
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-enterprise/Task-003
    type: depends_on
  - target: ix://agent-ix/spec-objects-enterprise/Task-007
    type: depends_on
  - target: ix://agent-ix/spec-objects-enterprise/FR-003
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/TC-020
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-021
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-022
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-023
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-024
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-025
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-026
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-028
    type: verifies
---
# Task-004: FR-003 — manifest 0.2.0, the semantic block and reference-form data_schema

## Scope

Take `spec_objects_enterprise/manifest.yaml` from 0.1.0 to 0.2.0: add the quoin
FR-070 `semantic` block, replace every `data_schema: {type: object}` with the
reference form, and leave every 0.1.0 locator exactly as it was.

## Subtasks

- [ ] **`semantic` block** with exactly the nine admitted keys: `contract_version: 1.0.0`, `semantic_core: 0.1.0`, `package: agent-ix/spec-objects-enterprise`, `exports` (the seven types), `imports: {}`, `targets: [json-schema, markdown]`, `mappings: [typed-table, sysml-fence, ocl-clause]`, `compatibility_posture: additive`, `legacy_forms: warning`.
- [ ] **Reference-form `data_schema`** on all seven types: `{schema: schemas/<Model>.json, digest: sha256:<hex>}`, written by the generator.
- [ ] **Version 0.2.0** in the manifest and in the `@jsonSchema` base, in one commit.
- [ ] **Baseline diff**: every 0.1.0 locator present with identical `from`, `path`, heading, `language`, `required`, `multiple` and `assert` facets, compared against the Task-007 baseline.
- [ ] **`allowed_links` / verb-enum equality** asserted per type (TC-028).
- [ ] **Registry load**: `quire.Registry.load_from([module dir])` lists all seven archetypes and `validate_document` reports no `semantic.*` load failure.
- [ ] **Refusal fixtures**: a manifest copy with an extra `semantic` key `foo`, and a copy with an altered digest, are each refused by the loader.

## Deliverables

- `spec_objects_enterprise/manifest.yaml` at 0.2.0
- `tests/test_manifest_semantic.py` covering TC-020..TC-026, TC-028

## Notes

- The digests are written by the generator, never by hand.
- The naming half of FR-003-AC-6 — that the refusal names the offending key or
  path — is an **expected failure** while `agent-ix/quire-rs#221` and
  `agent-ix/quire-rs#394` are open. Assert the refusal; mark the naming half
  as the expected failure and name both issues in the test. Do not delete the
  assertion and do not report the row green.
- The advisory posture (`additive`, `legacy_forms: warning`) is this ticket's
  discharge of the advisory-only-until-promotion merge gate. Do not change
  either value.
