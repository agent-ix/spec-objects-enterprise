import "@typespec/json-schema";
import "@agent-ix/semantic-core";

using TypeSpec.JsonSchema;
using AgentIx.Semantic.Core;

/**
 * Tier-2 enterprise-architecture object declaration schemas
 * (agent-ix/spec-objects-enterprise#4).
 *
 * One model per enterprise object type this module contributes, each validating
 * that type's Quire declaration record (fields, relations, clauses,
 * operations; quire-rs FR-070..FR-072) with type-specific required keys,
 * forbidden keys, and item rules (FR-004). Every grammar item is a `$ref` to
 * `@agent-ix/semantic-core` 0.3.0 and is never redeclared here (FR-004-CON-1);
 * this namespace contributes archetype shapes only.
 *
 * The definition / measurement boundary the ticket asks for lives in `Kpi`:
 * a KPI declaration names what is measured and in which unit (at least one
 * field carrying `type.unit`) and carries neither the identity of a reading
 * (zero identity fields) nor the instant of one (zero `Timestamp` fields), so a
 * record shaped like an observation is refused. `Objective` is its mirror: it
 * is time-bound (at least one `Timestamp` field) and references a measure
 * definition through `targets[].measure` rather than declaring one.
 *
 * The `$id` base embeds the manifest `version` by intent (FR-002-CON-5): one
 * schema URL names exactly one immutable byte sequence, so a downstream fixture
 * reader that pinned a version can never silently read later bytes. A bump edits
 * this base and `manifest.yaml`'s `version` in one commit and re-runs
 * `make schemas`.
 */
@jsonSchema("https://schemas.agent-ix.org/agent-ix/spec-objects-enterprise/0.2.0/")
namespace AgentIx.SpecObjects.Enterprise;

// ---------------------------------------------------------------------------
// Open marker models — `contains` predicates only
// ---------------------------------------------------------------------------

/**
 * Open marker: a `FieldDecl` flagged as identity. Deliberately open so it
 * matches any identity-flagged field.
 */
model IdentityField {
  identity: true;
}

/** Open marker: a `TypeRef` whose target is the kernel `Timestamp` scalar. */
model TemporalTypeRef {
  target: KernelScalar.Timestamp;
}

/**
 * Open marker: a `FieldDecl` whose type targets `Timestamp`. Required at least
 * once by `Objective` (the horizon) and forbidden entirely by `Kpi` (it would
 * be the instant of a reading).
 */
model TemporalField {
  type: TemporalTypeRef;
}

/** Open marker: a `TypeRef` carrying a unit symbol. */
model MeasuredTypeRef {
  unit: UnitSymbol;
}

/**
 * Open marker: a `FieldDecl` whose type carries a unit — the measure a KPI
 * definition names. A dimensionless measure uses the UCUM unity symbol `1`, so
 * a count or a ratio satisfies this predicate without a dimensional unit.
 */
model MeasuredField {
  type: MeasuredTypeRef;
}

// ---------------------------------------------------------------------------
// Closed vocabularies
// ---------------------------------------------------------------------------

/** How a measure aggregates its observations. */
enum AggregationKind {
  sum,
  average,
  median,
  percentile,
  ratio,
  count,
  max,
  min,
}

/** Which way is better for a measure. Not a score: a reading direction. */
enum Direction {
  higher_is_better,
  lower_is_better,
  target_band,
}

/** How a declared bound compares against a measure. */
enum Comparator {
  at_least,
  at_most,
  equals,
  within,
}

/** Alerting levels a KPI declaration may attach to a bound. */
enum ThresholdLevel {
  alert,
  warning,
  breach,
}

/** Lifecycle state of a declaration. */
enum LifecycleState {
  proposed,
  accepted,
  active,
  deprecated,
  retired,
}

// ---------------------------------------------------------------------------
// Relation-verb vocabularies — equal to each type's manifest `allowed_links`
// keys (FR-003-AC-7)
// ---------------------------------------------------------------------------

/** Relation verbs a `capability` declaration may use. */
enum CapabilityVerb {
  decomposes,
  realizes,
  depends_on,
  references,
}

/** Relation verbs a `business_function` declaration may use. */
enum BusinessFunctionVerb {
  supports,
  realizes,
  references,
}

/** Relation verbs a `value_stream` declaration may use. */
enum ValueStreamVerb {
  contains,
}

/** Relation verbs a `decision` declaration may use. */
enum DecisionVerb {
  references,
  supersedes,
  constrains,
}

