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
        getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
    except Exception as e:
        logger.error(f"An error occurred: {e}", True)
        raise
