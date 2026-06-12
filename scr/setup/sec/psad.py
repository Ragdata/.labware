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
SERVERIP = getIP()
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        clear()
        banner.execute()
        rule(f"[{yellow}]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - PSAD MODULE [/{yellow}]", style=yellow, align="left")
        global CHECKED
        if not CHECKED:
            CHECKED = checkRequired()
            config.set("setup", "checked", str(CHECKED))
        # ----------------------------------------------------------
        # EXTRAS - Port Scan Attack Detector ('psad')
        # ----------------------------------------------------------
        logger.info(f"Executing {__file__}")
        line()
        printWhite("Install 'psad'")
        line()
        pkgs = ["psad"]
        installAPT(pkgs)
        template = SETUPDIR / "/etc/psad/auto_dl.jinja"
        filedest = Path("/etc/psad/auto_dl")
        data = {"server_ip": SERVERIP}
        if not writeTemplate(template, filedest, data):
            logger.error(f"Could not write template to {filedest}", True, False, 1)
        while True:
            email_address = getData(f"[{cyan}]Enter admin email address[/{cyan}] (required): ")
            if email_address:
                break
        filepath = "/etc/psad/psad.conf"
        template = SETUPDIR / filepath
        filedest = Path(filepath)
        data = {"email_address": email_address}
        if not writeTemplate(template, filedest, data):
            logger.error(f"Could not write template to {filedest}", True, False, 1)
        run("iptables -A INPUT -j LOG")
        run("iptables -A FORWARD -j LOG")
        run("netfilter-persistent save")
        run("systemctl enable psad.service")
        run("systemctl restart psad")
        run("psad --sig-update")
        run("psad -H")
        run("psad --fw-analyze")
        line()
        getData(f"[{yellow}]MODULE COMPLETE :: Press [ENTER] to continue ...[/{yellow}] ")
    except Exception as e:
        reason = str(e)
        logger.error(f"Failed to install 'psad': {reason}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
