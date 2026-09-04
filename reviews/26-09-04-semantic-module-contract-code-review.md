---
id: SR-009
title: "Code review — spec-objects-enterprise semantic module contract (#4)"
type: SpecReview
analysis: code-review
scope: "typespec/, scripts/generate-schemas.mjs, spec_objects_enterprise/, tests/, plan/Plan-001-semantic-module-contract/"
review_set: subset
---
# SR-009: Code review — semantic module contract (#4)

## Summary

Reviewed the whole `spec/4-semantic-module-contract` branch diff against
`origin/main`: the TypeSpec source and generator, the 0.2.0 manifest, the
thirty-three emitted schemas, the rewritten skeletons, the ten negative
fixtures, and the 125-case test suite. Every gate was run rather than assumed.
Five findings — one high, two medium, two low — all fixed in this branch except
the high one, which is an engine defect filed upstream and pinned by a guard
test here.

## Verdict

**CONDITIONAL** — the one high finding is an upstream engine defect
(`agent-ix/quire-rs#399`) with a ticket, a repository-level guard test and no
weakened check; the remaining four are fixed. No finding is outstanding in this
repository.

## Findings

| ID | Severity | Summary | Refs |
|---|---|---|---|
| FND-001 | high | Quire's heading scan does not strip HTML comments, so a `## Sub-capabilities` line inside a skeleton's own instructional comment satisfies the `required: true` `section_body` locator it documents. The pre-existing mutation test — the one whose whole purpose is to prove the locator fires — went green with the real heading renamed away. Every required-heading contract in this module was silently unenforced for as long as the comments quoted their headings. Filed as `agent-ix/quire-rs#399`; the skeleton comments no longer carry heading-shaped lines, and `test_no_skeleton_comment_carries_a_literal_heading` keeps them that way until the engine is fixed. No locator was relaxed. | spec_objects_enterprise/skeletons/capability.md:9, tests/test_skeletons_and_validate.py:295 |
| FND-002 | medium | TC-012 checked only that a non-sibling `$ref` carried the semantic-core prefix. The generator falls back to that base for any relative `$ref` it does not recognise as a sibling, so a dangling `https://schemas.agent-ix.org/semantic-core/0.1.0/Nonexistent.json` would have passed with the right prefix and resolved to nothing. Fixed: each such `$ref` is now resolved against the semantic-core package the pinned toolchain installs. | tests/test_schema_emission.py:130 |
| FND-003 | medium | `package-lock.json` resolved **every** package through the npm.ix fall-through proxy, including the 74 public ones, which is exactly what FR-002-CON-4 forbids and what TC-019 exists to catch. TC-019 caught it. Re-installed with `--registry=https://registry.npmjs.org/ --@agent-ix:registry=http://npm.ix/`; only `@agent-ix/semantic-core` resolves from npm.ix now. | package-lock.json |
| FND-004 | medium | `OwnershipDecl`, `LifecycleDecl` and `ProvenanceDecl` shipped as emitted schemas that no record test ever validated against — three files a downstream fixture reader could consume with nothing asserting they mean anything. Fixed: TC-031 now validates a capability record carrying all three, and refuses a bare-token `owner`, a `LifecycleState` outside the closed set, and a `ProvenanceDecl` missing `source`. | tests/test_role_schemas.py:264, tests/records.py:118 |
| FND-005 | low | Three `# pragma: no cover` comments sat on environment guards in the test tree. Coverage is measured over `spec_objects_enterprise/` only, so they suppressed nothing — but a pragma that reads as "this is allowed to be uncovered" is the habit the integrity rule forbids. Removed. | tests/conftest.py:178 |

## Gates Run

| Gate | Result |
|---|---|
| `make lint` (ruff + black + `schemas-check`) | pass — all checks passed, 33 schemas match the committed output |
| `make test` | pass — 125 passed, 7 skipped, 2 xfailed, coverage 100% (`--cov-fail-under=100`) |
| `quire validate --scope . "spec/**/*.md"` | pass — zero errors, zero grammar warnings, 24/24 documents grammar-clean |
| `quire validate --scope . "plan/**/*.md"` | pass |
| `quire validate --scope . "reviews/**/*.md"` | pass |
| `quire coverage --scope .` | 111/111 rows backed (100%); 0 unbacked rows, 0 status lies |
| `node scripts/generate-schemas.mjs --check` | pass on the committed tree |
| `poetry build` / `npm pack` | both exercised by TC-015 and TC-071 |

## Language Dispatch

Python (`pyproject.toml`, `tests/*.py`) plus two Node build scripts and one
TypeSpec source. No Rust and no React in the change, so those lanes do not
apply. The repo's own idiom — module-level `test_*` functions with
`@pytest.mark.trace(...)`, not `TestFeature` classes — was followed; the
generic "leverage test classes" rule and the `.agent/rules/writing_tests.md`
Assumptions/Criteria docstring shape are outranked by the existing convention
in `tests/test_manifest.py` and `tests/test_skeletons_and_validate.py`, and by
the merged sibling module `agent-ix/spec-objects-business`.

