"""The lean-author plugin must stay installable on every target.

- claude.ai upload rejects frontmatter keys outside the Agent Skills spec and
  (through Customize > Plugins) a zip without ``.claude-plugin/plugin.json``.
- Codex registers a skill folder that contains ``.claude-plugin/`` under the
  plugin namespace (``name:name``), so ``$name`` stops resolving; skill folders
  under ``plugin/skills/`` stay plain.
- Claude Code accepts more than either, so a local run never shows these
  failures; only these checks do.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
import zipfile
from pathlib import Path

import pytest
import yaml

_ROOT = Path(__file__).resolve().parents[1]
_PLUGIN = _ROOT / "plugin"


def _packager():
    spec = importlib.util.spec_from_file_location("pkg", _ROOT / "tools" / "package.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_SKILLS = _packager().skills()


def _plugin_name() -> str:
    return _packager().plugin_name()


def _write_skill(root: Path, name: str, front: str) -> Path:
    d = root / name
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(f"---\n{front}---\nbody\n", encoding="utf-8")
    return d


def test_at_least_one_skill():
    assert _SKILLS, "plugin/skills/ has no SKILL.md folders"


@pytest.mark.parametrize("skill", _SKILLS, ids=lambda p: p.name)
def test_validator_passes(skill):
    assert _packager().validate(skill) == []


def test_plugin_passes():
    assert _packager().validate_plugin() == []


@pytest.mark.parametrize("skill", _SKILLS, ids=lambda p: p.name)
def test_frontmatter_parses_as_yaml_with_spec_keys_only(skill):
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    data = yaml.safe_load(text.split("---\n")[1])
    assert set(data) <= _packager().ALLOWED_KEYS
    assert data["name"] == skill.name
    assert 1 <= len(data["description"]) <= 1024
    meta = data.get("metadata", {})
    assert all(isinstance(v, str) for v in meta.values()), (
        "metadata values must be strings"
    )


def test_validator_rejects_claude_code_only_key(tmp_path):
    bad = _write_skill(
        tmp_path,
        "demo-skill",
        "name: demo-skill\ndescription: Demo.\ndisable-model-invocation: true\n",
    )
    assert any("unexpected frontmatter keys" in e for e in _packager().validate(bad))


def test_validator_rejects_name_folder_mismatch(tmp_path):
    bad = _write_skill(
        tmp_path, "folder-name", "name: other-name\ndescription: Demo.\n"
    )
    assert any("!= folder" in e for e in _packager().validate(bad))


@pytest.mark.parametrize("subdir", ["skills", "bin", ".claude-plugin"])
def test_validator_rejects_layout_breaking_dirs(tmp_path, subdir):
    bad = _write_skill(
        tmp_path,
        "demo-skill",
        'name: demo-skill\ndescription: Demo.\nmetadata:\n  version: "1.0.0"\n',
    )
    (bad / subdir).mkdir()
    assert any(f"{subdir}/ must not be" in e for e in _packager().validate(bad))


def test_validator_requires_metadata_version(tmp_path):
    bad = _write_skill(tmp_path, "demo-skill", "name: demo-skill\ndescription: Demo.\n")
    assert any("metadata.version missing" in e for e in _packager().validate(bad))


def test_validator_reads_version_not_a_lookalike_key(tmp_path):
    """`spec-version` must not satisfy the version check."""
    bad = _write_skill(
        tmp_path,
        "demo-skill",
        'name: demo-skill\ndescription: Demo.\nmetadata:\n  spec-version: "9.9.9"\n',
    )
    assert any("metadata.version missing" in e for e in _packager().validate(bad))


def _plugin_fixture(tmp_path, monkeypatch, manifest: dict | str):
    pkg = _packager()
    plugin = tmp_path / "plugin"
    (plugin / ".claude-plugin").mkdir(parents=True)
    text = manifest if isinstance(manifest, str) else json.dumps(manifest)
    (plugin / ".claude-plugin" / "plugin.json").write_text(text, encoding="utf-8")
    _write_skill(
        plugin / "skills",
        "demo-skill",
        'name: demo-skill\ndescription: Demo.\nmetadata:\n  version: "1.0.0"\n',
    )
    monkeypatch.setattr(pkg, "PLUGIN", plugin)
    monkeypatch.setattr(pkg, "MANIFEST", plugin / ".claude-plugin" / "plugin.json")
    return pkg, plugin


_GOOD = {"name": "demo", "version": "1.0.0", "description": "d", "license": "MIT"}


def test_plugin_validator_rejects_missing_manifest(tmp_path, monkeypatch):
    pkg = _packager()
    monkeypatch.setattr(pkg, "MANIFEST", tmp_path / "none.json")
    assert any("plugin.json missing" in e for e in pkg.validate_plugin())


@pytest.mark.parametrize(
    ("manifest", "message"),
    [
        ("{", "not valid JSON"),
        ({k: v for k, v in _GOOD.items() if k != "version"}, "version missing"),
        ({k: v for k, v in _GOOD.items() if k != "description"}, "description missing"),
        ({k: v for k, v in _GOOD.items() if k != "license"}, "license missing"),
        ({**_GOOD, "name": "Demo Plugin"}, "not kebab-case"),
        ({**_GOOD, "skills": "./skills/"}, "'skills' key"),
    ],
)
def test_plugin_validator_rejects(tmp_path, monkeypatch, manifest, message):
    pkg, _ = _plugin_fixture(tmp_path, monkeypatch, manifest)
    assert any(message in e for e in pkg.validate_plugin())


@pytest.mark.parametrize(
    ("path", "message"), [("bin", "bin/"), ("SKILL.md", "SKILL.md at plugin root")]
)
def test_plugin_validator_rejects_root_layout(tmp_path, monkeypatch, path, message):
    pkg, plugin = _plugin_fixture(tmp_path, monkeypatch, _GOOD)
    if path == "bin":
        (plugin / "bin").mkdir()
    else:
        (plugin / path).write_text("x", encoding="utf-8")
    assert any(message in e for e in pkg.validate_plugin())


def test_committed_zip_matches_source(tmp_path, monkeypatch):
    """releases/<plugin>.zip is what users upload; it must not lag the source."""
    committed = _ROOT / "releases" / f"{_plugin_name()}.zip"
    assert committed.is_file(), "run: python3 tools/package.py"
    pkg = _packager()
    monkeypatch.setattr(pkg, "DIST", tmp_path)
    rebuilt = pkg.package()
    assert rebuilt.read_bytes() == committed.read_bytes(), (
        "stale zip; run: python3 tools/package.py"
    )


def test_zip_build_is_os_independent(tmp_path, monkeypatch):
    """ZipInfo sets create_system from sys.platform; a Windows build must still
    match the committed zip, or the freshness test fails there."""
    pkg = _packager()
    monkeypatch.setattr(pkg, "DIST", tmp_path)
    monkeypatch.setattr(sys, "platform", "win32")
    rebuilt = pkg.package()
    committed = _ROOT / "releases" / f"{_plugin_name()}.zip"
    assert rebuilt.read_bytes() == committed.read_bytes()


def test_releases_hold_only_the_plugin_zip():
    names = sorted(p.name for p in (_ROOT / "releases").iterdir())
    assert names == [f"{_plugin_name()}.zip"]


def test_zip_is_a_plugin_upload():
    """claude.ai's upload requires .claude-plugin/plugin.json inside the zip,
    under the single top-level folder. Each skill sits in skills/<skill>/."""
    name = _plugin_name()
    with zipfile.ZipFile(_ROOT / "releases" / f"{name}.zip") as zf:
        names = zf.namelist()
        manifest = json.loads(zf.read(f"{name}/.claude-plugin/plugin.json"))
    assert {n.split("/")[0] for n in names} == {name}, "one top-level folder"
    assert manifest["name"] == name
    for skill in _SKILLS:
        assert f"{name}/skills/{skill.name}/SKILL.md" in names
    assert f"{name}/SKILL.md" not in names
    assert not any(n.startswith(f"{name}/bin/") for n in names)


def test_release_record_matches_content():
    """Claude Code updates an installed plugin only when its version changes,
    so shipped files that changed under the same version never reach users.
    plugin-release.json records the digest per version."""
    assert _packager().check_release() == []


def _release_fixture(tmp_path, monkeypatch, version, recorded):
    pkg, _ = _plugin_fixture(tmp_path, monkeypatch, {**_GOOD, "version": version})
    release = tmp_path / "plugin-release.json"
    release.write_text(json.dumps(recorded), encoding="utf-8")
    monkeypatch.setattr(pkg, "RELEASE", release)
    return pkg, release


def test_changed_files_need_a_new_plugin_version(tmp_path, monkeypatch):
    recorded = {"version": "1.0.0", "digest": "0" * 64}
    pkg, release = _release_fixture(tmp_path, monkeypatch, "1.0.0", recorded)
    assert any("bump version" in e for e in pkg.check_release())
    assert any("bump version" in e for e in pkg.record_release())
    assert json.loads(release.read_text(encoding="utf-8")) == recorded


def test_new_plugin_version_is_recorded(tmp_path, monkeypatch):
    recorded = {"version": "1.0.0", "digest": "0" * 64}
    pkg, release = _release_fixture(tmp_path, monkeypatch, "1.0.1", recorded)
    assert any("run tools/package.py" in e for e in pkg.check_release())
    assert pkg.record_release() == []
    assert json.loads(release.read_text(encoding="utf-8")) == {
        "version": "1.0.1",
        "digest": pkg.content_digest(),
    }
    assert pkg.check_release() == []


def test_digest_ignores_the_manifest_only(tmp_path, monkeypatch):
    """A version bump alone keeps the digest; any other shipped file moves it."""
    pkg, plugin = _plugin_fixture(tmp_path, monkeypatch, _GOOD)
    before = pkg.content_digest()
    manifest = plugin / ".claude-plugin" / "plugin.json"
    manifest.write_text(json.dumps({**_GOOD, "version": "2.0.0"}), encoding="utf-8")
    assert pkg.content_digest() == before
    (plugin / "README.md").write_text("changed", encoding="utf-8")
    assert pkg.content_digest() != before


_HANGUL = re.compile("[ᄀ-ᇿ㄰-㆏ꥠ-꥿가-퟿]")


def test_shipped_plugin_has_no_hangul():
    """The installed plugin is English only; docs/ outside plugin/ may differ."""
    hits = [
        f"{rel}:{n}"
        for rel, data in _packager().plugin_files().items()
        for n, line in enumerate(data.decode("utf-8").splitlines(), 1)
        if _HANGUL.search(line)
    ]
    assert not hits, f"Hangul in shipped files: {hits}"


def _marketplace() -> dict:
    path = _ROOT / ".claude-plugin" / "marketplace.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_marketplace_lists_the_one_plugin():
    """A stale marketplace entry installs nothing while `claude plugin validate`
    still passes. The marketplace, its one entry and plugin.json share a name."""
    market = _marketplace()
    entries = market["plugins"]
    assert market["name"] == _plugin_name()
    assert [e["name"] for e in entries] == [_plugin_name()]
    assert entries[0]["source"] == "./plugin"
    assert "version" not in entries[0], "plugin.json owns the version"


def test_install_docs_match_the_marketplace():
    """The README copies the install commands by hand; tie them to
    marketplace.json so a renamed plugin cannot leave them stale."""
    market = _marketplace()
    readme = (_ROOT / "README.md").read_text(encoding="utf-8")
    for e in market["plugins"]:
        assert f"/plugin install {e['name']}@{market['name']}" in readme
    for skill in _SKILLS:
        assert f"/{_plugin_name()}:{skill.name}" in readme
