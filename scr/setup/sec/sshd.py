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
SETUPDIR = Path(config.get("paths", "setup"))
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        clear()
        banner.execute()
        rule(f"[{yellow}]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - SSHD MODULE [/{yellow}]", style=yellow, align="left")
        global CHECKED
        if not CHECKED:
            line()
            CHECKED = checkRequired()
            config.set("setup", "checked", str(CHECKED))
        # ----------------------------------------------------------
        # Section 5.1 - SSH Hardening
        # ----------------------------------------------------------
        logger.info(f"Executing {__file__}")
        line()
        printHead("Section 5.1 - SSH Hardening")
        line()
        template = SETUPDIR / "etc/ssh/sshd_config.jinja"
        filedest = Path("/etc/ssh/sshd_config")
        labusers = getData(f"[{cyan}]Restrict SSH logins to the following users[/{cyan}] (ENTER for none): ")
        line()
        address  = getData(f"[{cyan}]Internal IP granted root access[/{cyan}] (ENTER for none): ")
        line()
        data = {"labusers": labusers, "internal_address": address}
        if not writeTemplate(template, filedest, data, 0o600, "root", "root"):
            logger.error(f"Could not write template to {filedest}", True, False, 1)
        template = SETUPDIR / "etc/security/access.conf.jinja"
        filedest = Path("/etc/security/access.conf")
        if not writeTemplate(template, filedest, data, 0o644, "root", "root"):
            logger.error(f"Could not write template to {filedest}", True, False, 1)
        line()
        run("systemctl daemon-reload")
        # run("systemctl enable ssh")
        run("systemctl restart sshd")
        run("systemctl mask debug-shell.service")
        run("systemctl stop debug-shell.service")
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
