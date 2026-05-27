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

sys.path.append("../mod")

from mod.filesys import *

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
        pkgs = ["auditd", "audispd-plugins"]
        installAPT(pkgs)
        copyRepoFile(SETUPDIR / "etc/audit/auditd.rules", "/etc/audit/rules.d/hardening.rules", True)
        files = ["/etc/audit/rules/50-scope.rules", "/etc/audit/rules/50-processes.rules", "/etc/audit/auditd.conf"]
        copyRepoFiles(SETUPDIR, files, True)
        run("systemctl --now enable auditd")
        run("systemctl restart auditd")
    except Exception as e:
        reason = str(e)
        outlog.logError(f"Failed to Harden AuditD: {reason}")
        raise e
