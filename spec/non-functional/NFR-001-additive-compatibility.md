---
id: NFR-001
title: "Additive compatibility of the semantic contract"
type: NFR
quality_attribute: compatibility
relationships:
  - target: "ix://agent-ix/spec-objects-enterprise/FR-003"
    type: "constrains"
  - target: "ix://agent-ix/spec-objects-enterprise/FR-004"
    type: "constrains"
  - target: "ix://agent-ix/spec-objects-enterprise/FR-005"
    type: "constrains"
---
# NFR-001: Additive compatibility of the semantic contract

## Statement

The module SHALL keep every artifact of the checked-in 0.1.0 skeleton set —
the seven skeletons as they stood at manifest version 0.1.0, which is the
population this NFR measures — validating against version 0.2.0 with at most
warning-level semantic findings.

The module SHALL keep every 0.1.0 `body_extraction` locator definition
unchanged at 0.2.0, and SHALL keep the untyped section and frontmatter strings
those locators yield byte-identical between the two versions. Yields of the
other 0.1.0 locators are unmeasured and are not claimed.

## Scope

- Applies to: `manifest.yaml`, the shipped schemas, and the skeletons.
- Operational context: existing corpus artifacts authored in legacy Properties
  forms (bullet lists, free-column tables, prose sections) under
  `legacy_forms: warning`; no corpus repository is edited.
- Gate: this NFR is the module's discharge of the ticket's advisory-only-until-promotion merge gate; the posture keys that carry it are `compatibility_posture: additive` and `legacy_forms: warning`, declared by FR-003.

## Rationale

The ticket's merge gate is advisory-only until corpus promotion. A module that
turned legacy artifacts into errors would force corpus edits this campaign
forbids; a module that changed a locator would change every existing
extraction record.

## Measurement and Evaluation

| Metric | Target | Threshold | Method |
|--------|--------|-----------|--------|
| 0.1.0 locators changed | 0 | 0 | Test |
| Checked-in 0.1.0 skeleton set under 0.2.0: error findings, per skeleton | 0 | 0 | Test |
| Each 0.1.0 skeleton under 0.2.0: `semantic.legacy-properties-form` warnings | 0 | 0 | Test |
| Required-heading and frontmatter yields for each 0.1.0 skeleton, 0.1.0 vs 0.2.0 | identical | identical | Test |

## Verification

NFR-001-AC-2 holds on the population this NFR measures, and the measurement
says why: no 0.1.0 skeleton carries a frontmatter `object:` key, so Quire runs
headings-only validation on it and never assembles or checks a typed record.
That is what makes 0.2.0 additive for the artifacts that exist today, and it is
asserted rather than assumed.

No 0.1.0 enterprise skeleton carries a `## Properties` section in any form, so
the legacy-properties-form warning count is 0 rather than 1 — the metric row
records the measured value, not the sibling business module's.

The engine defect behind the `object:` case is real but differently scoped:
once a legacy-form artifact *does* declare `object:`, quire 0.46.0 assembles
its declaration record as `{}` and validates it against the type schema
unconditionally, so it fails `semantic.record-invalid` at error severity even
under `legacy_forms: warning`. `agent-ix/quire-rs#391` owns that rule. The
module carries that case as an explicit expected failure beside NFR-001-AC-2
rather than relaxing a schema, so the day the engine changes, the row turns red
and is noticed.

A checked-in copy of the 0.1.0 `body_extraction` and of all seven 0.1.0
skeletons is compared against the 0.2.0 manifest and validated under it: the
locator definitions are equal, each legacy skeleton validates with no error and
no legacy-form warning, and its extracted required-section and frontmatter
strings are unchanged.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| NFR-001-AC-1 | Every 0.1.0 `body_extraction` locator is present in 0.2.0 with identical facets (0 changed). | Test |
| NFR-001-AC-2 | Every skeleton of the checked-in 0.1.0 set validates under 0.2.0 with 0 error findings. | Test |
| NFR-001-AC-3 | Each 0.1.0 skeleton yields 0 `semantic.legacy-properties-form` warnings, because none carries a `## Properties` section. | Test |
| NFR-001-AC-4 | Each 0.1.0 skeleton's extracted required-heading section bodies and frontmatter yields are byte-identical under 0.1.0 and 0.2.0. | Test |

## Dependencies

- **Upstream**: [FR-003](../functional/FR-003-semantic-manifest-contract.md), [FR-005](../functional/FR-005-executable-skeletons.md); quoin FR-074 (`ix://agent-ix/quoin/FR-074`)
- **Downstream**: corpus promotion (`agent-ix/quoin#291` sweep), outside this module
