"""Skeleton ↔ manifest parity + roundtrip validation for the 7 object types.

Mirrors the spec-artifacts-iso pattern: the per-object-type skeletons under
``spec_objects_enterprise/skeletons/`` are the authoring source of truth and
the manifest's ``body_extraction`` locators are the structural contract. These
tests cover:

* every object type ships a skeleton;
* parity: every required ``section_body`` heading exists in the skeleton at
  the asserted level, and (reverse direction) every skeleton H2 corresponds to
  a declared ``section_body`` locator, so neither side drifts;
* every required ``section_body`` is filled substantively (non-empty,
  no placeholder tokens);
* skeleton frontmatter carries every declared ``frontmatter_field`` (id,
  title, artifact_type, plus objective/kpi measurable fields) and
  ``artifact_type`` equals the object type name;
* the core locators are ``required: true`` in the manifest (the tightened
  contract cannot silently regress to trivially-passing);
* roundtrip: each skeleton passes the quire wheel's ``validate_document`` and
  a mutated copy fails (skipped cleanly when the installed wheel predates the
  markdown-default validator).
"""

from __future__ import annotations

import pathlib
import re

import pytest
import yaml

PKG_ROOT = pathlib.Path(__file__).resolve().parent.parent / "spec_objects_enterprise"
MANIFEST_PATH = PKG_ROOT / "manifest.yaml"
SKELETONS_DIR = PKG_ROOT / "skeletons"

_OBJECT_TYPE_NAMES = [
    "capability",
    "business_function",
    "value_stream",
    "decision",
    "objective",
    "principle",
    "kpi",
]

# Defining field(s) per type that the tightened manifest must require.
_DEFINING_REQUIRED = {
    "capability": {"sub_capabilities"},
    "business_function": {"description_body"},
    "value_stream": {"stages"},
    "decision": {"decision_body"},
    "objective": {"metric", "target"},
    "principle": {"rationale"},
    "kpi": {"metric", "target"},
}

_PLACEHOLDER_TOKENS = ("TODO", "TBD", "{{", "}}", "placeholder", "none specified")


def _object_types() -> list[dict]:
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    return manifest.get("object_types", [])


def _object_type(name: str) -> dict:
    return next(ot for ot in _object_types() if ot["name"] == name)


def _match(ot: dict) -> dict:
    be = ot.get("body_extraction") or {}
    return (be.get("yield_pattern") or {}).get("match") or {}


def _section_body_locators(ot: dict, required_only: bool = False) -> list[dict]:
    """Return ``[{field, heading, level}]`` for every ``section_body`` locator."""
    out: list[dict] = []
    for field, loc in _match(ot).items():
        if not isinstance(loc, dict) or loc.get("from") != "section_body":
            continue
        if required_only and not loc.get("required"):
            continue
        level = (loc.get("assert") or {}).get("level", 2)
        out.append({"field": field, "heading": loc["after_heading"], "level": level})
    return out


def _frontmatter_locators(ot: dict, required_only: bool = False) -> list[str]:
    """Return the frontmatter key for every ``frontmatter_field`` locator."""
    out: list[str] = []
    for loc in _match(ot).values():
        if not isinstance(loc, dict) or loc.get("from") != "frontmatter_field":
            continue
        if required_only and not loc.get("required"):
            continue
        out.append(loc["path"][0])
    return out


def _skeleton_text(name: str) -> str:
    return (SKELETONS_DIR / f"{name}.md").read_text()


def _skeleton_frontmatter(markdown: str) -> dict:
    fm = re.match(r"---\n(.*?)\n---\n", markdown, re.DOTALL)
    assert fm, "skeleton missing frontmatter"
    return yaml.safe_load(fm.group(1))


def _strip_frontmatter(markdown: str) -> str:
    return re.sub(r"^---\n.*?\n---\n", "", markdown, count=1, flags=re.DOTALL)


def _skeleton_headings(markdown: str) -> list[tuple[int, str]]:
    """Return ``[(level, text)]`` for every ATX heading in the body."""
    out: list[tuple[int, str]] = []
    for line in _strip_frontmatter(markdown).splitlines():
        m = re.match(r"^(#{1,6})\s+(.*\S)\s*$", line)
        if m:
            out.append((len(m.group(1)), m.group(2).strip()))
    return out


def _split_sections(markdown: str, level: int = 2) -> dict:
    """Return {section_name: body_text} for headings at the given level."""
    body = _strip_frontmatter(markdown)
    sections: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []
    prefix = "#" * level + " "
    for line in body.splitlines():
        if line.startswith(prefix) and not line[level + 1 :].startswith("#"):
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = line[len(prefix) :].strip()
            buf = []
        elif current is not None:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections


# ─── Manifest contract: the tightened asserts ─────────────────────────────


def test_manifest_declares_all_object_types() -> None:
    assert [ot["name"] for ot in _object_types()] == _OBJECT_TYPE_NAMES


@pytest.mark.parametrize("name", _OBJECT_TYPE_NAMES, ids=lambda n: n)
def test_core_frontmatter_locators_required(name: str) -> None:
    """id, title and artifact_type are required for every object type."""
    ot = _object_type(name)
    match = _match(ot)
    for field in ("id", "title", "artifact_type"):
        loc = match[field]
        assert loc["from"] == "frontmatter_field", f"{name}.{field} wrong locator"
        assert loc.get("required") is True, f"{name}.{field} is not required"


