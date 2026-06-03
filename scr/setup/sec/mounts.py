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
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        # ----------------------------------------------------------
        # Section 1.8 - Detect Mounted Critical Paths
        # ----------------------------------------------------------
        line()
        printHead("Section 1.8 - Detect Mounted Critical Paths")
        MOUNTS = ["/home", "/tmp", "/var", "/var/log", "/var/log/audit", "/var/tmp", "/dev/shm"]
        for mnt in MOUNTS:
            if run(f"mount | grep -q 'on {mnt}'").returncode == 0:
                logger.success(f"{mnt} is on a dedicated partition", True)
            else:
                logger.warning(f"{mnt} is NOT on a dedicated partition", True)
        line()
        getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
    except Exception as e:
        logger.error(f"An error occurred: {e}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
