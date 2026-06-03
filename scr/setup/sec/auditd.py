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
        # Section 6.1 - 'auditd' Logging & Audit Rules
        # ----------------------------------------------------------
        line()
        printHead("Section 6.1 - 'auditd' Logging & Audit Rules")
        pkgs = ["auditd", "audispd-plugins", "auditd-plugin-clickhouse"]
        installAPT(pkgs)
        copyRepoFile(SETUPDIR / "etc/audit/auditd.rules", "/etc/audit/rules.d/hardening.rules", True)
        files = ["/etc/audit/rules/50-scope.rules", "/etc/audit/rules/50-processes.rules", "/etc/audit/auditd.conf"]
        copyRepoFiles(SETUPDIR, files, True)
        run("systemctl --now enable auditd")
        run("systemctl restart auditd")
        line()
        getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
    except Exception as e:
        reason = str(e)
        logger.error(f"Failed to Harden 'auditd': {reason}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
