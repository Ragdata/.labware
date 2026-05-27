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

sys.path.append("../mod")

from mod.utils import *

#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
if __name__ == "__main__":
    try:
        pkgs = ["apparmor", "apparmor-utils", "apparmor-profiles", "apparmor-profiles-extra", "libpam-apparmor"]
        installAPT(pkgs)
        with os.scandir("/etc/apparmor.d") as entries:
            for entry in entries:
                if entry.is_file() and entry.name.startswith("profile"):
                    run(f"aa-complain {entry.name} >/dev/null 2>&1")
    except Exception as e:
        reason = str(e)
        outlog.logError(f"Failed to install Apparmor: {reason}")
        raise e
