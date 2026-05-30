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
if __name__ == "__main__":
    try:
        cmd = "curl -fsSL https://software.virtualmin.com/gpl/scripts/virtualmin-install.sh -- --bundle LEMP | sh"
        logger.success("Successfully installed Virtualmin", True) if run(cmd).returncode == 0 else logger.warning("Virtualmin not installed", True)
    except Exception as e:
        reason = str(e)
        logger.error(f"Failed to install Virtualmin: {reason}", True)
        raise
