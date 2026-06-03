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
import sys, unittest, tempfile

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
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    unittest.main(verbosity=2)
