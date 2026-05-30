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
# PROCESS
#-------------------------------------------------------------------
if __name__ == "__main__":
    try:
        # ----------------------------------------------------------
        # Section 6.4 - Enable 'acct' & Process Tracking
        # ----------------------------------------------------------
        line()
        printHead("Section 6.4 - Enable 'acct' & Process Tracking")
        pkgs = ["acct"]
        installAPT(pkgs)
        run("systemctl enable acct")
        line()
        getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
    except Exception as e:
        reason = str(e)
        logger.error(f"Failed to install 'acct': {reason}", True)
        raise
