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
import runpy, sys

from pathlib import Path

BASEDIR = Path(__file__).parents[2]

sys.path.append(str(BASEDIR))

from labware.config import *

config: Config = Config(config_file=BASEDIR / "scr" / "lab" / "cfg" / ".labware.cfg")

from labware.logger import *

logger: Logger = get_logger("setup")

from labware.filesys import *

#-------------------------------------------------------------------
# LOCAL FUNCTIONS
#-------------------------------------------------------------------
# LXC = 1 if isLXC() else 0
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
if __name__ == "__main__":
    try:
        checkRoot()
        checkPython()
        checkUbuntu()
        run("clear")
        # ----------------------------------------------------------
        # SETUP USERS & TOOLS
        # ----------------------------------------------------------
        runScript("sec/users.py")
        runScript("sec/tools.py")
        run("clear")
        # ----------------------------------------------------------
        # SERVER HARDENING
        # ----------------------------------------------------------
        rule(f"[yellow]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING [/yellow]", style="yellow", align="left")
        runScript("sec/remfiles.py")
        runScript("sec/boot.py")
        runScript("sec/apparmor.py")
        runScript("sec/core.py")
        runScript("sec/apt.py")
        runScript("sec/banners.py")
        runScript("sec/mounts.py")
        runScript("sec/timesyncd.py")
        runScript("sec/cron.py")
        runScript("sec/network.py")
        runScript("sec/firewalld.py")
        runScript("sec/sshd.py")
        runScript("sec/sudo.py")
        runScript("sec/account.py")
        runScript("sec/auditd.py")
        runScript("sec/rsyslog.py")
        runScript("sec/journald.py")
        runScript("sec/acct.py")
        runScript("sec/password.py")
        runScript("sec/sysstat.py")
        runScript("sec/psad.py")
        runScript("sec/usbguard.py")
        runScript("sec/rkhunter.py")
        runScript("sec/aide.py")
        runScript("sec/suid.py")
        runScript("sec/compilers.py")
        # ----------------------------------------------------------
        # CLEANUP
        # ----------------------------------------------------------
        line()
        printHead("CLEANUP")
        run("apt -qq -y clean && apt -qq -y autoremove")
        line()
        getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
        # ----------------------------------------------------------
        # REPORT
        # ----------------------------------------------------------
        run("clear")
        rule(f"[yellow]── REPORT[/yellow]", style="yellow", align="left")
        run("systemd-delta --no-pager")
        # ----------------------------------------------------------
        # REBOOT
        # ----------------------------------------------------------
        line()
        getData("[yellow]Press [ENTER] to reboot ...[/yellow] ")
        run("systemctl reboot")
    except Exception as e:
        logger.error(f"An error occurred: {e}", True)
        raise
