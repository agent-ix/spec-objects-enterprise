"""Skeleton fixture tests (FR-005): the skeletons as executable typed
fixtures, and the negative fixtures that pin what the schemas and the engine
refuse.

Two resolution paths are exercised and are kept distinct: `validate_document`
runs the module's own registry over one document, while `extract_semantic` runs
under a bundle index built from the skeleton frontmatter. Only the second can
resolve a `Type` cell that names another skeleton.
"""

from __future__ import annotations

import re
import subprocess

import pytest

from tests.conftest import (
    KERNEL_SCALARS,
    NEGATIVE_DIR,
    OBJECT_TYPES,
    PACKAGE_ROOT,
    REPO_ROOT,
    SKELETONS_DIR,
    frontmatter,
    locators,
    object_type,
)

IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

FIELD_BEARING = {
    "capability",
    "business_function",
    "value_stream",
    "decision",
    "objective",
    "kpi",
}
OPERATION_BEARING = {"business_function"}
ALTERNATES = ("capability", "objective", "kpi")

EXPECTED_NEGATIVES = {
    "kpi-observed-at-row.md": "semantic.record-invalid",
    "kpi-identity-row.md": "semantic.record-invalid",
    "kpi-no-unit-row.md": "semantic.record-invalid",
    "objective-no-horizon-row.md": "semantic.record-invalid",
    "principle-with-properties.md": "semantic.record-invalid",
    "capability-no-identity-row.md": "semantic.record-invalid",
    "business_function-no-operations.md": "semantic.record-invalid",
    "properties-both-forms.md": "semantic.properties-both-forms",
    "operation-dangling-post-clause.md": "semantic.dangling-clause-ref",
    "type-token-not-identifier.md": "semantic.invalid-type-token",
}

PLACEHOLDER_TOKENS = ("TODO", "TBD", "{{", "}}", "FIXME", "XXX")

SCORING_WORDS = (
    "maturity score",
    "trust score",
    "management score",
    "performance rating",
    "staff rating",
)


def skeleton_paths() -> list:
    return sorted(SKELETONS_DIR.glob("*.md"))


def extract(quire_engine, module, bundle, path):
    text = path.read_text()
    return quire_engine.extract_semantic(
        {
            "markdown": text,
            "module": module,
            "path": str(path),
            "sourceIdentity": (
                f"ix://agent-ix/spec-objects-enterprise/{frontmatter(text)['id']}"
            ),
            "bundle": bundle,
        }
    )


@pytest.mark.trace("TC-050", "FR-005-AC-1")
def test_every_skeleton_validates_with_no_error(quire_engine, skeletons):
    assert len(skeletons) == 10
    for path in skeletons:
        text = path.read_text()
        result = quire_engine.validate_document(
            frontmatter(text)["type"], str(PACKAGE_ROOT), text
        )
        assert result["is_valid"], (path.name, result["errors"])
        assert not [
            e for e in result["errors"] if "semantic.record-invalid" in e["message"]
        ], path.name


@pytest.mark.trace("TC-051", "FR-005-AC-2", "FR-005-CON-2")
def test_table_and_sysml_skeletons_extract_to_identical_fields(
    quire_engine, semantic_module, bundle_index
):
    for name in ALTERNATES:
        table = extract(
            quire_engine, semantic_module, bundle_index, SKELETONS_DIR / f"{name}.md"
        )
        fence = extract(
            quire_engine,
            semantic_module,
            bundle_index,
            SKELETONS_DIR / f"{name}.sysml.md",
        )
        assert table["fieldsForm"] == "table", name
        assert fence["fieldsForm"] == "fence", name
        assert table["fields"] == fence["fields"], name


@pytest.mark.trace("TC-052", "FR-005-AC-3")
def test_under_the_bundle_index_every_skeleton_extracts_clean(
    quire_engine, semantic_module, bundle_index
):
    prefix = "ix://agent-ix/spec-objects-enterprise/type/"
    for path in skeleton_paths():
        record = extract(quire_engine, semantic_module, bundle_index, path)
        diagnostics = record.get("diagnostics", [])
        assert not [d for d in diagnostics if d.get("severity") == "error"], (
            path.name,
            diagnostics,
        )
        assert not [
            d for d in diagnostics if d.get("code") == "semantic.unresolved-type"
        ], (path.name, diagnostics)
        for decl in record.get("fields") or []:
            target = decl["type"]["target"]
            if target in KERNEL_SCALARS:
                continue
            assert target.startswith(prefix), (path.name, target)


@pytest.mark.trace("TC-053", "FR-005-AC-4")
def test_availability_states_match_the_declared_set(
    quire_engine, semantic_module, bundle_index
):
    for path in skeleton_paths():
        name = frontmatter(path.read_text())["type"]
        record = extract(quire_engine, semantic_module, bundle_index, path)
        availability = record["availability"]
        assert availability["clauses"]["state"] == "available", path.name
        assert availability["fields"]["state"] == (
            "available" if name in FIELD_BEARING else "not_applicable"
        ), path.name
        assert availability["operations"]["state"] == (
            "available" if name in OPERATION_BEARING else "not_applicable"
        ), path.name


