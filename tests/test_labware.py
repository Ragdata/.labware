#!/usr/bin/env python3
"""
====================================================================
Package: labware
====================================================================
Test Suite for labware modules:
    - config.py
    - output.py
    - logger.py
    - filesys.py
    - utils.py
    - registry.py
    - regex.py
====================================================================
"""
import os
import sys
import logging
import tempfile
import unittest

from io import StringIO
from pathlib import Path
from unittest.mock import patch, MagicMock

# ---------------------------------------------------------------------------
# Path bootstrap — mirrors what the modules do so imports resolve without
# a full editable install being in place during CI.
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
# 2. OUTPUT TESTS
# ===========================================================================
class TestOutputFunctions(unittest.TestCase):
    """Tests for output.py console helpers."""

    def setUp(self):
        # Import here so the config singleton is already initialised
        from labware import output as out_mod
        self.out = out_mod

    def _capture(self, fn, *args, **kwargs):
        """Run an output function and return what was printed."""
        buf = StringIO()
        with patch.object(self.out.console, "print") as mock_print:
            fn(*args, **kwargs)
            return mock_print

    def test_printMessage_calls_console_print(self):
        with patch.object(self.out.console, "print") as mock_print:
            self.out.printMessage("hello")
            mock_print.assert_called_once()

    def test_printMessage_with_style(self):
        with patch.object(self.out.console, "print") as mock_print:
            self.out.printMessage("hello", style="info")
            _, kwargs = mock_print.call_args
            self.assertEqual(kwargs.get("style"), "info")

    def test_printInfo_prepends_symbol(self):
        with patch.object(self.out.console, "print") as mock_print:
            self.out.printInfo("test message")
            args, _ = mock_print.call_args
            self.assertIn(DEFAULT_CONFIG["symbols"]["info"], args[0])

    def test_printSuccess_prepends_symbol(self):
        with patch.object(self.out.console, "print") as mock_print:
            self.out.printSuccess("ok")
            args, _ = mock_print.call_args
            self.assertIn(DEFAULT_CONFIG["symbols"]["success"], args[0])

    def test_printWarning_prepends_symbol(self):
        with patch.object(self.out.console, "print") as mock_print:
            self.out.printWarning("warn")
            args, _ = mock_print.call_args
            self.assertIn(DEFAULT_CONFIG["symbols"]["warning"], args[0])

    def test_printError_prepends_symbol(self):
        with patch.object(self.out.console, "print") as mock_print:
            self.out.printError("err")
            args, _ = mock_print.call_args
            self.assertIn(DEFAULT_CONFIG["symbols"]["error"], args[0])

    def test_getData_calls_console_input(self):
        with patch.object(self.out.console, "input", return_value="x") as mock_input:
            result = self.out.getData(f"prompt: ")
            mock_input.assert_called_once_with("prompt: ")
            self.assertEqual(result, "x")

    def test_line_calls_console_line(self):
        with patch.object(self.out.console, "line") as mock_line:
            self.out.line(2)
            mock_line.assert_called_once_with(2)

    def test_rule_calls_console_rule(self):
        with patch.object(self.out.console, "rule") as mock_rule:
            self.out.rule("title")
            mock_rule.assert_called_once_with("title")

    def test_clear_calls_console_clear(self):
        with patch.object(self.out.console, "clear") as mock_clear:
            self.out.clear()
            mock_clear.assert_called_once_with(True)


