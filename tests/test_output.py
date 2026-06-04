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
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    unittest.main(verbosity=2)
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

from io import StringIO
from pathlib import Path
from unittest.mock import patch
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
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    unittest.main(verbosity=2)
