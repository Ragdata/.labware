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
if __name__ == "__main__":
    try:
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
