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
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        clear()
        banner.execute()
        rule(f"[yellow]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - SSHD MODULE [/yellow]", style="yellow", align="left")
        # ----------------------------------------------------------
        # Section 5.1 - SSH Hardening
        # ----------------------------------------------------------
        line()
        printHead("Section 5.1 - SSH Hardening")
        filepath = "/etc/ssh/sshd_config"
        template = SETUPDIR / filepath
        filedest = Path(filepath)
        labusers = getData("[cyan]Restrict SSH logins to the following users[/cyan] (ENTER for none): ")
        address  = getData("[cyan]Internal IP granted root access[/cyan] (ENTER for none): ")
        data = {"labusers": labusers, "internal_address": address}
        if not writeTemplate(template, filedest, data, 0o600, "root", "root"):
            logger.error(f"Could not write template to {filedest}", True, 1)
        filepath = "/etc/security/access.conf"
        template = SETUPDIR / filepath
        filedest = Path(filepath)
        if not writeTemplate(template, filedest, data):
            logger.error(f"Could not write template to {filedest}", True, 1)
        run("systemctl enable ssh")
        run("systemctl restart ssh")
        run("systemctl mask debug-shell.service")
        run("systemctl stop debug-shell.service")
        run("systemctl daemon-reload")
        line()
        getData("[yellow]MODULE COMPLETE :: Press [ENTER] to continue ...[/yellow] ")
    except Exception as e:
        logger.error(f"An error occurred: {e}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
