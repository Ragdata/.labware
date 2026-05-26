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
        run("echo 'kernel.randomize_va_space = 2' > /etc/sysctl.d/60-aslr.conf")
        run("echo 'kernel.yama.ptrace_scopr = 1' > /etc/sysctl.d/60-yama.conf")
        run("sysctl --system")
    except Exception as e:
        reason = str(e)
        outlog.logError(f"Failed to Harden Kernel: {reason}")
        raise e
