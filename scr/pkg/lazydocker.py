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
from labware.output import outlog
from labware.filesys import run

#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
if __name__ == "__main__":
    try:
        cmd = "curl https://raw.githubusercontent.com/jesseduffield/lazydocker/master/scripts/install_update_linux.sh | bash"
        logger.success("Successfully installed LazyDocker", True) if run(cmd).returncode == 0 else logger.warning("LazyDocker not installed", True)
    except Exception as e:
        reason = str(e)
        logger.error(f"Failed to install LazyDocker: {reason}", True)
        raise