# ===========================================================================
# 3. LOGGER TESTS
# ===========================================================================
class TestLoggerClass(unittest.TestCase):
    """Tests for the custom Logger class in logger.py."""

    def _make_logger(self, name="test"):
        from labware.logger import Logger
        log = Logger(name, level=logging.DEBUG)
        # Add a memory handler so we can inspect records
        self.handler = logging.handlers_list = []
        mem = logging.handlers.MemoryHandler(capacity=100, flushLevel=logging.CRITICAL + 1)
        log.addHandler(mem)
        self.mem_handler = mem
        return log

    def setUp(self):
        import logging.handlers
        self.logging_handlers = logging.handlers

    def test_logger_is_logging_logger_subclass(self):
        from labware.logger import Logger
        self.assertTrue(issubclass(Logger, logging.Logger))

    def test_info_logs_at_info_level(self):
        from labware.logger import Logger
        log = Logger("ti", level=logging.DEBUG)
        with patch.object(log, "_log") as mock_log:
            log.info("hello")
            mock_log.assert_called_once()
            self.assertEqual(mock_log.call_args[0][0], logging.INFO)

    def test_error_logs_at_error_level(self):
        from labware.logger import Logger
        log = Logger("te", level=logging.DEBUG)
        with patch.object(log, "_log") as mock_log:
            log.error("boom")
            mock_log.assert_called_once()
            self.assertEqual(mock_log.call_args[0][0], logging.ERROR)

    def test_debug_logs_at_debug_level(self):
        from labware.logger import Logger
        log = Logger("td", level=logging.DEBUG)
        with patch.object(log, "_log") as mock_log:
            log.debug("dbg")
            self.assertEqual(mock_log.call_args[0][0], logging.DEBUG)

    def test_warning_logs_at_warning_level(self):
        from labware.logger import Logger
        log = Logger("tw", level=logging.DEBUG)
        with patch.object(log, "_log") as mock_log:
            log.warning("warn")
            self.assertEqual(mock_log.call_args[0][0], logging.WARNING)

    def test_out_flag_calls_outlog(self):
        from labware.logger import Logger
        log = Logger("to", level=logging.DEBUG)
        with patch.object(log, "_log"), \
             patch.object(log, "outlog") as mock_outlog:
            log.info("msg", out=True)
            mock_outlog.assert_called_once_with("msg", "info")

    def test_exit_flag_calls_exit(self):
        from labware.logger import Logger
        log = Logger("tx", level=logging.DEBUG)
        with patch.object(log, "_log"), patch("builtins.exit") as mock_exit:
            log.error("bye", xit=1)
            mock_exit.assert_called_once_with(1)

    def test_outlog_prepends_symbol(self):
        from labware.logger import Logger
        from labware import output as out
        log = Logger("tol", level=logging.DEBUG)
        with patch.object(out.console, "print") as mock_print:
            log.outlog("hello", style="info")
            args, _ = mock_print.call_args
            self.assertIn(DEFAULT_CONFIG["symbols"]["info"], args[0])


