---
id: SR-008
title: "Scope and boundary analysis of the issue #4 semantic module contract specification"
type: SpecReview
analysis: scope-boundary
scope: "spec/spec.md, spec/functional/FR-001..FR-005, spec/non-functional/NFR-001, spec/integration/IT-001..IT-002"
review_set: all
---
# Scope and boundary analysis of the issue #4 semantic module contract specification

## Summary

System boundary, external dependencies with their assumed-versus-guaranteed
status, and responsibility allocation for all seven requirements.

The module owns three artifacts and nothing else: a manifest, a set of emitted
JSON Schemas, and a set of Markdown skeletons. It runs no service, stores no
state, and performs no traversal. Every behaviour a requirement describes is
either the production of one of those three artifacts or an assertion about how
a named neighbour reads them.

The boundary work that mattered was checking the ticket's four safety gates are
each *allocated* rather than merely mentioned. Three were:
"no management score or trust score" lands on FR-004-CON-3, FR-005-CON-3,
FR-004-AC-14, TC-043 and TC-065; "role changes require evidence from the corpus
review" lands on FR-004's `OwnershipDecl` rule (no role name, no score, no
rating) plus an explicit out-of-scope entry; "no corpus repository is edited"
lands on FR-005-CON-1 and TC-058. The fourth — **advisory-only until
promotion** — appeared only in NFR-001's Rationale, where it read as background
rather than as an obligation anyone discharges. It is now named in the In Scope
list and in NFR-001's Scope, allocated to the two manifest posture keys FR-003
declares.

Five open upstream issues are carried as boundary statements rather than as
work: `quire-rs#392` (the wheel on no committable index), `quire-rs#221` and
`#394` (silent load refusals), `quire-rs#391` (record validation of a legacy
`object:` artifact), and `filament-core-service#23` (reference-form
`data_schema` not resolved into a stored snapshot). Each names its owning issue
and each has a matching expected failure or out-of-scope entry; none is worked
around. The generated-language fixtures are likewise refused rather than faked:
`filament-core-data#21`/`#22`/`#23` produce them, `quoin#290` gates their
publication, and `filament-core-data#11` owns the semantic-core language
packages.

One real asymmetry is recorded and left as it is: FR-003 states that
`quoin module` will list the module after a successful install. That is an
expectation of a neighbour, not an obligation this module discharges, and it is
verified at the boundary by IT-002 rather than by anything under this repo's
control. The sibling module states it identically.

## Verdict

**CONDITIONAL** — one medium (the unallocated advisory-only gate) applied; the
remaining findings are recorded boundary statements.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | medium | The ticket's merge gate "Advisory-only until promotion" was mentioned only in NFR-001's Rationale and in the Out of Scope note about `quoin#291`, so no requirement carried it and no criterion measured it. It is discharged by two manifest posture keys (`compatibility_posture: additive`, `legacy_forms: warning`) that FR-003 already declares and TC-020 already asserts; the gate simply was not named as what those keys are for. Escape cause: correct-requirement-no-evidence. | spec/spec.md In Scope, NFR-001 Scope, FR-003 Behavior |
| FND-002 | low | FR-003 Behavior states "When the install has completed, `quoin module` SHALL list `spec-objects-enterprise`" — an obligation on a neighbour's CLI, not on this module. It is a boundary expectation verified by IT-002 and stated identically by the merged sibling module; rewriting it to a passive expectation would lose the fact that a failure here is a real defect somewhere. No change. | FR-003 Behavior, IT-002 |
| FND-003 | low | FR-002-CON-4 confines `make schemas`/`make schemas-check` to a machine whose user-level npm config routes `@agent-ix` to npm.ix, which excludes the GitHub workflow. The repo's CI is `workflow_dispatch`-only, so no scheduled run can hit the excluded path today, but the exclusion is a standing boundary a later CI change could cross silently. Recorded; resolved upstream when `filament-core-data#11` publishes semantic-core publicly. No change. | FR-002-CON-4, `.github/workflows/ci.yml` |
| FND-004 | low | FR-001-AC-4 and IT-001-SC-03 assert the registry stores the reference-form `data_schema` verbatim, which is only correct while `filament-core-service#23` is open; when it lands, the service will store a resolved snapshot and both criteria change meaning. The dependency is named in Out of Scope, and the criteria are worded to assert what is true today rather than what will be. No change. | FR-001-AC-4, IT-001, spec/spec.md Out of Scope |
| FND-005 | low | Thirteen declared record keys are optional because no extractor populates them (`agent-ix/quoin#335`). That is a boundary between this module's schema vocabulary and quire's Markdown mapping, and FR-004 states that criteria over those keys are verified against hand-built records with the limitation named in the test itself. Recorded so a later reader does not take those rows for extraction evidence. No change. | FR-004 Behavior, spec/tests.md Test Environment |
| FND-006 | low | The module declares `imports: {}` — it imports no other semantic module — while the ticket's Deliverables name "cross-module imports". No enterprise type needs a business or operational type today, and declaring an empty import map is the honest form; a populated one would name a module this ticket does not depend on. Recorded as a deliberate non-delivery of that Deliverables bullet. No change. | FR-003 Behavior, issue #4 Deliverables |

## System Context

