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

sys.path.append(".")

import banner

from labware.filesys import *

#-------------------------------------------------------------------
# VARIABLES
#-------------------------------------------------------------------
CHECKED: bool = config.getboolean("setup", "checked", fallback=False)
SETUPDIR = Path(config.get("paths", "setup"))
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        clear()
        banner.execute()
        rule(f"[{yellow}]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - NETWORK MODULE [/{yellow}]", style=yellow, align="left")
        global CHECKED
        if not CHECKED:
            CHECKED = checkRequired()
            config.set("setup", "checked", str(CHECKED))
        # ----------------------------------------------------------
        # Section 3 - Network Stack Hardening
        # ----------------------------------------------------------
        logger.info(f"Executing {__file__}")
        line()
        printHead("Section 3 - Network Stack Hardening")
        line()
        files = ["/etc/sysctl.d/60-ipv6.conf", "/etc/sysctl.d/60-net.conf", "/etc/modprobe.d/disable.conf", "/etc/systemd/logind.conf", "/etc/hosts.allow", "/etc/hosts.deny"]
        copyRepoFiles(SETUPDIR, files, True)
        run(f"sysctl -p /etc/sysctl.d/60-ipv6.conf")
        run(f"sysctl -p /etc/sysctl.d/60-net.conf")
        run("systemctl restart systemd-sysctl")
        modules = ["dccp", "tipc", "rds", "sctp"]
        for mod in modules:
            run(f"modprobe -r {mod} 2>/dev/null")
        line()
        getData(f"[{yellow}]MODULE COMPLETE :: Press [ENTER] to continue ...[/{yellow}] ")
    except Exception as e:
        logger.error(f"An error occurred: {e}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
