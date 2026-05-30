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
        cmd = "curl -o webmin-setup-repo.sh https://raw.githubusercontent.com/webmin/webmin/master/webmin-setup-repo.sh | sh"
        logger.success("Successfully installed Webmin", True) if run(cmd).returncode == 0 else logger.warning("Webmin not installed", True)
    except Exception as e:
        reason = str(e)
        logger.error(f"Failed to install Webmin: {reason}", True)
        raise
