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

from mod.utils import *

#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
if __name__ == "__main__":
    try:
        cmd = "curl -fsSL https://software.virtualmin.com/gpl/scripts/virtualmin-install.sh -- --bundle LEMP | sh"
        outlog.logSuccess("Successfully installed Virtualmin") if run(cmd).returncode == 0 else outlog.logWarning("Virtualmin not installed")
    except Exception as e:
        reason = str(e)
        outlog.logError(f"Failed to install Virtualmin: {reason}")
        raise e
