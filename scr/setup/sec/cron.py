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
        rule(f"[yellow]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - CRON MODULE [/yellow]", style="yellow", align="left")
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
        getData("[yellow]MODULE COMPLETE :: Press [ENTER] to continue ...[/yellow] ")
    except Exception as e:
        logger.error(f"An error occurred: {e}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
