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
        outlog.logSuccess("Successfully installed LazyDocker") if run(cmd).returncode == 0 else outlog.logWarning("LazyDocker not installed")
    except Exception as e:
        reason = str(e)
        outlog.logError(f"Failed to install LazyDocker: {reason}")
        raise e
