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

from labware.logger import *
from datetime import datetime

#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        # ----------------------------------------------------------
        # SHOW LABWARE BANNER
        # ----------------------------------------------------------
        year = datetime.now().year
        with open(BASEDIR / "sys/assets/ascii/labware.txt", "r") as f:
            printYellow(f.read(), lt=True)
            printYellow(f"Copyright © 2025-{year} - Redeyed Technologies (MIT Licensed)")

    except Exception as e:
        logger.error(f"An error occurred: {e}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
