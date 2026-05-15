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
EXECUSR = pwd.getpwuid(os.geteuid()).pw_name
REALUSR = getpass.getuser()
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
        ############################################################
        # Gather Information
        ############################################################
        users = []
        while True:
            data = getData("[cyan]Enter list of sudo users to setup (space delimited): [/cyan]")
            if data != "":
                users = data.split(" ")
                for user in users:
                    if not userExists(user):
                        errorExit(f"User '{user}' does not exist")
                break
            else:
                continue
        ############################################################
        # COPY FILES TO USER DIR
        ############################################################
        for user in users:
            USERDIR = Path(f"/home/{user}") if user != "root" else Path("/root")
            run("clear")
            rule(f"Copying files for user '{user}'", align="left")

    except Exception as e:
        raise e
