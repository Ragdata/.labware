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
CHECKED: bool = config.getbool("setup", "checked", fallback=False)
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        clear()
        banner.execute()
        rule(f"[{yellow}]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - FIREWALLD MODULE [/{yellow}]", style=yellow, align="left")
        global CHECKED
        if not CHECKED:
            line()
            CHECKED = checkRequired()
            config.set("setup", "checked", str(CHECKED))
        # ----------------------------------------------------------
        # Section 4 - Install & Configure FirewallD
        # ----------------------------------------------------------
        logger.info(f"Executing {__file__}")
        line()
        printHead("Section 4 - Install & Configure FirewallD")
        line()
        run("apt install -y firewalld python3-firewall", True)
        if isInstalled("ufw"):
            run("systemctl stop ufw")
            run("systemctl disable ufw")
        run("systemctl enable --now firewalld")
        ports = getList(BASEDIR / "setup/cfg/app-firewalld.cfg")
        for port in ports:
            if port[0].isdigit():
                command = f"firewall-cmd --permanent --zone=public --add-port={port}/tcp"
            else:
                command = f"firewall-cmd --permanent --zone=public --add-service={port}"
            run(command)
        run("firewall-cmd --reload")
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
