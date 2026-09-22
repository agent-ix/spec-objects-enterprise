---
id: FR-005
title: "Make every skeleton an executable typed fixture"
type: FR
relationships:
  - target: "ix://agent-ix/spec-objects-enterprise/US-001"
    type: "implements"
  - target: "ix://agent-ix/spec-objects-enterprise/FR-003"
    type: "depends_on"
  - target: "ix://agent-ix/spec-objects-enterprise/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-071"
    type: "depends_on"
  - target: "ix://agent-ix/quoin/FR-072"
    type: "depends_on"
---
# FR-005: Make every skeleton an executable typed fixture

## Description

Every skeleton under `spec_objects_enterprise/skeletons/` SHALL author its
declarations in the quoin FR-071/FR-072 Markdown forms (typed `## Properties`
table by default, `## Invariants` clause fences, `## Operations` subsections)
and validate through Quire against this module, accompanied by negative
fixtures that fail for a named reason, so that the skeletons are the module's
executable positive fixtures and the negatives pin what the schemas refuse.

## Inputs

- The rewritten skeletons `skeletons/<type>.md` (one per object type) and the
  alternate-form skeletons `skeletons/capability.sysml.md`,
  `skeletons/objective.sysml.md`, `skeletons/kpi.sysml.md`.
- Negative fixtures `tests/fixtures/negative/<type>-<case>.md`, each with
  frontmatter `expect:` naming the diagnostic code or reason the fixture must
  produce.
- The Quire wheel 0.47.1 or later, exposing `extract_semantic`,
  `validate_document`, and `Registry`, declared as a dev dependency resolved
  from `internal-pypi` (see Behavior).

## Outputs

- A validation result per skeleton with no error and no `semantic.record-invalid`.
- A semantic record per skeleton whose `fields`, `clauses`, and `operations`
  availability match the type's required set.

## Behavior

- Each skeleton whose type admits `fields` (`capability`, `business_function`, `value_stream`, `decision`, `objective`, `kpi`) SHALL author `## Properties` as one table with the header exactly `Field | Type | Multiplicity | Constraints`.
- The `principle` skeleton SHALL carry no `## Properties` section, because `Principle.json` forbids `fields`.
- The `capability`, `objective`, and `kpi` alternate skeletons SHALL author the same declarations as one ```` ```sysml ```` fence of `attribute <name> : <Type>[<mult>] { <constraints> }` and `ref item <name> : <Type>[<mult>]` lines.
- Each alternate skeleton SHALL declare the same fields as its table skeleton, under that skeleton's frontmatter `id` and `title`; the module therefore ships two files under one id by intent, and the identity of their extracted `FieldDecl[]` is the obligation FR-005-AC-2 tests.
- The `kpi` skeleton and its alternate SHALL carry at least one measured field (a `Type` cell with a trailing ` [unit]` on a unit-allowed kernel scalar), no identity row, and no `Timestamp` row, so the shipped fixture is a measure definition and not a reading of one.
- Where a `kpi` row is dimensionless, its `Type` cell SHALL carry the unity symbol `[1]`, so the fixture shows how a count or ratio satisfies the measured-field rule.
- The `objective` skeleton and its alternate SHALL carry an identity row and a `Timestamp` row (the objective's horizon).
- All seven skeletons SHALL author `## Invariants` with one `### <clauseId>` per clause, each owning exactly one ```` ```ocl ```` fence.
- The clause text inside an ```` ```ocl ```` fence SHALL be carried verbatim, never evaluated, parsed, or asserted by this module.
- The test suite SHALL assert the `ClauseRef` identity, language, and source span only; expression semantics belong to `agent-ix/quire-contract-ir#52`.
- The `business_function` skeleton SHALL author `## Operations` with one `### <name>` per operation, an optional `| Param | Type | Multiplicity | Constraints |` table, a `Returns:` line where the operation returns a value, and optional `Pre:`/`Post:` lines that, when present, name clause ids declared in the same artifact.
- No other skeleton SHALL author `## Operations`, because every other type forbids `operations`.
- Each skeleton's frontmatter SHALL carry `object: <type name>` beside `type: <type name>`, because Quire runs the semantic layer (extraction and record validation) on the `object:` archetype of a document; a skeleton without it validates its headings only.
- The manifest SHALL gain a `required: false` `section_body` locator for every `## Properties`, `## Invariants`, and `## Operations` section a skeleton introduces, so the section is asserted by the manifest and remains optional for existing artifacts.
- Every skeleton `title` SHALL be an `Identifier` (`^[A-Za-z_][A-Za-z0-9_]*$`), distinct across all skeletons and outside the `KernelScalar` names, so a `Type` cell can name it.
- Every `Type` cell that names another skeleton SHALL use that skeleton's `title`, so that under a bundle index built from the skeletons every non-kernel token resolves to `ix://agent-ix/spec-objects-enterprise/type/<Title>` with no `semantic.unresolved-type` finding.
- Every skeleton SHALL keep every H2 heading whose manifest locator is `required: true` for its type: `## Sub-capabilities` (capability), `## Description` (business_function), `## Stages` (value_stream), `## Decision` (decision), `## Rationale` (principle).
- The `objective` and `kpi` skeletons SHALL keep their required frontmatter `metric` and `target` fields, and the `kpi` skeleton its optional `threshold` field, unchanged in form.
- No skeleton SHALL carry an H2 heading the manifest does not assert.
- Where a typed section and a prose section describe the same declarations (the KPI `metric`/`target` frontmatter and its `## Properties` table; the value-stream `## Stages` prose and the optional `stages` key; the capability `## Sub-capabilities` prose and the `decomposes` relations), the typed section SHALL be the authority and the prose section a derived, human-facing view.
- Each negative fixture SHALL fail `validate_document` with an error whose message carries the fixture's `expect:` code, covering at least: a KPI carrying a `Timestamp` row (`semantic.record-invalid`), a KPI carrying an identity row (`semantic.record-invalid`), a KPI whose rows carry no unit (`semantic.record-invalid`), an objective without a `Timestamp` row (`semantic.record-invalid`), a principle with a `## Properties` table (`semantic.record-invalid`), a capability without an identity row (`semantic.record-invalid`), a business function whose `## Operations` declares no operation (`semantic.record-invalid`), a `## Properties` section carrying both a table and a fence (`semantic.properties-both-forms`), an operation whose `Post:` names an undeclared clause (`semantic.dangling-clause-ref`), and a `Type` token that is not an `Identifier` (`semantic.invalid-type-token`); the last three re-check the engine's published diagnostics under this module's schemas rather than re-specify them.
- The module SHALL declare `quire` in `pyproject.toml` as a dev dependency pinned to the `internal-pypi` source, so `poetry install` provisions the engine and no lookup falls through to public PyPI, where `quire` names an unrelated package.
- If the installed Quire wheel is absent or lacks `extract_semantic`, then every semantic test SHALL fail — not skip — with a message naming the missing function and `poetry install`, so that no matrix row can pass or be reported green without the engine under test.
- Only a criterion this specification names as blocked SHALL be exempt from the previous rule, as an explicit expected failure naming the blocking issue. Today that is the record validation of a legacy-form artifact declaring `object:` (`agent-ix/quire-rs#391`, beside NFR-001-AC-2) and the naming half of FR-003-AC-6 (`agent-ix/quire-rs#221`, `agent-ix/quire-rs#394`).

