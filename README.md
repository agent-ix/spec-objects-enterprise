# spec-objects-enterprise

> Filament Module: tier-2 enterprise-architecture ObjectTypes (capability, business_function, value_stream, decision, objective, principle, kpi)

An Agent-IX Filament module loaded by [`quire-cli`](https://github.com/agent-ix/quire-cli) and [`quoin`](https://github.com/agent-ix/quoin).

## Installing quire-cli

`@agent-ix` packages are published to public npm. Install the CLI globally:

```bash
npm install -g @agent-ix/quire-cli
```

See https://github.com/agent-ix/quire-cli#install for details.

## Install this module via npm

This module is also published as a config-only npm package: `@agent-ix/spec-objects-enterprise`.
The package root **is** the Filament module (`manifest.yaml` + schemas/skeletons),
so it works directly as a `--module` target or via quoin's `package:` source.

```bash
npm install @agent-ix/spec-objects-enterprise
```

```bash
# quoin — resolve the module from npm by name
quoin plugin install package:@agent-ix/spec-objects-enterprise

# or point any tool at the installed package root
quire validate spec/**/*.md --module node_modules/@agent-ix/spec-objects-enterprise
```

## Object types provided

| Object | `type:` | Description |
|:-------|:--------|:------------|
| Capability | `capability` | An ability the organization possesses (e.g. Order Fulfillment), decomposed into an H2 "Sub-capabilities" list of child capabilities. |
| Business Function | `business_function` | An organizational function (e.g. Supply Chain Management) described in an H2 "Description" covering what it does, who performs it and which capabilities it supports. |
| Value Stream | `value_stream` | An end-to-end flow of value to a stakeholder (e.g. Order to Delivery), listing its ordered "Stages" and the value each stage adds. |
| Decision | `decision` | An architectural decision (e.g. adopt event-driven order orchestration) stated in an H2 "Decision" with its scope and the alternatives it supersedes. |
| Objective | `objective` | A measurable goal carrying frontmatter `metric` and `target` (with optional `deadline`), explaining why it matters and how it will be pursued. |
| Principle | `principle` | A guiding rule (e.g. promise only what the network can deliver) justified in an H2 "Rationale" with its implications. |
| KPI | `kpi` | A key performance indicator carrying frontmatter `metric` and `target` (with optional `threshold`), explaining how it is computed, who owns it and what happens on a breach. |

## Semantic contract

Every object type ships a real JSON Schema 2020-12 declaration record under
`spec_objects_enterprise/schemas/`, emitted from `typespec/main.tsp` against
`@agent-ix/semantic-core` 0.1.0 and referenced from `manifest.yaml` by path and
SHA-256 digest. The skeletons author their declarations in the typed
`## Properties` table (or the equivalent ```sysml``` fence), with clauses as
```ocl``` fences under `## Invariants`.

One rule is worth naming here, because it is the reason the KPI type has a
schema at all: **a KPI declaration is a measure definition, never a reading of
one.** `Kpi.json` requires at least one field carrying a unit (a dimensionless
measure uses the UCUM unity symbol `1`) and admits no identity field and no
`Timestamp` field — the identity and the instant an observation would carry. An
objective is its mirror: time-bound, and referencing a KPI definition through
its `targets` rather than declaring a measure of its own.

```bash
make schemas        # re-emit schemas/ and the manifest digests from typespec/
make schemas-check  # fail on any drift (also run by `make lint`)
make dev-quire      # install the Quire wheel the semantic tests need
```

`make dev-quire` exists because the Quire release carrying `extract_semantic`
is on no index this repository may commit a dependency against
(`agent-ix/quire-rs#392`). The semantic tests **fail** rather than skip when it
is absent: a skipped row is not coverage.

## How this module is used

### With quoin (recommended)

```bash
quoin plugin install path:../spec-objects-enterprise
quoin catalog list
quoin write . --types capability,value_stream
quoin review
```

See https://github.com/agent-ix/quoin.

### With quire-cli directly

```bash
quire schema capability --module ./spec_objects_enterprise
quire validate spec/**/*.md --module ./spec_objects_enterprise
quire extract DEC-001.md --module ./spec_objects_enterprise
```

See https://github.com/agent-ix/quire-cli#usage-instructions.

## Development

Native Poetry-based Python 3.13+ package (flat layout, package at root). Common targets:

```bash
make install          # install dependencies in Poetry venv
make test             # run pytest
make lint             # ruff + black check
make format           # ruff + black format
make build            # build wheel + sdist under dist/
make update-lock      # update poetry.lock
make local-publish    # publish to local pypi.ix
```

CI (GitHub Actions) runs tests and lint on push/PR, and on a `v*.*.*` tag builds with `poetry build` and publishes to Google Artifact Registry via `twine upload -r internal-pypi`. Versioning is dynamic from the Git tag. Required CI config: secret `GCP_SERVICE_ACCOUNT_KEY`; variables `GCP_REGION`, `GCP_PROJECT_NAME`, `GCP_PYPI`.