class TestGetLogger(unittest.TestCase):
    """Tests for get_logger singleton factory."""

    def setUp(self):
        from labware import logger as log_mod
        self.log_mod = log_mod
        # Clear singleton cache
        if hasattr(log_mod.get_logger, "_instances"):
            log_mod.get_logger._instances.clear()

    def test_returns_logger_instance(self):
        with patch("labware.logger.initRotatingFileHandler") as mock_rfh:
            mock_rfh.return_value = MagicMock(spec=logging.Handler)
            mock_rfh.return_value.level = logging.DEBUG
            log = self.log_mod.get_logger("mytest")
            self.assertIsInstance(log, self.log_mod.Logger)

    def test_same_name_returns_same_object(self):
        with patch("labware.logger.initRotatingFileHandler") as mock_rfh:
            mock_rfh.return_value = MagicMock(spec=logging.Handler)
            mock_rfh.return_value.level = logging.DEBUG
            a = self.log_mod.get_logger("dup")
            b = self.log_mod.get_logger("dup")
            self.assertIs(a, b)

    def tearDown(self):
        if hasattr(self.log_mod.get_logger, "_instances"):
            self.log_mod.get_logger._instances.clear()


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
# 6. REGISTRY TESTS
# ===========================================================================
class TestRegistry(unittest.TestCase):
    """Tests for Registry class in registry.py."""

    def setUp(self):
        # Use a temp directory for DB files
        self.tmp = Path(tempfile.mkdtemp())
        try:
            from labware.registry import Registry
            self.Registry = Registry
            self.skip = False
        except ImportError:
            self.skip = True

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _make_reg(self, name="test"):
        return self.Registry(db_name=name, db_dir=self.tmp)

    def test_skip_if_no_sqlitedict(self):
        if self.skip:
            self.skipTest("sqlitedict not installed")

    def test_set_and_get(self):
        if self.skip: self.skipTest("sqlitedict not installed")
        with self._make_reg() as reg:
            reg.set("key1", "value1")
            self.assertEqual(reg.get("key1"), "value1")

    def test_dict_style_access(self):
        if self.skip: self.skipTest("sqlitedict not installed")
        with self._make_reg() as reg:
            reg["mykey"] = 42
            self.assertEqual(reg["mykey"], 42)

    def test_exists_true(self):
        if self.skip: self.skipTest("sqlitedict not installed")
        with self._make_reg() as reg:
            reg.set("k", "v")
            self.assertTrue(reg.exists("k"))

    def test_exists_false(self):
        if self.skip: self.skipTest("sqlitedict not installed")
        with self._make_reg() as reg:
            self.assertFalse(reg.exists("nonexistent"))

    def test_contains_operator(self):
        if self.skip: self.skipTest("sqlitedict not installed")
        with self._make_reg() as reg:
            reg["x"] = 1
            self.assertIn("x", reg)
            self.assertNotIn("z", reg)

    def test_delete(self):
        if self.skip: self.skipTest("sqlitedict not installed")
        with self._make_reg() as reg:
            reg.set("d", "val")
            reg.delete("d")
            self.assertFalse(reg.exists("d"))

    def test_del_operator(self):
        if self.skip: self.skipTest("sqlitedict not installed")
        with self._make_reg() as reg:
            reg["delme"] = True
            del reg["delme"]
            self.assertNotIn("delme", reg)

    def test_count(self):
        if self.skip: self.skipTest("sqlitedict not installed")
        with self._make_reg() as reg:
            reg.set("a", 1)
            reg.set("b", 2)
            self.assertEqual(len(reg), 2)

    def test_clear(self):
        if self.skip: self.skipTest("sqlitedict not installed")
        with self._make_reg() as reg:
            reg.set("a", 1)
            reg.clear()
            self.assertEqual(len(reg), 0)

    def test_get_default(self):
        if self.skip: self.skipTest("sqlitedict not installed")
        with self._make_reg() as reg:
            self.assertIsNone(reg.get("missing"))
            self.assertEqual(reg.get("missing", default="fallback"), "fallback")

    def test_to_dict(self):
        if self.skip: self.skipTest("sqlitedict not installed")
        with self._make_reg() as reg:
            reg.set("p", 1)
            reg.set("q", 2)
            d = reg.to_dict()
        self.assertEqual(d, {"p": 1, "q": 2})

    def test_update(self):
        if self.skip: self.skipTest("sqlitedict not installed")
        with self._make_reg() as reg:
            reg.update({"x": 10, "y": 20})
            self.assertEqual(reg.get("x"), 10)
            self.assertEqual(reg.get("y"), 20)

    def test_keys(self):
        if self.skip: self.skipTest("sqlitedict not installed")
        with self._make_reg() as reg:
            reg.set("k1", "v1")
            reg.set("k2", "v2")
            self.assertEqual(set(reg.keys()), {"k1", "k2"})

    def test_values(self):
        if self.skip: self.skipTest("sqlitedict not installed")
        with self._make_reg() as reg:
            reg.set("k1", "v1")
            self.assertIn("v1", list(reg.values()))

    def test_items(self):
        if self.skip: self.skipTest("sqlitedict not installed")
        with self._make_reg() as reg:
            reg.set("k", "v")
            self.assertIn(("k", "v"), list(reg.items()))

    def test_persistence_across_instances(self):
        if self.skip: self.skipTest("sqlitedict not installed")
        with self._make_reg("persist") as reg:
            reg.set("saved", "hello")
        with self._make_reg("persist") as reg2:
            self.assertEqual(reg2.get("saved"), "hello")

    def test_repr_contains_path(self):
        if self.skip: self.skipTest("sqlitedict not installed")
        reg = self._make_reg()
        self.assertIn("Registry", repr(reg))


