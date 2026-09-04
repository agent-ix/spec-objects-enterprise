---
id: SR-003
title: "Failure-domain analysis of the issue #4 semantic module contract specification"
type: SpecReview
analysis: failure-domain
scope: "spec/functional/FR-002, spec/functional/FR-004, spec/functional/FR-005, spec/non-functional/NFR-001, spec/tests.md"
review_set: all
---
# Failure-domain analysis of the issue #4 semantic module contract specification

## Summary

Extension points, entity identity, evaluation purity and topological
robustness, checked against the seven object-type contract and the engine
behaviour measured on quire 0.46.0.

**Identity** is where this module's risk concentrates, because the ticket's own
headline criterion is an identity claim: a metric definition must not be
mistaken for a measured value. The specification carries that as five rules
(≥ 1 unit-bearing field, 0 identity fields, 0 `Timestamp` fields on `Kpi`;
`Objective` admits no `measure`; `Kpi` admits no `targets`). This analysis
attacked those rules with the shapes a real KPI takes and found one true hole,
now closed by the integrity round: a count or a ratio carries no dimensional
unit and was refused. Two further identity keys were undeclared — the
uniqueness key of `stages`, `outcomes`, and `alternatives` items — and are now
stated.

**Topology** is the second cluster. Nothing forbade a capability from
`decomposes`-ing itself, a decision from `supersedes`-ing itself, or either
graph from carrying a cycle, and the `principle` type's `governs: ["*"]`
wildcard admitted a principle governing itself. None of the four is
expressible in JSON Schema, so each is now an explicit reader rule with the
non-claim stated beside it, rather than an unstated assumption a downstream
traversal would discover.

**Purity** is clean and now explicit: the OCL clause text is carried verbatim
and is never evaluated, parsed, or asserted here, and no requirement reads a
clock, a network, or an environment value into a declaration. The one
environment dependency in the whole module — the pinned TypeSpec toolchain
under `node_modules` — is confined to the emission step and gated by
`toolchain.json` plus `make schemas-check`.

**Extension points**: this module registers no callback, hook, or plugin. The
one trust boundary is the Quire loader, whose failure behaviour is *silent*
(`quire-rs#221` empties the model on an unknown key, `quire-rs#394` drops an
object type on a digest mismatch, neither naming what it refused). That is a
strict-versus-resilient choice the engine made, not one this module may make;
the specification carries it as an expected failure naming both issues rather
than as a workaround.

## Verdict

**CONDITIONAL** — one high finding (the dimensionless-measure hole in the
module's central identity rule) was found and closed in the integrity round;
three mediums applied; four lows recorded.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | high | Identity: the `Kpi` "≥ 1 measured field" rule reads `type.unit`, so a KPI whose measure is a count or a ratio — the two commonest enterprise KPI shapes, and both of the shapes the shipped 0.1.0 `kpi` skeleton describes in prose — carried no unit and was refused as a definition. The rule that exists to separate definitions from readings therefore rejected legitimate definitions. Closed by naming the UCUM unity symbol `1`. Escape cause: wrong-requirement. | FR-004 Behavior, FR-004-AC-5, FR-005 Behavior |
| FND-002 | medium | Identity: `stages`, `outcomes`, and `alternatives` are arrays of named declarations with no stated uniqueness key, so two stages named `Pick` in one value stream were admissible and a consumer had no key to join on. Escape cause: missing-requirement. | FR-004 Behavior |
| FND-003 | medium | Topology: nothing forbade a self-referential or cyclic `decomposes` (capability) or `supersedes` (decision) relation, so a consumer traversing either graph had no stated termination guarantee. Escape cause: missing-requirement. | FR-004 Behavior, manifest `allowed_links` |
| FND-004 | medium | Purity: FR-005 obliged each clause to own an `ocl` fence but never said the fence text is inert, leaving open whether a test may parse or evaluate it — the exact scope creep `agent-ix/quire-contract-ir#52` owns. Escape cause: missing-requirement. | FR-005 Behavior |
| FND-005 | low | Topology: the `principle` type's `allowed_links` is `governs: ["*"]`, which admitted a principle governing itself. Stated as a reader rule beside the other two. Escape cause: missing-requirement. | FR-004 Behavior, manifest `allowed_links` |
| FND-006 | low | Extension point: the Quire loader's refusal policy is silent for both an unknown `semantic` key and a digest mismatch, so a module this specification declares correct can be seen as absent by a consumer with no diagnostic. The policy belongs to the engine; carried as an expected failure naming `quire-rs#221` and `quire-rs#394` rather than worked around by, for example, inlining the schema. No change here. | FR-003 Behavior, spec/spec.md Out of Scope |
| FND-007 | low | Topology: capability decomposition depth and value-stream stage count are unbounded. This module performs no traversal — it declares shapes — so a depth bound would be a constraint on consumers it cannot enforce. Allocated to the consuming frontends (`quire-contract-ir#52`, `filament-core-data#36`). No change. | FR-004 Behavior |
| FND-008 | low | Identity: an `objective` may declare no `targets`, so a time-bound objective measured by nothing validates. `targets` cannot be required because no extractor populates it (FR-004 Behavior), and requiring an unpopulated key would make every skeleton fail. Recorded as a known consequence of the extraction gap `agent-ix/quoin#335` owns. No change. | FR-004 table, spec/spec.md Out of Scope |

## Checklist

| Area | Result |
|---|---|
| Extension points (trust boundaries) | No callback, hook, or plugin is registered. The one boundary is the Quire loader; its failure behaviour is silent-drop, owned by `quire-rs#221`/`#394`, carried as an expected failure (FND-006). |
| Entity identity | `fields`/`operations`/`params` unique by `name` (semantic-core reader rules); `stages`/`outcomes`/`alternatives` unique by `name` (FND-002, applied); `StageDecl.order` unique and contiguous; skeleton `title` unique and an `Identifier` (FR-005-AC-8); KPI definition versus reading separated by five rules (FND-001, applied). |
| Evaluation purity | Clause text inert and never evaluated (FND-004, applied); no clock, network, or environment read in any declaration; emission deterministic (FR-002-CON-3) and confined to `schemas/` plus manifest digests. |
| Topological robustness | `decomposes` and `supersedes` acyclic and irreflexive (FND-003, applied); a principle does not govern itself (FND-005, applied); unbounded depth allocated to consumers (FND-007). |

## Dispositions

| Finding | Disposition |
|---|---|
| FND-001 | Applied in the integrity round: FR-004 admits the unity symbol `1` as a unit; FR-005 obliges the `kpi` skeleton to demonstrate it. The identity rule was extended to cover the dimensionless case, never relaxed. |
| FND-002 | Applied: FR-004 Behavior states uniqueness by `name` within `stages`, `outcomes`, and `alternatives`. |
| FND-003 | Applied: FR-004 Behavior forbids a self-naming `decomposes`/`supersedes` relation and requires both graphs to be acyclic, with the "not claimed as a schema refusal" note extended to cover them. |
| FND-004 | Applied: FR-005 Behavior states the clause text is carried verbatim and never evaluated, and that the suite asserts identity, language, and source span only. |
| FND-005 | Applied: FR-004 Behavior forbids a principle governing itself. |
| FND-006..FND-008 | Recorded, no change. |
