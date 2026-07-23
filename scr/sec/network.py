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
import sys, socket

sys.path.append(".")

import banner

from labware.filesys import *

#-------------------------------------------------------------------
# VARIABLES
#-------------------------------------------------------------------
CHECKED: bool = config.getbool("setup", "checked", fallback=False)
SETUPDIR = Path(config.get("paths", "setup"))
#-------------------------------------------------------------------
# FUNCTIONS
#-------------------------------------------------------------------
def setHostname(name: str) -> None:
    try:
        if run(f"hostnamectl set-hostname {name}", True).returncode == 0:
            logger.info(f"Hostname set to {name}", True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to set hostname: {e}", True, False, 1)
    except FileNotFoundError:
        logger.error("The 'hostnamectl' command was not found.", True, False, 1)

def updateHostfiles(name: str) -> None:
    run(f"hostname {name}", True)
    # Write to /etc/hostname
    with open("/etc/hostname", "w") as f:
        if f.write(f"{name}\n") == len(name) + 1:
            logger.info(f"Updated /etc/hostname", True)
        else:
            logger.error(f"Failed to update /etc/hostname", True, False, 1)
    # Update /etc/hosts
    oldName = socket.gethostname()
    with open("/etc/hosts", "r") as f:
        content = f.read()
    updated = content.replace(oldName, name)
    with open("/etc/hosts", "w") as f:
        if f.write(updated) == len(updated):
            logger.info(f"Updated /etc/hosts", True)
        else:
            logger.error(f"Failed to update /etc/hosts", True, False, 1)

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
            line()
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
        line()
        run(f"sysctl -p /etc/sysctl.d/60-ipv6.conf")
        run(f"sysctl -p /etc/sysctl.d/60-net.conf")
        run("systemctl restart systemd-sysctl")
        modules = ["dccp", "tipc", "rds", "sctp"]
        for mod in modules:
            run(f"modprobe -r {mod} 2>/dev/null")
        line()
        printHead("Hostname & Hostfiles")
        line()
        oldName = socket.gethostname()
        printDot(f"Current Hostname: {oldName}")
        line()
        hostname = getData(f"[{cyan}]Enter new hostname[/{cyan}] (ENTER to bypass): ")
        if hostname:
            line()
            setHostname(hostname)
            line()
            updateHostfiles(hostname)
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
