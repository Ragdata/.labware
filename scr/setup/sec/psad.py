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

from labware.filesys import *

from scr.setup.sec import banner

#-------------------------------------------------------------------
# VARIABLES
#-------------------------------------------------------------------
BASEDIR  = Path(config.get("paths", "base"))
SETUPDIR = BASEDIR / "scr/setup"
SERVERIP = getIP()
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        clear()
        banner.execute()
        rule(f"[yellow]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - PSAD MODULE [/yellow]", style="yellow", align="left")
        # ----------------------------------------------------------
        # Install 'psad'
        # ----------------------------------------------------------
        line()
        printWhite("Install 'psad'")
        pkgs = ["psad"]
        installAPT(pkgs)
        filepath = "/etc/psad/auto_dl"
        template = SETUPDIR / filepath
        filedest = Path(filepath)
        data = {"server_ip": SERVERIP}
        if not writeTemplate(template, filedest, data):
            logger.error(f"Could not write template to {filedest}", True, 1)
        while True:
            email_address = getData("[cyan]Enter admin email address[/cyan] (required): ")
            if email_address:
                break
        filepath = "/etc/psad/psad.conf"
        template = SETUPDIR / filepath
        filedest = Path(filepath)
        data = {"email_address": email_address}
        if not writeTemplate(template, filedest, data):
            logger.error(f"Could not write template to {filedest}", True, 1)
        run("iptables -A INPUT -j LOG")
        run("iptables -A FORWARD -j LOG")
        run("netfilter-persistent save")
        run("systemctl enable psad.service")
        run("systemctl restart psad")
        run("psad --sig-update")
        run("psad -H")
        run("psad --fw-analyze")
        line()
        getData("[yellow]MODULE COMPLETE :: Press [ENTER] to continue ...[/yellow] ")
    except Exception as e:
        reason = str(e)
        logger.error(f"Failed to install 'psad': {reason}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
