"""Hand-built declaration records for the FR-004 schema tests.

Every builder here produces a record shaped the way Quire assembles one, but
built by hand rather than extracted. That distinction matters: the extractor
populates `fields`, `clauses` and `operations` only (quire-rs FR-070/FR-071),
so every criterion over `relations`, `stages`, `targets`, `measure`,
`thresholds`, `outcomes`, `alternatives`, `owner`, `lifecycle`, `provenance`,
`scope`, `inputs` or `outputs` is **schema evidence, not extraction evidence**,
and the tests that use those keys say so. The extraction path for them is
`agent-ix/quoin#335` and its quire-rs successor.
"""

from __future__ import annotations

from typing import Any

PACKAGE = "ix://agent-ix/spec-objects-enterprise"


def field(
    name: str,
    target: str = "String",
    *,
    lower: int = 1,
    upper: int | None = 1,
    identity: bool = False,
    unit: str | None = None,
    decimal: tuple[int, int] | None = None,
) -> dict[str, Any]:
    multiplicity: dict[str, Any] = {"lower": lower}
    if upper is not None:
        multiplicity["upper"] = upper
    type_ref: dict[str, Any] = {"target": target, "multiplicity": multiplicity}
    if unit is not None:
        type_ref["unit"] = unit
    if decimal is not None:
        type_ref["decimal"] = {"precision": decimal[0], "scale": decimal[1]}
    decl: dict[str, Any] = {"name": name, "type": type_ref}
    if identity:
        decl["identity"] = True
    return decl


def identity_field(name: str = "id") -> dict[str, Any]:
    return field(name, "UUID", identity=True)


def temporal_field(name: str = "horizon") -> dict[str, Any]:
    return field(name, "Timestamp")


def measured_field(name: str = "value", unit: str = "%") -> dict[str, Any]:
    return field(name, "Decimal", unit=unit, decimal=(5, 2))


def dimensionless_field(name: str = "count") -> dict[str, Any]:
    """A count: dimensionless, so it carries the UCUM unity symbol."""
    return field(name, "Integer", unit="1")


def clause(clause_id: str = "SomeInvariant") -> dict[str, Any]:
    return {
        "language": "ocl",
        "clauseId": clause_id,
        "sourceSpan": {
            "sourceIdentity": f"{PACKAGE}/type/Example",
            "path": "skeletons/example.md",
            "startLine": 1,
            "startColumn": 1,
        },
    }


def operation(name: str = "perform") -> dict[str, Any]:
    return {"name": name, "params": []}


def relation(
    verb: str,
    *,
    category: str = "structural",
    target: str = f"{PACKAGE}/type/Something",
) -> dict[str, Any]:
    return {"verb": verb, "category": category, "target": target}


def stage(name: str = "Capture", order: int = 1) -> dict[str, Any]:
    return {"name": name, "order": order, "value": "The order is confirmed."}


def target_decl(
    measure: str = f"{PACKAGE}/type/OnTimeDeliveryRate",
) -> dict[str, Any]:
    return {"measure": measure, "comparator": "at_least", "bound": "97"}


def measure_decl() -> dict[str, Any]:
    return {
        "name": "OnTimeDeliveryRate",
        "unit": "%",
        "aggregation": "ratio",
        "direction": "higher_is_better",
    }


def alternative(name: str = "ScaleTheOrchestrator") -> dict[str, Any]:
    return {
        "name": name,
        "doc": "Scale the existing synchronous orchestrator with retries.",
        "rejected_because": "It cannot meet peak throughput without over-provisioning.",
    }


def outcome(name: str = "OrderDelivered") -> dict[str, Any]:
    return {"name": name, "doc": "The customer receives the ordered goods."}


def ownership() -> dict[str, Any]:
    """Owner and steward as references. No role name, no score, no rating —
    FR-004-CON-3, the ticket's safety gate."""
    return {"owner": f"{PACKAGE}/type/FulfillmentPlatform"}


def lifecycle(state: str = "active") -> dict[str, Any]:
    return {"state": state, "since": "2026-01-01"}


def provenance() -> dict[str, Any]:
    return {"source": f"{PACKAGE}/type/AdoptEventDrivenOrchestration"}


def capability_record(**overrides: Any) -> dict[str, Any]:
    record: dict[str, Any] = {"fields": [identity_field("capability_id")]}
    record.update(overrides)
    return record


def business_function_record(**overrides: Any) -> dict[str, Any]:
    record: dict[str, Any] = {
        "fields": [identity_field("function_id")],
        "operations": [operation("forecast_demand")],
    }
    record.update(overrides)
    return record


def value_stream_record(**overrides: Any) -> dict[str, Any]:
    record: dict[str, Any] = {
        "fields": [identity_field("stream_id")],
        "clauses": [clause("PromiseIsHonoured")],
    }
    record.update(overrides)
    return record


def decision_record(**overrides: Any) -> dict[str, Any]:
    record: dict[str, Any] = {"clauses": [clause("OrchestrationIsEventDriven")]}
    record.update(overrides)
    return record


def objective_record(**overrides: Any) -> dict[str, Any]:
    record: dict[str, Any] = {
        "fields": [identity_field("objective_id"), temporal_field("horizon")],
        "clauses": [clause("MedianIsHalved")],
    }
    record.update(overrides)
    return record


def principle_record(**overrides: Any) -> dict[str, Any]:
    record: dict[str, Any] = {"clauses": [clause("PromiseFromLiveCapacity")]}
    record.update(overrides)
    return record


def kpi_record(**overrides: Any) -> dict[str, Any]:
    record: dict[str, Any] = {
        "fields": [
            measured_field("delivered_within_promise", "%"),
            dimensionless_field("delivered_order_count"),
        ]
    }
    record.update(overrides)
    return record


RECORD_OF = {
    "Capability": capability_record,
    "BusinessFunction": business_function_record,
    "ValueStream": value_stream_record,
    "Decision": decision_record,
    "Objective": objective_record,
    "Principle": principle_record,
    "Kpi": kpi_record,
}
