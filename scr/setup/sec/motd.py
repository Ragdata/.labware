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
        rule(f"[yellow]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - MOTD MODULE [/yellow]", style="yellow", align="left")
        # ----------------------------------------------------------
        # Section 1.6 - Legal Banners
        # ----------------------------------------------------------
        line()
        printHead("Section 1.6 - Legal Banners")
        files = ["/etc/issue.net", "/etc/issue", "/etc/motd"]
        copyRepoFiles(SETUPDIR, files, True)
        run("chmod -x /etc/update-motd.d/*")
        run("systemctl stop motd-news.timer")
        run("systemctl mask motd-news.timer")
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