@pytest.mark.trace("TC-064", "FR-005-AC-9")
def test_kpi_declares_a_measure_and_the_objective_declares_a_horizon(
    quire_engine, semantic_module, bundle_index
):
    """The definition / measurement boundary, read off the extracted records."""
    kpi = extract(quire_engine, semantic_module, bundle_index, SKELETONS_DIR / "kpi.md")
    fields = kpi["fields"]
    assert [f for f in fields if "unit" in f["type"]]
    assert not [f for f in fields if f.get("identity")]
    assert not [f for f in fields if f["type"]["target"] == "Timestamp"]
    # A dimensionless measure is carried by the UCUM unity symbol.
    assert [f for f in fields if f["type"].get("unit") == "1"]

    objective = extract(
        quire_engine, semantic_module, bundle_index, SKELETONS_DIR / "objective.md"
    )
    fields = objective["fields"]
    assert [f for f in fields if f.get("identity")]
    assert [f for f in fields if f["type"]["target"] == "Timestamp"]


@pytest.mark.trace("TC-054", "FR-005-AC-5")
def test_every_negative_fixture_fails_with_its_expected_code(quire_engine):
    present = {path.name for path in NEGATIVE_DIR.glob("*.md")}
    assert present == set(EXPECTED_NEGATIVES), present ^ set(EXPECTED_NEGATIVES)
    for name, code in EXPECTED_NEGATIVES.items():
        path = NEGATIVE_DIR / name
        text = path.read_text()
        front = frontmatter(text)
        assert front["expect"] == code, name
        result = quire_engine.validate_document(front["type"], str(PACKAGE_ROOT), text)
        assert not result["is_valid"], name
        assert any(code in e["message"] for e in result["errors"]), (
            name,
            [e["message"] for e in result["errors"]],
        )


@pytest.mark.trace("TC-057", "FR-005-CON-2")
def test_both_properties_forms_in_one_artifact_are_refused(quire_engine):
    path = NEGATIVE_DIR / "properties-both-forms.md"
    text = path.read_text()
    result = quire_engine.validate_document(
        frontmatter(text)["type"], str(PACKAGE_ROOT), text
    )
    assert any(
        "semantic.properties-both-forms" in e["message"] for e in result["errors"]
    ), result["errors"]


@pytest.mark.trace("TC-056", "FR-005-AC-7")
def test_no_skeleton_carries_a_placeholder_token():
    for path in skeleton_paths():
        body = re.sub(r"<!--.*?-->", "", path.read_text(), flags=re.DOTALL)
        for token in PLACEHOLDER_TOKENS:
            assert token not in body, (path.name, token)


@pytest.mark.trace("TC-059", "FR-005-AC-8")
def test_skeleton_titles_are_identifiers_and_object_equals_type():
    titles: dict[str, str] = {}
    for path in skeleton_paths():
        front = frontmatter(path.read_text())
        title = front["title"]
        assert IDENTIFIER.match(title), (path.name, title)
        assert title not in KERNEL_SCALARS, (path.name, title)
        assert front["object"] == front["type"], path.name
        # Two files may share one id (a table skeleton and its alternate), and
        # when they do they declare the same title by intent.
        if front["id"] in titles:
            assert titles[front["id"]] == title, path.name
        titles[front["id"]] = title
    assert len(set(titles.values())) == len(titles)


@pytest.mark.trace("TC-058", "FR-005-CON-1")
def test_no_corpus_repository_or_vendored_fixture_is_edited():
    """Inspection over the branch diff: every changed path is inside this
    repository's own module, spec, plan, tests or build files."""
    diff = subprocess.run(
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split()
    allowed = (
        "spec/",
        "plan/",
        "tests/",
        "scripts/",
        "typespec/",
        "spec_objects_enterprise/",
        ".github/",
    )
    allowed_files = {
        "Makefile",
        "package.json",
        "package-lock.json",
        "pyproject.toml",
        "poetry.lock",
        ".gitattributes",
        "README.md",
    }
    for path in diff:
        assert path.startswith(allowed) or path in allowed_files, path
        assert "vendor" not in path, path


@pytest.mark.trace("TC-065", "FR-005-CON-3")
def test_no_skeleton_scores_or_rates_an_organizational_unit():
    """The ticket's safety gate, read over the authored prose as well as the
    typed rows."""
    for path in skeleton_paths():
        lowered = path.read_text().lower()
        for phrase in SCORING_WORDS:
            assert phrase not in lowered, (path.name, phrase)


@pytest.mark.trace("TC-055", "FR-005-AC-6")
def test_every_skeleton_heading_is_asserted_by_the_manifest():
    for path in skeleton_paths():
        front = frontmatter(path.read_text())
        ot = object_type(front["type"])
        declared = {
            loc["after_heading"]
            for loc in locators(ot).values()
            if loc.get("from") == "section_body"
        }
        required = {
            loc["after_heading"]
            for loc in locators(ot).values()
            if loc.get("from") == "section_body" and loc.get("required")
        }
        body = re.sub(r"<!--.*?-->", "", path.read_text(), flags=re.DOTALL)
        headings = {
            m.group(1).strip() for m in re.finditer(r"^## (.+)$", body, re.MULTILINE)
        }
        assert headings <= declared, (path.name, headings - declared)
        assert required <= headings, (path.name, required - headings)


@pytest.mark.trace("TC-023", "FR-003-AC-3", "FR-003-CON-2")
def test_every_added_locator_is_optional():
    """The locators this change adds assert the sections the skeletons
    introduce and must never make an existing artifact invalid."""
    added = {"properties", "invariants", "operations"}
    for name in OBJECT_TYPES:
        for field, loc in locators(object_type(name)).items():
            if field in added:
                assert loc.get("required") is False, (name, field)