/** Relation verbs an `objective` declaration may use. */
enum ObjectiveVerb {
  supports,
  references,
}

/** Relation verbs a `principle` declaration may use. */
enum PrincipleVerb {
  governs,
}

/** Relation verbs a `kpi` declaration may use. */
enum KpiVerb {
  measures,
}

// ---------------------------------------------------------------------------
// Declaration support models
// ---------------------------------------------------------------------------

/**
 * The definition of a measure: what is measured, in which unit, how it
 * aggregates, and which way is better. It carries no value and no instant —
 * those belong to an observation, which this module does not type.
 */
model MeasureDecl {
  name: Identifier;
  unit: UnitSymbol;
  aggregation: AggregationKind;
  direction: Direction;
  window?: string;
  doc?: string;
  ...Record<never>;
}

/**
 * A declared target against a named measure definition. `measure` is a
 * `SemanticId` naming a `kpi` declaration, and `bound` is the limit the
 * objective commits to — never an observed reading.
 */
model TargetDecl {
  measure: SemanticId;
  comparator: Comparator;
  bound: string;
  by?: string;
  doc?: string;
  ...Record<never>;
}

/** A declared alerting bound on a measure definition. */
model ThresholdDecl {
  level: ThresholdLevel;
  comparator: Comparator;
  bound: string;
  doc?: string;
  ...Record<never>;
}

/**
 * One stage of a value stream.
 *
 * Reader rules JSON Schema cannot express (FR-004): `order` is unique and
 * contiguous from 1 within one `stages` array, and `name` is unique within it.
 */
model StageDecl {
  name: Identifier;

  @minValue(1)
  order: int32;

  value: string;
  inputs?: SemanticId[];
  outputs?: SemanticId[];
  doc?: string;
  ...Record<never>;
}

/** One outcome a capability produces. Unique by `name` within `outcomes`. */
model OutcomeDecl {
  name: Identifier;
  doc: string;
  ...Record<never>;
}

/** One alternative a decision rejected. Unique by `name` within `alternatives`. */
model AlternativeDecl {
  name: Identifier;
  doc: string;
  rejected_because: string;
  ...Record<never>;
}

/** The lifecycle state of a declaration. */
model LifecycleDecl {
  state: LifecycleState;
  since?: string;
  superseded_by?: SemanticId;
  ...Record<never>;
}

/**
 * Who owns a declaration.
 *
 * Deliberately carries no role name, no score and no rating: the organizational
 * role vocabulary is corpus-review evidence this module does not have
 * (FR-004-CON-3, the ticket's safety gate).
 */
model OwnershipDecl {
  owner: SemanticId;
  steward?: SemanticId;
  ...Record<never>;
}

/** Where a declaration came from. */
model ProvenanceDecl {
  source: SemanticId;
  method?: string;
  recorded_in?: SemanticId;
  ...Record<never>;
}

// ---------------------------------------------------------------------------
// Object-type declaration records
// ---------------------------------------------------------------------------

/**
 * A capability: an ability the organization holds. It is identified in the
 * architecture graph, so it carries at least one identity field; `operations`
 * is forbidden by the seal, because a capability exposes no interface — the
 * business functions that realize it do.
 */
@extension(
  "allOf",
  #[
    #{
      properties: #{
        relations: #{ items: #{ properties: #{ verb: #{ `$ref`: "CapabilityVerb.json" } } } },
      },
    }
  ]
)
model Capability {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  relations?: RelationDecl[];
  clauses?: ClauseRef[];
  scope?: string;
  outcomes?: OutcomeDecl[];
  owner?: OwnershipDecl;
  lifecycle?: LifecycleDecl;
  provenance?: ProvenanceDecl;
  ...Record<never>;
}

/**
 * A business function: what the organization performs. A function is defined by
 * what it does, so `operations` is required and non-empty.
 */
@extension(
  "allOf",
  #[
    #{
      properties: #{
        relations: #{
          items: #{ properties: #{ verb: #{ `$ref`: "BusinessFunctionVerb.json" } } },
        },
      },
    }
  ]
)
model BusinessFunction {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  @minItems(1)
  operations: OperationDecl[];

  relations?: RelationDecl[];
  clauses?: ClauseRef[];
  scope?: string;
  inputs?: SemanticId[];
  outputs?: SemanticId[];
  owner?: OwnershipDecl;
  lifecycle?: LifecycleDecl;
  provenance?: ProvenanceDecl;
  ...Record<never>;
}

