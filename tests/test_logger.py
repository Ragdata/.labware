#!/usr/bin/env python3
"""
====================================================================
Package: labware
====================================================================
Author:			Ragdata
Date:			06/06/2026
License:		MIT License
Repository:		https://github.com/Ragdata/.labware
Copyright:		Copyright © 2026 Redeyed Technologies
====================================================================

Test Module for labware.logger

Tests the refactored logger module with:
- Multiple named logger instances (singleton-per-name)
- Lazy configuration loading with graceful fallback
- Optional console output
- Robust error handling
- External package support
"""
import sys
import unittest
import logging
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock, Mock
from io import StringIO

# ---------------------------------------------------------------------------
# Path bootstrap — mirrors what the modules do so imports resolve without
# a full editable installation being in place during CI.
# ---------------------------------------------------------------------------
BASEDIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASEDIR / "src"))

# ===========================================================================
# LOGGER CLASS TESTS
# ===========================================================================
class TestLoggerClass(unittest.TestCase):
    """Tests for the custom Logger class."""

    def test_logger_is_logging_logger_subclass(self):
        """Logger should be a subclass of logging.Logger"""
        from labware.logger import Logger
        self.assertTrue(issubclass(Logger, logging.Logger))

    def test_logger_init_with_explicit_level(self):
        """Logger should initialise with an explicit level"""
        from labware.logger import Logger
        log = Logger("test", level=logging.DEBUG)
        self.assertEqual(log.level, logging.DEBUG)
        self.assertEqual(log.name, "test")

    def test_logger_init_with_default_level(self):
        """Logger should use config default level when not specified"""
        from labware.logger import Logger
        log = Logger("test")
        # Should default to config level (which fallback is logging.INFO)
        self.assertGreaterEqual(log.level, logging.INFO)

    def test_info_logs_at_info_level(self):
        """info() should log at the INFO level"""
        from labware.logger import Logger
        log = Logger("test", level=logging.DEBUG)
        with patch.object(log, "_log") as mock_log:
            log.info("test message")
            self.assertEqual(mock_log.call_args[0][0], logging.INFO)

    def test_debug_logs_at_debug_level(self):
        """debug() should log at the DEBUG level"""
        from labware.logger import Logger
        log = Logger("test", level=logging.DEBUG)
        with patch.object(log, "_log") as mock_log:
            log.debug("debug message")
            self.assertEqual(mock_log.call_args[0][0], logging.DEBUG)

    def test_warning_logs_at_warning_level(self):
        """warning() should log at WARNING level"""
        from labware.logger import Logger
        log = Logger("test", level=logging.DEBUG)
        with patch.object(log, "_log") as mock_log:
            log.warning("warning message")
            self.assertEqual(mock_log.call_args[0][0], logging.WARNING)

    def test_error_logs_at_error_level(self):
        """error() should log at ERROR level"""
        from labware.logger import Logger
        log = Logger("test", level=logging.DEBUG)
        with patch.object(log, "_log") as mock_log:
            log.error("error message")
            self.assertEqual(mock_log.call_args[0][0], logging.ERROR)

    def test_critical_logs_at_critical_level(self):
        """critical() should log at CRITICAL level"""
        from labware.logger import Logger
        log = Logger("test", level=logging.DEBUG)
        with patch.object(log, "_log") as mock_log:
            log.critical("critical message")
            self.assertEqual(mock_log.call_args[0][0], logging.CRITICAL)

    def test_success_logs_at_info_level(self):
        """success() should log at INFO level (custom style)"""
        from labware.logger import Logger
        log = Logger("test", level=logging.DEBUG)
        with patch.object(log, "_log") as mock_log:
            log.success("success message")
            self.assertEqual(mock_log.call_args[0][0], logging.INFO)

    def test_tip_logs_at_info_level(self):
        """tip() should log at INFO level (custom style)"""
        from labware.logger import Logger
        log = Logger("test", level=logging.DEBUG)
        with patch.object(log, "_log") as mock_log:
            log.tip("tip message")
            self.assertEqual(mock_log.call_args[0][0], logging.INFO)

    def test_out_flag_calls_outlog(self):
        """out=True should call outlog() with the style"""
        from labware.logger import Logger
        log = Logger("test", level=logging.DEBUG)
        with patch.object(log, "_log"), \
             patch.object(log, "outlog") as mock_outlog:
            log.info("message", out=True)
            mock_outlog.assert_called_once_with("message", "info")

    def test_xit_flag_calls_exit(self):
        """xit parameter should call exit() with the code"""
        from labware.logger import Logger
        log = Logger("test", level=logging.DEBUG)
        with patch.object(log, "_log"), \
             patch("builtins.exit") as mock_exit:
            log.error("fatal error", xit=42)
            mock_exit.assert_called_once_with(42)

    def test_outlog_with_output_module(self):
        """outlog() should use Rich console when output module available"""
        from labware.logger import Logger
        log = Logger("test", level=logging.DEBUG)

        with patch("labware.logger.HAS_OUTPUT", True), \
             patch("labware.logger.printMessage") as mock_print, \
             patch("labware.logger.cfg") as mock_cfg:
            mock_cfg.get.return_value = "✓"
            log.outlog("message", style="success")
            mock_print.assert_called_once()

    def test_outlog_without_output_module(self):
        """outlog() should fallback to print() when output unavailable"""
        from labware.logger import Logger
        log = Logger("test", level=logging.DEBUG)

        with patch("labware.logger.HAS_OUTPUT", False), \
             patch("builtins.print") as mock_print:
            log.outlog("message", style="info")
            mock_print.assert_called_once()

    def test_exception_logs_with_exc_info(self):
        """exception() should log at ERROR level with exc_info=True"""
        from labware.logger import Logger
        log = Logger("test", level=logging.DEBUG)
        with patch.object(log, "_log") as mock_log:
            log.exception("error occurred")
            self.assertEqual(mock_log.call_args[0][0], logging.ERROR)
            self.assertTrue(mock_log.call_args[1].get("exc_info"))


