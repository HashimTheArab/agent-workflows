#!/usr/bin/env python3
"""Validate the engineering-workflows plugin for Claude Code and Codex."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import agents_block


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "engineering-workflows"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_DESCRIPTION = 250  # Claude Code cuts longer descriptions in its skill listing.
MAX_SKILL_LINES = 120
MAX_BLOCK_LINES = 12


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON at {path.relative_to(ROOT)}: {exc}")


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---(?:\n|$)", text, re.DOTALL)
    if not match:
        fail(f"missing YAML frontmatter: {path.relative_to(ROOT)}")

    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.startswith((" ", "\t")):
            continue
        key, separator, value = line.partition(":")
        if separator:
            result[key.strip()] = value.strip().strip('"\'')
    return result


def validate_manifests() -> None:
    expected = "engineering-workflows"
    manifests = (
        ("Codex", load_json(PLUGIN / ".codex-plugin" / "plugin.json")),
        ("Claude", load_json(PLUGIN / ".claude-plugin" / "plugin.json")),
    )
    for label, manifest in manifests:
        if manifest.get("name") != expected:
            fail(f"{label} plugin name must be {expected!r}")
        if not manifest.get("version"):
            fail(f"{label} plugin manifest lacks a version")

    versions = {manifest["version"] for _, manifest in manifests}
    if len(versions) != 1:
        fail(f"plugin manifest versions must match, found {sorted(versions)!r}")

    markets = (
        ("Codex", ROOT / ".agents" / "plugins" / "marketplace.json", lambda e: e.get("source", {}).get("path")),
        ("Claude", ROOT / ".claude-plugin" / "marketplace.json", lambda e: e.get("source")),
    )
    for label, path, source_of in markets:
        market = load_json(path)
        if market.get("name") != "hashim-workflows":
            fail(f"{label} marketplace name must be 'hashim-workflows'")
        entry = next((e for e in market.get("plugins", []) if e.get("name") == expected), None)
        if entry is None:
            fail(f"{label} marketplace does not expose {expected}")
        source = source_of(entry)
        if not isinstance(source, str) or (ROOT / source).resolve() != PLUGIN.resolve():
            fail(f"{label} marketplace source must point at {PLUGIN.relative_to(ROOT)}")


def validate_skills() -> None:
    count = 0
    for directory in sorted(path for path in (PLUGIN / "skills").iterdir() if path.is_dir()):
        skill = directory / "SKILL.md"
        if not skill.is_file():
            fail(f"skill directory lacks SKILL.md: {directory.relative_to(ROOT)}")
        rel = skill.relative_to(ROOT)
        metadata = parse_frontmatter(skill)
        name = metadata.get("name", "")
        description = metadata.get("description", "")
        if name != directory.name:
            fail(f"skill name {name!r} does not match directory {directory.name!r}")
        if not NAME_RE.fullmatch(name):
            fail(f"invalid skill name: {name!r}")
        if not description:
            fail(f"missing description: {rel}")
        if len(description) > MAX_DESCRIPTION:
            fail(f"description is {len(description)} chars, max {MAX_DESCRIPTION}: {rel}")
        lines = len(skill.read_text(encoding="utf-8").splitlines())
        if lines > MAX_SKILL_LINES:
            fail(f"{rel} has {lines} lines, max {MAX_SKILL_LINES}")
        count += 1
    print(f"Validated {count} skills")


def validate_agents_block() -> None:
    try:
        body = agents_block.source_body()
    except agents_block.BlockError as exc:
        fail(str(exc))
    if not body:
        fail("agents block is empty")
    if len(body) > MAX_BLOCK_LINES:
        fail(f"agents block has {len(body)} lines, max {MAX_BLOCK_LINES}")
    print(f"Agents block: {len(body)} lines")


def validate_no_injection() -> None:
    for forbidden in ("hooks", ".mcp.json", "AGENTS.md", "CLAUDE.md"):
        if (PLUGIN / forbidden).exists():
            fail(f"forbidden plugin runtime surface exists: {forbidden}")


def main() -> None:
    validate_manifests()
    validate_skills()
    validate_agents_block()
    validate_no_injection()
    print("Validation passed")


if __name__ == "__main__":
    main()
