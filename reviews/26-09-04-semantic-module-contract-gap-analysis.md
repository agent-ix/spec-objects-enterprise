---
id: SR-010
title: "Gap analysis — Plan-001 semantic module contract (#4)"
type: SpecReview
analysis: gap-analysis
scope: "plan/Plan-001-semantic-module-contract/, spec/tests.md, spec_objects_enterprise/, tests/"
review_set: subset
relationships:
  - target: "ix://agent-ix/spec-objects-enterprise/Plan-001"
    type: reviews
  - target: "ix://agent-ix/spec-objects-enterprise/TM-001"
    type: references
---
# SR-010: Gap analysis — Plan-001 semantic module contract (#4)

## Summary

Post-implementation verification gate over `Plan-001`: plan completion, matrix
verification through `quire coverage`, the reverse code→spec gap, and a
semantic intent↔test↔code pass over the five requirements. Ten of eleven tasks
are `done`; Task-009 is `blocked` on a Quoin release that does not exist.
`quire coverage` reports **111/111 rows backed, 0 unbacked rows, 0 status
lies**. Four findings, none high.

## Verdict

**CONDITIONAL** — one task is blocked on an upstream release rather than
incomplete, and every matrix row is backed. The remaining findings are recorded
drift and evidence-plan gaps, all with named owners.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | Task-009 (IT-002, the Quoin install roundtrip) is `status: blocked`, not `done`: no Quoin release carries the semantic installer, which lives on `agent-ix/quoin` main at or after `3e842ce`. TC-027 and TC-070 stay `🚧` naming that reason and the three tests are opt-in behind `QUOIN_INSTALL_ROUNDTRIP=1`. The rows are backed by tagged tests, so the matrix does not lie; what is missing is a run, not a test. | plan/Plan-001-semantic-module-contract/tasks/Task-009-quoin-install-roundtrip.md, spec/tests.md TC-027, TC-070 |
| FND-002 | medium | Four trace ids (`IT-002-SC-02`..`SC-05`) are authored on real tests and mint nothing: `spec-artifacts-process` declares `trace_target`s for `TestMatrix`, `FR`, `NFR`, `StR`, `SuiteRegistry` and `Inspections`, but none for the `IT` archetype, so an integration test's success criteria can never bind. `quire coverage` reports them as untracked symbols. Pre-existing and ecosystem-wide (`agent-ix/spec-artifacts-process#63` closed the FR/US/StR half); recorded rather than worked around by deleting the ids, because deleting them would lose the only human trace from the test to the IT procedure. | tests/test_quoin_install_roundtrip.py:86, `spec-artifacts-process/manifest.yaml` traceability.trace_targets |
| FND-003 | low | Reverse gap: `tests/test_manifest.py` asserts three behaviours no requirement states — that `manifest_version` is `1.0.0`, that every object type carries a `data_schema` key, and that object-type names are unique. They are true and worth asserting; FR-001 and FR-003 simply never say them. Recorded as underspecified rather than deleted or promoted, because promoting them would widen FR-001, which this issue does not otherwise change. | tests/test_manifest.py:16, tests/test_manifest.py:32 |
| FND-004 | low | Evidence plan: no `SuiteRegistry` document declares which suite produces each evidence kind and no `Inspections` document discharges the eight `Inspection`/`Demonstration`/`Manual` rows; `quire coverage` reports both declarations as `archetype-matches-nothing`. The obligations have methods and the rows are backed by tagged tests, so this is a missing evidence-plan artifact rather than a missing test. Carried identically by the merged sibling module and tracked upstream as `agent-ix/spec-artifacts-process#75`. | spec/tests.md Coverage Gaps |

## Coverage

| Question | Result |
|---|---|
| Is the plan done? | 10 of 11 tasks `done`; Task-009 `blocked` (FND-001). No stale `plan.md` checkbox: IT-001 and IT-002 are the two left unchecked, and both are environment-gated. |
| Is the Test Matrix real? | `quire coverage --scope .`: **111/111 rows backed (100%)**, `unbacked_rows: 0`, `status_lies: 0`. Per document: FR-001 4/4, FR-002 9/9, FR-003 7/7, FR-004 14/14, FR-005 9/9, NFR-001 4/4, StR-001 3/3, `spec/tests.md` 61/61. Python binding: 69 bound of 69 tagged over 80 candidate symbols (86%); the 11 untagged are the pre-existing generic manifest tests of FND-003. |
| Is anything unspecified? | One cluster, FND-003. No stub, no placeholder return and no re-export-only module: the change ships no new source module at all — the deliverables are a TypeSpec source, a generator, JSON Schemas and Markdown. |
| Does intent match reality? | Semantic review **run**, inline rather than fanned out to subagents (the concurrency limit made subagents unavailable in this session; recorded so the method is not overstated). Per-requirement result below. |

### Semantic review (intent ↔ test ↔ code)

| Requirement | Intent | Test exercises real code? | Verdict |
|---|---|---|---|
| FR-002 | The shipped schema is the compiled one, and drift fails the build. | Yes — every emission test runs the real `tsp compile` through the real generator over a throwaway tree, and TC-016 compares bytes across two runs. | agrees |
| FR-003 | Quoin verifies the schemas at install and Quire validates records against them, with the 0.1.0 locators untouched. | Yes — the registry loader, `validate_document`, and a real mutated-manifest copy. The `allowed_links`/verb-enum equality (TC-028) reads both artifacts rather than restating either. | agrees; the naming half of AC-6 is a strict `xfail` on `quire-rs#221`/`#394` |
| FR-004 | No type is a placeholder, and a metric definition cannot be mistaken for a measured value. | Yes — a real 2020-12 validator over the committed bytes with every `$ref` resolved locally, and the same rules again end-to-end through the engine by three negative fixtures. The definition/reading pair is asserted directly in TC-075. | agrees |
| FR-005 | The skeletons are the module's executable positive fixtures and the negatives pin what is refused. | Yes — `validate_document` and `extract_semantic` on the real engine; the table/fence identity is compared on extracted records, not on the source text. | agrees |
| NFR-001 | The change is additive over the checked-in 0.1.0 set. | Yes — against a baseline captured from `origin/main` and verified byte-identical to it. TC-063 compares the engine's yield against an independent regex oracle over the frozen fixture rather than against a second engine run. | agrees; the `object:`-declaring case is a strict `xfail` on `quire-rs#391` |

### Deliberately untested

FR-004 states six rules JSON Schema cannot express — uniqueness by `name`
within `stages`/`outcomes`/`alternatives`, irreflexive and acyclic
`decomposes`/`supersedes`, a principle not governing itself, contiguous
`StageDecl.order`, and `TargetDecl.measure` naming a `kpi` of the same bundle.
Each is stated as a reader rule with "not claimed as a schema refusal" beside
it, and **no test asserts one as a refusal**. That is the correct outcome, not
a gap: a test asserting them would claim an enforcement the shipped schema does
not perform. They are recorded here so a later reader does not mistake the
absence for an oversight.
