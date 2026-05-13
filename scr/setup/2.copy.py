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

sys.path.append('.')

from utils import *

BASEDIR = Path(config.get("paths", "base"))
#-------------------------------------------------------------------
# FUNCTIONS
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
if __name__ == "__main__":
    try:
        checkRoot()
        checkPython()
        checkRoot()
        run("clear")
        printDot(f"{BASEDIR}")
    except Exception as e:
        outlog.logError(f"Problem encountered during file copy: {e}")
        raise e
