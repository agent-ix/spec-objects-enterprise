---
id: SR-007
title: "Risk and complexity analysis of the issue #4 semantic module contract specification"
type: SpecReview
analysis: risk-complexity
scope: "spec/stakeholder/StR-001, spec/functional/FR-001..FR-005, spec/non-functional/NFR-001"
review_set: all
---
# Risk and complexity analysis of the issue #4 semantic module contract specification

## Summary

Two-axis scoring (technical risk, volatility) over the seven requirements,
with mitigations for every High. Nothing here touches concurrency, a security
boundary, or a quantified latency budget, so the technical-risk profile is
driven entirely by **novel technology**: the TypeSpec emission toolchain and
the semantic layer of Quire 0.46.0 are both first use in this repository.

The single High/High item is FR-005, and the reason is worth stating plainly:
its acceptance criteria are discharged by a Quire wheel that exists on no index
this repository may commit a dependency against. `internal-pypi` serves 0.33.0
at most, no `quire-rs` tag carries the semantic layer, and the diagnostic the
criteria assert (`semantic.record-invalid`) exists in quire-rs source but in no
quire-rs acceptance criterion — `agent-ix/quire-rs#391` is where that contract
is still being settled. The mitigation is not to soften the criteria: it is the
`make dev-quire` target plus the fail-not-skip policy, so the day the engine
moves under the module the suite goes red instead of quietly green. That policy
is itself the mitigation for the volatility, and it is already specified.

FR-004 is the highest-value, lowest-volatility item and is where a spike pays:
the definition / measurement boundary is expressed through `@contains` markers
and an `@extension("allOf", …)` clause, and the emitter's behaviour on two
`allOf` entries over one array is the one thing in the module that could turn
out not to compile as designed. It was de-risked before authoring — a probe run
of `quire.extract_semantic` 0.46.0 confirmed that `type.unit` and
`type.decimal` populate from both the typed table and the `sysml` fence, and
that both forms extract to identical `FieldDecl[]` — so the remaining unknown
is emitter mechanics, not engine semantics.

The `catch-all-universal` result from `quire coverage` (no criterion in the
bundle names a property shape) is recorded as a complexity signal rather than a
defect: the whole contract quantifies over closed enumerations, which is what
makes it cheap to verify exhaustively and expensive to verify generatively.

## Verdict

**CONDITIONAL** — one High/High requirement (FR-005) and one High/Low (FR-004),
both with named mitigations already in the specification; no unmitigated High.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | FR-005 is High on both axes: every one of its nine criteria needs a Quire wheel that is on no committable index (`agent-ix/quire-rs#392`), and the `semantic.record-invalid` diagnostic they assert is an unpinned neighbour contract still being settled in `agent-ix/quire-rs#391`. Without a stated policy, an absent engine would turn the whole requirement into skipped rows reported as coverage. Escape cause: correct-requirement-no-evidence. | FR-005 Inputs, FR-005 Behavior, spec/tests.md Test Environment |
| FND-002 | medium | FR-004 is High technical risk: the item rules depend on the official emitter accepting two `@extension("allOf", …)` `contains` clauses over one array, which no other module in the programme exercises — the sibling `spec-objects-business` uses exactly one. If the emitter refuses the second clause, the temporal and measured rules cannot both be expressed and the KPI identity claim has to be re-derived. Escape cause: correct-requirement-no-evidence. | FR-004 Behavior, FR-004-AC-5, FR-004-AC-6 |
| FND-003 | medium | FR-002 is High technical risk on novel technology alone: this repository has never run `tsp compile`, and the digest chain (`$id` → schema bytes → `data_schema.digest` → `toolchain.json`) means a single non-determinism in the emitter turns every downstream criterion red at once. Escape cause: correct-requirement-no-evidence. | FR-002 Behavior, FR-002-CON-3, FR-002-CON-5 |
| FND-004 | low | FR-003 is Medium/High volatility: the `semantic` block's admitted key set is `agent-ix/quoin` FR-070's to change, and the module-manifest schema is pinned only by a revision (`a77f31e`), not by a released version. A consumer vendoring a different copy is a skew defect on that consumer, which FR-003 Inputs already states. No change. | FR-003 Inputs |
| FND-005 | low | NFR-001's population is seven checked-in skeletons — small enough that the compatibility claim is exhaustively verified and large enough to be meaningful, but it says nothing about the corpus, which is what `agent-ix/quoin#291` sweeps. The NFR is explicit that it measures the checked-in set only; recorded so the number is not read as a corpus result. No change. | NFR-001 Statement, NFR-001 Verification |
| FND-006 | low | `quire coverage` reports `catch-all-universal` for all seven documents binding extractable criteria. This is a consequence of a contract over closed enumerations, not an authoring defect, and the evidence lens records the decision not to take the `property-based-testing` recommendations. No change. | spec/reviews/4-semantic-module-contract/evidence.md |

