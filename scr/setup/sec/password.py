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

path = Path(__file__).parents[3] / "lab"

sys.path.append(str(path))
sys.path.append(".")

import banner

import lab.genPasswordList as pw

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
        files = ["/etc/login.defs", "/etc/profile.d/timeout.sh", "/etc/bash.bashrc"]
        copyRepoFiles(SETUPDIR, files, True)
        line()
        pw.execute()
        run("useradd -D -f 30")
        run("chmod +x /etc/profile.d/timeout.sh")
        run("passwd -l root")
        run(f"grep -v '^$' /usr/share/dict/passwords | strings > /usr/share/dict/passwords_text")
        run("update-cracklib")

        # Set default umask
        # @TODO - Refine
        filepath = Path("/etc/init.d/rc")
        if filepath.is_file():
            run(f"sed -i 's/umask 022/umask 077/g' {filepath}")
        if run("grep -q -i 'umask' '/etc/profile' 2> /dev/null").returncode != 0:
            run("echo 'umask 077' >> /etc/profile")
        if run("grep -q -i 'umask' '/etc/bash.bashrc' 2> /dev/null").returncode != 0:
            run("echo 'umask 077' >> /etc/bash.bashrc")
        if run("grep -q -i 'TMOUT' '/etc/profile.d/*' 2> /dev/null").returncode != 0:
            run("echo -e 'TMOUT=600\nreadonly TMOUT\nexport TMOUT' > /etc/profile.d/autologout.sh")
            run("chmod +x /etc/profile.d/autologout.sh")

        # # Set default root umask in .profile
        # dotfile = Path.home() / ".bash_profile"
        # if not dotfile.exists():
        #     dotfile = Path.home() / ".profile"
        # if not dotfile.exists():
        #     raise FileNotFoundError(f"File not found '{dotfile}'")
        # if not findFileString(dotfile, "umask 027"):
        #     with open(dotfile, "a") as f:
        #         f.write("umask 027")
        # # Set default root umask in .bashrc
        # dotfile = Path.home() / ".bashrc"
        # if not dotfile.exists():
        #     raise FileNotFoundError(f"File not found '{dotfile}'")
        # if not findFileString(dotfile, "umask 027"):
        #     with open(dotfile, "a") as f:
        #         f.write("umask 027")
        line()
        getData(f"[{cyan}]Press [ENTER] to continue ...[/{cyan}] ")
        # ----------------------------------------------------------
        # Section 6.5 - Secure Password Files
        # ----------------------------------------------------------
        line()
        printHead("Section 6.5 - Secure Password Files")
        data = {
            "/etc/passwd":   [0o644, "root", "root"],
            "/etc/shadow":   [0o000, "root", "shadow"],
            "/etc/group":    [0o644, "root", "root"],
            "/etc/gshadow":  [0o000, "root", "shadow"],
            "/etc/passwd-":  [0o600, "root", "root"],
            "/etc/shadow-":  [0o600, "root", "shadow"],
            "/etc/group-":   [0o600, "root", "root"],
            "/etc/gshadow-": [0o600, "root", "shadow"]
        }
        perms(data)
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