```mermaid
flowchart LR
  author([Spec author])
  gen([Agent CLI generator])
  subgraph SUT [spec-objects-enterprise]
    tsp[typespec/main.tsp]
    genr[scripts/generate-schemas.mjs]
    sch[(schemas/*.json)]
    man[manifest.yaml]
    skel[(skeletons/*.md)]
  end
  core[(filament-core-service)]
  quoin[(Quoin installer)]
  quire[(Quire engine)]
  sc[(@agent-ix/semantic-core 0.1.0)]
  tsc[(@typespec/compiler + json-schema 1.15.0)]
  fe[(quire-contract-ir / filament-core-data frontends)]
  sc --> tsp
  tsp --> genr
  tsc --> genr
  genr --> sch
  genr --> man
  author --> skel
  man --> core
  man --> quoin
  skel --> quire
  sch --> quire
  sch --> fe
  skel --> fe
  gen --> skel
```

## In-Scope Responsibilities

- Declare seven enterprise-architecture object types with a role-distinct
  JSON Schema each, emitted from one TypeSpec source.
- Refuse, by schema, a KPI declaration shaped like a measurement of the KPI.
- Publish a manifest carrying the `semantic` block and a reference-form
  `data_schema` (path plus digest) per exported type.
- Ship one executable typed skeleton per type, three alternate-form skeletons,
  and ten negative fixtures that fail for a named reason.
- Hold every 0.1.0 extraction locator and every 0.1.0 skeleton valid under
  0.2.0.
- Ship at an advisory posture (`additive`, `legacy_forms: warning`) until
  corpus promotion.

## External Dependencies

| Dependency | Type | Assumed or Guaranteed | Contract |
|---|---|---|---|
| `filament-core-service` module activation (FR-035, rev `a77f31e`) | HTTP API | Guaranteed | IT-001 (TC-002..TC-004, `🚧` — needs a running instance) |
| Quoin module installer (`quoin` main ≥ `3e842ce`, FR-070/073/075) | Local CLI | Guaranteed | IT-002 (TC-070, `🚧` — no release carries it) |
| Quire engine: registry loader, `extract_semantic`, `validate_document` (0.46.0) | Python wheel | Guaranteed | FR-003 and FR-005 harness (TC-024..TC-026, TC-050..TC-054); the module's Quire contract test, with no IT of its own |
| `@agent-ix/semantic-core` 0.1.0 grammar and reader rules | npm package (npm.ix) | Assumed, partially guaranteed | Assumed per `filament-core-data` FR-031..FR-034; `$ref` resolution guaranteed by TC-012 and TC-040, and by the test schema registry resolving every `$ref` against the installed package |
| `@typespec/compiler` + `@typespec/json-schema` 1.15.0 | npm packages | Assumed, partially guaranteed | Versions recorded in `toolchain.json` (TC-010); determinism guaranteed by TC-016; exact pins guaranteed by TC-018 |
| npm.ix routing for the `@agent-ix` scope | Registry config | Assumed | User-level npm config (FR-002-CON-4); lockfile origin guaranteed by TC-019 |
| pypi.ix (dev-only) for the Quire 0.46.0 wheel | Python index | Assumed | `make dev-quire`; `agent-ix/quire-rs#392` tracks making it committable |
| Corpus repositories | Markdown artifacts | Out of boundary | Not read, not written; FR-005-CON-1 and TC-058 |

## Responsibility Allocation

| Requirement | Owning Component | Class |
|---|---|---|
| StR-001 | `spec-objects-enterprise` module | core |
| US-001 | `spec-objects-enterprise` module | core |
| FR-001 | `spec_objects_enterprise/manifest.yaml` | core |
| FR-002 | `typespec/` + `scripts/generate-schemas.mjs` (build) | infrastructure |
| FR-003 | `spec_objects_enterprise/manifest.yaml` | core |
| FR-004 | `typespec/main.tsp` (declaration models) | core |
| FR-005 | `spec_objects_enterprise/skeletons/` + `tests/fixtures/negative/` | core |
| NFR-001 | `spec_objects_enterprise/manifest.yaml` + skeletons, measured against the checked-in 0.1.0 baseline | cross-cutting |
| IT-001 | Boundary with `filament-core-service` | infrastructure |
| IT-002 | Boundary with the Quoin installer | infrastructure |

## Safety Gate Allocation

| Ticket gate | Allocated to | Evidence |
|---|---|---|
| Advisory-only until promotion | FR-003 (`compatibility_posture: additive`, `legacy_forms: warning`), NFR-001 Scope, spec.md In Scope | TC-020, TC-061, TC-062 |
| No management score or trust score is introduced | FR-004-CON-3, FR-004-AC-14, FR-005-CON-3 | TC-043, TC-065 |
| Role changes require evidence from the corpus review | FR-004 `OwnershipDecl` rule (no role name, no score, no rating); spec.md Out of Scope | TC-043 |
| No corpus repository is edited | FR-005-CON-1; spec.md Out of Scope | TC-058 |

## Dispositions

| Finding | Disposition |
|---|---|
| FND-001 | Applied: the advisory posture is named in spec.md In Scope and in NFR-001 Scope, allocated to the two FR-003 manifest keys TC-020 asserts. |
| FND-002..FND-006 | Recorded, no change; each is a boundary statement or a deliberate non-delivery with its owning issue named. |