## Risk Register

| Req | Tech Risk | Volatility | Drivers | Mitigation |
|---|---|---|---|---|
| StR-001 | Low | Low | A stable stakeholder need; VC-3 added by this issue restates it for typed consumers. | None needed. |
| FR-001 | Low | Low | Unchanged activation behaviour; only its verification-method cells were corrected. | Re-verified by TC-001; the integration rows stay `🚧`. |
| FR-002 | High | Low | First use of `@typespec/compiler` 1.15.0 and the official JSON Schema emitter in this repo; a digest chain where one non-deterministic byte fails every downstream criterion. | Exact toolchain pins recorded in `toolchain.json`; determinism asserted as FR-002-CON-3 (TC-016); `make schemas-check` wired into `make lint` so drift fails before push; the sibling module's generator is the proven starting point. |
| FR-003 | Medium | High | The `semantic` key set belongs to quoin FR-070; the manifest schema is pinned by revision, not release; two engine defects make a refusal silent. | Key set asserted exactly (TC-020); digests asserted against shipped bytes (TC-021); the silent-refusal half of AC-6 carried as an expected failure naming `quire-rs#221` and `#394`. |
| FR-004 | High | Low | Two `allOf` `contains` clauses over one array, unexercised elsewhere in the programme; the KPI identity claim rests on them. | Spike first: emit `Kpi.json` and `Objective.json` before any other model and check both `contains` clauses survive; engine semantics already de-risked by an `extract_semantic` probe; 21-pair distinctness asserted by TC-030. |
| FR-005 | High | High | Nine criteria discharged only by a Quire wheel on no committable index; the asserted diagnostic is an unpinned neighbour contract. | `make dev-quire` provisioning target; fail-not-skip policy so no row is green without the engine; the two blocked halves named as expected failures against `quire-rs#391`/`#392`; ten negative fixtures pin the refusals rather than trusting them. |
| NFR-001 | Low | Medium | Measures seven checked-in skeletons; the corpus behaviour it is often mistaken for belongs to `quoin#291`. | Baseline of the 0.1.0 locators and skeletons checked in and diffed (TC-060..TC-063); the Verification section states the population explicitly. |

## Top hazards

1. **FR-005 / the engine dependency** — the only requirement whose evidence
   cannot be produced from a committed dependency. Review the fail-not-skip
   policy live before planning; if it is weakened to a skip, every row it backs
   becomes unfalsifiable.
2. **FR-004 / the two-`contains` expression** — spike `Kpi.json` and
   `Objective.json` first. If the emitter refuses the second `allOf` clause,
   the KPI definition / measurement rule needs a different expression and the
   ticket's headline acceptance criterion moves.
3. **FR-002 / the digest chain** — one emitter non-determinism fails FR-002,
   FR-003 and FR-005 together. TC-016 is the canary and should run early.
4. **FR-003 / quoin FR-070 volatility** — the admitted `semantic` key set is a
   neighbour's contract; a change there is a manifest change here, not a
   schema change, and the exact-key assertion (TC-020) is what makes the
   breakage visible rather than silent.

## Failure-domain gaps

See `spec/reviews/4-semantic-module-contract/failure-domain.md`. Open gaps:
none. Four findings from that lens were applied (dimensionless measures, named
uniqueness keys, acyclic `decomposes`/`supersedes`, inert clause text) and four
are recorded as allocated elsewhere (silent loader refusal to `quire-rs#221`/
`#394`, unbounded decomposition depth to the consuming frontends, optional
`targets` to `quoin#335`, unbounded stage count to consumers).

## Dispositions

| Finding | Disposition |
|---|---|
| FND-001 | Recorded, mitigation already specified: `make dev-quire`, fail-not-skip, and the two named expected failures. No requirement is softened. |
| FND-002 | Accepted into the plan: FR-004's `Kpi`/`Objective` models are emitted first as a spike before the remaining five models are written. |
| FND-003 | Recorded, mitigation already specified: exact pins, `toolchain.json`, TC-016, and `make schemas-check` in `make lint`. |
| FND-004..FND-006 | Recorded, no change. |
