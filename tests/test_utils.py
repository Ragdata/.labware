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
import sys, unittest

from pathlib import Path
from unittest.mock import MagicMock, patch

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
# 5. UTILS TESTS
# ===========================================================================
class TestUtilsFunctions(unittest.TestCase):
    """Tests for utils.py helpers."""

    def setUp(self):
        from labware import utils as ut_mod
        self.ut = ut_mod

    # ── userExists ────────────────────────────────────────────────────────────
    def test_userExists_root_exists(self):
        self.assertTrue(self.ut.userExists("root"))

    def test_userExists_bogus_user(self):
        self.assertFalse(self.ut.userExists("__no_such_user_xyzzy__"))

    # ── run ───────────────────────────────────────────────────────────────────
    def test_run_success(self):
        result = self.ut.run("echo hello", capture=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("hello", result.stdout)

    def test_run_capture_false_returns_result(self):
        result = self.ut.run("true")
        self.assertEqual(result.returncode, 0)

    def test_run_failure_with_check_exits(self):
        with patch("sys.exit") as mock_exit, \
             patch("labware.utils.logger"):
            try:
                self.ut.run("false", check=True)
            except SystemExit:
                pass
            mock_exit.assert_called_with(1)

    def test_run_failure_check_false_raises(self):
        # check=False means CalledProcessError is not raised by subprocess,
        # returncode is non-zero but no exception
        result = self.ut.run("false", check=False)
        self.assertNotEqual(result.returncode, 0)

    # ── checkPython ───────────────────────────────────────────────────────────
    def test_checkPython_passes_on_312_plus(self):
        with patch("sys.version_info", (3, 12, 0)), \
             patch("labware.utils.printSuccess"):
            # Should not raise / exit
            self.ut.checkPython()

    def test_checkPython_fails_on_old_version(self):
        with patch("sys.version_info", (3, 10, 0)), \
             patch("labware.utils.logger") as mock_log, \
             patch("builtins.exit"):
            self.ut.checkPython()
            mock_log.error.assert_called_once()

    # ── checkRoot ─────────────────────────────────────────────────────────────
    def test_checkRoot_passes_when_root(self):
        with patch("os.geteuid", return_value=0), \
             patch("labware.utils.printSuccess"):
            self.ut.checkRoot()

    def test_checkRoot_fails_when_not_root(self):
        with patch("os.geteuid", return_value=1000), \
             patch("labware.utils.logger") as mock_log, \
             patch("builtins.exit"):
            self.ut.checkRoot()
            mock_log.error.assert_called_once()

    # ── runScript ─────────────────────────────────────────────────────────────
    def test_runScript_returns_dict_keys(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0, stdout="ok\n", stderr=""
            )
            result = self.ut.runScript("dummy.py")
        self.assertIn("success", result)
        self.assertIn("code", result)
        self.assertIn("stdout", result)
        self.assertIn("stderr", result)

    def test_runScript_success_flag_true_on_zero_exit(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0, stdout="", stderr=""
            )
            result = self.ut.runScript("dummy.py")
        self.assertTrue(result["success"])

    def test_runScript_success_flag_false_on_nonzero_exit(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=1, stdout="", stderr="err"
            )
            result = self.ut.runScript("dummy.py")
        self.assertFalse(result["success"])



# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    unittest.main(verbosity=2)