@pytest.mark.parametrize("name", _OBJECT_TYPE_NAMES, ids=lambda n: n)
def test_defining_fields_required(name: str) -> None:
    """Each type's defining field(s) carry ``required: true`` in the manifest."""
    ot = _object_type(name)
    match = _match(ot)
    for field in _DEFINING_REQUIRED[name]:
        loc = match[field]
        assert loc.get("required") is True, f"{name}.{field} is not required"


# ─── Skeleton presence + parity (both directions) ─────────────────────────


@pytest.mark.parametrize("name", _OBJECT_TYPE_NAMES, ids=lambda n: n)
def test_skeleton_exists(name: str) -> None:
    assert (SKELETONS_DIR / f"{name}.md").exists(), f"missing skeleton {name}.md"


@pytest.mark.parametrize("name", _OBJECT_TYPE_NAMES, ids=lambda n: n)
def test_asserted_headings_present_at_level(name: str) -> None:
    """Every ``section_body`` heading the manifest asserts exists in the
    skeleton at the asserted level."""
    ot = _object_type(name)
    headings = set(_skeleton_headings(_skeleton_text(name)))
    for sec in _section_body_locators(ot):
        assert (sec["level"], sec["heading"]) in headings, (
            f"{name}: asserted heading {sec['heading']!r} (H{sec['level']}) "
            f"absent from skeleton"
        )


@pytest.mark.parametrize("name", _OBJECT_TYPE_NAMES, ids=lambda n: n)
def test_reverse_parity_no_skeleton_drift(name: str) -> None:
    """Reverse direction: every skeleton H2 corresponds to a declared
    ``section_body`` locator, so the skeleton cannot drift ahead of the
    manifest contract. Types with no section locators carry no H2s."""
    ot = _object_type(name)
    declared = {(s["level"], s["heading"]) for s in _section_body_locators(ot)}
    declared_levels = {lvl for lvl, _ in declared} or {2}
    for lvl, text in _skeleton_headings(_skeleton_text(name)):
        if lvl == 1:
            continue  # the H1 carries the variable [id] title, never asserted
        assert lvl in declared_levels and (lvl, text) in declared, (
            f"{name}: skeleton heading {text!r} (H{lvl}) is not declared by the "
            f"manifest (skeleton drifted ahead of the contract)"
        )


@pytest.mark.parametrize("name", _OBJECT_TYPE_NAMES, ids=lambda n: n)
def test_required_section_bodies_substantive(name: str) -> None:
    """Every required ``section_body`` is filled with substantive,
    non-placeholder content."""
    ot = _object_type(name)
    sections = _split_sections(_skeleton_text(name), level=2)
    for sec in _section_body_locators(ot, required_only=True):
        heading = sec["heading"]
        assert heading in sections, f"{name}: section {heading!r} missing"
        body = sections[heading]
        assert body, f"{name}: section_body {heading!r} is empty in skeleton"
        lowered = body.lower()
        for token in _PLACEHOLDER_TOKENS:
            assert token.lower() not in lowered, (
                f"{name}: section_body {heading!r} carries placeholder token "
                f"{token!r}"
            )


@pytest.mark.parametrize("name", _OBJECT_TYPE_NAMES, ids=lambda n: n)
def test_frontmatter_carries_declared_fields(name: str) -> None:
    """The skeleton frontmatter carries every declared ``frontmatter_field``
    (required or optional) with a real value, and artifact_type == type name."""
    ot = _object_type(name)
    fm = _skeleton_frontmatter(_skeleton_text(name))
    for key in _frontmatter_locators(ot):
        assert key in fm, f"{name}: frontmatter missing {key!r}"
        value = fm[key]
        assert value not in (None, ""), f"{name}: frontmatter {key!r} is empty"
        lowered = str(value).lower()
        for token in _PLACEHOLDER_TOKENS:
            assert (
                token.lower() not in lowered
            ), f"{name}: frontmatter {key!r} carries placeholder token {token!r}"
    assert fm["artifact_type"] == name, (
        f"{name}: frontmatter artifact_type is {fm['artifact_type']!r}, "
        f"expected {name!r}"
    )


# ─── Roundtrip against the quire wheel ─────────────────────────────────────


def _quire_doc_validator():
    """Return the quire wheel iff it exposes the markdown-default validator."""
    try:
        import quire
    except ImportError:
        return None
    if not hasattr(quire, "validate_document"):
        return None
    return quire


@pytest.mark.parametrize("name", _OBJECT_TYPE_NAMES, ids=lambda n: n)
def test_roundtrip_skeleton_validates(name: str) -> None:
    """Each filled skeleton passes ``validate_document`` against this module.

    Skips when the installed quire wheel predates the markdown-default
    validator; install a quire >=0.3.6 wheel to exercise it."""
    quire = _quire_doc_validator()
    if quire is None:
        pytest.skip("quire wheel lacks validate_document")
    res = quire.validate_document(name, str(PKG_ROOT), _skeleton_text(name))
    assert res["is_valid"], res["errors"]


def test_roundtrip_mutation_fails() -> None:
    """Deleting the required Sub-capabilities section fails validation."""
    quire = _quire_doc_validator()
    if quire is None:
        pytest.skip("quire wheel lacks validate_document")
    base = _skeleton_text("capability")
    mutated = base.replace("## Sub-capabilities", "## Something Else", 1)
    assert mutated != base, "mutation did not apply"
    res = quire.validate_document("capability", str(PKG_ROOT), mutated)
    assert not res["is_valid"], "mutated capability skeleton still validates"
