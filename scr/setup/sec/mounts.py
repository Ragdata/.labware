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
        # ----------------------------------------------------------
        # Section 1.8 - Detect Mounted Critical Paths
        # ----------------------------------------------------------
        line()
        printHead("Section 1.8 - Detect Mounted Critical Paths")
        MOUNTS = ["/home", "/tmp", "/var", "/var/log", "/var/log/audit", "/var/tmp", "/dev/shm"]
        for mnt in MOUNTS:
            if run(f"mount | grep -q 'on {mnt}'").returncode == 0:
                outlog.logSuccess(f"{mnt} is on a dedicated partition")
            else:
                outlog.logWarning(f"{mnt} is NOT on a dedicated partition")
        line()
        getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
    except Exception as e:
        outlog.logError(f"An error occurred: {e}")
        raise e
