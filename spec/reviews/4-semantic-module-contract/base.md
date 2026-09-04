---
id: SR-001
title: "Base review of the issue #4 semantic module contract specification"
type: SpecReview
analysis: base
scope: "spec/spec.md, spec/stakeholder/StR-001, spec/usecase/US-001, spec/functional/FR-001..FR-005, spec/non-functional/NFR-001, spec/integration/IT-001..IT-002, spec/tests.md"
review_set: all
---
# Base review of the issue #4 semantic module contract specification

## Summary

Checklist review (id formats, story and requirement quality, the six coverage
rules, cross-references) of the specification authored for
`agent-ix/spec-objects-enterprise#4`. Ids are well-formed and sequential per
class (StR-001, US-001, FR-001..FR-005, NFR-001, IT-001..IT-002, TM-001,
TC-001..TC-075 in blocks); ids were allocated off the global maximum across all
four remote branches, which carry only FR-001, IT-001 and StR-001. Every new FR
links US-001, US-001 traces to StR-001, and NFR-001 constrains FR-003..FR-005.
`quire validate --scope . "spec/**/*.md" --summary` reports 19/19 documents
grammar-clean with zero findings and zero structural errors. `quire coverage`
reports 0/111 rows backed, which is the expected pre-implementation state: the
matrix is authored ahead of the tests that back it. Three bookkeeping defects
were found (uncatalogued verification methods on FR-001, a `Type` vocabulary
drift away from the sibling module, and an upstream status-column mismatch) and
are dispositioned below.

## Verdict

**CONDITIONAL** — no high finding; the two mediums are bookkeeping fixes
applied before planning, and the third is an upstream defect recorded, not
worked around (see Dispositions).

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | FR-001's Verification cells read `Schema Test` and `Integration Test`, which `quire coverage` reports as `uncatalogued-verification-method` (neither a catalog method id nor a declared class), so nothing can say what discharging those four rows means. The declared class value is `Test`. Pre-existing wording, corrected here because the new matrix depends on those rows. Escape cause: wrong-requirement. | FR-001-AC-1..4 |
| FND-002 | medium | The matrix used `Static` for the four analysis-only rows and `Unit` for the StR-001-VC-3 row, while the sibling module `spec-objects-business` and the `spec-artifacts-process` catalog use `Inspection` and `Demonstration` for exactly those kinds. The `## Coverage Gaps` note about a missing `Inspections` document is only coherent against the catalog names. Escape cause: wrong-requirement. | spec/tests.md TC-005, TC-017, TC-018, TC-058, TC-065, TC-075 |
| FND-003 | medium | `quire coverage` reports `status-column-matches-nothing`: the `functional-coverage` traceability declaration in `spec-artifacts-process` reads a status column named `Status`, while the `TestMatrix` archetype in the same manifest asserts the column is named `Coverage Status`. Status classification is therefore skipped and a complete-but-unbacked FR row cannot be detected. The two declarations are in one manifest and disagree with each other; this module cannot fix it from here and must not rename a column the archetype asserts. Reproduced identically on the merged `spec-objects-business` branch. Filed as `agent-ix/spec-artifacts-process#81`. Escape cause: correct-requirement-no-evidence. | spec/tests.md, `spec-artifacts-process/manifest.yaml` |
| FND-004 | low | `quire coverage` reports `no-symbol-bound`: the fourteen existing python evidence symbols carry no `@pytest.mark.trace` marker, so every matrix row reads as unbacked. This is the pre-implementation state, not a defect; the plan lands the tags. | tests/test_basic.py, tests/test_manifest.py, tests/test_skeletons_and_validate.py |
| FND-005 | low | US-001 carries illustrative examples (US-001-EX-1..3) rather than Given/When/Then acceptance criteria, so the checklist item "≥ 2 acceptance criteria" is met by the examples plus the FR criteria they lead to. This follows the `spec-artifacts-iso` US skeleton, which keeps verification out of stories. No change. | US-001 |
| FND-006 | low | No FR carries an `## Options` section; the design choice (TypeSpec over hand-authored schemas) is recorded in US-001 Options and in the ticket's authoring contract, so an FR-level options table would repeat it. No change. | FR-002..FR-005 |
| FND-007 | low | `quire coverage` reports `catch-all-universal`: 7 of 7 documents binding extractable criteria name a specific property shape for none of them. The criteria here are example-shaped refusals over hand-built and extracted records rather than quantified properties, so `Property`-typed rows would overclaim. No change. | spec/functional/*, spec/non-functional/NFR-001 |
| FND-008 | low | TC-002..TC-004 and TC-070 trace to `IT-001-SC-*` / `IT-002-SC-*` alongside their FR criteria. No `trace_target` declaration exists for the `IT` archetype, so those SC ids mint nothing and only the FR criterion in the same cell binds the row. Kept for human traceability, matching the sibling module. | spec/tests.md |

## Coverage Rules

1. Coverage: every AC and named constraint has ≥ 1 TC (FR-001: 4 AC; FR-002: 9 AC + 5 CON; FR-003: 7 AC + 2 CON; FR-004: 14 AC + 3 CON; FR-005: 9 AC + 3 CON; NFR-001: 4 metrics with 4 matching AC; StR-001: 3 VC; IT-001: 4 SC; IT-002: 6 SC).
2. Option permutation: both Properties forms × the three alternate-form types (TC-051), all seven object types (TC-030..TC-043, TC-050).
3. Constraint boundary: zero/one identity field, zero/one temporal field, absent/present unit, empty/one-item arrays, `StageDecl.order` 0 versus 1 (TC-031..TC-038).
4. Error path: digest mismatch, unknown manifest key, both Properties forms, dangling clause, non-Identifier token, out-of-set relation verb, `measure` on an objective, `targets` on a KPI (TC-013, TC-026, TC-041, TC-042, TC-054, TC-057).
5. State transition: availability states `available`/`not_applicable`/`unavailable` per declaration kind (TC-053).
6. Edge case: empty record, legacy 0.1.0 artifact, unresolved placeholder target (TC-038, TC-039, TC-061..TC-063).

## Dispositions

| Finding | Disposition |
|---|---|
| FND-001 | Applied: FR-001-AC-1..4 Verification cells changed to `Test`. |
| FND-002 | Applied: TC-017, TC-018, TC-058, TC-065 retyped `Inspection`; TC-005 and TC-075 retyped `Demonstration`; the `## Coverage Gaps` wording follows. |
| FND-003 | Recorded, no change: filed upstream as `agent-ix/spec-artifacts-process#81` rather than worked around; neither column is renamed here because the archetype asserts `Coverage Status`. |
| FND-004 | Recorded, no change: discharged by the implementation, which lands `@pytest.mark.trace` on every test. |
| FND-005..FND-008 | Recorded, no change. |
