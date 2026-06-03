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
        # Section 1.4 - Coredumps
        # ----------------------------------------------------------
        line()
        printHead("Section 1.4 - Coredumps")
        copyRepoFile(SETUPDIR, "/etc/security/limits.conf", True)
        run("echo 'fs.suid_dumpable = 0' > /etc/sysctl.d/60-coredump.conf")
        run("sysctl -p /etc/sysctl.d/60-coredump.conf")
        copyRepoFile(SETUPDIR, "/etc/systemd/coredump.conf", True)
        run("systemctl restart systemd-journald")
        line()
        getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
    except Exception as e:
        reason = str(e)
        logger.error(f"Failed to Harden Coredumps: {reason}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
