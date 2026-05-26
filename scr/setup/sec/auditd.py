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
# PROCESS
#-------------------------------------------------------------------
if __name__ == "__main__":
    try:
        pkgs = ["auditd" "audispd-plugins"]
        installAPT(pkgs)
        run("systemctl --now enable auditd")
        filepath = "/etc/audit/rules/50-scope.rules"
        template = BASEDIR / filepath
        filedest = Path(filepath)
        copyFiles(template, filedest, True)
        filepath = "/etc/audit/rules/50-processes.rules"
        template = BASEDIR / filepath
        filedest = Path(filepath)
        copyFiles(template, filedest, True)
        filepath = "/etc/auditd.conf"
        template = BASEDIR / filepath
        filedest = Path(filepath)
        copyFiles(template, filedest, True)
    except Exception as e:
        reason = str(e)
        outlog.logError(f"Failed to Harden AuditD: {reason}")
        raise e
