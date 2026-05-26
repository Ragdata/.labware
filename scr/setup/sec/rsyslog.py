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
        pkgs = ["rsyslog"]
        installAPT(pkgs)
        run("systemctl --now enable rsyslog")
        filepath = "/etc/rsyslog.d/50-default.conf"
        template = BASEDIR / filepath
        filedest = Path(filepath)
        copyFiles(template, filedest, True)
        run("find /var/log -type f -exec chmod 640 {} \\;")
        run("find /var/log -type d -exec chmod 750 {} \\;")
        chmod(Path("/var/log/sudo.log"), 0o640)
    except Exception as e:
        reason = str(e)
        outlog.logError(f"Failed to Harden AuditD: {reason}")
        raise e
