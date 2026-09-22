"""Additive-compatibility tests (NFR-001): the 0.2.0 module stays additive over
the checked-in 0.1.0 set.

The population is the frozen baseline under `tests/fixtures/baseline-0.1.0/`:
the 0.1.0 `body_extraction` locators and all seven 0.1.0 skeletons, captured
from `origin/main` before this change touched anything. It is the checked-in
set, not the corpus; the corpus sweep is `agent-ix/quoin#291`.
"""

from __future__ import annotations

import json
import re

import pytest

from tests.conftest import (
    BASELINE_DIR,
    PACKAGE_ROOT,
    frontmatter,
    locators,
    object_type,
    semantic_core_engine_xfail,
)


def baseline_locators() -> dict:
    return json.loads((BASELINE_DIR / "body_extraction.json").read_text())


def baseline_skeletons() -> list:
    return sorted((BASELINE_DIR / "skeletons").glob("*.md"))


def extract_semantic(quire_engine, module, path):
    return quire_engine.extract_semantic(
        {
            "markdown": path.read_text(),
            "module": module,
            "path": str(path),
            "bundle": {
                "package": module["package"],
                "objects": [],
                "enumerations": [],
                "imports": {},
            },
        }
    )


def section_body(path, heading: str) -> str:
    """The section body as it stood at 0.1.0, read straight from the frozen
    fixture — an independent oracle, not another engine run."""
    text = path.read_text()
    text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    match = re.search(
        rf"^## {re.escape(heading)}[ \t]*$(.*?)(?=^## |\Z)",
        text,
        re.DOTALL | re.MULTILINE,
    )
    assert match, f"{path.name} has no `## {heading}` section"
    return match.group(1).strip()


@pytest.mark.trace("TC-060", "NFR-001-AC-1")
def test_no_baseline_locator_definition_changed():
    baseline = baseline_locators()
    assert baseline["version"] == "0.1.0"
    changed = []
    for name, extraction in baseline["object_types"].items():
        old = (extraction or {})["yield_pattern"]["match"]
        new = locators(object_type(name))
        for key, facets in old.items():
            if new.get(key) != facets:
                changed.append(f"{name}.{key}")
    assert changed == []


@pytest.mark.trace("TC-061", "NFR-001-AC-2")
@semantic_core_engine_xfail()
def test_every_baseline_skeleton_validates_under_the_new_manifest(quire_engine):
    """Measured, not assumed: the seven 0.1.0 skeletons carry no frontmatter
    `object:` key, so Quire runs headings-only validation on them and the typed
    record is never assembled or checked. That is what makes 0.2.0 additive for
    the artifacts that exist today."""
    baseline = baseline_skeletons()
    assert len(baseline) == 7
    failures = {}
    for path in baseline:
        text = path.read_text()
        assert "object" not in frontmatter(text), path.name
        result = quire_engine.validate_document(
            frontmatter(text)["type"], str(PACKAGE_ROOT), text
        )
        if result["errors"]:
            failures[path.name] = [e["message"] for e in result["errors"]]
    assert failures == {}


@pytest.mark.trace("TC-061", "NFR-001-AC-2")
@pytest.mark.xfail(
    strict=True,
    reason=(
        "The engine defect NFR-001's Verification names: once a legacy-form "
        "artifact carries `object:`, quire 0.46.0 assembles its declaration "
        "record as `{}` and checks it against the type schema unconditionally, "
        "so it fails `semantic.record-invalid` at error severity even under "
        "`legacy_forms: warning`. agent-ix/quire-rs#391 owns the rule. The "
        "schema is not relaxed and the row is an expected failure, never a skip."
    ),
)
def test_a_legacy_form_artifact_that_declares_its_object_is_not_an_error(quire_engine):
    text = (BASELINE_DIR / "skeletons" / "capability.md").read_text()
    text = text.replace(
        "type: capability\n", "type: capability\nobject: capability\n", 1
    )
    result = quire_engine.validate_document("capability", str(PACKAGE_ROOT), text)
    assert [e["message"] for e in result["errors"]] == []


@pytest.mark.trace("TC-062", "NFR-001-AC-3")
@semantic_core_engine_xfail()
def test_no_baseline_skeleton_yields_a_legacy_properties_warning(
    quire_engine, semantic_module
):
    """The measured value is 0, not the sibling business module's 1: no 0.1.0
    enterprise skeleton carries a `## Properties` section in any form, so there
    is no legacy Properties form to warn about."""
    for path in baseline_skeletons():
        assert "## Properties" not in path.read_text(), path.name
        record = extract_semantic(quire_engine, semantic_module, path)
        warnings = [
            d
            for d in record.get("diagnostics", [])
            if d.get("code") == "semantic.legacy-properties-form"
        ]
        assert warnings == [], (path.name, record.get("diagnostics"))


@pytest.mark.trace("TC-063", "NFR-001-AC-4")
@semantic_core_engine_xfail()
def test_the_required_yields_are_byte_identical_across_versions(quire_engine):
    """The untyped section and frontmatter yields are what every existing
    consumer reads; the 0.2.0 locators must leave them untouched."""
    baseline = baseline_locators()["object_types"]
    for path in baseline_skeletons():
        name = path.stem
        text = path.read_text()
        extracted = quire_engine.extract(name, str(PACKAGE_ROOT), text)["extraction"]
        assert len(extracted) == 1, (name, extracted)
        record = extracted[0]
        front = frontmatter(text)
        old = (baseline[name] or {})["yield_pattern"]["match"]
        checked = 0
        for key, facets in old.items():
            if not facets.get("required"):
                continue
            if facets["from"] == "frontmatter_field":
                assert record[key] == front[facets["path"][0]], (name, key)
            else:
                assert record[key] == section_body(path, facets["after_heading"]), (
                    name,
                    key,
                )
            checked += 1
        assert checked >= 3, (name, checked)
