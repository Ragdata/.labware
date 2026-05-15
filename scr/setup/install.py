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

sys.path.append('modules')

from modules.utils import *


#-------------------------------------------------------------------
# VARIABLES
#-------------------------------------------------------------------
BASEDIR = Path(config.get("paths", "base"))

#-------------------------------------------------------------------
# FUNCTIONS
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
if __name__ == "__main__":
    try:
        checkRoot()
        checkPython()
        checkUbuntu()
        run("clear")
        # Gather Information
        while True:
            data = getData("[cyan]Enter list of sudo users to setup (space delimited): [/cyan]")
            if data != "":
                users = data.split(" ")
                for user in users:
                    try:
                        pwd.getpwnam(user)
                    except KeyError:
                        errorExit(f"User '{user}' does not exist")
            else:
                continue



    except Exception as e:
        raise e
