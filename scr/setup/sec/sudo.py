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
        # Section 5.2 - Secure SUDO
        # ----------------------------------------------------------
        line()
        printHead("Section 5.2 - Secure SUDO")
        copyRepoFile(SETUPDIR, "/etc/sudoers.d/01_base", True, mode=0o440)
        copyRepoFile(SETUPDIR, "/etc/pam.d/su", True)
        # if run(f"visudo -c -f {filedest}").returncode != 0:
        #     logger.error(f"SUDO config failed validation", True, 1)
        line()
        getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
    except Exception as e:
        logger.error(f"An error occurred: {e}", True)
        raise
