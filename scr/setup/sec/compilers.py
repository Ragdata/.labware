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
        # EXTRAS - Restrict Access to Compilers
        # ----------------------------------------------------------
        line()
        printWhite("Restrict Access to Compilers")
        compilers = run("dpkg-query -L $(dpkg -l | grep compil | awk '{print $2}')", capture=True).stdout.strip()
        for comp in compilers:
            if comp.is_file() and os.access(comp, os.X_OK):
                if not os.path.islink(comp):
                    chmod(comp, 0o750)
        ascomp = run("command -v as", capture=True).stdout.strip()
        if ascomp.is_file() and os.access(ascomp, os.X_OK):
            chmod(run("readlink -eq $(command -v as)", capture=True).stdout.strip(), 0o750)
        line()
        getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
    except Exception as e:
        reason = str(e)
        outlog.logError(f"Failed to Harden Limits: {reason}")
        raise e
