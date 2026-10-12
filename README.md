# lean-author

A plugin for authoring Claude agents, skills and commands. Give it an authoring request and it produces a plugin folder whose instructions keep the core directives and drop the sprawl: a Markdown heading skeleton with XML tags for examples, constraints and boundaries, a short `SKILL.md` body, and reference files read only when needed.

**Status: pre-release (0.1.x).** The skill is a placeholder until 1.0.0.

It does not depend on any framework. The skill follows the subset of the [Agent Skills spec](https://agentskills.io/specification) that claude.ai, Claude Code and Codex all accept.

## Install

| Where | How |
|---|---|
| Claude Code | `/plugin marketplace add ajitta/lean-author`, then `/plugin install lean-author@lean-author` (2.1.275+: `/plugin install lean-author --marketplace ajitta/lean-author` in one step) |
| Claude Code, pinned version | `/plugin marketplace add ajitta/lean-author#lean-author--v<version>` |
| claude.ai (Customize > Plugins > Add) | Add marketplace with `ajitta/lean-author`, or Upload plugin with [`releases/lean-author.zip`](./releases/lean-author.zip) |
| Codex | Copy `plugin/skills/lean-author` to `~/.agents/skills/` |

## Invoke

- Claude Code: `/lean-author:lean-author <request>`, or ask in words
- Codex: `$lean-author <request>`

## Layout

```
.claude-plugin/marketplace.json   this repository is the marketplace; its one entry points at ./plugin
plugin/                           the shipped plugin: only this folder is installed or zipped
releases/lean-author.zip          plugin/ as a zip for claude.ai upload
tools/package.py                  validate + zip + version digest (stdlib only)
plugin-release.json               digest of the shipped files for the current version
tests/                            pytest checks for every target
docs/                             design history (not shipped)
```

## Develop

```bash
uv run python tools/package.py          # validate, record the digest, rebuild the zip
uv run python tools/package.py --check  # validate only
uv run pytest
uv run ruff check && uv run ruff format --check
claude plugin validate . --strict
```

When anything under `plugin/` changes, bump `version` in `plugin/.claude-plugin/plugin.json` (and `metadata.version` in the changed `SKILL.md`), then run `tools/package.py`. Claude Code updates an installed plugin only when the version changes, so the build and tests fail on changed files under an unchanged version. `main` is the release channel; tag each release with `claude plugin tag --push`.

## License

MIT
