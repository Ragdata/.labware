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

from labware.filesys import *

from scr.setup.sec import banner

#-------------------------------------------------------------------
# VARIABLES
#-------------------------------------------------------------------
BASEDIR  = Path(config.get("paths", "base"))
SETUPDIR = BASEDIR / "scr/setup"
HOSTNAME = socket.getfqdn()
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        clear()
        banner.execute()
        rule(f"[{yellow}]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - POSTFIX MODULE [/{yellow}]", style=yellow, align="left")
        # ----------------------------------------------------------
        # EXTRAS - Install Postfix
        # ----------------------------------------------------------
        pkgs = ["postfix", "mailutils"]
        installAPT(pkgs)
        run("postconf -e disable_vrfy_command=yes")
        run(f"postconf -e smtpd_banner=\"{HOSTNAME} ESMTP\"")
        run("postconf -e smtpd_client_restrictions=permit_mynetworks,reject_unauth_destination")
        run("postconf -e inet_interfaces=loopback-only")
        run("systemctl restart postfix.service")
        line()
        getData(f"[{yellow}]MODULE COMPLETE :: Press [ENTER] to continue ...[/{yellow}] ")
    except Exception as e:
        reason = str(e)
        logger.error(f"Failed to install Postfix: {reason}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
