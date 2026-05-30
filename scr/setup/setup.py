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

from pathlib import Path

BASEDIR = Path(__file__).parents[2]

sys.path.append(str(BASEDIR))
sys.path.append(".")

from labware.config import *

config: Config = Config(config_file=BASEDIR / "scr" / "lab" / "cfg" / ".labware.cfg")

from labware.logger import *

logger: Logger = get_logger("setup")

from labware.filesys import *

import sec.users as users, sec.tools as tools, sec.remfiles as remfiles, sec.boot as boot, sec.apparmor as apparmor, sec.core as core, sec.apt as apt
import sec.banners as banners, sec.mounts as mounts, sec.timesyncd as timesyncd, sec.cron as cron, sec.network as network, sec.firewalld as firewalld
import sec.sshd as sshd, sec.sudo as sudo, sec.account as account, sec.auditd as auditd, sec.rsyslog as rsyslog, sec.journald as journald, sec.acct as acct
import sec.password as password, sec.sysstat as sysstat, sec.psad as psad, sec.usbguard as usbguard, sec.rkhunter as rkhunter, sec.aide as aide, sec.suid as suid
import sec.compilers as compilers

#sec.logrotate as logrotate, sec.fail2ban as fail2ban, sec.unattended as unattended, sec.appsec as appsec, sec.misc as misc


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
        users.execute()
        tools.execute()
        run("clear")
        # ----------------------------------------------------------
        # SERVER HARDENING
        # ----------------------------------------------------------
        rule(f"[yellow]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING [/yellow]", style="yellow", align="left")
        remfiles.execute()
        boot.execute()
        apparmor.execute()
        core.execute()
        apt.execute()
        banners.execute()
        mounts.execute()
        timesyncd.execute()
        cron.execute()
        network.execute()
        firewalld.execute()
        sshd.execute()
        sudo.execute()
        account.execute()
        auditd.execute()
        rsyslog.execute()
        journald.execute()
        acct.execute()
        password.execute()
        sysstat.execute()
        psad.execute()
        usbguard.execute()
        rkhunter.execute()
        aide.execute()
        suid.execute()
        compilers.execute()
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
