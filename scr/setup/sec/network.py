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
# VARIABLES
#-------------------------------------------------------------------
BASEDIR  = Path(config.get("paths", "base"))
SETUPDIR = BASEDIR / "scr/setup"
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        # ----------------------------------------------------------
        # Section 3 - Network Stack Hardening
        # ----------------------------------------------------------
        line()
        printHead("Section 3 - Network Stack Hardening")
        files = ["/etc/sysctl.d/60-ipv6.conf", "/etc/sysctl.d/60-net.conf", "/etc/modprobe.d/disable.conf", "/etc/systemd/logind.conf", "/etc/hosts.allow", "/etc/hosts.deny"]
        copyRepoFiles(SETUPDIR, files, True)
        run(f"sysctl -p /etc/sysctl.d/60-ipv6.conf")
        run(f"sysctl -p /etc/sysctl.d/60-net.conf")
        run("systemctl restart systemd-sysctl")
        modules = ["dccp", "tipc", "rds", "sctp"]
        for mod in modules:
            run(f"modprobe -r {mod} 2>/dev/null")
        line()
        getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
    except Exception as e:
        logger.error(f"An error occurred: {e}", True)
        raise
