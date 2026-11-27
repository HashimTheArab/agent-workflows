#!/usr/bin/env python3
"""Copy the delivery-loop rules block into repo AGENTS.md files and check copies for drift.

usage: agents_block.py sync <AGENTS.md>... | check <AGENTS.md>... | status [<AGENTS.md>...]
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "plugins" / "engineering-workflows" / "skills" / "delivery-loop" / "SKILL.md"
START = "<!-- agents-block:start -->"
END = "<!-- agents-block:end -->"
SOURCE_PREFIX = "<!-- source: agent-workflows "


class BlockError(Exception):
    pass


def find_region(lines: list[str], where: str) -> tuple[int, int] | None:
    """Returns (start, end) indexes of the marker lines, or None when neither marker is present."""
    starts = [i for i, line in enumerate(lines) if line.rstrip("\r\n") == START]
    ends = [i for i, line in enumerate(lines) if line.rstrip("\r\n") == END]
    if not starts and not ends:
        return None
    if len(starts) != 1 or len(ends) != 1 or ends[0] < starts[0]:
        raise BlockError(f"{where}: need exactly one {START} followed by one {END}")
    return starts[0], ends[0]


def digest(body: list[str]) -> str:
    return hashlib.sha256("".join(line.rstrip("\r\n") + "\n" for line in body).encode()).hexdigest()


def source_body() -> list[str]:
    lines = SOURCE.read_text(encoding="utf-8").splitlines(keepends=True)
    region = find_region(lines, str(SOURCE))
    if region is None:
        raise BlockError(f"{SOURCE}: markers missing")
    return lines[region[0] + 1 : region[1]]


def source_sha() -> str:
    def git(*args: str) -> str:
        return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, check=True).stdout.strip()

    try:
        sha = git("rev-parse", "--short", "HEAD")
        dirty = git("status", "--porcelain", "--", str(SOURCE))
    except (OSError, subprocess.CalledProcessError):
        return "unknown"
    return sha + ("+dirty" if dirty else "")


def target_state(path: Path, want: str) -> str:
    """Returns ok, stale, edited or missing for one target file."""
    lines = path.resolve().read_text(encoding="utf-8").splitlines(keepends=True)
    region = find_region(lines, str(path))
    if region is None:
        return "missing"
    inner = lines[region[0] + 1 : region[1]]
    if not inner or not inner[0].startswith(SOURCE_PREFIX):
        return "edited"
    recorded = inner[0].rstrip("\r\n").rsplit("sha256:", 1)[-1].removesuffix(" -->").strip()
    actual = digest(inner[1:])
    if actual != recorded:
        return "edited"
    return "ok" if actual == want else "stale"


def sync(path: Path, body: list[str], sha: str) -> None:
    if target_state(path, digest(body)) == "ok":
        return  # same rules: leave the recorded sha alone so unrelated commits cause no churn
    real = path.resolve()
    text = real.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    block = [START + "\n", f"{SOURCE_PREFIX}{sha} sha256:{digest(body)} -->\n", *body, END + "\n"]
    region = find_region(lines, str(path))
    if region is None:
        prefix = text if text.endswith("\n") or not text else text + "\n"
        new = prefix + ("\n" if prefix else "") + "".join(block)
    else:
        new = "".join(lines[: region[0]] + block + lines[region[1] + 1 :])
    if new != text:
        real.write_text(new, encoding="utf-8")


def main(argv: list[str]) -> int:
    if not argv or argv[0] not in {"sync", "check", "status"} or (argv[0] != "status" and len(argv) < 2):
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 2
    command, paths = argv[0], [Path(p) for p in argv[1:]]
    try:
        body = source_body()
        want = digest(body)
        sha = source_sha() if command != "check" else ""
        if command == "status":
            print(f"source {sha} sha256:{want} ({len(body)} lines)")
        failed = False
        for path in paths:
            if command == "sync":
                sync(path, body, sha)
                print(f"synced {path}")
                continue
            state = target_state(path, want)
            print(f"{state:8} {path}")
            failed |= state != "ok"
    except (OSError, BlockError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 1 if failed and command == "check" else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