# ===========================================================================
# 7. REGEX TESTS
# ===========================================================================
class TestRegexPatterns(unittest.TestCase):
    """Tests for regex patterns in regex.py."""

    def setUp(self):
        from labware import regex as rx_mod
        self.rx = rx_mod

    # ── isFQDN ───────────────────────────────────────────────────────────────
    def test_fqdn_valid(self):
        for val in ("example.com", "sub.example.co.uk", "a1.b2.c3.io"):
            with self.subTest(val=val):
                self.assertRegex(val, self.rx.isFQDN)

    def test_fqdn_invalid(self):
        for val in ("-example.com", "example", "UPPER.com"):
            with self.subTest(val=val):
                self.assertNotRegex(val, self.rx.isFQDN)

    # ── isHOST ───────────────────────────────────────────────────────────────
    def test_host_valid(self):
        for val in ("myhost", "host-01", "Server123"):
            with self.subTest(val=val):
                self.assertRegex(val, self.rx.isHOST)

    def test_host_invalid(self):
        for val in ("host.name", "host name", "host_name"):
            with self.subTest(val=val):
                self.assertNotRegex(val, self.rx.isHOST)

    # ── isPORT ───────────────────────────────────────────────────────────────
    def test_port_valid(self):
        for val in ("80", "443", "8080", "65535"):
            with self.subTest(val=val):
                self.assertRegex(val, self.rx.isPORT)

    def test_port_invalid(self):
        for val in ("0", "1", "99", "abc"):
            with self.subTest(val=val):
                self.assertNotRegex(val, self.rx.isPORT)

    # ── isIPv4 ───────────────────────────────────────────────────────────────
    def test_ipv4_valid(self):
        for val in ("192.168.1.1", "10.0.0.1", "255.255.255.0", "0.0.0.0"):
            with self.subTest(val=val):
                self.assertRegex(val, self.rx.isIPv4)

    def test_ipv4_invalid(self):
        for val in ("999.0.0.1", "192.168.1", "not.an.ip.addr"):
            with self.subTest(val=val):
                self.assertNotRegex(val, self.rx.isIPv4)

    # ── isIPv6 ───────────────────────────────────────────────────────────────
    def test_ipv6_valid(self):
        for val in (
            "2001:0DB8:0000:0000:0000:0000:0000:0001",
            "::1",
            "FE80::1",
            "::",
        ):
            with self.subTest(val=val):
                self.assertRegex(val, self.rx.isIPv6)

    def test_ipv6_invalid(self):
        for val in ("192.168.1.1", "ZZZZ::1", "gggg::1"):
            with self.subTest(val=val):
                self.assertNotRegex(val, self.rx.isIPv6)

    # ── isMAC ────────────────────────────────────────────────────────────────
    def test_mac_valid(self):
        for val in ("00:1A:2B:3C:4D:5E", "00-1A-2B-3C-4D-5E", "001A2B3C4D5E"):
            with self.subTest(val=val):
                self.assertRegex(val, self.rx.isMAC)

    def test_mac_invalid(self):
        for val in ("00:1A:2B:3C:4D", "GG:HH:II:JJ:KK:LL"):
            with self.subTest(val=val):
                self.assertNotRegex(val, self.rx.isMAC)

    # ── isEMAIL ──────────────────────────────────────────────────────────────
    def test_email_valid(self):
        for val in ("user@example.com", "u.name+tag@sub.domain.io"):
            with self.subTest(val=val):
                self.assertRegex(val, self.rx.isEMAIL)

    def test_email_invalid(self):
        for val in ("@nodomain.com", "nodomain", "two@@at.com", "UPPER@domain.com"):
            with self.subTest(val=val):
                self.assertNotRegex(val, self.rx.isEMAIL)


# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    unittest.main(verbosity=2)
