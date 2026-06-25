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
import importlib.util

from pathlib import Path

path = Path(__file__).parents[2].resolve() / "lab/genPasswordList.py"
name = "genPasswordList"

spec = importlib.util.spec_from_file_location(name, path)
pw = importlib.util.module_from_spec(spec)

sys.modules[name] = pw
spec.loader.exec_module(pw)

sys.path.append(".")

import banner

from labware.filesys import *

#-------------------------------------------------------------------
# VARIABLES
#-------------------------------------------------------------------
CHECKED: bool = config.getbool("setup", "checked", fallback=False)
SETUPDIR = Path(config.get("paths", "setup"))
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        clear()
        banner.execute()
        rule(f"[{yellow}]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - PASSWORD MODULE [/{yellow}]", style=yellow, align="left")
        global CHECKED
        if not CHECKED:
            line()
            CHECKED = checkRequired()
            config.set("setup", "checked", str(CHECKED))
        # ----------------------------------------------------------
        # Section 5.4 - Password Policy
        # ----------------------------------------------------------
        logger.info(f"Executing {__file__}")
        line()
        printHead("Section 5.4 - Password Policy")
        line()
        files = [
            "/etc/login.defs", "/etc/profile.d/timeout.sh", "/etc/bash.bashrc",
            "/etc/pam.d/common-password", "/etc/pam.d/common-account", "/etc/pam.d/common-auth", "/etc/pam.d/login", "/etc/pam.d/su",
            "/etc/security/pwquality.conf", "/etc/security/faillock.conf"
        ]
        copyRepoFiles(SETUPDIR, files, True)
        line()
        lockout = getData(f"[{cyan}]Do you want to lock the root account?[/{cyan}] (y/N) ").lower()
        if lockout == "y":
            run("passwd -l root")
        line()
        expire = getData(f"[{cyan}]Do you want to expire passwords every 30 days?[/{cyan}] (y/N) ").lower()
        if expire == "y":
            run("useradd -D -f 30")
        line()
        pw.execute()
        run(f"grep -v '^$' /usr/share/dict/passwords | strings > /usr/share/dict/passwords_text")
        run("update-cracklib")
        line()
        getData(f"[{cyan}]Press [ENTER] to continue ...[/{cyan}] ")
        # ----------------------------------------------------------
        # Section 6.5 - Secure Password Files
        # ----------------------------------------------------------
        line()
        printHead("Section 6.5 - Secure Password Files")
        data = {
            "/etc/passwd":                  [0o644, "root", "root"],
            "/etc/shadow":                  [0o000, "root", "shadow"],
            "/etc/group":                   [0o644, "root", "root"],
            "/etc/gshadow":                 [0o000, "root", "shadow"],
            "/etc/passwd-":                 [0o600, "root", "root"],
            "/etc/shadow-":                 [0o600, "root", "shadow"],
            "/etc/group-":                  [0o600, "root", "root"],
            "/etc/gshadow-":                [0o600, "root", "shadow"],
            "/etc/profile.d/timeout.sh":    [0o755, "root", "root"]
        }
        perms(data)
        line()
        logger.success("Password files secured")
        line()
        getData(f"[{yellow}]MODULE COMPLETE :: Press [ENTER] to continue ...[/{yellow}] ")
    except Exception as e:
        logger.error(f"An error occurred: {e}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
