"""Shared fixtures for the module's test suite.

Two policies are enforced here and nowhere else:

* **The engine is a hard dependency of the semantic rows.** ``quire`` is not
  declared in ``pyproject.toml`` — no index a repository may commit against
  carries 0.46.0 (``internal-pypi`` serves 0.33.0 at most and no ``quire-rs``
  tag carries the semantic layer), so the wheel is provisioned by
  ``make dev-quire`` and ``agent-ix/quire-rs#392`` is the blocking issue. When
  it is absent the semantic tests **fail**; they never skip, because a skipped
  row is not coverage (FR-005).
* **The emitted schemas are read from the committed tree**, and every
  ``$ref`` to semantic-core resolves against the package the toolchain
  installs, so a record test validates against the real bytes.
"""

from __future__ import annotations

import functools
import hashlib
import json
import pathlib
import re
from typing import Any

import pytest
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
PACKAGE_ROOT = REPO_ROOT / "spec_objects_enterprise"
MANIFEST_PATH = PACKAGE_ROOT / "manifest.yaml"
SCHEMAS_DIR = PACKAGE_ROOT / "schemas"
SKELETONS_DIR = PACKAGE_ROOT / "skeletons"
NEGATIVE_DIR = REPO_ROOT / "tests" / "fixtures" / "negative"
BASELINE_DIR = REPO_ROOT / "tests" / "fixtures" / "baseline-0.1.0"
SEMANTIC_CORE_DIR = (
    REPO_ROOT
    / "node_modules"
    / "@agent-ix"
    / "semantic-core"
    / "generated"
    / "json-schema"
)

SEMANTIC_CORE_BASE = "https://schemas.agent-ix.org/semantic-core/0.3.0/"

#: The manifest declares `semantic_core: 0.3.0` (the only real, published
#: version — 0.1.0/0.2.0 never left a private dev-only mirror). quire-rs
#: vendors semantic-core bundles by exact version string
#: (`src/semantic/vendored.rs` `SEMANTIC_CORE_VERSIONS`) and the installed
#: wheel (pypi.ix's quire 0.46.0, the latest published anywhere) only vendors
#: 0.1.0, so every call through the engine for THIS module now fails: a direct
#: `extract_semantic` call raises `semantic.unsupported-semantic-core`, and
#: `validate_document`/`Registry.load_from` (which read the manifest from disk
#: themselves) silently load zero archetypes, so they report
#: `quire.QuireSchemaError: unknown archetype: <kind>` instead. Confirmed
#: empirically (verified against 0.3.0 directly, not assumed from the error
#: string). agent-ix/quire-rs#487 tracks vendoring 0.3.0 and publishing a
#: wheel that carries it.
SEMANTIC_CORE_ENGINE_ISSUE = "agent-ix/quire-rs#487"
SEMANTIC_CORE_ENGINE_REASON = (
    "the installed quire wheel (0.46.0, the latest published anywhere) only "
    "vendors semantic-core 0.1.0 and this module's real semantic_core is "
    "0.3.0, so extract_semantic/validate_document/Registry.load_from all "
    f"fail against it; {SEMANTIC_CORE_ENGINE_ISSUE}"
)

QUIRE_MISSING = (
    "the Quire wheel exposing `extract_semantic` is not installed in this "
    "environment. Run `make dev-quire` (agent-ix/quire-rs#392 tracks publishing "
    "0.46.0 to an index this repository may depend on). The semantic tests fail "
    "rather than skip, because a skipped row is not coverage."
)

OBJECT_TYPES = (
    "capability",
    "business_function",
    "value_stream",
    "decision",
    "objective",
    "principle",
    "kpi",
)

MODEL_OF = {
    "capability": "Capability",
    "business_function": "BusinessFunction",
    "value_stream": "ValueStream",
    "decision": "Decision",
    "objective": "Objective",
    "principle": "Principle",
    "kpi": "Kpi",
}

VERB_ENUM_OF = {
    "capability": "CapabilityVerb",
    "business_function": "BusinessFunctionVerb",
    "value_stream": "ValueStreamVerb",
    "decision": "DecisionVerb",
    "objective": "ObjectiveVerb",
    "principle": "PrincipleVerb",
    "kpi": "KpiVerb",
}

MARKER_MODELS = (
    "IdentityField",
    "TemporalField",
    "TemporalTypeRef",
    "MeasuredField",
    "MeasuredTypeRef",
)

DECLARATION_MODELS = (
    "MeasureDecl",
    "TargetDecl",
    "ThresholdDecl",
    "StageDecl",
    "OutcomeDecl",
    "AlternativeDecl",
    "LifecycleDecl",
    "OwnershipDecl",
    "ProvenanceDecl",
)

VOCABULARY_ENUMS = (
    "AggregationKind",
    "Direction",
    "Comparator",
    "ThresholdLevel",
    "LifecycleState",
)

SUPPORT_MODELS = (
    MARKER_MODELS + DECLARATION_MODELS + VOCABULARY_ENUMS + tuple(VERB_ENUM_OF.values())
)

KERNEL_SCALARS = frozenset(
    {
        "UUID",
        "Boolean",
        "Integer",
        "Decimal",
        "String",
        "Timestamp",
        "Duration",
        "Bytes",
        "JsonObject",
    }
)


def load_manifest() -> dict[str, Any]:
    return yaml.safe_load(MANIFEST_PATH.read_text())


def manifest_version() -> str:
    return load_manifest()["version"]


def module_base() -> str:
    """The `$id` base, read from the manifest version — never hard-coded
    (FR-002-CON-5)."""
    return (
        "https://schemas.agent-ix.org/agent-ix/spec-objects-enterprise/"
        f"{manifest_version()}/"
    )


