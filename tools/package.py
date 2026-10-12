#!/usr/bin/env python3
"""Validate the lean-author plugin under plugin/ and package it for upload.

The repository is its own marketplace (.claude-plugin/marketplace.json points at
./plugin). plugin/ is the shipped unit; everything else in the repository stays
out of installs and the zip:

    plugin/
      .claude-plugin/plugin.json          the manifest
      README.md                           user-facing description
      skills/<skill>/SKILL.md, references/, scripts/   plain Agent Skills
    releases/<plugin>.zip                 plugin/ under one top-level <plugin>/

Skill folders stay plain (no .claude-plugin/ inside): Codex registers a folder
with a manifest as <name>:<name>, and Claude Code loads one in .claude/skills/
as a plugin. claude.ai upload rejects frontmatter keys outside the Agent Skills
spec. The zip is byte-reproducible on every OS (fixed timestamps, modes,
create_system, LF line endings for text files).

Claude Code updates an installed plugin only when its version changes. So
plugin-release.json (not shipped) records a digest of the shipped files for the
current version, and a build refuses changed files under the same version.
Before a version is first released, delete the record and rebuild.

Usage: python3 tools/package.py [--check]   (stdlib only)
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugin"
MANIFEST = PLUGIN / ".claude-plugin" / "plugin.json"
DIST = ROOT / "releases"
RELEASE = ROOT / "plugin-release.json"
ALLOWED_KEYS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_BODY_LINES = 200
# A skill folder stays a plain skill: a manifest dir in it changes the Codex
# skill name and how Claude Code loads it from .claude/skills/; skills/ and bin/
# are plugin-level directories and stay out of a skill folder.
FORBIDDEN_DIRS = ("skills", "bin", ".claude-plugin", ".codex-plugin")
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".txt", ".py", ".sh"}


def skills() -> list[Path]:
    root = PLUGIN / "skills"
    if not root.is_dir():
        return []
    return sorted(p for p in root.iterdir() if (p / "SKILL.md").is_file())


def frontmatter(text: str) -> tuple[dict, dict, str]:
    """Return (top-level keys, metadata map, body). Minimal YAML subset:
    `key: value` lines, plus one indented level of `key: value` under metadata."""
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with '---' on line 1")
    end = text.index("\n---\n", 4)
    block, body = text[4:end], text[end + 5 :]
    data: dict = {}
    meta: dict = {}
    current = None
    for line in block.splitlines():
        if not line.strip():
            continue
        if line.startswith((" ", "\t")):
            if current is None:
                raise ValueError(f"indented line before any key: {line!r}")
            if current == "metadata":
                k, _, v = line.strip().partition(":")
                meta[k.strip()] = v.strip().strip('"')
            else:
                data[current] = (data[current] + "\n" + line.strip()).strip()
            continue
        key, _, value = line.partition(":")
        current = key.strip()
        data[current] = value.strip().strip('"')
    return data, meta, body


def validate(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"{skill_dir.name}: SKILL.md missing"]
    try:
        data, meta, body = frontmatter(skill_md.read_text(encoding="utf-8"))
    except ValueError as e:
        return [f"{skill_dir.name}: {e}"]
    extra = set(data) - ALLOWED_KEYS
    if extra:
        errors.append(
            f"unexpected frontmatter keys (upload would fail): {sorted(extra)}"
        )
    name = data.get("name", "")
    if not (1 <= len(name) <= 64 and NAME_RE.match(name)):
        errors.append(f"invalid name {name!r}")
    if name != skill_dir.name:
        errors.append(f"name {name!r} != folder {skill_dir.name!r}")
    desc = data.get("description", "")
    if not 1 <= len(desc) <= 1024:
        errors.append(f"description length {len(desc)} not in 1..1024")
    if "<" in desc or ">" in desc:
        errors.append("description contains angle brackets")
    if len(data.get("compatibility", "")) > 500:
        errors.append("compatibility > 500 chars")
    for d in FORBIDDEN_DIRS:
        if (skill_dir / d).exists():
            errors.append(
                f"{d}/ must not be in the skill folder "
                "(changes the Codex skill name or how the plugin loads)"
            )
    n = len(body.splitlines())
    if n > MAX_BODY_LINES:
        errors.append(f"body {n} lines > {MAX_BODY_LINES}")
    for link in re.findall(r"\]\(([^)#]+)\)", body):
        if not link.startswith("http") and not (skill_dir / link).exists():
            errors.append(f"broken relative link {link}")
    if not meta.get("version"):
        errors.append("metadata.version missing")
    return [f"{skill_dir.name}: {e}" for e in errors]


def validate_plugin() -> list[str]:
    """The manifest and plugin-level layout that claude.ai and Claude Code need."""
    if not MANIFEST.is_file():
        return ["plugin/.claude-plugin/plugin.json missing"]
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"plugin.json is not valid JSON: {e}"]
    errors = []
    name = data.get("name", "")
    if not (1 <= len(name) <= 64 and NAME_RE.match(name)):
        errors.append(f"name {name!r} is not kebab-case")
    for key in ("version", "description", "license"):
        if not data.get(key):
            errors.append(f"{key} missing")
    if "skills" in data:
        errors.append("'skills' key: skills/ is already scanned by default")
    if (PLUGIN / "bin").exists():
        errors.append("bin/ in plugin/: claude.ai does not install such plugins")
    if (PLUGIN / "SKILL.md").exists():
        errors.append("SKILL.md at plugin root loads the plugin as one skill")
    if not skills():
        errors.append("no skills under plugin/skills/")
    return [f"plugin.json: {e}" for e in errors]


def plugin_name() -> str:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))["name"]


def _normalized(path: Path) -> bytes:
    data = path.read_bytes()
    if path.suffix in TEXT_SUFFIXES:
        data = data.replace(b"\r\n", b"\n")
    return data


def plugin_files() -> dict:
    """Every shipped file, keyed by its path relative to plugin/."""
    return {
        f.relative_to(PLUGIN).as_posix(): _normalized(f)
        for f in PLUGIN.rglob("*")
        if f.is_file() and "__pycache__" not in f.parts and f.name != ".DS_Store"
    }


def content_digest() -> str:
    """sha256 over the shipped files minus the manifest, so a version bump
    alone leaves it unchanged."""
    h = hashlib.sha256()
    for rel, data in sorted(plugin_files().items()):
        if rel != ".claude-plugin/plugin.json":
            h.update(rel.encode() + b"\0" + data + b"\0")
    return h.hexdigest()


def _release_state() -> tuple[str, str, dict]:
    version = json.loads(MANIFEST.read_text(encoding="utf-8"))["version"]
    try:
        recorded = json.loads(RELEASE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        recorded = {}
    return version, content_digest(), recorded


def _bump_error(version: str) -> str:
    return (
        f"plugin files changed since {version}: bump version in "
        "plugin/.claude-plugin/plugin.json, then run tools/package.py"
    )


def check_release() -> list[str]:
    version, digest, recorded = _release_state()
    if recorded.get("version") != version:
        return [
            (
                f"plugin-release.json records {recorded.get('version')!r}, "
                f"plugin.json says {version!r}: run tools/package.py"
            )
        ]
    if recorded.get("digest") != digest:
        return [_bump_error(version)]
    return []


def record_release() -> list[str]:
    version, digest, recorded = _release_state()
    if recorded.get("version") == version and recorded.get("digest") != digest:
        return [_bump_error(version)]
    RELEASE.write_text(
        json.dumps({"version": version, "digest": digest}, indent=2) + "\n",
        encoding="utf-8",
    )
    return []


def package() -> Path:
    name = plugin_name()
    DIST.mkdir(parents=True, exist_ok=True)
    out = DIST / f"{name}.zip"
    files = {f"{name}/{rel}": data for rel, data in plugin_files().items()}
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for arcname in sorted(files):
            info = zipfile.ZipInfo(arcname, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3  # unix; ZipInfo defaults to 0 on Windows
            info.external_attr = 0o644 << 16
            zf.writestr(info, files[arcname])
    return out


def main() -> int:
    check_only = "--check" in sys.argv
    errors = validate_plugin() + [e for s in skills() for e in validate(s)]
    if not errors:
        errors = check_release() if check_only else record_release()
    for e in errors:
        print("ERROR", e)
    if errors:
        return 1
    for s in skills():
        print("ok", s.name)
    if not check_only:
        print("->", package().relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
