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
if __name__ == "__main__":
    try:
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
        getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
    except Exception as e:
        reason = str(e)
        outlog.logError(f"Failed to install ACCT: {reason}")
        raise e