/**
 * A value stream: the end-to-end path from a triggering stakeholder to the
 * value received. `clauses` is required because a value stream exists to make a
 * guarantee; `operations` is forbidden by the seal.
 */
@extension(
  "allOf",
  #[
    #{
      properties: #{
        relations: #{ items: #{ properties: #{ verb: #{ `$ref`: "ValueStreamVerb.json" } } } },
      },
    }
  ]
)
model ValueStream {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  @minItems(1)
  clauses: ClauseRef[];

  relations?: RelationDecl[];
  scope?: string;
  stages?: StageDecl[];
  owner?: OwnershipDecl;
  lifecycle?: LifecycleDecl;
  provenance?: ProvenanceDecl;
  ...Record<never>;
}

/**
 * A decision: a commitment taken, stated as an asserted clause rather than as
 * prose. `operations` is forbidden by the seal.
 */
@extension(
  "allOf",
  #[
    #{
      properties: #{
        relations: #{ items: #{ properties: #{ verb: #{ `$ref`: "DecisionVerb.json" } } } },
      },
    }
  ]
)
model Decision {
  @minItems(1)
  clauses: ClauseRef[];

  fields?: FieldDecl[];
  relations?: RelationDecl[];
  alternatives?: AlternativeDecl[];
  owner?: OwnershipDecl;
  lifecycle?: LifecycleDecl;
  provenance?: ProvenanceDecl;
  ...Record<never>;
}

/**
 * An objective: a time-bound commitment measured against a KPI definition.
 *
 * Its `fields` carry an identity and a horizon, expressed as a second
 * `contains` predicate through `allOf` because JSON Schema admits one
 * `contains` per array. `measure` is absent by intent: an objective references
 * a measure definition through `targets[].measure` and never declares one.
 */
@extension(
  "allOf",
  #[
    #{ properties: #{ fields: #{ contains: #{ `$ref`: "TemporalField.json" }, minContains: 1 } } },
    #{
      properties: #{
        relations: #{ items: #{ properties: #{ verb: #{ `$ref`: "ObjectiveVerb.json" } } } },
      },
    }
  ]
)
model Objective {
  @minItems(1)
  @contains(IdentityField)
  fields: FieldDecl[];

  @minItems(1)
  clauses: ClauseRef[];

  relations?: RelationDecl[];
  targets?: TargetDecl[];
  owner?: OwnershipDecl;
  lifecycle?: LifecycleDecl;
  provenance?: ProvenanceDecl;
  ...Record<never>;
}

/**
 * A principle: a rule that governs. It declares no data and no behaviour, so
 * `fields` and `operations` are both forbidden by the seal.
 */
@extension(
  "allOf",
  #[
    #{
      properties: #{
        relations: #{ items: #{ properties: #{ verb: #{ `$ref`: "PrincipleVerb.json" } } } },
      },
    }
  ]
)
model Principle {
  @minItems(1)
  clauses: ClauseRef[];

  relations?: RelationDecl[];
  owner?: OwnershipDecl;
  lifecycle?: LifecycleDecl;
  provenance?: ProvenanceDecl;
  ...Record<never>;
}

/**
 * A KPI: the definition of a measure, never a reading of one.
 *
 * Three item rules carry the ticket's headline criterion. At least one field
 * carries a unit (what is measured, and in what) — a dimensionless measure uses
 * the UCUM unity symbol `1`. No field is an identity field: a definition has no
 * per-occurrence identity, an observation does. No field targets `Timestamp`:
 * a definition has no instant, an observation does. `targets` is absent by
 * intent — the goal set against a measure belongs to the objective that sets
 * it, not to the measure.
 */
@extension(
  "allOf",
  #[
    #{ properties: #{ fields: #{ contains: #{ `$ref`: "MeasuredField.json" }, minContains: 1 } } },
    #{
      properties: #{
        fields: #{ contains: #{ `$ref`: "TemporalField.json" }, minContains: 0, maxContains: 0 },
      },
    },
    #{
      properties: #{
        relations: #{ items: #{ properties: #{ verb: #{ `$ref`: "KpiVerb.json" } } } },
      },
    }
  ]
)
model Kpi {
  @minItems(1)
  @contains(IdentityField)
  @minContains(0)
  @maxContains(0)
  fields: FieldDecl[];

  relations?: RelationDecl[];
  clauses?: ClauseRef[];
  measure?: MeasureDecl;
  thresholds?: ThresholdDecl[];
  owner?: OwnershipDecl;
  lifecycle?: LifecycleDecl;
  provenance?: ProvenanceDecl;
  ...Record<never>;
}
