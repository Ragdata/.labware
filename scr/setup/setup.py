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
import runpy

from labware.logger import *

logger = get_logger("setup")

from labware.filesys import *

#-------------------------------------------------------------------
# LOCAL FUNCTIONS
#-------------------------------------------------------------------
# LXC = 1 if isLXC() else 0
def setPaths() -> None:
    REPOBASE = Path(__file__).resolve().parent.parent.parent
    config.add_section("paths")
    config.set("paths", "base",      str(REPOBASE))
    config.set("paths", "pkg",       str(REPOBASE / "pkg"))
    config.set("paths", "scr",       str(REPOBASE / "scr"))
    config.set("paths", "svc",       str(REPOBASE / "svc"))
    config.set("paths", "sys",       str(REPOBASE / "sys"))
    config.set("paths", "dot",       str(REPOBASE / "sys" / "dots"))
    config.set("paths", "lib",       str(REPOBASE / "sys" / "lib"))
    config.set("paths", "admin",     str(REPOBASE / "scr" / "admin"))
    config.set("paths", "scripts",   str(REPOBASE / "scr" / "pkg"))
    config.set("paths", "setup",     str(REPOBASE / "scr" / "setup"))
    config.set("paths", "templates", str(REPOBASE / "scr" / "setup" / "etc"))
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
if __name__ == "__main__":
    try:
        checkRoot()
        checkPython()
        checkUbuntu()
        setPaths()
        run("clear")
        # ----------------------------------------------------------
        # SETUP USERS & TOOLS
        # ----------------------------------------------------------
        runpy.run_path("sec/users.py")
        runpy.run_path("sec/tools.py")
        run("clear")
        # ----------------------------------------------------------
        # SERVER HARDENING
        # ----------------------------------------------------------
        rule(f"[yellow]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING [/yellow]")
        runpy.run_path("sec/remfiles.py")
        runpy.run_path("sec/boot.py")
        runpy.run_path("sec/apparmor.py")
        runpy.run_path("sec/core.py")
        runpy.run_path("sec/apt.py")
        runpy.run_path("sec/banners.py")
        runpy.run_path("sec/mounts.py")
        runpy.run_path("sec/timesyncd.py")
        runpy.run_path("sec/cron.py")
        runpy.run_path("sec/network.py")
        runpy.run_path("sec/firewalld.py")
        runpy.run_path("sec/sshd.py")
        runpy.run_path("sec/sudo.py")
        runpy.run_path("sec/account.py")
        runpy.run_path("sec/auditd.py")
        runpy.run_path("sec/rsyslog.py")
        runpy.run_path("sec/journald.py")
        runpy.run_path("sec/acct.py")
        runpy.run_path("sec/password.py")
        runpy.run_path("sec/sysstat.py")
        runpy.run_path("sec/psad.py")
        runpy.run_path("sec/usbguard.py")
        runpy.run_path("sec/rkhunter.py")
        runpy.run_path("sec/aide.py")
        runpy.run_path("sec/suid.py")
        runpy.run_path("sec/compilers.py")
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
        rule(f"[yellow]── REPORT[/yellow]")
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
