#!/usr/bin/env python3
"""Validate the dual-platform engineering-workflows plugin."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "engineering-workflows"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FORBIDDEN_RUNTIME_RE = re.compile(
    r"(?:^|[/`])\.(?:omx|superpowers)(?:[/`]|$)"
    r"|\bomx\s+(?:state|setup|team|sparkshell)\b"
    r"|\$(?:ralplan|ralph|team|deep-interview)\b"
    r"|\bdependency-expert\b"
    r"|\b(?:style-reviewer|performance-reviewer|quality-reviewer)\b"
    r"|\b(?:planner|analyst)\s+for\s+(?:plan|requirements)"
    r"|\{\{[A-Z_]+\}\}"
    r"|Superpowers-owned",
    re.IGNORECASE | re.MULTILINE,
)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON at {path.relative_to(ROOT)}: {exc}")


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text()
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
    codex = load_json(PLUGIN / ".codex-plugin" / "plugin.json")
    claude = load_json(PLUGIN / ".claude-plugin" / "plugin.json")
    codex_market = load_json(ROOT / ".agents" / "plugins" / "marketplace.json")
    claude_market = load_json(ROOT / ".claude-plugin" / "marketplace.json")

    expected = "engineering-workflows"
    for label, manifest in (("Codex", codex), ("Claude", claude)):
        if manifest.get("name") != expected:
            fail(f"{label} plugin name must be {expected!r}")

    for label, market in (("Codex", codex_market), ("Claude", claude_market)):
        if market.get("name") != "hashim-workflows":
            fail(f"{label} marketplace name must be 'hashim-workflows'")
        entries = market.get("plugins", [])
        if not any(entry.get("name") == expected for entry in entries):
            fail(f"{label} marketplace does not expose {expected}")


def validate_skills() -> None:
    skills = PLUGIN / "skills"
    count = 0
    for directory in sorted(path for path in skills.iterdir() if path.is_dir()):
        skill = directory / "SKILL.md"
        if not skill.is_file():
            fail(f"skill directory lacks SKILL.md: {directory.relative_to(ROOT)}")
        metadata = parse_frontmatter(skill)
        name = metadata.get("name", "")
        description = metadata.get("description", "")
        if name != directory.name:
            fail(f"skill name {name!r} does not match directory {directory.name!r}")
        if not NAME_RE.fullmatch(name):
            fail(f"invalid skill name: {name!r}")
        if not description:
            fail(f"missing description: {skill.relative_to(ROOT)}")
        count += 1

    if count < 10:
        fail(f"expected a substantive bundle, found only {count} skills")
    print(f"Validated {count} skills")


def validate_portability() -> None:
    for base in (PLUGIN / "skills", PLUGIN / "agents"):
        for path in base.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".sh"}:
                if FORBIDDEN_RUNTIME_RE.search(path.read_text(errors="replace")):
                    fail(f"runtime-specific state reference remains in {path.relative_to(ROOT)}")

    for forbidden in ("hooks", ".mcp.json", "AGENTS.md", "CLAUDE.md"):
        if (PLUGIN / forbidden).exists():
            fail(f"forbidden plugin runtime surface exists: {forbidden}")
    print("No runtime-specific state or instruction injection detected")


def main() -> None:
    validate_manifests()
    validate_skills()
    validate_portability()
    print("Validation passed")


if __name__ == "__main__":
    main()
