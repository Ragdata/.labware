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
        rule(f"[yellow]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - APT MODULE [/yellow]", style="yellow", align="left")
        # ----------------------------------------------------------
        # Section 1.5 - Unattended Upgrades + APT Config
        # ----------------------------------------------------------
        line()
        printHead("Section 1.5 - Unattended Upgrades + APT Config")
        files = ["/etc/apt/apt.conf.d/50unattended-upgrades", "/etc/apt/apt.conf.d/98-hardening", "/etc/apt/apt.conf.d/99-noexec-tmp"]
        copyRepoFiles(SETUPDIR, files, True)
        line()
        getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
    except Exception as e:
        logger.error(f"An error occurred: {e}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
