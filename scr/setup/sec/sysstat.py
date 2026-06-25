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

import banner

from labware.filesys import *

#-------------------------------------------------------------------
# VARIABLES
#-------------------------------------------------------------------
CHECKED: bool = config.getbool("setup", "checked", fallback=False)
SETUPDIR = Path(config.get("paths", "setup"))
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        clear()
        banner.execute()
        rule(f"[{yellow}]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - SYSSTAT MODULE [/{yellow}]", style=yellow, align="left")
        global CHECKED
        if not CHECKED:
            line()
            CHECKED = checkRequired()
            config.set("setup", "checked", str(CHECKED))
        # ----------------------------------------------------------
        # EXTRAS - Enable 'sysstat'
        # ----------------------------------------------------------
        logger.info(f"Executing {__file__}")
        line()
        printWhite("Enable 'sysstat'")
        line()
        copyRepoFile(SETUPDIR, "/etc/default/sysstat", True)
        run("systemctl enable sysstat")
        line()
        getData(f"[{yellow}]MODULE COMPLETE :: Press [ENTER] to continue ...[/{yellow}] ")
    except Exception as e:
        logger.error(f"An error occurred: {e}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
