---
id: Task-009
title: "IT-002 — Quoin install roundtrip with unconditional restore"
type: Task
status: todo
track: C
priority: P1
relationships:
  - target: ix://agent-ix/spec-objects-enterprise/Task-004
    type: depends_on
  - target: ix://agent-ix/spec-objects-enterprise/IT-002
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/FR-003
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/TC-027
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-070
    type: verifies
---
# Task-009: IT-002 — Quoin install roundtrip with unconditional restore

## Scope

Verify the boundary between this module's shipped directory and the Quoin
module installer.

## Subtasks

- [ ] **Record** `quoin module` before the install, including any existing `spec-objects-enterprise` entry (IT-002-SC-01).
- [ ] **Install** `quoin module install path:<checkout>/spec_objects_enterprise`; exit 0 and no `semantic.*` error diagnostic (IT-002-SC-02).
- [ ] **List** the module from the path (IT-002-SC-03).
- [ ] **Inspect** `semantic/package-manifest.json` for `package.identity` `agent-ix/spec-objects-enterprise` and one export per `semantic.exports` entry (IT-002-SC-04).
- [ ] **Restore unconditionally**, whether or not the earlier steps passed (IT-002-SC-05, IT-002-SC-06).

## Deliverables

- `tests/test_quoin_install_roundtrip.py` covering TC-027 and TC-070

## Notes

- Blocked on a Quoin built from `agent-ix/quoin` main at or after `3e842ce`;
  no release tag carries the semantic installer. The rows stay `🚧` with that
  reason named until one does.
- The restore step runs in a `finally`. A test that leaves the operator's
  module set changed is a defect regardless of its assertion result.