## Constraints

| ID | Constraint | Type | Validation |
|----|------------|------|------------|
| FR-005-CON-1 | The module SHALL keep the skeletons and negatives in this repository only, editing no corpus repository and no vendored quoin/quire fixture. | Boundary | Inspection |
| FR-005-CON-2 | A skeleton SHALL carry one Properties form; the alternate form is a separate file, never a second block in the same artifact. | Integrity | Test |
| FR-005-CON-3 | No skeleton SHALL author a field, clause, or prose line that scores or rates an organizational unit or a person. | Boundary | Inspection |

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-005-AC-1 | Every skeleton file (seven types plus three alternates) passes `validate_document` against this module with `is_valid` true and no `semantic.record-invalid` error. | Test |
| FR-005-AC-2 | For `capability`, `objective`, and `kpi`, the table and `sysml` skeletons extract to identical normalized `fields` with `fieldsForm` `table` and `fence` respectively. | Test |
| FR-005-AC-3 | Under a bundle index built from the skeleton frontmatter, every skeleton extracts with zero `error` diagnostics and zero `semantic.unresolved-type` findings, and every non-kernel `type.target` starts with `ix://agent-ix/spec-objects-enterprise/type/`. | Test |
| FR-005-AC-4 | Each skeleton's `availability` states match its type: `fields` `available` for the six field-bearing types, `clauses` `available` for all seven, `operations` `available` for `business_function`; `not_applicable` for every other kind. | Test |
| FR-005-AC-5 | Every negative fixture fails validation with an error message containing its `expect:` code, and at least the ten cases listed in Behavior are present. | Test |
| FR-005-AC-6 | Every skeleton's H2 set equals a subset of the headings the manifest asserts for its type and includes every `required: true` heading. | Test |
| FR-005-AC-7 | The skeleton for each of the seven types has no placeholder token and every asserted section body is non-empty. | Test |
| FR-005-AC-8 | Every skeleton `title` matches the `Identifier` pattern, is unique across the skeletons, and is not a `KernelScalar` name; every skeleton frontmatter carries `object` equal to `type`. | Test |
| FR-005-AC-9 | The extracted `kpi` record carries at least one field with `type.unit`, no field with `identity`, and no field whose `type.target` is `Timestamp`; the extracted `objective` record carries at least one of each of the first and third. | Test |

## Dependencies

- **Upstream**: [FR-003](./FR-003-semantic-manifest-contract.md), [FR-004](./FR-004-role-schemas.md); quoin FR-071/FR-072 (`ix://agent-ix/quoin/FR-071`, `ix://agent-ix/quoin/FR-072`); quire-rs FR-070/FR-071/FR-072
- **Upstream (unpinned neighbour contract)**: the `semantic.record-invalid` diagnostic this requirement's Outputs and FR-005-AC-1 depend on exists in quire-rs source but in no quire-rs acceptance criterion; `agent-ix/quire-rs#391` is where that record-validation contract, and the code naming it, are being settled.
- **Downstream**: `agent-ix/quire-contract-ir#52` and `agent-ix/filament-core-data#36` consume the skeletons read-only
