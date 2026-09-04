---
id: Task-001
title: "FR-002 (enablement) — TypeSpec toolchain, schema generator and drift gate"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-enterprise/FR-002
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/US-001
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/TC-013
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-014
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-016
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-017
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-018
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-019
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-073
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-074
    type: verifies
---
# Task-001: FR-002 (enablement) — TypeSpec toolchain, schema generator and drift gate

## Scope

Stand up the emission toolchain and the generator that will write
`spec_objects_enterprise/schemas/` and the manifest digests. This is FR-002's
enablement half: everything that must exist before a single model can be
authored.

## Subtasks

- [x] **Exact toolchain pins.** `@typespec/compiler` 1.15.0, `@typespec/json-schema` 1.15.0 and `@agent-ix/semantic-core` 0.1.0 as exact `devDependencies` with a committed `package-lock.json`. No `.npmrc` in the repository; `@agent-ix` resolves from the user-level npm config.
- [x] **`typespec/tspconfig.yaml`** emitting `@typespec/json-schema` with `file-type: json`.
- [x] **`scripts/generate-schemas.mjs`**, Node built-ins only: compile to a scratch dir, keep only the `$id`s under the module base, normalize any relative `$id`/`$ref`, render two-space JSON with a trailing newline, write `toolchain.json`, and rewrite `manifest.yaml`'s `data_schema.digest` lines textually so anchors and comments survive.
- [x] **`--check` mode** that writes nothing and names every differing, missing or stale file.
- [x] **Base/version agreement** — the `@jsonSchema` base version and the manifest `version` must match or the generator fails naming both.
- [x] **Make and poe targets**: `schemas`, `schemas-check`, `dev-quire`; `lint` gains `schemas-check`.
- [x] **`.gitattributes`** marking `*.json` and `*.tsp` `eol=lf`, so a checkout with `autocrlf` cannot change the digested bytes.
- [x] **`scripts/stage-npm.mjs --clean`** and a `postpack` hook, so no `manifest.yaml` is left at the repository root where every Filament tool would find a second module.

## Deliverables

- `package.json`, `package-lock.json`, `typespec/tspconfig.yaml`
- `scripts/generate-schemas.mjs`, `scripts/stage-npm.mjs` (with `--clean`)
- `Makefile` and `pyproject.toml` task entries, `.gitattributes`
- `tests/test_schema_emission.py` rows TC-013, TC-014, TC-016..TC-019, TC-073, TC-074

## Notes

- The generator is the single writer of `schemas/` and of the manifest digests.
  No other task writes those bytes; a wrong schema is fixed in `typespec/` and
  regenerated, never hand-edited (FR-002-CON-1).
- `make schemas`/`make schemas-check` cannot run in the GitHub workflow while
  `@agent-ix/semantic-core` is npm.ix-only (FR-002-CON-4); the repo's CI is
  `workflow_dispatch`-only today, and `filament-core-data#11` resolves it.
- Start from the merged `agent-ix/spec-objects-business` generator; it is
  proven against this exact toolchain. Change the package name, the base URL
  and the package directory, nothing else.
