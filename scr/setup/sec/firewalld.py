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
        # ----------------------------------------------------------
        # Section 4 - Install & Configure FirewallD
        # ----------------------------------------------------------
        line()
        printHead("Section 4 - Install & Configure FirewallD")
        run("apt install -y firewalld")
        run("systemctl enable firewalld")
        run("systemctl start firewalld")
        ports = getList(BASEDIR / "scr/setup/cfg/app-firewalld.conf")
        for port in ports:
            if port[0].isdigit():
                command = f"firewall-cmd --permanent --zone=public --add-port={port}/tcp"
            else:
                command = f"firewall-cmd --permanent --zone=public --add-service={port}"
            run(command)
        run("firewall-cmd --reload")
        line()
        getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
    except Exception as e:
        outlog.logError(f"An error occurred: {e}")
        raise e
