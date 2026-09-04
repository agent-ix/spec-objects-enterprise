---
id: SR-002
title: "Integrity analysis of the issue #4 semantic module contract specification"
type: SpecReview
analysis: integrity
scope: "spec/spec.md, spec/stakeholder/StR-001, spec/usecase/US-001, spec/functional/FR-001..FR-005, spec/non-functional/NFR-001, spec/tests.md"
review_set: all
---
# Integrity analysis of the issue #4 semantic module contract specification

## Summary

Completeness, consistency and atomicity gate over the seven-type semantic
module contract. The traceability chain closes for the new work
(US-001 → FR-002..FR-005 → StR-001; NFR-001 constrains FR-003..FR-005;
IT-001 verifies FR-001, IT-002 verifies FR-003) and every FR criterion has a
verification method from the declared class set. Atomicity is clean: `quire
validate --summary` reports 19/19 documents grammar-clean with zero
`ears:non-singular` and zero `ears:unclassifiable` findings after this round.

Three integrity defects were found and applied. FR-001 traced to no
stakeholder requirement, so the oldest requirement in the bundle hung off the
chain the matrix claims. The `$ref` normalization in FR-002 performed a lookup
over two sources (this module's emitted files and semantic-core) with no
stated tie-break. And the central KPI rule — "≥ 1 measured field" — silently
excluded the two most common enterprise measures, a count and a ratio, because
neither carries a dimensional unit; the fix names the UCUM unity symbol `1`
rather than weakening the rule.

The definition / measurement boundary was re-derived rather than assumed. It
rests on three item rules over the extracted `fields` (≥ 1 unit-bearing field,
0 identity fields, 0 `Timestamp`-targeted fields) plus two seal exclusions
(`Objective` admits no `measure`, `Kpi` admits no `targets`). Those five rules
were checked against the record shapes the engine actually produces: a probe
run of `quire.extract_semantic` 0.46.0 confirms `type.unit` is populated from a
trailing ` [symbol]` cell in both the typed table and the `sysml` fence, so the
rule is expressible in the authored Markdown and is not a schema-only claim.

Pairwise distinctness (FR-004-AC-1) was checked exhaustively over all 21 pairs
of the seven types and holds; the two closest pairs are Objective / ValueStream
(separated only by the temporal-field item rule) and Decision / Principle
(separated only by Principle forbidding `fields`), and both separations are
asserted by a criterion rather than left implicit.

## Verdict

**CONDITIONAL** — no high finding; three mediums applied, five lows recorded.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | FR-001 carried no relationship to any stakeholder requirement, so the completeness rule "every FR maps to ≥ 1 StR" failed for it while `spec/tests.md` claims StR-001 traces to FR-001..FR-005. Escape cause: missing-requirement. | FR-001 frontmatter, spec/tests.md Stakeholder Requirement Coverage |
| FND-002 | medium | FR-002's normalization step is a lookup over two sources (files this module emitted, and semantic-core models) and stated no tie-breaking policy for a name present in both, which the hidden-assumption probe for multi-source lookup requires as an explicit decision. Escape cause: missing-requirement. | FR-002 Behavior |
| FND-003 | medium | The `Kpi` "≥ 1 measured field" rule reads `type.unit` presence, and a count ("orders delivered") or a ratio ("share of orders") carries no dimensional unit, so the rule as written refused two of the commonest KPI definitions while claiming to type them. UCUM expresses the dimensionless case as the unity symbol `1`, which the engine accepts (`Integer [1]`, `Decimal(5,2) [%]` both extract `type.unit`). Escape cause: wrong-requirement. | FR-004 Behavior, FR-005 Behavior, FR-004-AC-5 |
| FND-004 | low | FR-004's item rules read as if they applied to every artifact of the type, while the engine assembles a declaration record only for an artifact declaring frontmatter `object:`. NFR-001 depends on exactly that distinction; leaving it implicit in FR-004 made NFR-001's Verification section look like an exemption granted rather than a mechanism measured. Stated explicitly. Escape cause: correct-requirement-no-evidence. | FR-004 Behavior, NFR-001 Verification |
| FND-005 | low | FR-002-AC-1 names the emitted set by indirection ("the support models FR-004 Outputs names") rather than a literal count, so a model added to FR-004 without a matching schema cannot be caught by reading AC-1 alone. The indirection is deliberate — a literal count would have to be re-edited on every model change and would drift silently — and `make schemas-check` catches the real drift. No change. | FR-002-AC-1, FR-004 Outputs |
| FND-006 | low | FR-002 delegates to two external binaries (`node`, `tsp`). The hidden-assumption probe asks for a minimum version, a detection method, and a user-facing error; all three are stated in FR-002 Behavior and Inputs rather than in an NFR. Placing them in the FR keeps one requirement per obligation, and no other requirement contradicts them. No change. | FR-002 Inputs, FR-002 Behavior |
| FND-007 | low | FR-003 and NFR-001 both oblige the 0.1.0 locators to stay unchanged. This is not a duplicate with different wording: FR-003 states the manifest obligation and NFR-001 states the compatibility bound the obligation exists to hold, and the two are cross-linked. No change. | FR-003 Behavior, NFR-001 Statement |
| FND-008 | low | `Decision` and `Capability` both admit `relations` and `clauses` and differ in required keys only; a reader could take them for near-duplicates. They are separated by required key (`clauses` versus `fields`) and by a forbidden key on neither, which FR-004-AC-1 asserts pairwise, so the overlap is intended vocabulary reuse rather than a duplicated requirement. No change. | FR-004 table |

## Traceability Matrix

| US | FR/SR | StR | Verification |
|---|---|---|---|
| — | FR-001 | StR-001 (VC-1) | TC-001..TC-004, IT-001 |
| US-001 | FR-002 | StR-001 (VC-3) | TC-010..TC-019, TC-071..TC-074 |
| US-001 | FR-003 | StR-001 (VC-1, VC-3) | TC-020..TC-028, IT-002 |
| US-001 | FR-004 | StR-001 (VC-3) | TC-030..TC-043, TC-075 |
| US-001 | FR-005 | StR-001 (VC-2, VC-3) | TC-050..TC-059, TC-064, TC-065 |
| US-001 | NFR-001 | StR-001 (VC-2) | TC-060..TC-063 |

## Dispositions

| Finding | Disposition |
|---|---|
| FND-001 | Applied: FR-001 frontmatter gained `traces_to ix://agent-ix/spec-objects-enterprise/StR-001`. |
| FND-002 | Applied: FR-002 Behavior gained three rules — module-emitted names resolve to the module base, everything else to the semantic-core base, and the collision the tie-break would decide is impossible under FR-004-CON-1. |
| FND-003 | Applied: FR-004 Behavior gained the unity-symbol rule; FR-005 Behavior obliges the `kpi` skeleton to show `[1]` on a dimensionless row. The rule was extended to admit the dimensionless case, never relaxed to drop the measured-field requirement. |
| FND-004 | Applied: FR-004 Behavior states that the item rules reach an assembled record only, naming NFR-001's mechanism. |
| FND-005..FND-008 | Recorded, no change. |
