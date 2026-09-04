---
id: Task-010
title: "FR-001 / StR-001 — activation re-verification and the trace-tag gate"
type: Task
status: todo
track: C
priority: P1
relationships:
  - target: ix://agent-ix/spec-objects-enterprise/Task-006
    type: depends_on
  - target: ix://agent-ix/spec-objects-enterprise/FR-001
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/StR-001
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/IT-001
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/TC-001
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-002
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-003
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-004
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-005
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-006
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-075
    type: verifies
---
# Task-010: FR-001 / StR-001 — activation re-verification and the trace-tag gate

## Scope

Re-verify the unchanged activation behaviour against the new manifest, close
StR-001-VC-3, and make every test in the repository bind the row it verifies.

## Subtasks

- [ ] **TC-001**: the 0.2.0 manifest validates against the vendored FR-035 module-manifest schema through `quire.validate_manifest`.
- [ ] **TC-002..TC-004**: activation, idempotent re-activation and registry read-back; `🚧`, needs a running filament-core.
- [ ] **TC-005, TC-006**: the two StR demonstrations; `🚧`.
- [ ] **TC-075**: StR-001-VC-3 — every object type ships a typed schema a fixture reader can consume, and a capability, a KPI definition and an observation-shaped record are distinguishable by schema alone.
- [ ] **Trace tags on every test**: `@pytest.mark.trace("TC-0NN", "FR-0NN-AC-N")` on the test function, in the `pytest-trace-marker` form the engine declares.
- [ ] **Trace-tag audit** before the PR: run `black` and `ruff` first, then confirm no marker was wrapped onto a line the form cannot read, no TC id sits on a module or class docstring or a plain helper, and no bare TC id appears in a comment where it would bind the next symbol.
- [ ] **`quire coverage --scope .`** reconciled against the `spec/tests.md` figure, with the two numbers' meanings stated.

## Deliverables

- `tests/test_activation_and_stakeholder.py`
- Trace tags across the whole suite

## Notes

- Three tag traps have bitten this programme: a `black`-wrapped marker binds
  nothing silently (`agent-ix/quire-rs#395`); a tag on a container docstring or
  a plain helper binds nothing (`tag-on-non-binding-symbol`); and a bare TC id
  in a comment binds the **next** symbol, so a comment explaining a
  deliberately untagged test mints the very trace it disclaims. Grep for all
  three before opening the PR.
- `quire coverage` counts matrix rows backed by a bound source symbol.
  `spec/tests.md` counts test cases. They are different populations and the
  report must say which is which.
