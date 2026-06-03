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
        getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
    except Exception as e:
        reason = str(e)
        logger.error(f"Failed to install 'rkhunter': {reason}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
