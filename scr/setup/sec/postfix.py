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
import socket

from labware.filesys import *

#-------------------------------------------------------------------
# VARIABLES
#-------------------------------------------------------------------
BASEDIR  = Path(config.get("paths", "base"))
SETUPDIR = BASEDIR / "scr/setup"
HOSTNAME = socket.getfqdn()
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
if __name__ == "__main__":
    try:
        pkgs = ["postfix", "mailutils"]
        installAPT(pkgs)
        run("postconf -e disable_vrfy_command=yes")
        run(f"postconf -e smtpd_banner=\"{HOSTNAME} ESMTP\"")
        run("postconf -e smtpd_client_restrictions=permit_mynetworks,reject_unauth_destination")
        run("postconf -e inet_interfaces=loopback-only")
        run("systemctl restart postfix.service")
    except Exception as e:
        reason = str(e)
        logger.error(f"Failed to install Postfix: {reason}", True)
        raise
