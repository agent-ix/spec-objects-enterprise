---
id: Task-008
title: "NFR-001 — additive-compatibility verification against the 0.1.0 baseline"
type: Task
status: done
track: C
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-enterprise/Task-006
    type: depends_on
  - target: ix://agent-ix/spec-objects-enterprise/Task-007
    type: depends_on
  - target: ix://agent-ix/spec-objects-enterprise/NFR-001
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/TC-060
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-061
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-062
    type: verifies
  - target: ix://agent-ix/spec-objects-enterprise/TC-063
    type: verifies
---
# Task-008: NFR-001 — additive-compatibility verification against the 0.1.0 baseline

## Scope

Measure the four NFR-001 metrics against the finished 0.2.0 manifest and the
checked-in 0.1.0 baseline.

## Subtasks

- [x] **Zero locators changed**: every 0.1.0 locator present in 0.2.0 with identical facets (TC-060).
- [x] **Zero error findings**: every checked-in 0.1.0 skeleton validates under 0.2.0 (TC-061).
- [x] **Zero legacy-form warnings**: no 0.1.0 enterprise skeleton carries a `## Properties` section in any form, so the measured value is 0, not the sibling module's 1 (TC-062).
- [x] **Identical yields**: each 0.1.0 skeleton's required-heading section bodies and frontmatter yields are byte-identical under 0.1.0 and 0.2.0 (TC-063).

## Deliverables

- `tests/test_additive_compatibility.py` covering TC-060..TC-063

## Notes

- NFR-001-AC-2 holds because no 0.1.0 skeleton declares frontmatter `object:`,
  so Quire runs headings-only validation and assembles no typed record. Assert
  that fact rather than assuming it.
- Carry the `object:`-declaring legacy case as an **expected failure** naming
  `agent-ix/quire-rs#391`: quire 0.46.0 assembles such a record as `{}` and
  validates it unconditionally, so it errors even under `legacy_forms:
  warning`. Do not relax a schema to make it pass — the day the engine changes,
  the row must turn red and be noticed.
- The population is the seven checked-in skeletons. Do not report the number as
  a corpus result; the corpus sweep is `agent-ix/quoin#291`.
