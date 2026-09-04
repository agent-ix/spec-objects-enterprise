"""Role-distinct declaration schemas (FR-004).

Every record here is **hand-built** (see `tests/records.py`), because the
current extractor populates `fields`, `clauses` and `operations` only. Rows
that exercise `relations`, `stages`, `targets`, `measure`, `alternatives` or
`outcomes` are schema evidence, never extraction evidence; the extraction path
for those keys is `agent-ix/quoin#335`.
"""

from __future__ import annotations

import json

import pytest

from tests import records
from tests.conftest import (
    MODEL_OF,
    OBJECT_TYPES,
    SCHEMAS_DIR,
    SEMANTIC_CORE_BASE,
    VERB_ENUM_OF,
    module_base,
    schema_json,
)

SCORING_TOKENS = (
    "score",
    "rating",
    "maturity",
    "observed",
    "sample",
    "reading",
    "measurement",
)


def valid(validator_for, model: str, record: dict) -> None:
    errors = sorted(validator_for(model).iter_errors(record), key=str)
    assert not errors, (model, [e.message for e in errors])


def invalid(validator_for, model: str, record: dict) -> None:
    assert not validator_for(model).is_valid(record), (model, record)


# ---------------------------------------------------------------------------
# Distinctness and the seal
# ---------------------------------------------------------------------------


@pytest.mark.trace("TC-030", "FR-004-AC-1")
def test_each_object_type_schema_is_role_distinct(schema_registry):
    """No schema is `type: object` only, and all 21 pairs differ in a required
    key, a forbidden key, or an item rule."""

    def signature(model: str) -> tuple:
        schema = schema_json(model)
        props = schema["properties"]
        fields = props.get("fields", {})
        item_rules = (
            fields.get("minItems"),
            fields.get("minContains"),
            fields.get("maxContains"),
            props.get("clauses", {}).get("minItems"),
            props.get("operations", {}).get("minItems"),
            json.dumps(
                [
                    entry
                    for entry in schema.get("allOf", [])
                    if "fields" in entry.get("properties", {})
                ],
                sort_keys=True,
            ),
        )
        return (
            tuple(sorted(schema["required"])),
            tuple(sorted(set(MODEL_PROPERTY_SETS) - set(props))),
            item_rules,
        )

    signatures = {}
    for name in OBJECT_TYPES:
        model = MODEL_OF[name]
        schema = schema_json(model)
        assert set(schema) > {"$id", "type"}, model
        assert schema["properties"], model
        signatures[model] = signature(model)

    seen: dict[tuple, str] = {}
    for model, sig in signatures.items():
        assert sig not in seen, (model, seen.get(sig))
        seen[sig] = model


MODEL_PROPERTY_SETS = ("fields", "operations", "relations", "clauses")


@pytest.mark.trace("TC-038", "FR-004-AC-9", "FR-004-CON-2")
def test_the_empty_record_fails_every_object_type(schema_registry):
    """Every type's required set is non-empty, so `{}` passes none of the seven,
    and each failure names that type's own missing key."""
    expected = {
        "Capability": "fields",
        "BusinessFunction": "fields",
        "ValueStream": "fields",
        "Decision": "clauses",
        "Objective": "fields",
        "Principle": "clauses",
        "Kpi": "fields",
    }
    for model, key in expected.items():
        errors = list(schema_registry(model).iter_errors({}))
        assert errors, model
        assert any(key in error.message for error in errors), (model, key)


@pytest.mark.trace("TC-043", "FR-004-AC-14", "FR-004-CON-3")
def test_no_schema_declares_a_score_or_an_observation_property(schema_registry):
    """The ticket's safety gate: no management score, no trust score, and no key
    that would carry an observation rather than a declaration."""
    for path in sorted(SCHEMAS_DIR.glob("*.json")):
        if path.name == "toolchain.json":
            continue
        schema = json.loads(path.read_text())
        for name in schema.get("properties", {}):
            assert not any(token in name.lower() for token in SCORING_TOKENS), (
                path.name,
                name,
            )
    for name in OBJECT_TYPES:
        model = MODEL_OF[name]
        record = dict(records.RECORD_OF[model]())
        record["maturity_score"] = 4
        invalid(schema_registry, model, record)


