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

sys.path.append(config.get("paths", "base"))

from scr.setup.sec import banner

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
        clear()
        banner.execute()
        rule(f"[{yellow}]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - AIDE MODULE [/{yellow}]", style=yellow, align="left")
        # ----------------------------------------------------------
        # EXTRAS - Install 'aide'
        # ----------------------------------------------------------
        line()
        printWhite("Install 'aide'")
        pkgs = ["aide", "aide-common"]
        installAPT(pkgs)
        copyRepoFile(SETUPDIR, "/etc/aide/aide.conf", True)
        run("aideinit --yes")
        db = Path("/var/lib/aide/aide.db.new")
        if db.exists():
            mv = Path("/var/lib/aide/aide.db")
            db.replace(mv)
        files = ["/etc/systemd/system/aide-check.service", "/etc/systemd/system/aide-check.timer"]
        copyRepoFiles(SETUPDIR, files, True)
        run("systemctl enable aide-check.timer")
        run("systemctl start aide-check.timer")
        run("systemctl daemon-reload")
        line()
        getData(f"[{yellow}]MODULE COMPLETE :: Press [ENTER] to continue ...[/{yellow}] ")
    except Exception as e:
        reason = str(e)
        logger.error(f"Failed to install 'aide': {reason}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
