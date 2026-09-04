---
id: Task-007
title: "FR-005 — Quire provisioning, the no-vacuous-skip rule and the 0.1.0 baseline"
type: Task
status: todo
track: B
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-enterprise/FR-005
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/NFR-001
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/FR-003
    type: references
---
# Task-007: FR-005 — Quire provisioning, the no-vacuous-skip rule and the 0.1.0 baseline

## Scope

Two things that must exist before anything else can be trusted: a documented
way to get the engine under test into the environment, and a checked-in
pre-image of the 0.1.0 manifest and skeletons.

## Subtasks

- [ ] **`make dev-quire`** installing the Quire wheel exposing `extract_semantic` from the dev-only `pypi.ix`. `quire` is **not** declared in `pyproject.toml`: no committable index carries 0.46.0 (`agent-ix/quire-rs#392`).
- [ ] **Fail, never skip.** `tests/conftest.py` fails every semantic test when `quire` is absent or lacks `extract_semantic`, with a message naming the missing function, `make dev-quire` and `agent-ix/quire-rs#392`.
- [ ] **Schema registry fixture** that resolves every `$ref` locally — module models from the committed `schemas/`, grammar models from the installed `@agent-ix/semantic-core` — and fails naming `npm ci` when the package is absent.
- [ ] **0.1.0 baseline**, captured before Task-004 edits the manifest: `tests/fixtures/baseline-0.1.0/body_extraction.json` and `tests/fixtures/baseline-0.1.0/skeletons/*.md` (all seven, verbatim).
- [ ] **Shared fixtures** for the manifest, the `semantic` block, the `module` block `extract_semantic` takes, and a bundle index built from the skeleton frontmatter.

## Deliverables

- `tests/conftest.py`
- `tests/fixtures/baseline-0.1.0/`
- `Makefile` / `pyproject.toml` `dev-quire` target

## Notes

- A skipped row is not coverage. If the engine is absent the suite goes red;
  that is the point, and it is the plan's quality gate 2.
- Capture the baseline first. After Task-004 the 0.1.0 manifest exists only in
  git history, and a baseline reconstructed from history is a baseline nobody
  reviewed.