# ===========================================================================
# CONFIGURATION TESTS
# ===========================================================================
class TestConfigurationLoading(unittest.TestCase):
    """Tests for lazy configuration loading and defaults."""

    def setUp(self):
        """Reset cached config before each test"""
        import labware.logger as log_mod
        log_mod._log_config = None

    def test_get_config_returns_dict(self):
        """_get_config() should return a configuration dictionary"""
        from labware.logger import _get_config
        config = _get_config()
        self.assertIsInstance(config, dict)
        self.assertIn("level", config)
        self.assertIn("size", config)
        self.assertIn("formats", config)

    def test_default_config_has_required_keys(self):
        """Default config should have all required keys"""
        from labware.logger import _get_config
        config = _get_config()
        required_keys = ["level", "size", "count", "format", "logdir", "formats", "date"]
        for key in required_keys:
            self.assertIn(key, config)

    def test_config_caching(self):
        """_get_config() should cache configuration after the first call"""
        from labware.logger import _get_config
        config1 = _get_config()
        config2 = _get_config()
        # Should be same object (cached)
        self.assertIs(config1, config2)

    def test_get_log_level_convenience_function(self):
        """get_log_level() should return the configured level"""
        from labware.logger import get_log_level
        level = get_log_level()
        self.assertIsInstance(level, int)
        self.assertGreaterEqual(level, logging.DEBUG)

    def test_get_log_dir_convenience_function(self):
        """get_log_dir() should return Path to the log directory"""
        from labware.logger import get_log_dir
        log_dir = get_log_dir()
        self.assertIsInstance(log_dir, Path)
        self.assertTrue(str(log_dir).endswith(".labware/log"))

    def test_get_log_size_convenience_function(self):
        """get_log_size() should return max file size"""
        from labware.logger import get_log_size
        size = get_log_size()
        self.assertIsInstance(size, int)
        self.assertGreater(size, 0)

    def test_get_log_count_convenience_function(self):
        """get_log_count() should return backup count"""
        from labware.logger import get_log_count
        count = get_log_count()
        self.assertIsInstance(count, int)
        self.assertGreater(count, 0)

    def test_get_log_format_convenience_function(self):
        """get_log_format() should return the default format style"""
        from labware.logger import get_log_format
        fmt = get_log_format()
        self.assertIsInstance(fmt, str)
        self.assertIn(fmt, ["std", "short", "long", "console"])

    def test_get_date_format_convenience_function(self):
        """get_date_format() should return a date format string"""
        from labware.logger import get_date_format
        date_fmt = get_date_format()
        self.assertIsInstance(date_fmt, str)
        self.assertIn("%", date_fmt)

    def test_get_log_formats_convenience_function(self):
        """get_log_formats() should return format templates"""
        from labware.logger import get_log_formats
        formats = get_log_formats()
        self.assertIsInstance(formats, dict)
        self.assertIn("std", formats)
        self.assertIn("short", formats)
        self.assertIn("long", formats)


