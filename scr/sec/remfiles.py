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
        rule(f"[{yellow}]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - REMFILES MODULE [/{yellow}]", style=yellow, align="left")
        global CHECKED
        if not CHECKED:
            line()
            CHECKED = checkRequired()
            config.set("setup", "checked", str(CHECKED))
        # ----------------------------------------------------------
        # Section 1.1 - Remove Unnecessary Filesystems
        # ----------------------------------------------------------
        logger.info(f"Executing {__file__}")
        line()
        printHead("Section 1.1 - Remove Unnecessary Filesystems")
        filesys = BASEDIR / "setup/cfg/apt-filesys.cfg"
        if not filesys.exists():
            raise FileNotFoundError(f"File not found: '{filesys}'")
        files = getList(filesys)
        removeAPT(files)
        # autofs = Path("/etc/systemd/system/autofs.service")
        # if autofs.exists():
        #     line()
        #     run("systemctl mask autofs")
        line()
        getData(f"[{cyan}]Press [ENTER] to continue ...[/{cyan}] ")
        # ----------------------------------------------------------
        # Section 2.1 - Remove Unused Services
        # ----------------------------------------------------------
        line()
        printHead("Section 2.1 - Remove Unused Services")
        line()
        remove = BASEDIR / "setup/cfg/apt-remove.cfg"
        if not remove.exists():
            raise FileNotFoundError(f"File not found: '{remove}'")
        pkgs = getList(remove)
        removeAPT(pkgs)
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