## Test Standards

- **Tracking tags.** Every test added by this change carries
  `@pytest.mark.trace(...)` with its TC id and the acceptance criterion or
  constraint it discharges; the marker is registered in `pyproject.toml`, so
  `filterwarnings = ["error"]` does not turn an unknown mark into a failure.
- **The three tag traps were audited before the PR, not after.** No marker
  spans more than one line (`agent-ix/quire-rs#395`, the `black`-wrap trap);
  no trace id sits on a module docstring, a class or a plain helper — one did,
  `FR-005` on `tests.test_skeletons_semantic`, and `quire coverage` named it as
  `tag-on-non-binding-symbol` before it could report a row unbacked; and no
  bare TC id appears in any comment, where it would bind the next symbol.
- **No mocks anywhere.** Every test drives the real generator, the real
  emitter, the real Quire engine, or the real shipped bytes. There is no
  `unittest.mock`, no `@patch` and no `mocker` usage in the change, so the
  mock-boundary rules are vacuously satisfied — and no test can pass against a
  hollow stub.
- **No database interaction and no network read**: the only subprocesses are
  `node`, `poetry build`, `npm pack`, `git diff` and (opt-in) `quoin`.
- **Skips.** Seven, and every one names the environment it needs and the matrix
  row that stays `🚧` because of it: a running `filament-core-service` at
  `a77f31e` or later (four) and an opt-in Quoin install roundtrip (three). No
  semantic test skips: `tests/conftest.py` `require_quire` **fails** when the
  engine is absent, naming `make dev-quire` and `agent-ix/quire-rs#392`, and
  the two pre-existing vacuous skips in `test_skeletons_and_validate.py` were
  converted to that hard failure.
- **Expected failures.** Two, both `strict=True` so they turn red the day the
  engine is fixed, and both naming the upstream issue in the reason:
  `agent-ix/quire-rs#221`/`#394` (the refusal names nothing) and
  `agent-ix/quire-rs#391` (a legacy artifact declaring `object:`).

## Completeness

No `TODO`, `FIXME` or `XXX` in the change; a test asserts it over every
skeleton. No stub module, no placeholder return, no empty test and no
assertion-free test: every added test asserts a value or a refusal. The one
source package (`spec_objects_enterprise/__init__.py`) is unchanged and at 100%
coverage.

## Edge Case & Logic Review

The change ships Markdown, JSON and two build scripts; it registers no route,
opens no socket, holds no mutable state and takes no user input at runtime. The
categories that apply:

- **Input validation.** The generator resolves its own repo root from its file
  location rather than `process.cwd()`, so a run from a subdirectory cannot
  read the wrong package. It writes only under `spec_objects_enterprise/schemas/`
  and edits `manifest.yaml` at `data_schema.digest` lines only, textually, so
  the file's YAML anchors and comments survive.
- **Error handling.** `tsp compile` failure, a missing emitted set, an
  unsupported Node version and a base/version disagreement each exit non-zero
  **without touching the committed output**; TC-014 and TC-073 assert the
  no-write property directly by comparing bytes before and after.
- **Boundaries.** The item-rule edges are tested at both sides: zero versus one
  identity field, zero versus one temporal field, absent versus present unit,
  empty versus one-item arrays, and `StageDecl.order` 0 versus 1.
- **Resource constraints.** Every subprocess test runs against a throwaway tree
  under `tmp_path`; none mutates the repository. The one test that can touch
  operator state — the Quoin install roundtrip — restores it in a `finally` and
  is opt-in behind an environment variable.

## Spec-Code Faithfulness

Each FR was checked against what actually ships:

- **FR-002** — `typespec/main.tsp` + `scripts/generate-schemas.mjs` emit 33
  schemas through the official emitter; `make lint` runs the drift gate.
- **FR-003** — the manifest carries the nine admitted `semantic` keys, seven
  reference-form `data_schema` entries with live digests, and every 0.1.0
  locator unchanged against a checked-in baseline captured from `origin/main`.
- **FR-004** — seven sealed object-type models and twenty-six support models;
  the KPI definition / measurement rules and the `Objective`/`Kpi` key
  exclusion are asserted against the real emitted bytes with a real 2020-12
  validator, and again end-to-end through the engine by three negative fixtures.
- **FR-005** — ten skeletons and ten negative fixtures, every one exercised
  through `validate_document` and `extract_semantic`.
- **NFR-001** — measured against the frozen 0.1.0 baseline, with the
  legacy-warning metric recorded as the value this module actually measures (0)
  rather than the sibling's (1).

Nothing in the spec describes behaviour the code does not have, and no FR
references an artifact that does not ship.
