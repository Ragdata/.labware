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
        run("echo '* hard core 0' >> /etc/security/limits.conf")
        run("echo 'fs.suid_dumpable = 0' > /etc/sysctl.d/60-coredump.conf")
        run("sysctl -p /etc/sysctl.d/60-coredump.conf")
    except Exception as e:
        reason = str(e)
        outlog.logError(f"Failed to Harden Kernel: {reason}")
        raise e
