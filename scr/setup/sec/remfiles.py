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
        # Section 1.1 - Remove Unnecessary Filesystems
        # ----------------------------------------------------------
        line()
        printHead("Section 1.1 - Remove Unnecessary Filesystems")
        filesys = BASEDIR / "src/setup/cfg/apt-filesys.cfg"
        if not filesys.exists():
            raise FileNotFoundError(f"File not found: '{filesys}'")
        files = getList(filesys)
        removeAPT(files)
        run("systemctl mask autofs")
        line()
        getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
        # ----------------------------------------------------------
        # Section 2.1 - Remove Unused Services
        # ----------------------------------------------------------
        line()
        printHead("Section 2.1 - Remove Unused Services")
        remove = BASEDIR / "src/setup/cfg/apt-remove.cfg"
        if not remove.exists():
            raise FileNotFoundError(f"File not found: '{remove}'")
        pkgs = getList(remove)
        removeAPT(pkgs)
        line()
        getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
    except Exception as e:
        outlog.logError(f"An error occurred: {e}")
        raise e
