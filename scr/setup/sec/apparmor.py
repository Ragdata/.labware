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
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        clear()
        banner.execute()
        rule(f"[{yellow}]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - APPARMOR MODULE [/{yellow}]", style=yellow, align="left")
        global CHECKED
        if not CHECKED:
            CHECKED = checkRequired()
            config.set("setup", "checked", str(CHECKED))
        # ----------------------------------------------------------
        # Section 1.3 - Enable AppArmor & Secure Kernel
        # ----------------------------------------------------------
        logger.info(f"Executing {__file__}")
        line()
        printHead("Section 1.3 - Enable AppArmor & Secure Kernel")
        line()
        pkgs = ["apparmor", "apparmor-utils", "apparmor-profiles", "apparmor-profiles-extra", "libpam-apparmor"]
        installAPT(pkgs)
        with os.scandir("/etc/apparmor.d") as entries:
            for entry in entries:
                if entry.is_file() and entry.name.startswith("profile"):
                    run(f"aa-complain {entry.name} >/dev/null 2>&1")
        if run("grep 'session.*pam_apparmor.so order=user,group,default' /etc/pam.d/*").returncode != 0:
            run("echo 'session optional pam_apparmor.so order=user,group,default' > /etc/pam.d/apparmor")
        run("echo 'kernel.randomize_va_space = 2' > /etc/sysctl.d/60-aslr.conf")
        run("echo 'kernel.yama.ptrace_scopr = 1' > /etc/sysctl.d/60-yama.conf")
        run("sysctl --system")
        line()
        getData(f"[{yellow}]MODULE COMPLETE :: Press [ENTER] to continue ...[/{yellow}] ")
    except Exception as e:
        reason = str(e)
        logger.error(f"Failed to install Apparmor: {reason}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
