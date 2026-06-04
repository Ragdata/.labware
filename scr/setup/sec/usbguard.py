#!/usr/bin/env python3
"""
====================================================================
Package: labware
====================================================================
Author:			Ragdata
Date:			12/05/2026
License:		MIT License
Repository:		https://github.com/Ragdata/.labware
Copyright:		Copyright © 2026 Redeyed Technologies
====================================================================
"""
import sys

sys.path.append(".")

from labware.filesys import *

from scr.setup.sec import banner

#-------------------------------------------------------------------
# VARIABLES
#-------------------------------------------------------------------
BASEDIR  = Path(config.get("paths", "base"))
SETUPDIR = BASEDIR / "scr/setup"
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        clear()
        banner.execute()
        rule(f"[{yellow}]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - USBGUARD MODULE [/{yellow}]", style=yellow, align="left")
        # ----------------------------------------------------------
        # EXTRAS - USBGUARD
        # ----------------------------------------------------------
        line()
        printWhite("Install 'usbguard'")
        run("apt install -y --no-install-recommends usbguard")
        run("usbguard generate-policy > /tmp/rules.conf")
        run("install -m 0600 -o root -g root /tmp/rules.conf /etc/usbguard/rules.conf")
        run("systemctl enable usbguard.service")
        run("systemctl start usbguard.service")
        line()
        getData(f"[{yellow}]MODULE COMPLETE :: Press [ENTER] to continue ...[/{yellow}] ")
    except Exception as e:
        reason = str(e)
        logger.error(f"Failed to Harden 'usbguard': {reason}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
