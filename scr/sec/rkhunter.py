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
SETUPDIR = Path(config.get("paths", "sec"))
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        clear()
        banner.execute()
        rule(f"[{yellow}]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - RKHUNTER MODULE [/{yellow}]", style=yellow, align="left")
        global CHECKED
        if not CHECKED:
            line()
            CHECKED = checkRequired()
            config.set("setup", "checked", str(CHECKED))
        # ----------------------------------------------------------
        # EXTRAS - Install 'rkhunter'
        # ----------------------------------------------------------
        logger.info(f"Executing {__file__}")
        line()
        printWhite("Install Rootkit Hunter ('rkhunter')")
        line()
        pkgs = ["rkhunter"]
        installAPT(pkgs)
        files = ["/etc/systemd/system/rkhunter.service", "/etc/systemd/system/rkhunter.timer"]
        copyRepoFiles(SETUPDIR, files)
        line()
        while True:
            email = getData(f"[{cyan}]Enter email address for reports:[/{cyan}] ")
            if email:
                break
        line()
        tmpl = SETUPDIR / "etc/default/rkhunter.jinja"
        dest = Path("/etc/default/rkhunter")
        data = {"email_address": email}
        if not writeTemplate(tmpl, dest, data):
            logger.error(f"Could not write template to {dest}", True, False, 1)
        line()
        run("systemctl daemon-reload")
        run("systemctl enable rkhunter.timer")
        run("systemctl start rkhunter.timer")
        run("rkhunter --update")
        run("rkhunter --propupd")
        line()
        getData(f"[{yellow}]MODULE COMPLETE :: Press [ENTER] to continue ...[/{yellow}] ")
    except Exception as e:
        reason = str(e)
        logger.error(f"Failed to install 'rkhunter': {reason}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
