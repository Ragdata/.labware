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
        # Section 2.5 - Secure 'cron' and 'at'
        # ----------------------------------------------------------
        line()
        printHead("Section 2.5 - Secure 'cron' and 'at'")
        files = ["/etc/cron.allow", "/etc/at.allow"]
        copyRepoFiles(SETUPDIR, files, True)
        run("chown root:root /etc/cron*")
        run("chmod og-rwx /etc/cron*")
        run("chown root:root /etc/at*")
        run("chmod og-rwx /etc/at*")
        run("systemctl mask atd.service")
        run("systemctl stop atd.service")
        run("systemctl daemon-reload")
        line()
        getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
    except Exception as e:
        logger.error(f"An error occurred: {e}", True)
        raise
