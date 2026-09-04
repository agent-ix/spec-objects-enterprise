---
id: SR-006
title: "EARS requirement-grammar analysis of the issue #4 semantic module contract specification"
type: SpecReview
analysis: ears-conformance
scope: "spec/stakeholder/StR-001, spec/functional/FR-001..FR-005, spec/non-functional/NFR-001"
review_set: all
---
# EARS requirement-grammar analysis of the issue #4 semantic module contract specification

## Summary

Engine check plus semantic judgment over the requirement-bearing artifacts
(StR-001, FR-001..FR-005, NFR-001; US-001 and the matrix are out of scope for
this lens). `quire validate --scope . "spec/**/*.md" --summary` reports
**24/24 documents grammar-clean, 0 grammar findings** across roughly 119
`shall`-bearing statements. Six `ears:non-singular` and two
`quality:agentless-passive` findings were raised during authoring and every one
was fixed by splitting the statement or naming the performing component, not by
suppressing the check — the fixed statements are recorded below so the clean
run is not read as a spec that never had defects.

The semantic pass — the part the engine cannot do — checked three things the
lexicon lets through: whether a `When` clause names a momentary event or a
continuous state, whether a response that avoids the vague-verb list is
nevertheless unmeasurable, and whether any unwanted condition is written as
`When …` where `If … then …` is meant. All the unwanted conditions in FR-002
(compile failure, wrong Node, base/version disagreement, drift, stale file) use
`If … then …` correctly, and the two `When …` clauses in FR-002 and FR-003
name real events (`When no $id or $ref is relative`, `When the install has
completed`). The thirteen `Where …` clauses in FR-004 and FR-005 are the
optional-feature pattern used for its purpose — a key the extractor does not
populate, a type that declares operations — and are correct.

Two low findings remain, both about responses that pass the lexicon and are
still soft; neither changes what gets built, and both are already carried by a
measurable criterion elsewhere.

## Verdict

**PASS** — no high or medium finding; the engine reports zero grammar findings
and the two remaining lows are recorded without change.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | low | StR-001's Stakeholder Need closes on "so that tier-2 enterprise architecture can be authored and consumed as first-class graph objects", which passes the vague-verb lexicon but is not measurable as written. The measurable form is StR-001-VC-1..VC-3, which the matrix traces; the Need is the rationale half of the artifact and is correctly informal. Pre-existing wording. No change. | StR-001 |
| FND-002 | low | FR-004 Behavior's "Each schema SHALL describe the declared shape only, never a runtime occurrence" uses `describe`, an abstract response. It is made concrete by the parenthetical (a measured reading, a dated review, a scored assessment) and measured by FR-004-AC-14 and FR-004-CON-3, so rewriting it would move the concreteness away from where a reader meets it. No change. | FR-004 Behavior, FR-004-AC-14 |
| FND-003 | low | FR-002's "In `--check` mode the generator SHALL write no file" is a state-driven obligation phrased as a prepositional clause rather than `While the generator runs in --check mode, …`. The engine's `non-canonical-trigger` check accepts it and the obligation is unambiguous; the canonical rewrite would add words without adding meaning. No change. | FR-002 Behavior |
| FND-004 | low | FR-001's Behavior section states two obligations in two adjacent sentences of one paragraph ("The manifest SHALL validate …" / "Re-activation SHALL be a no-op …"). The engine reads them as two statements and both are clean; the paragraph shape is pre-existing and splitting it into bullets would touch a requirement this issue does not otherwise change. No change. | FR-001 Behavior |

## Statements Corrected During Authoring

| Statement | Check | Fix |
|---|---|---|
| FR-002 Behavior, relative `$ref` normalization | `ears:non-singular` | Split into three statements: module-emitted names resolve to the module base, everything else to the semantic-core base, and the collision is impossible under FR-004-CON-1. |
| FR-004 Behavior, seal and forbidden keys | `ears:non-singular` | Split into "no model declares such a key" and "each model seals its record". |
| FR-004 Behavior, `Objective`/`Kpi` mutual exclusion | `ears:non-singular` | Split into one statement per model. |
| FR-004 Behavior, `OwnershipDecl` | `ears:non-singular` | Split into the shape statement and the no-role/no-score statement. |
| FR-004 Behavior, relation-verb narrowing | `quality:agentless-passive` | Subject named: "The TypeSpec source SHALL narrow …". |
| FR-004 Behavior, `$ref` validation and verb narrowing | `ears:non-singular` | Split into "each model SHALL validate every item by `$ref`" and "the TypeSpec source SHALL apply the narrowing over that `$ref`". |
| FR-004 Behavior, `StageDecl.order` and `TargetDecl.measure` reader rules | `ears:non-singular` | Split into one rule per statement plus a third statement carrying the not-a-schema-refusal note. |
| FR-004 Behavior, self-reference and acyclicity | `ears:non-singular` | Split into the irreflexivity statement and the acyclicity statement. |
| FR-005 Behavior, OCL clause inertness | `ears:non-singular`, then `quality:agentless-passive` | Split into "the clause text SHALL be carried verbatim, never evaluated" and "the test suite SHALL assert identity, language and source span only". |

## Dispositions

| Finding | Disposition |
|---|---|
| FND-001..FND-004 | Recorded, no change; each is a soft response already discharged by a measurable criterion, or a pre-existing paragraph this issue does not otherwise touch. |
