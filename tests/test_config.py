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

# ── config ──────────────────────────────────────────────────────────────────
from labware.config import Config, get_config, DEFAULT_CONFIG


# ===========================================================================
# 1. CONFIG TESTS
# ===========================================================================
class TestDefaultConfig(unittest.TestCase):
    """Verify the structure and contents of DEFAULT_CONFIG."""

    def test_required_sections_present(self):
        for section in ("symbols", "styles", "logging", "log_formats"):
            with self.subTest(section=section):
                self.assertIn(section, DEFAULT_CONFIG)

    def test_symbols_keys(self):
        expected = {"info", "success", "warning", "error", "tip",
                    "important", "debug", "head", "dot"}
        self.assertEqual(set(DEFAULT_CONFIG["symbols"].keys()), expected)

    def test_styles_keys_match_symbols(self):
        self.assertEqual(
            set(DEFAULT_CONFIG["styles"].keys()),
            set(DEFAULT_CONFIG["symbols"].keys()),
        )

    def test_logging_required_keys(self):
        for key in ("level", "size", "count", "format", "logdir"):
            with self.subTest(key=key):
                self.assertIn(key, DEFAULT_CONFIG["logging"])

    def test_log_formats_keys(self):
        for key in ("std", "short", "long", "console", "date"):
            with self.subTest(key=key):
                self.assertIn(key, DEFAULT_CONFIG["log_formats"])


class TestConfigInit(unittest.TestCase):
    """Config.__init__ / _set_defaults behaviour."""

    def test_default_sections_populated(self):
        cfg = Config()
        for section in DEFAULT_CONFIG:
            self.assertTrue(cfg.has_section(section), f"Missing section: {section}")

    def test_default_values_readable(self):
        cfg = Config()
        self.assertEqual(cfg.get("symbols", "info"), DEFAULT_CONFIG["symbols"]["info"])

    def test_custom_defaults_override(self):
        custom = {"mysec": {"mykey": "myval"}}
        cfg = Config(defaults=custom)
        self.assertTrue(cfg.has_section("mysec"))
        self.assertEqual(cfg.get("mysec", "mykey"), "myval")

    def test_missing_config_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            Config(config_file="/nonexistent/path/.labware.cfg")

    def test_existing_config_file_loaded(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".cfg", delete=False) as f:
            f.write("[symbols]\ninfo = X\n")
            fname = f.name
        try:
            cfg = Config(config_file=fname)
            self.assertEqual(cfg.get("symbols", "info"), "X")
        finally:
            os.unlink(fname)


class TestConfigGet(unittest.TestCase):
    """Config.get / getint / getbool fallback logic."""

    def setUp(self):
        self.cfg = Config()

    def test_get_existing_value(self):
        val = self.cfg.get("logging", "level")
        self.assertEqual(val, str(DEFAULT_CONFIG["logging"]["level"]))

    def test_get_with_fallback_for_missing(self):
        val = self.cfg.get("nosection", "nokey", fallback="default")
        self.assertEqual(val, "default")

    def test_get_missing_no_fallback_returns_empty(self):
        val = self.cfg.get("nosection", "nokey")
        self.assertEqual(val, "")

    def test_getint_existing(self):
        val = self.cfg.getint("logging", "level")
        self.assertIsInstance(val, int)
        self.assertEqual(val, int(DEFAULT_CONFIG["logging"]["level"]))

    def test_getint_fallback(self):
        val = self.cfg.getint("nosection", "nokey", fallback=42)
        self.assertEqual(val, 42)

    def test_getint_missing_no_fallback_returns_zero(self):
        val = self.cfg.getint("nosection", "nokey")
        self.assertEqual(val, 0)

    def test_getbool_fallback(self):
        val = self.cfg.getbool("nosection", "nokey", fallback=True)
        self.assertTrue(val)

    def test_getbool_missing_no_fallback_returns_false(self):
        val = self.cfg.getbool("nosection", "nokey")
        self.assertFalse(val)


class TestGetConfigSingleton(unittest.TestCase):
    """get_config() returns a singleton."""

    def setUp(self):
        # Reset singleton so each test starts fresh
        if hasattr(get_config, "_instance"):
            del get_config._instance

    def test_returns_config_instance(self):
        self.assertIsInstance(get_config(), Config)

    def test_singleton_same_object(self):
        a = get_config()
        b = get_config()
        self.assertIs(a, b)

    def tearDown(self):
        if hasattr(get_config, "_instance"):
            del get_config._instance


# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    unittest.main(verbosity=2)
