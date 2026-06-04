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
        rule(f"[yellow]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - RKHUNTER MODULE [/yellow]", style="yellow", align="left")
        # ----------------------------------------------------------
        # EXTRAS - Install 'rkhunter'
        # ----------------------------------------------------------
        line()
        printWhite("Install 'rkhunter'")
        pkgs = ["rkhunter"]
        installAPT(pkgs)
        copyRepoFile(SETUPDIR, "/etc/default/rkhunter", True)
        run("rkhunter --update")
        run("rkhunter --propupd")
        line()
        getData("[yellow]MODULE COMPLETE :: Press [ENTER] to continue ...[/yellow] ")
    except Exception as e:
        reason = str(e)
        logger.error(f"Failed to install 'rkhunter': {reason}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
