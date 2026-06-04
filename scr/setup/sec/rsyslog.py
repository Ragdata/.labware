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

from labware.filesys import *

from scr.setup.sec import banner

#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        clear()
        banner.execute()
        rule(f"[yellow]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - RSYSLOG MODULE [/yellow]", style="yellow", align="left")
        # ----------------------------------------------------------
        # Section 6.2 - Secure 'rsyslog'
        # ----------------------------------------------------------
        line()
        printHead("Section 6.2 - Secure 'rsyslog'")
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
        line()
        getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
    except Exception as e:
        reason = str(e)
        logger.error(f"Failed to Harden 'rsyslog': {reason}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
