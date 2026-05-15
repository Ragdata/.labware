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
REPOLIB = BASEDIR / "sys" / "lib"
REPODOT = BASEDIR / "sys" / "dots"
REPOETC = BASEDIR / "sys" / "etc"
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
            WAREDIR = USERDIR / ".labware"
            run("clear")
            rule(f"[yellow]── Copying Files for User '{user}'[/yellow]", style="yellow", align="left")
            # Library Files
            line()
            printHead("Installing Library Files ...")
            copyFiles(REPOLIB, WAREDIR / "lib")
            # Backup Dotfiles
            line()
            printHead("Backup Dotfiles ...")
            printSuccess("Backup '.bashrc'") if backup(USERDIR / ".bashrc") else printWarning("Failed to backup '.bashrc'")
            printSuccess("Backup '.profile'") if backup(USERDIR / ".profile") else printWarning("Failed to backup '.profile'")
            # Install Dotfiles
            line()
            printHead("Installing Dotfiles ...")
            copyFiles(REPODOT, USERDIR)
            if user == EXECUSR:
                line()
                printHead("Installing Configs ...")
                copyFiles(REPOETC, WAREDIR / "etc")
            line()
            CONT = getData("[cyan]Press [ENTER] to continue ...[/cyan] ")
    except Exception as e:
        raise e
