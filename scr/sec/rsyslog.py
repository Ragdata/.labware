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
SETUPDIR = Path(config.get("paths", "sec"))
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        clear()
        banner.execute()
        rule(f"[{yellow}]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - RSYSLOG MODULE [/{yellow}]", style=yellow, align="left")
        global CHECKED
        if not CHECKED:
            line()
            CHECKED = checkRequired()
            config.set("setup", "checked", str(CHECKED))
        # ----------------------------------------------------------
        # Section 6.2 - Secure 'rsyslog'
        # ----------------------------------------------------------
        logger.info(f"Executing {__file__}")
        line()
        printHead("Section 6.2 - Secure 'rsyslog'")
        line()
        pkgs = ["rsyslog"]
        installAPT(pkgs)
        run("systemctl --now enable rsyslog")
        line()
        template = SETUPDIR / "etc/rsyslog.d/50-default.conf"
        filedest = Path("/etc/rsyslog.d/50-default.conf")
        copyFiles(template, filedest, True)
        line()
        run("find /var/log -type f -exec chmod 640 {} \\;")
        run("find /var/log -type d -exec chmod 750 {} \\;")
        chmod(Path("/var/log/sudo.log"), 0o640)
        line()
        getData(f"[{yellow}]MODULE COMPLETE :: Press [ENTER] to continue ...[/{yellow}] ")
    except Exception as e:
        reason = str(e)
        logger.error(f"Failed to Harden 'rsyslog': {reason}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
