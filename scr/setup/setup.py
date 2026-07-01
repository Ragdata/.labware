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

from labware.filesys import *

import sec.users as users, sec.tools as tools, sec.remfiles as remfiles, sec.boot as boot, sec.apparmor as apparmor, sec.core as core, sec.apt as apt
import sec.motd as motd, sec.mounts as mounts, sec.timesyncd as timesyncd, sec.cron as cron, sec.network as network, sec.firewalld as firewalld
import sec.sshd as sshd, sec.sudo as sudo, sec.account as account, sec.auditd as auditd, sec.rsyslog as rsyslog, sec.journald as journald, sec.acct as acct
import sec.password as password, sec.sysstat as sysstat, sec.psad as psad, sec.usbguard as usbguard, sec.rkhunter as rkhunter, sec.aide as aide, sec.suid as suid
import sec.compilers as compilers, sec.banner as banner, sec.package as package

#sec.postfix as postfix, sec.logrotate as logrotate, sec.fail2ban as fail2ban, sec.unattended as unattended, sec.appsec as appsec, sec.misc as misc

config: Config = get_config()
logger: Logger = get_logger("setup", logging.DEBUG)

#-------------------------------------------------------------------
# VARIABLES
#-------------------------------------------------------------------
CHECKED: bool = config.getbool("setup", "checked", fallback=False)
#-------------------------------------------------------------------
# LOCAL FUNCTIONS
#-------------------------------------------------------------------
# LXC = 1 if isLXC() else 0
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute() -> None:
    try:
        global CHECKED
        if not CHECKED:
            CHECKED = checkRequired()
            config.set("setup", "checked", str(CHECKED))
        # ----------------------------------------------------------
        # SETUP USERS & TOOLS
        # ----------------------------------------------------------
        users.execute()
        tools.execute()
        # ----------------------------------------------------------
        # SERVER HARDENING
        # ----------------------------------------------------------
        remfiles.execute()
        if Path("/boot/grub/grub.cfg").exists():
            boot.execute()
        if run("aa-status").returncode != 1:
            apparmor.execute()
        core.execute()
        apt.execute()
        motd.execute()
        mounts.execute()
        timesyncd.execute()
        cron.execute()
        network.execute()
        if not isWSL2():
            firewalld.execute()
        sshd.execute()
        sudo.execute()
        account.execute()
        if not isWSL2():
            auditd.execute()
        rsyslog.execute()
        journald.execute()
        acct.execute()
        password.execute()
        sysstat.execute()
        suid.execute()
        compilers.execute()
        psad.execute()
        if Path("/sys/bus/usb/devices").exists():
            usbguard.execute()
        rkhunter.execute()
        # postfix.execute()
        aide.execute()
        # ----------------------------------------------------------
        # INSTALL PACKAGES
        # ----------------------------------------------------------
        package.execute()
        # ----------------------------------------------------------
        # CLEANUP
        # ----------------------------------------------------------
        clear()
        banner.execute()
        line()
        rule(f"[{yellow}]── CLEANUP[/{yellow}]", style=yellow, align="left")
        printHead("CLEANUP")
        run("apt -qq -y clean && apt -qq -y autoremove")
        line()
        getData(f"[{cyan}]Press [ENTER] to continue ...[/{cyan}] ")
        # ----------------------------------------------------------
        # REPORT
        # ----------------------------------------------------------
        clear()
        banner.execute()
        line()
        rule(f"[{yellow}]── REPORT[/{yellow}]", style=yellow, align="left")
        run("systemd-delta --no-pager")
        # ----------------------------------------------------------
        # REBOOT
        # ----------------------------------------------------------
        line()
        getData(f"[{yellow}]Press [ENTER] to reboot ...[/{yellow}] ")
        run("systemctl reboot")
    except Exception as e:
        logger.error(f"An error occurred: {e}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
