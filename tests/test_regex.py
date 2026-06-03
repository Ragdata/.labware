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
