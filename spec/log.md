---
type: log
title: "Update Log"
description: "Chronological log of structural changes to this bundle."
---
# Update Log

## History

* **2026-06-15** — Adopted OKF-compatible bundle structure with directory indexes.
* **2026-09-04** — Issue #4 (semantic module contract): added US-001, FR-002..FR-005, NFR-001, IT-002 and StR-001-VC-3; converted `tests.md` to a `TestMatrix`; spec scope extended to the TypeSpec-emitted schemas, the semantic-module contract, and the KPI definition / measurement boundary.
* **2026-09-04** — Issue #4 review round: eight SpecReviews under `spec/reviews/4-semantic-module-contract/` (base, integrity, failure-domain, dependency, evidence, EARS conformance, risk-complexity, scope-boundary); every high and every applied medium recorded with a disposition. Filed `agent-ix/spec-artifacts-process#81` (the status-lie check has never run on the FR/StR/US coverage tables).
* **2026-09-04** — Issue #4 implemented and reviewed: `reviews/26-09-04-semantic-module-contract-code-review.md` (SR-009) and `reviews/26-09-04-semantic-module-contract-gap-analysis.md` (SR-010). Filed `agent-ix/quire-rs#399` (a `## Heading` inside an HTML comment satisfies a required `section_body` locator). `quire coverage`: 111/111 rows backed.
* **2026-09-22** — PLAT-974: CI off dev mirrors. `agent-ix/quire-rs#392` is resolved (quire 0.47.1 published to `internal-pypi`), so FR-005 now declares `quire` as a dev dependency pinned to the `internal-pypi` source; the `make dev-quire`/`dev-quire` poe task and the `pypi.ix` poetry source are deleted, and spec.md drops the Out of Scope bullet naming that blocker. `@agent-ix/semantic-core` resolves from GitHub Packages, not `npm.ix` (FR-002-CON-4, TC-019, US-001). `ci.yml`'s `ci:` job moves from `lib-ci.yml` to `semantic-module-ci.yml`, which runs `poetry install` and `npm ci` so the workflow actually installs both engines; `Makefile` gains a `semantic-install` target (`npm ci`) for that half. The `engine_accepts_module_semantic_core`/`semantic_core_engine_xfail` gate in `tests/conftest.py`, which existed only because the previously installed quire lacked the module's declared `semantic_core` 0.3.0, is deleted along with every `@semantic_core_engine_xfail()` marker it guarded; quire 0.47.1 vendors 0.3.0, so every one of those rows now runs unconditionally. No locator, xfail, or test behavior otherwise changed: the full suite (pytest, `schemas-check`, black, ruff) was already green under 0.47.1 with no other drift.
