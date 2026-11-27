"""Round-trip tests for agents_block.py: text outside the markers survives and drift is caught."""

from __future__ import annotations

import os
import shutil
import tempfile
import unittest
from pathlib import Path

import agents_block as ab


class AgentsBlockTest(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.dir)
        self.body = ab.source_body()
        self.want = ab.digest(self.body)

    def write(self, name: str, text: str) -> Path:
        path = self.dir / name
        path.write_text(text, encoding="utf-8")
        return path

    def test_sync_appends_then_replaces_in_place(self) -> None:
        path = self.write("AGENTS.md", "# Repo\n\nlocal rule\n")
        self.assertEqual(ab.target_state(path, self.want), "missing")
        ab.sync(path, self.body, "abc1234")
        first = path.read_text()
        self.assertTrue(first.startswith("# Repo\n\nlocal rule\n\n" + ab.START))
        path.write_text(first + "\ntrailing rule\n")
        ab.sync(path, self.body, "abc1234")
        self.assertEqual(path.read_text(), first + "\ntrailing rule\n")
        self.assertEqual(ab.target_state(path, self.want), "ok")

    def test_unchanged_rules_from_a_newer_commit_leave_the_file_alone(self) -> None:
        path = self.write("AGENTS.md", "")
        ab.sync(path, self.body, "abc1234")
        first = path.read_text()
        ab.sync(path, self.body, "def5678")
        self.assertEqual(path.read_text(), first)

    def test_hand_edit_and_stale_source_are_caught(self) -> None:
        path = self.write("AGENTS.md", "")
        ab.sync(path, self.body, "abc1234")
        self.assertEqual(ab.target_state(path, "0" * 64), "stale")
        path.write_text(path.read_text().replace(self.body[0], "- edited\n"))
        self.assertEqual(ab.target_state(path, self.want), "edited")

    def test_symlink_target_is_written(self) -> None:
        real = self.write("real.md", "x\n")
        link = self.dir / "AGENTS.md"
        os.symlink(real, link)
        ab.sync(link, self.body, "abc1234")
        self.assertTrue(link.is_symlink())
        self.assertEqual(ab.target_state(real, self.want), "ok")

    def test_unpaired_markers_fail(self) -> None:
        path = self.write("AGENTS.md", f"{ab.START}\n{ab.START}\n{ab.END}\n")
        with self.assertRaises(ab.BlockError):
            ab.sync(path, self.body, "abc1234")


if __name__ == "__main__":
    unittest.main()
