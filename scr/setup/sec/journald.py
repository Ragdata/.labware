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
        rule(f"[yellow]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - JOURNALD MODULE [/yellow]", style="yellow", align="left")
        # ----------------------------------------------------------
        # Section 6.3 - Log Rotation & JournalD
        # ----------------------------------------------------------
        line()
        printHead("Section 6.3 - Log Rotation & JournalD")
        files = ["/etc/logrotate.conf", "/etc/logrotate.d/sudo", "/etc/systemd/journald.conf"]
        copyRepoFiles(SETUPDIR, files, True)
        run("systemctl restart systemd-journald")
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
