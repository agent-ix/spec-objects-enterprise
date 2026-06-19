# spec-objects-enterprise

> Filament Module: tier-2 enterprise-architecture ObjectTypes (capability, business_function, value_stream, decision, objective, principle, kpi)

An Agent-IX Filament module loaded by [`quire-cli`](https://github.com/agent-ix/quire-cli) and [`quoin`](https://github.com/agent-ix/quoin).

## Installing quire-cli

This module is consumed by `@agent-ix/quire-cli`, published to GitHub Packages. Add an `.npmrc` so the `@agent-ix` scope resolves there:

```ini
@agent-ix:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}
```

```bash
npm install -g @agent-ix/quire-cli
```

See https://github.com/agent-ix/quire-cli#install for details.

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
