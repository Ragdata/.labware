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
from labware.filesys import *

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
        getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
    except Exception as e:
        reason = str(e)
        logger.error(f"Failed to Harden 'usbguard': {reason}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
