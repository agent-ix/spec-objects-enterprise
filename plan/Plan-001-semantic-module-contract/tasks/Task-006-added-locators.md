---
id: Task-006
title: "FR-003 — required:false locators for the sections the skeletons introduce"
type: Task
status: todo
track: A
priority: P1
relationships:
  - target: ix://agent-ix/spec-objects-enterprise/Task-005
    type: depends_on
  - target: ix://agent-ix/spec-objects-enterprise/FR-003
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/FR-005
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/TC-055
    type: verifies
---
# Task-006: FR-003 — required:false locators for the sections the skeletons introduce

## Scope

Add one `required: false` `section_body` locator per `## Properties`,
`## Invariants` and `## Operations` section the rewritten skeletons introduce,
so the section is asserted by the manifest and remains optional for artifacts
that predate it.

## Subtasks

- [ ] **`properties`** locator on `capability`, `business_function`, `value_stream`, `decision`, `objective`, `kpi`.
- [ ] **`invariants`** locator on all seven types.
- [ ] **`operations`** locator on `business_function`.
- [ ] **Every added locator `required: false`** (FR-003-CON-2), asserted by TC-023.
- [ ] **No skeleton carries an H2 the manifest does not assert**, and every `required: true` heading is present (TC-055).
- [ ] **Regenerate digests** — the manifest changed, so `make schemas` runs and `make schemas-check` must exit zero.

## Deliverables

- `spec_objects_enterprise/manifest.yaml` locator additions
- `tests/test_skeletons_semantic.py` TC-055 assertions

## Notes

- The locators come **after** the sections exist (Task-005), so the manifest
  never asserts a heading no skeleton carries.
- Adding a `required: true` locator here would break every existing artifact
  and is the failure mode NFR-001 measures.
