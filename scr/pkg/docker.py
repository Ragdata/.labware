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
        cmd = "curl -fsSL https://get.docker.com | sh"
        # cmd = "curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh"
        logger.success("Docker installed successfully", True) if run(cmd).returncode == 0 else logger.error("Docker not installed", True, False, 1)
        # Start and enable Docker service
        run("systemctl enable docker")
        printDot("Successfully started Docker") if run("systemctl start docker").returncode == 0 else logger.error("Docker not started", True, False, 1)
        printWhite("Hardening Docker Security")
        copyFiles(Path("../setup/etc/docker/daemon.json"), Path("/etc/docker/daemon.json"))
        copyFiles(Path("../setup/etc/security/limits.d/docker.conf"), Path("/etc/security/limits.d/docker.conf"))
        printDot("Docker daemon config copied")
        run("systemctl restart docker")
    except Exception as e:
        reason = str(e)
        logger.error(f"Failed to install Docker: {reason}", True)
        raise