@pytest.mark.trace("TC-040", "FR-004-AC-11", "FR-004-CON-1")
def test_grammar_items_are_refs_to_semantic_core(schema_registry):
    """No module schema redeclares a semantic-core model; every grammar item is
    a `$ref`, including under the relation-verb narrowing."""
    grammar = {
        "fields": "FieldDecl",
        "relations": "RelationDecl",
        "clauses": "ClauseRef",
        "operations": "OperationDecl",
    }
    for name in OBJECT_TYPES:
        schema = schema_json(MODEL_OF[name])
        for key, model in grammar.items():
            prop = schema["properties"].get(key)
            if prop is None:
                continue
            assert prop["items"]["$ref"] == f"{SEMANTIC_CORE_BASE}{model}.json", (
                name,
                key,
            )
        for entry in schema.get("allOf", []):
            relations = entry.get("properties", {}).get("relations")
            if relations is None:
                continue
            assert set(relations["items"]) == {"properties"}, name
            assert set(relations["items"]["properties"]) == {"verb"}, name
    emitted = {
        path.stem
        for path in SCHEMAS_DIR.glob("*.json")
        if path.name != "toolchain.json"
    }
    semantic_core = {
        "FieldDecl",
        "TypeRef",
        "RelationDecl",
        "OperationDecl",
        "ClauseRef",
        "EnumValue",
        "Identifier",
        "SemanticId",
        "KernelScalar",
        "UnitSymbol",
        "Multiplicity",
        "ConstraintDecl",
        "EdgeCategory",
    }
    assert not emitted & semantic_core


# ---------------------------------------------------------------------------
# Per-type rules
# ---------------------------------------------------------------------------


@pytest.mark.trace("TC-031", "FR-004-AC-2")
def test_capability_rules(schema_registry):
    valid(schema_registry, "Capability", records.capability_record())
    valid(
        schema_registry,
        "Capability",
        records.capability_record(outcomes=[records.outcome()], scope="Fulfillment"),
    )
    invalid(
        schema_registry,
        "Capability",
        {"fields": [records.field("label")]},
    )
    invalid(schema_registry, "Capability", {"relations": []})
    invalid(
        schema_registry,
        "Capability",
        records.capability_record(operations=[records.operation()]),
    )
    # The cross-cutting support models the FR-004 table gives every type. They
    # are hand-built: no extractor populates them (agent-ix/quoin#335), so this
    # is schema evidence, not extraction evidence.
    valid(
        schema_registry,
        "Capability",
        records.capability_record(
            owner=records.ownership(),
            lifecycle=records.lifecycle(),
            provenance=records.provenance(),
        ),
    )
    invalid(
        schema_registry,
        "Capability",
        records.capability_record(owner={"owner": "FulfillmentPlatform"}),
    )
    invalid(
        schema_registry,
        "Capability",
        records.capability_record(lifecycle=records.lifecycle("retired_but_not")),
    )
    invalid(
        schema_registry,
        "Capability",
        records.capability_record(provenance={"method": "corpus review"}),
    )


@pytest.mark.trace("TC-032", "FR-004-AC-3")
def test_business_function_rules(schema_registry):
    valid(schema_registry, "BusinessFunction", records.business_function_record())
    valid(
        schema_registry,
        "BusinessFunction",
        records.business_function_record(
            inputs=[f"{records.PACKAGE}/type/Forecast"],
            outputs=[f"{records.PACKAGE}/type/PurchaseOrder"],
        ),
    )
    invalid(
        schema_registry,
        "BusinessFunction",
        records.business_function_record(operations=[]),
    )
    invalid(
        schema_registry,
        "BusinessFunction",
        {"fields": [records.identity_field("function_id")]},
    )


@pytest.mark.trace("TC-033", "FR-004-AC-4")
def test_value_stream_rules(schema_registry):
    valid(schema_registry, "ValueStream", records.value_stream_record())
    valid(
        schema_registry,
        "ValueStream",
        records.value_stream_record(stages=[records.stage("Capture", 1)]),
    )
    invalid(
        schema_registry,
        "ValueStream",
        {"fields": [records.identity_field("stream_id")]},
    )
    invalid(
        schema_registry,
        "ValueStream",
        records.value_stream_record(stages=[records.stage("Capture", 0)]),
    )
    invalid(
        schema_registry,
        "ValueStream",
        records.value_stream_record(operations=[records.operation()]),
    )


@pytest.mark.trace("TC-037", "FR-004-AC-8")
def test_decision_rules(schema_registry):
    valid(schema_registry, "Decision", records.decision_record())
    valid(
        schema_registry,
        "Decision",
        records.decision_record(alternatives=[records.alternative()]),
    )
    invalid(schema_registry, "Decision", {"fields": [records.field("status")]})
    broken = dict(records.alternative())
    del broken["rejected_because"]
    invalid(schema_registry, "Decision", records.decision_record(alternatives=[broken]))


@pytest.mark.trace("TC-036", "FR-004-AC-7")
def test_principle_rules(schema_registry):
    valid(schema_registry, "Principle", records.principle_record())
    invalid(
        schema_registry,
        "Principle",
        records.principle_record(fields=[records.field("label")]),
    )
    invalid(
        schema_registry,
        "Principle",
        records.principle_record(operations=[records.operation()]),
    )
    invalid(schema_registry, "Principle", {"clauses": []})


