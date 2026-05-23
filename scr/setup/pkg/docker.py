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
        cmd = "curl -fsSL https://get.docker.com | sh"
        # cmd = "curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh"
        outlog.logSuccess("Docker installed successfully") if run(cmd).returncode == 0 else outlog.logError("Docker not installed", 1)
        # Start and enable Docker service
        run("systemctl enable docker")
        printDot("Successfully started Docker") if run("systemctl start docker").returncode == 0 else outlog.logError("Docker not started", 1)
        printWhite("Hardening Docker Security")
        copyFiles(Path("../etc/docker/daemon.json"), Path("/etc/docker/daemon.json"))
        copyFiles(Path("../etc/security/limits.d/docker.conf"), Path("/etc/security/limits.d/docker.conf"))
        printDot("Docker daemon config copied")
        run("systemctl restart docker")
    except Exception as e:
        reason = str(e)
        outlog.logError(f"Failed to install Docker: {reason}")
        raise e
