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
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        clear()
        banner.execute()
        rule(f"[{yellow}]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - TOOLS MODULE [/{yellow}]", style=yellow, align="left")
        global CHECKED
        if not CHECKED:
            line()
            CHECKED = checkRequired()
            config.set("setup", "checked", str(CHECKED))
        # ----------------------------------------------------------
        # INSTALL BASIC TOOLS
        # ----------------------------------------------------------
        logger.info(f"Executing {__file__}")
        line()
        printHead("Installing Basic Tools ...")
        line()
        basic = Path(config.get("paths", "setup")) / "cfg" / "apt-basic.cfg"
        if not basic.exists():
            raise FileNotFoundError(f"File not found: '{basic}'")
        pkgs = getList(basic)
        installAPT(pkgs)
        line()
        getData(f"[{cyan}]Press [ENTER] to continue ...[/{cyan}] ")
        # ----------------------------------------------------------
        # INSTALL SECURITY TOOLS
        # ----------------------------------------------------------
        clear()
        banner.execute()
        rule(f"[{yellow}]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - TOOLS MODULE [/{yellow}]", style=yellow, align="left")
        line()
        printHead("Installing Security Tools ...")
        secure = Path(config.get("paths", "setup")) / "cfg" / "apt-secure.cfg"
        if not secure.exists():
            raise FileNotFoundError(f"File not found: '{secure}'")
        pkgs = getList(secure)
        installAPT(pkgs)
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