def object_types() -> list[dict[str, Any]]:
    return load_manifest()["object_types"]


def object_type(name: str) -> dict[str, Any]:
    return next(ot for ot in object_types() if ot["name"] == name)


def locators(ot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    body = ot.get("body_extraction") or {}
    return ((body.get("yield_pattern") or {}).get("match")) or {}


def frontmatter(markdown: str) -> dict[str, Any]:
    match = re.match(r"---\n(.*?)\n---\n", markdown, re.DOTALL)
    assert match, "document has no frontmatter"
    return yaml.safe_load(match.group(1))


def sha256_of(path: pathlib.Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def schema_json(model: str) -> dict[str, Any]:
    return json.loads((SCHEMAS_DIR / f"{model}.json").read_text())


def require_quire():
    """Import quire, or fail the test naming the provisioning path."""
    try:
        import quire
    except ImportError as error:
        pytest.fail(f"{QUIRE_MISSING} (import error: {error})")
    if not hasattr(quire, "extract_semantic"):
        pytest.fail(
            f"`extract_semantic` is missing from the installed quire: {QUIRE_MISSING}"
        )
    return quire


@pytest.fixture(scope="session")
def quire_engine():
    return require_quire()


@pytest.fixture(scope="session")
def manifest() -> dict[str, Any]:
    return load_manifest()


@pytest.fixture(scope="session")
def semantic_block(manifest: dict[str, Any]) -> dict[str, Any]:
    return manifest["semantic"]


@pytest.fixture(scope="session")
def semantic_module(semantic_block: dict[str, Any]) -> dict[str, Any]:
    """The `module` block `extract_semantic` takes, derived from the manifest."""
    return {
        "contractVersion": semantic_block["contract_version"],
        "semanticCore": semantic_block["semantic_core"],
        "package": semantic_block["package"],
        "exports": semantic_block["exports"],
        "imports": semantic_block["imports"],
        "compatibilityPosture": semantic_block["compatibility_posture"],
        "legacyForms": semantic_block["legacy_forms"],
    }


@pytest.fixture(scope="session")
def skeletons() -> list[pathlib.Path]:
    return sorted(SKELETONS_DIR.glob("*.md"))


@pytest.fixture(scope="session")
def bundle_index(semantic_block: dict[str, Any]) -> dict[str, Any]:
    """A bundle index built from the skeleton frontmatter (FR-005-AC-3)."""
    objects: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in sorted(SKELETONS_DIR.glob("*.md")):
        front = frontmatter(path.read_text())
        if front["id"] in seen:
            continue
        seen.add(front["id"])
        objects.append({"id": front["id"], "names": [front["id"], front["title"]]})
    return {
        "package": semantic_block["package"],
        "objects": objects,
        "enumerations": [],
        "imports": {},
    }


@pytest.fixture(scope="session")
def schema_registry():
    """A 2020-12 validator factory over the shipped schemas plus semantic-core.

    Every `$ref` resolves locally: module models from the committed
    `schemas/` directory, grammar models from the semantic-core package the
    pinned toolchain installs.
    """
    from referencing import Registry, Resource

    if not SEMANTIC_CORE_DIR.is_dir():
        pytest.fail(
            "@agent-ix/semantic-core is not installed, so `$ref`s to the grammar "
            "cannot resolve. Run `npm ci` (FR-002-CON-4: `@agent-ix` resolves "
            "from npm.ix through the user-level npm config)."
        )
    resources = []
    for path in sorted(SCHEMAS_DIR.glob("*.json")):
        if path.name == "toolchain.json":
            continue
        schema = json.loads(path.read_text())
        resources.append((schema["$id"], Resource.from_contents(schema)))
    for path in sorted(SEMANTIC_CORE_DIR.glob("*.json")):
        schema = json.loads(path.read_text())
        uri = schema.get("$id") or f"{SEMANTIC_CORE_BASE}{path.name}"
        resources.append((uri, Resource.from_contents(schema)))
    registry = Registry().with_resources(resources)

    def validator_for(model: str):
        from jsonschema import Draft202012Validator

        return Draft202012Validator(schema_json(model), registry=registry)

    return validator_for


@functools.cache
def engine_accepts_module_semantic_core() -> bool:
    """Whether the installed quire engine vendors a bundle for this module's
    *real* declared `semantic_core` (read from the manifest). Probed
    empirically against the manifest value, never assumed from the version
    number alone."""
    try:
        import quire
    except ImportError:
        return True  # `require_quire` fails those tests by name.
    version = load_manifest()["semantic"]["semantic_core"]
    request = {
        "markdown": (
            "---\nid: probe\ntitle: Probe\ntype: principle\n"
            "object: principle\n---\n# [probe] Probe\n\n"
            "## Rationale\n\nThe probe exists to check engine support only.\n"
        ),
        "module": {
            "contractVersion": "1.0.0",
            "semanticCore": version,
            "package": "agent-ix/spec-objects-enterprise",
            "exports": ["principle"],
        },
        "path": "spec/probe.md",
        "bundle": {"package": "agent-ix/spec-objects-enterprise"},
    }
    try:
        quire.extract_semantic(request)
    except TypeError as error:
        if "semantic.unsupported-semantic-core" in str(error):
            return False
        raise
    return True


def semantic_core_engine_xfail():
    """A strict xfail on an installed engine that does not vendor this
    module's declared `semantic_core` yet; agent-ix/quire-rs#487. Covers both
    failure shapes: a direct `extract_semantic` `TypeError` and the silent
    zero-archetype load that `validate_document`/`Registry.load_from` turn
    into `unknown archetype: <kind>`."""
    return pytest.mark.xfail(
        condition=not engine_accepts_module_semantic_core(),
        strict=True,
        reason=SEMANTIC_CORE_ENGINE_REASON,
    )
