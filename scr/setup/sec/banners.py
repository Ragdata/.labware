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
        outlog.logError(f"An error occurred: {e}")
        raise e