# ---------------------------------------------------------------------------
# The definition / measurement boundary
# ---------------------------------------------------------------------------


@pytest.mark.trace("TC-034", "FR-004-AC-5")
def test_kpi_is_a_definition_and_never_a_reading(schema_registry):
    """The ticket's headline criterion, as five schema rules."""
    valid(schema_registry, "Kpi", records.kpi_record())
    # A dimensionless measure alone is enough: the unity symbol carries it.
    valid(
        schema_registry,
        "Kpi",
        {"fields": [records.dimensionless_field("delivered_order_count")]},
    )
    valid(
        schema_registry,
        "Kpi",
        records.kpi_record(
            measure=records.measure_decl(),
            thresholds=[
                {"level": "alert", "comparator": "at_most", "bound": "95"},
            ],
        ),
    )
    # An observation's identity.
    invalid(
        schema_registry,
        "Kpi",
        records.kpi_record(
            fields=[records.measured_field(), records.identity_field("observation_id")]
        ),
    )
    # An observation's instant.
    invalid(
        schema_registry,
        "Kpi",
        records.kpi_record(
            fields=[records.measured_field(), records.temporal_field("observed_at")]
        ),
    )
    # No unit: nothing says what is measured.
    invalid(
        schema_registry, "Kpi", {"fields": [records.field("delivered_within_promise")]}
    )
    invalid(schema_registry, "Kpi", {"fields": []})
    invalid(
        schema_registry, "Kpi", records.kpi_record(operations=[records.operation()])
    )


@pytest.mark.trace("TC-035", "FR-004-AC-6")
def test_objective_is_time_bound_and_references_a_measure(schema_registry):
    valid(schema_registry, "Objective", records.objective_record())
    valid(
        schema_registry,
        "Objective",
        records.objective_record(targets=[records.target_decl()]),
    )
    # No horizon: not an objective.
    invalid(
        schema_registry,
        "Objective",
        records.objective_record(fields=[records.identity_field("objective_id")]),
    )
    # A bare token is not a SemanticId.
    invalid(
        schema_registry,
        "Objective",
        records.objective_record(targets=[records.target_decl("OnTimeDeliveryRate")]),
    )
    invalid(
        schema_registry,
        "Objective",
        records.objective_record(operations=[records.operation()]),
    )


@pytest.mark.trace("TC-042", "FR-004-AC-13")
def test_objective_declares_no_measure_and_kpi_carries_no_target(schema_registry):
    """An objective references a measure definition; a KPI never carries the
    goal set against it."""
    invalid(
        schema_registry,
        "Objective",
        records.objective_record(measure=records.measure_decl()),
    )
    invalid(schema_registry, "Kpi", records.kpi_record(targets=[records.target_decl()]))


# ---------------------------------------------------------------------------
# Cross-references and relation vocabularies
# ---------------------------------------------------------------------------


@pytest.mark.trace("TC-039", "FR-004-AC-10")
def test_unresolved_placeholder_is_a_semantic_id_and_a_bare_token_is_not(
    schema_registry,
):
    placeholder = f"{records.PACKAGE}/unresolved/Mystery"
    valid(
        schema_registry,
        "Capability",
        records.capability_record(
            fields=[
                records.identity_field("capability_id"),
                records.field("mystery", placeholder),
            ]
        ),
    )
    invalid(
        schema_registry,
        "Capability",
        records.capability_record(
            fields=[
                records.identity_field("capability_id"),
                records.field("mystery", "Mystery"),
            ]
        ),
    )


@pytest.mark.trace("TC-041", "FR-004-AC-12")
def test_each_type_narrows_its_relation_verbs(schema_registry):
    """Schema evidence only: `relations` is not populated by today's extractor."""
    for name in OBJECT_TYPES:
        model = MODEL_OF[name]
        verbs = schema_json(VERB_ENUM_OF[name])["enum"]
        record = records.RECORD_OF[model]()
        valid(
            schema_registry,
            model,
            dict(record, relations=[records.relation(verbs[0])]),
        )
        invalid(
            schema_registry,
            model,
            dict(record, relations=[records.relation("annotates")]),
        )


@pytest.mark.trace("TC-011", "FR-002-AC-2")
def test_every_schema_id_is_read_from_the_manifest_version(schema_registry):
    base = module_base()
    for path in sorted(SCHEMAS_DIR.glob("*.json")):
        if path.name == "toolchain.json":
            continue
        schema = json.loads(path.read_text())
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert schema["$id"] == f"{base}{path.name}", path.name
