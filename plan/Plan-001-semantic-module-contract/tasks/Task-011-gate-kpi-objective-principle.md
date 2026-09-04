---
id: Task-011
title: "Gate — Kpi, Objective and Principle end to end"
type: Task
status: done
track: A
priority: P0
relationships:
  - target: ix://agent-ix/spec-objects-enterprise/Task-003
    type: depends_on
  - target: ix://agent-ix/spec-objects-enterprise/FR-004
    type: references
  - target: ix://agent-ix/spec-objects-enterprise/FR-002
    type: references
---
# Task-011: Gate — Kpi, Objective and Principle end to end

## Scope

A hard gate between the model spike and the rest of the implementation. Three
types carry everything that could fail structurally, and they are emitted,
validated and exercised before the other four models or any skeleton is
written.

## Gate criteria

- [x] **`Kpi.json` emits with both `allOf` `contains` clauses intact** — the measured-field rule (`minContains: 1`) and the temporal-field rule (`maxContains: 0`) — alongside the `@contains(IdentityField) @maxContains(0)` clause on the same array. This is the risk register's top technical hazard: no other module in the programme emits two `allOf` `contains` clauses over one array.
- [x] **`Objective.json` emits with the temporal rule** (`minContains: 1` on `TemporalField`) and the identity rule together.
- [x] **`Principle.json` seals with `fields` and `operations` absent**, so a record carrying either is refused.
- [x] **A real 2020-12 validator agrees** with all three, with every `$ref` resolved against the committed `schemas/` and the installed semantic-core, and with the records sealed.
- [x] **The five identity rules discriminate**: a definition-shaped KPI record validates; the same record with an identity field, with a `Timestamp` field, or with no unit-bearing field each fails; a record carrying `targets` fails; an objective record carrying `measure` fails.
- [x] **`make schemas-check` exits zero** on the committed tree after the spike.

## Deliverables

- `schemas/Kpi.json`, `schemas/Objective.json`, `schemas/Principle.json` and their support models
- The TC-034, TC-035, TC-036, TC-042 assertions

## Notes

- If the emitter refuses the second `allOf` clause, **stop**. Do not weaken the
  KPI rule to one `contains` and do not move the temporal rule into prose: the
  ticket's headline acceptance criterion is that a metric definition cannot be
  mistaken for a measured value, and it is expressed here or nowhere. Re-derive
  the expression, record the new one in FR-004, and re-run the gate.
- The engine half is already de-risked: a probe of `extract_semantic` 0.46.0
  confirmed `type.unit` populates from a trailing ` [symbol]` cell in both the
  typed table and the `sysml` fence, and both forms extract identical
  `FieldDecl[]`. What this gate tests is emitter mechanics.
