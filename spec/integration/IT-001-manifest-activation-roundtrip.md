---
id: IT-001
title: "Manifest activation roundtrip against filament-core"
type: IT
relationships:
  - target: "ix://agent-ix/spec-objects-enterprise/FR-001"
    type: "verifies"
---
# [IT-001] Manifest activation roundtrip

## Objective

Verify the integration boundary between this Module's manifest and a clean
filament-core-service instance: activating `spec_objects_enterprise/manifest.yaml`
against an empty filament-core SHALL land all declared contributions (archetypes,
object-types, grammars, artifact-types) in the database, and re-activating the same
manifest SHALL be an idempotent no-op. Without this test, a manifest that silently
fails to register its contributions would go undetected.

## Target Integration

The system under test is this Module's manifest; the external dependency is
filament-core-service, reached over its HTTP module-activation and read APIs
(`/api/v1/modules/activate`, `/api/v1/archetypes`, `/api/v1/object-types`,
`/api/v1/grammars`, `/api/v1/artifact-types`). The integration type exercised is an
HTTP client call that POSTs the manifest and then reads back the persisted
contributions.

## Preconditions

A filament-core-service instance is running and reachable on a clean cluster (or
the kind dev cluster), and its database is empty so that the presence of newly
created rows is meaningful.

## Inputs

The single input is this Module's `spec_objects_enterprise/manifest.yaml`, declaring
its archetype, object-type, grammar, and artifact-type contributions. The same
manifest is submitted twice to exercise the idempotency property.

## Test Procedure

Each step performs one discrete action and has its own success criterion.

1. Deploy filament-core-service to a clean cluster (or use the kind dev cluster).
   - IT-001-SC-01: the service is reachable and reports an empty module set.
2. POST `spec_objects_enterprise/manifest.yaml` to `/api/v1/modules/activate`.
   - IT-001-SC-02: the endpoint returns 200 OK and a Module row is created.
3. GET `/api/v1/archetypes`, `/api/v1/object-types`, `/api/v1/grammars`, and
   `/api/v1/artifact-types`.
   - IT-001-SC-03: each declared item is present with the correct attributes.
4. Re-POST the same manifest to `/api/v1/modules/activate`.
   - IT-001-SC-04: activation is an idempotent no-op — the same `modules.id` is
     returned and no rows are duplicated.

## Expected Results

All declared contributions are persisted with correct attributes after the first
activation, and the second activation produces the same `modules.id` and the same
SHA-256 content hash with no row duplication. The test passes only when every
per-step success criterion holds.

## Traceability

This integration test verifies FR-001 (manifest activation against filament-core).
