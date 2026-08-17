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
SETUPDIR = Path(config.get("paths", "sec"))
CHECKED: bool = config.getbool("setup", "checked", fallback=False)
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        clear()
        banner.execute()
        rule(f"[{yellow}]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - EXTRAS [/{yellow}]", style=yellow, align="left")
        global CHECKED
        if not CHECKED:
            CHECKED = checkRequired()
            config.set("setup", "checked", str(CHECKED))
        # ----------------------------------------------------------
        #
        # ----------------------------------------------------------
        logger.info(f"Executing {__file__}")
        line()
        printHead("Install Logwatch")
        line()
        pkgs = ["msmtp", "msmtp-mta", "logwatch"]
        installAPT(pkgs)
        line()
        tmpl = SETUPDIR / "etc/logwatch/conf/logwatch.conf.jinja"
        dest = Path("/etc/logwatch/conf/logwatch.conf")
        data = {"home": str(Path.home())}
        if not writeTemplate(tmpl, dest, data, bkp=True):
            logger.error(f"Could not write template to {dest}", True, False, 1)
        files = ["/etc/systemd/system/logwatch.service", "/etc/systemd/system/logwatch.timer"]
        copyRepoFiles(SETUPDIR, files, True)
        run("systemctl daemon-reload")
        run("systemctl enable logwatch.service")
        run("systemctl enable logwatch.timer")
        run("systemctl start logwatch.service")
        run("systemctl start logwatch.timer")
        line()
        getData(f"[{cyan}]Press [ENTER] to continue ...[/{cyan}] ")
    except Exception as e:
        logger.error(f"An error occurred: {e}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
