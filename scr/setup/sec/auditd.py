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
        rule(f"[{yellow}]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - AUDITD MODULE [/{yellow}]", style=yellow, align="left")
        global CHECKED
        if not CHECKED:
            line()
            CHECKED = checkRequired()
            config.set("setup", "checked", str(CHECKED))
        # ----------------------------------------------------------
        # Section 6.1 - 'auditd' Logging & Audit Rules
        # ----------------------------------------------------------
        logger.info(f"Executing {__file__}")
        line()
        printHead("Section 6.1 - 'auditd' Logging & Audit Rules")
        line()
        pkgs = ["auditd", "audispd-plugins"]
        installAPT(pkgs)
        line()
        files = ["/etc/audit/rules.d/50-scope.rules", "/etc/audit/rules.d/50-processes.rules", "/etc/audit/auditd.conf"]
        copyRepoFiles(SETUPDIR, files, True)
        line()
        run("systemctl daemon-reload")
        run("systemctl --now enable auditd")
        run("systemctl restart auditd")
        line()
        getData(f"[{yellow}]MODULE COMPLETE :: Press [ENTER] to continue ...[/{yellow}] ")
    except Exception as e:
        reason = str(e)
        logger.error(f"Failed to Harden 'auditd': {reason}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
