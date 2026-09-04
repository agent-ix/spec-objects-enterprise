---
id: Task-003
title: "FR-002 (emitted set) — schemas, toolchain.json, digests and packaging"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-enterprise/Task-002
    type: depends_on
  - target: ix://agent-ix/spec-objects-enterprise/FR-002
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/TC-010
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-011
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-012
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-015
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-071
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-072
    type: verifies
---
# Task-003: FR-002 (emitted set) — schemas, toolchain.json, digests and packaging

## Scope

Run the generator over the finished models and assert what it produced: the
emitted file set, every `$schema`/`$id`, every `$ref`, the digests written back
into the manifest, and the two package payloads.

## Subtasks

- [x] **Emit and commit** `spec_objects_enterprise/schemas/*.json` plus `toolchain.json`.
- [x] **Assert the emitted set** equals what `toolchain.json` lists — the seven object-type models plus the support models FR-004 Outputs names — with compiler and emitter 1.15.0 recorded.
- [x] **Assert every `$id`** is `<base><Model>.json` with the version segment read from `manifest.yaml`, never hard-coded, and every `$schema` is 2020-12.
- [x] **Assert every `$ref`** resolves to a shipped sibling or to semantic-core 0.1.0, and to no other host or version.
- [x] **Wheel payload**: `make build` produces a wheel containing every emitted schema.
- [x] **npm payload**: `npm pack` produces a tarball with `manifest.yaml` and a sibling `schemas/<Model>.json` for every exported type's `data_schema.schema` path, and the staged copies are removed from the repository root afterwards.
- [x] **Atomic bump**: bumping the manifest `version` and the `@jsonSchema` base together re-emits every `$id`, `$ref` and digest at the new version and `make schemas-check` exits zero; bumping one half exits non-zero.

## Deliverables

- `spec_objects_enterprise/schemas/` and `toolchain.json`
- `tests/test_schema_emission.py` covering TC-010..TC-012, TC-015, TC-071, TC-072

## Notes

- Every test reads the version segment from the manifest (FR-002-CON-5). A
  hard-coded `0.2.0` in a test is the defect TC-074 exists to catch.
- The bump test must run against a copy of the tree, never the working tree.
