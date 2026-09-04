---
id: SR-005
title: "Verification and evidence analysis of the issue #4 semantic module contract specification"
type: SpecReview
analysis: evidence
scope: "spec/functional/FR-001..FR-005, spec/non-functional/NFR-001, spec/tests.md"
review_set: all
---
# Verification and evidence analysis of the issue #4 semantic module contract specification

## Summary

`quoin advise` was run over the bundle rather than recalled: it reports 51
obligations (43 FR acceptance criteria, 4 NFR acceptance criteria, 4 NFR
measurement metrics), of which **1 mismatch, 0 uncatalogued, 0 inconclusive**.
Every method authored in a `Verification` cell is a declared class, and the
`uncatalogued-verification-method` finding that `quire coverage` raised against
FR-001's `Schema Test` / `Integration Test` cells was cleared in the base round.

The single mismatch is FR-003-AC-5, authored `Demonstration` where the advisor
recommends `unit-testing` / `bdd-spec-by-example`. The authored method is
confirmed by judgement and the judgement is recorded here rather than presented
as a verdict: the criterion runs `quoin module install path:` against a Quoin
built from `agent-ix/quoin` main at or after `3e842ce`, and no release tag
carries the semantic module installer. There is no automated harness this
repository can stand up, so an example-based test would be a test that cannot
run — a green row over an absent binary. `Demonstration` says what is true: a
human runs it and records the result. The row stays `🚧` in the matrix until
someone does.

The advisor recommends `property-based-testing (universal)` on 22 obligations.
That recommendation is read here as what it is — a rule keyed on universal
quantifiers in the statement ("every schema", "each of the seven") — and is
**not** taken. The population these criteria quantify over is closed and small:
seven object types, twenty-six support models, ten skeletons, ten negative
fixtures. A generator over a closed enumeration is an enumeration with extra
machinery, and `quire coverage` already reports `catch-all-universal` for the
whole bundle, meaning it could not name a property shape for a single
criterion. The matrix therefore enumerates rather than generates, and this
paragraph is the record of that judgement.

Two recommendations are rejected outright as rule misfires, and are named so
that a later reader does not take the silence for an oversight:
`dast`/`iast`/`negative-abuse-testing` on FR-004-AC-6 and FR-005-AC-7, matched
on refusal vocabulary ("fails", "refuses", "placeholder"), describe an attack
surface. This module has none: it ships Markdown and JSON and runs no service.
`concolic-execution` was not recommended for any obligation and is not used.

Suite planning is the one real gap, and it is a gap in the plan rather than in
the spec: no `SuiteRegistry` document declares a producer for the `Unit`,
`Integration`, `Inspection`, `Demonstration` and `Manual` evidence kinds, and
no `Inspections` document exists to discharge the eight non-automated rows.
`quire coverage` reports both as `archetype-matches-nothing`. The sibling
module `spec-objects-business` shipped with the same two absences and they are
carried identically here.

## Verdict

**CONDITIONAL** — one mismatch confirmed by recorded judgement; two evidence
artifacts (`SuiteRegistry`, `Inspections`) absent and carried by the plan.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | FR-003-AC-5 is authored `Demonstration`; the advisor recommends `unit-testing`/`bdd-spec-by-example`. Confirmed as authored by judgement: the criterion needs a Quoin built from `quoin` main ≥ `3e842ce`, which no release carries, so an automated row would be green over an absent binary. Escape cause: correct-requirement-no-evidence. | FR-003-AC-5, spec/tests.md TC-027, TC-070 |
| FND-002 | medium | No `SuiteRegistry` document declares which suite produces each evidence kind, and no `Inspections` document discharges the `Inspection`, `Demonstration` and `Manual` rows (TC-005, TC-006, TC-017, TC-018, TC-027, TC-058, TC-065, TC-070); `quire coverage` reports both declarations as `archetype-matches-nothing`. The obligations have methods; nothing states which artifact proves them. Escape cause: correct-requirement-no-evidence. | spec/tests.md Coverage Gaps, `spec-artifacts-process` traceability declarations |
| FND-003 | low | The advisor recommends `property-based-testing (universal)` on 22 of 51 obligations. Not taken: each quantifies over a closed enumeration (7 types, 26 support models, 10 skeletons, 10 negatives) that the matrix enumerates directly, and `quire coverage` reports `catch-all-universal` — it could name a property shape for none of them. Judgement recorded rather than defaulted. No change. | FR-002-AC-2/3/5, FR-004-AC-1..5/7/8/11/12/14, FR-005-AC-1/4/5/6/8, NFR-001-AC-1..3 |
| FND-004 | low | `dast`, `iast` and `negative-abuse-testing` are recommended for FR-004-AC-6 and FR-005-AC-7, matched on refusal vocabulary. The module ships Markdown and JSON and exposes no runtime surface, so there is no attack surface to drive. Rejected, and named here so the omission is a decision. No change. | FR-004-AC-6, FR-005-AC-7 |
| FND-005 | low | `performance-benchmarking (quantified-threshold)` is recommended for the four NFR-001 metrics because each carries a numeric target. All four targets are counts of findings (`0 locators changed`, `0 error findings`, `0 warnings`, `identical yields`), not rates or latencies, so `Test` is the correct class and a benchmark harness would measure nothing. No change. | NFR-001 Measurement and Evaluation |
| FND-006 | low | `golden-approval-testing (stable-output)` is recommended for NFR-001-AC-4 (byte-identical yields under 0.1.0 and 0.2.0). The authored `Test` discharges it as a checked-in baseline compared byte-for-byte, which is golden-approval testing under another name; the class value stays `Test` because that is the declared class the catalog admits in the cell. No change. | NFR-001-AC-4, spec/tests.md TC-063 |

## Method Confirmation

| Obligation set | Authored | Confirmed | Basis |
|---|---|---|---|
| FR-001-AC-1..4 | Test | Test | Advisor: example / universal; corrected from the uncatalogued `Schema Test`/`Integration Test` in the base round. |
| FR-002-AC-1..9 | Test | Test | Advisor: example on 5, universal on 3, temporal on AC-8; the temporal case is the version-bump procedure, discharged by an end-to-end bump-and-check run rather than a model checker. |
| FR-003-AC-1..4, AC-6, AC-7 | Test | Test | Advisor agrees. |
| FR-003-AC-5 | Demonstration | Demonstration | Mismatch confirmed by judgement (FND-001). |
| FR-004-AC-1..14 | Test | Test | Advisor: universal on 10, example on 2, security misfire on AC-6 (FND-004), stakeholder-acceptance on AC-10 — the last discharged by the extractor run the criterion already names. |
| FR-005-AC-1..9 | Test | Test | Advisor agrees on 3, universal on 5, security misfire on AC-7 (FND-004). |
| NFR-001-AC-1..4, M-1..M-4 | Test | Test | FND-005, FND-006. |

## Dispositions

| Finding | Disposition |
|---|---|
| FND-001 | Confirmed as authored: `Demonstration` stays on FR-003-AC-5, and TC-027 / TC-070 stay `🚧` with the Quoin-build reason named. |
| FND-002 | Recorded, carried by the plan: the two evidence artifacts are named in `spec/tests.md` `## Coverage Gaps` as absent, matching the sibling module; nothing is reported green in their place. |
| FND-003..FND-006 | Recorded, no change; each is a rule misfire or a recommendation declined by recorded judgement. |
