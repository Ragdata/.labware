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
from labware.filesys import *

#-------------------------------------------------------------------
# VARIABLES
#-------------------------------------------------------------------
BASEDIR  = Path(config.get("paths", "base"))
SETUPDIR = BASEDIR / "scr/setup"
#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        # ----------------------------------------------------------
        # EXTRAS - Remove SUID Bits
        # ----------------------------------------------------------
        line()
        printWhite("Remove SUID Bits")
        filename = SETUPDIR / "cfg/suid-list.cfg"
        if not filename.exists():
            raise FileNotFoundError(f"{filename} not found")
        ids = getList(filename)
        for i in ids:
            file = run(f"command -v {i}", capture=True).stdout.strip()
            if os.access(file, os.X_OK):
                run(f"chmod -s {file}")
                oc = run(f"stat -c \"%A\" {file} | sed 's/s/x/g'", capture=True).stdout.strip()
                ug = run(f"stat -c \"%U %G\" {file}", capture=True).stdout.strip()
                run(f"dpkg-statoverride --remove {file} 2> /dev/null")
                run(f"dpkg-statoverride --add \"{ug}\" \"{oc}\" \"{file}\" 2> /dev/null")
        shells = run(f"grep -v '^#' /etc/shells", capture=True).stdout.strip()
        for shell in shells:
            if shell.exists():
                run(f"chmod -s {shell}")
        line()
        getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
    except Exception as e:
        reason = str(e)
        logger.error(f"Failed to Harden SUID: {reason}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