# ===========================================================================
# HANDLER INITIALIZATION TESTS
# ===========================================================================
class TestHandlerInitialization(unittest.TestCase):
    """Tests for handler initialisation functions."""

    def test_init_rotating_file_handler(self):
        """initRotatingFileHandler() should create a RotatingFileHandler"""
        from labware.logger import initRotatingFileHandler
        from logging.handlers import RotatingFileHandler

        with tempfile.TemporaryDirectory() as tmpdir:
            handler = initRotatingFileHandler("test", path=Path(tmpdir))
            self.assertIsInstance(handler, RotatingFileHandler)

    def test_init_rotating_file_handler_with_custom_params(self):
        """initRotatingFileHandler() should accept custom parameters"""
        from labware.logger import initRotatingFileHandler

        with tempfile.TemporaryDirectory() as tmpdir:
            handler = initRotatingFileHandler(
                "test",
                path=Path(tmpdir),
                maxSize=2097152,
                backups=5
            )
            self.assertEqual(handler.maxBytes, 2097152)
            self.assertEqual(handler.backupCount, 5)

    def test_init_stream_handler(self):
        """initStreamHandler() should create a StreamHandler"""
        from labware.logger import initStreamHandler
        import logging

        stream = StringIO()
        handler = initStreamHandler(stream=stream)
        self.assertIsInstance(handler, logging.StreamHandler)

    def test_init_stream_handler_with_custom_level(self):
        """initStreamHandler() should accept a custom level"""
        from labware.logger import initStreamHandler

        stream = StringIO()
        handler = initStreamHandler(stream=stream, level=logging.DEBUG)
        self.assertEqual(handler.level, logging.DEBUG)

    def test_get_formatter(self):
        """getFormatter() should return a Formatter"""
        from labware.logger import getFormatter

        formatter = getFormatter("std")
        self.assertIsInstance(formatter, logging.Formatter)

    def test_get_formatter_with_different_styles(self):
        """getFormatter() should support different format styles"""
        from labware.logger import getFormatter

        for style in ["std", "short", "long", "console"]:
            formatter = getFormatter(style)
            self.assertIsInstance(formatter, logging.Formatter)


# ===========================================================================
# GET_LOGGER FACTORY TESTS
# ===========================================================================
class TestGetLogger(unittest.TestCase):
    """Tests for the get_logger singleton factory function."""

    def setUp(self):
        """Clear the logger registry before each test"""
        from labware import logger as log_mod
        if hasattr(log_mod.get_logger, "_instances"):
            log_mod.get_logger._instances.clear()

    def tearDown(self):
        """Clear the logger registry after each test"""
        from labware import logger as log_mod
        if hasattr(log_mod.get_logger, "_instances"):
            log_mod.get_logger._instances.clear()

    def test_get_logger_returns_logger_instance(self):
        """get_logger() should return a Logger instance"""
        from labware.logger import get_logger, Logger

        with patch("labware.logger.initRotatingFileHandler") as mock_fh:
            mock_fh.return_value = MagicMock(spec=logging.Handler)
            log = get_logger("test")
            self.assertIsInstance(log, Logger)

    def test_same_name_returns_same_instance(self):
        """Calling get_logger() with the same name should return the same instance (singleton)"""
        from labware.logger import get_logger

        with patch("labware.logger.initRotatingFileHandler") as mock_fh:
            mock_fh.return_value = MagicMock(spec=logging.Handler)
            log1 = get_logger("singleton_test")
            log2 = get_logger("singleton_test")
            self.assertIs(log1, log2)

    def test_different_names_return_different_instances(self):
        """Calling get_logger() with different names should return different instances"""
        from labware.logger import get_logger

        with patch("labware.logger.initRotatingFileHandler") as mock_fh:
            mock_fh.return_value = MagicMock(spec=logging.Handler)
            log1 = get_logger("name1")
            log2 = get_logger("name2")
            self.assertIsNot(log1, log2)

    def test_get_logger_with_custom_level(self):
        """get_logger() should accept a custom level"""
        from labware.logger import get_logger

        with patch("labware.logger.initRotatingFileHandler") as mock_fh:
            mock_fh.return_value = MagicMock(spec=logging.Handler)
            log = get_logger("test", level=logging.DEBUG)
            self.assertEqual(log.level, logging.DEBUG)

    def test_get_logger_with_custom_format(self):
        """get_logger() should accept a custom format style"""
        from labware.logger import get_logger

        with patch("labware.logger.initRotatingFileHandler") as mock_fh, \
             patch("labware.logger.getFormatter") as mock_fmt:
            mock_fh.return_value = MagicMock(spec=logging.Handler)
            mock_fmt.return_value = MagicMock(spec=logging.Formatter)
            log = get_logger("test", fmt="long")
            mock_fmt.assert_called()

    def test_get_logger_with_add_stream(self):
        """get_logger() should add a stream handler when add_stream=True"""
        from labware.logger import get_logger

        with patch("labware.logger.initRotatingFileHandler") as mock_fh, \
             patch("labware.logger.initStreamHandler") as mock_sh:
            mock_fh.return_value = MagicMock(spec=logging.Handler)
            mock_sh.return_value = MagicMock(spec=logging.Handler)
            log = get_logger("test", add_stream=True)
            mock_sh.assert_called()

    def test_get_logger_graceful_error_handling(self):
        """get_logger() should return functional logger even on error"""
        from labware.logger import get_logger, Logger

        with patch("labware.logger.getFileLogger", side_effect=Exception("Test error")):
            log = get_logger("test")
            # Should return a Logger instance, not None
            self.assertIsInstance(log, Logger)
            # Should have handler
            self.assertTrue(len(log.handlers) > 0)


