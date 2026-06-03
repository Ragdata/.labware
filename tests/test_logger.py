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
import sys, unittest, logging

from pathlib import Path
from unittest.mock import patch, MagicMock
from labware.config import DEFAULT_CONFIG

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
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    unittest.main(verbosity=2)
