#!/usr/bin/env python3
"""
====================================================================
Package: labware
====================================================================
Author:			Ragdata
Date:			31/05/2026
License:		MIT License
Repository:		https://github.com/Ragdata/.labware
Copyright:		Copyright © 2026 Redeyed Technologies
====================================================================

Test Module for
"""
import os, sys, unittest, tempfile

from pathlib import Path
from unittest.mock import patch

# ---------------------------------------------------------------------------
# Path bootstrap — mirrors what the modules do so imports resolve without
# a full editable installation being in place during CI.
# ---------------------------------------------------------------------------
BASEDIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASEDIR))

# ---------------------------------------------------------------------------
# Minimal stubs so modules that depend on each other can be imported
# independently in a test environment that may lack optional deps (jinja2,
# sqlitedict, rich …).  Real integration tests import the live modules.
# ---------------------------------------------------------------------------


# ===========================================================================
# 4. FILESYS TESTS
# ===========================================================================
class TestFilesysFunctions(unittest.TestCase):
    """Tests for filesys.py file manipulation helpers."""

    def setUp(self):
        from labware import filesys as fs_mod
        self.fs = fs_mod
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ── backup ──────────────────────────────────────────────────────────────
    def test_backup_creates_file(self):
        src = self.tmp / "orig.txt"
        src.write_text("data")
        bkpdir = self.tmp / "bkp"
        result = self.fs.backup(src, backupdir=bkpdir)
        self.assertTrue(result)
        self.assertTrue(bkpdir.exists())
        backups = list(bkpdir.iterdir())
        self.assertEqual(len(backups), 1)

    def test_backup_nonexistent_raises(self):
        with self.assertRaises(FileNotFoundError):
            self.fs.backup(self.tmp / "ghost.txt")

    # ── chmod ────────────────────────────────────────────────────────────────
    def test_chmod_file(self):
        f = self.tmp / "f.txt"
        f.write_text("x")
        self.fs.chmod(f, 0o600)
        self.assertEqual(f.stat().st_mode & 0o777, 0o600)

    def test_chmod_directory_recursive(self):
        d = self.tmp / "subdir"
        d.mkdir()
        f = d / "inner.txt"
        f.write_text("y")
        self.fs.chmod(d, 0o644)
        self.assertEqual(f.stat().st_mode & 0o777, 0o644)

    def test_chmod_nonexistent_does_nothing(self):
        # Should not raise
        self.fs.chmod(self.tmp / "ghost", 0o644)

    # ── findFileString ────────────────────────────────────────────────────────
    def test_findFileString_found(self):
        f = self.tmp / "search.txt"
        f.write_text("hello world\nfoo bar\n")
        self.assertTrue(self.fs.findFileString(f, "foo bar"))

    def test_findFileString_not_found(self):
        f = self.tmp / "search.txt"
        f.write_text("hello world\n")
        self.assertFalse(self.fs.findFileString(f, "missing"))

    def test_findFileString_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            self.fs.findFileString(self.tmp / "ghost.txt", "x")

    # ── getList ───────────────────────────────────────────────────────────────
    def test_getList_returns_lines(self):
        f = self.tmp / "list.txt"
        f.write_text("alpha\nbeta\ngamma\n")
        result = self.fs.getList(f)
        self.assertEqual(result, ["alpha", "beta", "gamma"])

    def test_getList_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            self.fs.getList(self.tmp / "ghost.txt")

    # ── mergeFiles ────────────────────────────────────────────────────────────
    def test_mergeFiles_deduplicates(self):
        a = self.tmp / "a.txt"
        b = self.tmp / "b.txt"
        out = self.tmp / "merged.txt"
        a.write_text("line1\nline2\n")
        b.write_text("line2\nline3\n")
        result = self.fs.mergeFiles([str(a), str(b)], str(out))
        self.assertTrue(result)
        content = out.read_text()
        self.assertEqual(content.count("line2"), 1)
        self.assertIn("line1", content)
        self.assertIn("line3", content)

    # ── writeFile ─────────────────────────────────────────────────────────────
    def test_writeFile_creates_and_writes(self):
        dst = self.tmp / "out.txt"
        import pwd as _pwd
        user = _pwd.getpwuid(os.geteuid()).pw_name
        with patch("labware.filesys.chown"), \
             patch("labware.filesys.chmod"), \
             patch("labware.filesys.printSuccess"):
            result = self.fs.writeFile(dst, "content", user=user, group=user)
        self.assertTrue(result)
        self.assertEqual(dst.read_text(), "content")

    def test_writeFile_overwrites_existing(self):
        dst = self.tmp / "existing.txt"
        dst.write_text("old content")
        import pwd as _pwd
        user = _pwd.getpwuid(os.geteuid()).pw_name
        with patch("labware.filesys.chown"), \
             patch("labware.filesys.chmod"), \
             patch("labware.filesys.printSuccess"):
            self.fs.writeFile(dst, "new content", user=user, group=user)
        self.assertEqual(dst.read_text(), "new content")



# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    unittest.main(verbosity=2)