# ===========================================================================
# MODULE-LEVEL LOGGER TESTS
# ===========================================================================
class TestModuleLevelLogger(unittest.TestCase):
    """Tests for the module-level logger instance."""

    def test_module_logger_exists(self):
        """Module should have a logger instance"""
        from labware.logger import logger
        from labware.logger import Logger
        self.assertIsInstance(logger, Logger)

    def test_module_logger_has_name(self):
        """Module logger should have the name 'labware'"""
        from labware.logger import logger
        self.assertEqual(logger.name, "labware")


# ===========================================================================
# EXTERNAL USAGE TESTS
# ===========================================================================
class TestExternalPackageUsage(unittest.TestCase):
    """Tests for using logger in external packages."""

    def setUp(self):
        """Clear the logger registry before each test"""
        from labware import logger as log_mod
        if hasattr(log_mod.get_logger, "_instances"):
            log_mod.get_logger._instances.clear()

    def tearDown(self):
        """Clear the logger registry after each test"""
        from labware import logger as log_mod
        if hasattr(log_mod.get_logger, "_instances"):
            log_mod.get_logger._instances.clear()

    def test_external_app_can_create_logger(self):
        """External applications should be able to create loggers"""
        from labware.logger import get_logger

        with patch("labware.logger.initRotatingFileHandler") as mock_fh:
            mock_fh.return_value = MagicMock(spec=logging.Handler)
            log = get_logger("external_app")
            self.assertEqual(log.name, "external_app")

    def test_external_app_logger_with_console(self):
        """External app should be able to create logger with console output"""
        from labware.logger import get_logger

        with patch("labware.logger.initRotatingFileHandler") as mock_fh, \
             patch("labware.logger.initStreamHandler") as mock_sh:
            mock_fh.return_value = MagicMock(spec=logging.Handler)
            mock_sh.return_value = MagicMock(spec=logging.Handler)
            log = get_logger("external_app", add_stream=True)
            # Stream handler should have been added
            mock_sh.assert_called()


# ===========================================================================
# INTEGRATION TESTS
# ===========================================================================
class TestIntegration(unittest.TestCase):
    """Integration tests for complete logging workflows."""

    def setUp(self):
        """Clear the logger registry before each test"""
        from labware import logger as log_mod
        if hasattr(log_mod.get_logger, "_instances"):
            log_mod.get_logger._instances.clear()

    def tearDown(self):
        """Clear the logger registry after each test"""
        from labware import logger as log_mod
        if hasattr(log_mod.get_logger, "_instances"):
            log_mod.get_logger._instances.clear()

    def test_complete_workflow_file_logging(self):
        """Test complete workflow: create logger, log messages, check handlers"""
        from labware.logger import get_logger

        with patch("labware.logger.initRotatingFileHandler") as mock_fh:
            mock_handler = MagicMock(spec=logging.Handler)
            mock_handler.level = logging.DEBUG
            mock_fh.return_value = mock_handler

            log = get_logger("workflow_test")
            log.info("test message")

            self.assertEqual(log.name, "workflow_test")
            self.assertTrue(len(log.handlers) > 0)

    def test_multiple_loggers_in_application(self):
        """Test creating multiple loggers for different modules"""
        from labware.logger import get_logger

        with patch("labware.logger.initRotatingFileHandler") as mock_fh:
            mock_fh.return_value = MagicMock(spec=logging.Handler)

            app_log = get_logger("myapp")
            auth_log = get_logger("myapp.auth")
            db_log = get_logger("myapp.database")

            # Each should be different instance
            self.assertIsNot(app_log, auth_log)
            self.assertIsNot(auth_log, db_log)

            # Each should have correct name
            self.assertEqual(app_log.name, "myapp")
            self.assertEqual(auth_log.name, "myapp.auth")
            self.assertEqual(db_log.name, "myapp.database")

    def test_logging_with_different_levels(self):
        """Test logging at different levels"""
        from labware.logger import get_logger

        with patch("labware.logger.initRotatingFileHandler") as mock_fh:
            mock_fh.return_value = MagicMock(spec=logging.Handler)

            debug_log = get_logger("debug", level=logging.DEBUG)
            info_log = get_logger("info", level=logging.INFO)

            self.assertEqual(debug_log.level, logging.DEBUG)
            self.assertEqual(info_log.level, logging.INFO)


# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    unittest.main(verbosity=2)
